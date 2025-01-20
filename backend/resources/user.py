# resources/user.py
from flask_restful import Resource, reqparse
from models import User
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from database import db_session
import bcrypt


class Login(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("email", type=str, required=True, help="Email is required")
        self.parser.add_argument("password", type=str, required=True, help="Password is required")

    def post(self):
        args = self.parser.parse_args()
        user = db_session.query(User).filter(User.email == args["email"]).first()

        if not user:
            return {"message": "User not found"}, 404

        if bcrypt.checkpw(args["password"].encode("utf-8"), user.password.encode("utf-8")):
            return jsonify({"message": "Login successful", "user": user.to_dict()})

        return {"message": "Invalid password"}, 401


class UserResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("f_name", type=str, required=True, help="First name is required")
        self.parser.add_argument("l_name", type=str, required=True, help="Last name is required")
        self.parser.add_argument("email", type=str, required=True, help="Email is required")
        self.parser.add_argument("password", type=str, required=True, help="Password is required")

    def get(self, user_id=None):
        if user_id:
            user = db_session.query(User).get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            return jsonify(user.to_dict())

        users = db_session.query(User).all()
        return jsonify([user.to_dict() for user in users])

    def post(self):
        args = self.parser.parse_args()

        # Hash the password
        hashed = bcrypt.hashpw(args["password"].encode("utf-8"), bcrypt.gensalt())

        try:
            new_user = User(
                f_name=args["f_name"],
                l_name=args["l_name"],
                email=args["email"],
                password=hashed.decode("utf-8"),
            )
            db_session.add(new_user)
            db_session.commit()
            return {"status": f"User with {new_user.id} created.", "ddata": new_user.to_dict()}, 201
        except IntegrityError:
            db_session.rollback()
            return {"message": "Email already exists"}, 400

    def put(self, user_id):
        user = db_session.query(User).get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        args = self.parser.parse_args()

        user.f_name = args["f_name"]
        user.l_name = args["l_name"]
        user.email = args["email"]

        if args["password"]:
            hashed = bcrypt.hashpw(args["password"].encode("utf-8"), bcrypt.gensalt())
            user.password = hashed.decode("utf-8")

        try:
            db_session.commit()
            return jsonify(user.to_dict())
        except IntegrityError:
            db_session.rollback()
            return {"message": "Email already exists"}, 400

    def delete(self, user_id):
        user = db_session.query(User).get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        try:
            db_session.delete(user)
            db_session.commit()
            return "", 204
        except Exception as e:
            db_session.rollback()
            return {"message": f"Failed to delete user: {str(e)}"}, 500


import os
import pandas as pd

from flask import current_app as app


class FileUpload(Resource):
    def post(self):
        # Check if the file is provided in the request
        if 'file' not in request.files:
            return {"status": "fail", "message": "No file provided"}, 400

        file = request.files['file']

        # Check if a file was selected
        if file.filename == '':
            return {"status": "fail", "message": "No file selected"}, 400

        # Save the uploaded file to the configured folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            # Load the CSV file into a Pandas DataFrame
            df = pd.read_csv(file_path)
        except Exception as e:
            # Handle file parsing errors
            return {"status": "fail", "message": f"File processing error: {str(e)}"}, 400

        # Prepare analytics data
        try:
            salary_distribution = pd.cut(df['Salary'], bins=10).value_counts().sort_index()
            age_distribution = pd.cut(df['Age'], bins=[20, 30, 40, 50, 60]).value_counts().sort_index()
            df['Joining Year'] = pd.to_datetime(df['Joining Date']).dt.year
            joining_trend = df['Joining Year'].value_counts().sort_index()

            analytics = {
                "status": "success",
                # "columns": df.columns.tolist(),
                # "shape": df.shape,
                # "missing_values": df.isnull().sum().to_dict(),
                # "descriptive_stats": df.describe(include="all").to_dict(),
                "salary_distribution": {
                    "labels": [f"{int(interval.left)}-{int(interval.right)}" for interval in salary_distribution.index],
                    "values": salary_distribution.values.tolist(),
                },
                "age_distribution": {
                    "labels": [f"{int(interval.left)}-{int(interval.right)}" for interval in age_distribution.index],
                    "values": age_distribution.values.tolist(),
                },
                "joining_trend": {
                    "labels": joining_trend.index.tolist(),
                    "values": joining_trend.values.tolist(),
                },
            }
        except Exception as e:
            return {"status": "fail", "message": f"Analytics processing error: {str(e)}"}, 400

        # Return the analytics data
        return analytics, 200
