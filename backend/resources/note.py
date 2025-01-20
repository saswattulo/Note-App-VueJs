# resources/note.py
from flask_restful import Resource, reqparse
from models import Note, Tag
from flask import jsonify
from database import db_session


class NoteResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("title", type=str, required=True, help="Title is required")
        self.parser.add_argument("content", type=str, required=True, help="Content is required")
        self.parser.add_argument("user_id", type=int, required=True, help="User ID is required")

    def get(self, note_id=None):
        if note_id:
            note = db_session.query(Note).get(note_id)
            if not note:
                return {"message": "Note not found"}, 404
            return {"status": "success", "data": note.to_dict()}, 200

        notes = db_session.query(Note).all()
        return {"status": "success", "data": [note.to_dict() for note in notes]}, 200

    def post(self):
        args = self.parser.parse_args()
        new_note = Note(title=args["title"], content=args["content"], user_id=args["user_id"])
        try:
            db_session.add(new_note)
            db_session.commit()
            return {"status": "success", "data": new_note.to_dict()}, 200
        except Exception as e:
            db_session.rollback()
            return {"message": f"Failed to create note: {str(e)}"}, 500

    def put(self, note_id):
        note = db_session.query(Note).get(note_id)
        if not note:
            return {"message": "Note not found"}, 404

        args = self.parser.parse_args()

        note.title = args["title"]
        note.content = args["content"]
        note.user_id = args["user_id"]

        try:
            db_session.commit()
            return {"status": "success", "data": note.to_dict()}, 200
        except Exception as e:
            db_session.rollback()
            return {"message": f"Failed to update note: {str(e)}"}, 500

    def delete(self, note_id):
        note = db_session.query(Note).get(note_id)
        if not note:
            return {"message": "Note not found"}, 404

        try:
            db_session.delete(note)
            db_session.commit()
            return "", 204
        except Exception as e:
            db_session.rollback()
            return {"message": f"Failed to delete note: {str(e)}"}, 500


class TagResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name", type=str, required=True, help="Tag name is required")
        self.parser.add_argument("note_id", type=int, required=True, help="Note ID is required")

    def get(self, tag_id=None):
        if tag_id:
            tag = db_session.query(Tag).get(tag_id)
            if not tag:
                return {"message": "Tag not found"}, 404
            return {"status": "success", "data": tag.to_dict()}, 200

        tags = db_session.query(Tag).all()
        return {"status": "success", "data": [tag.to_dict() for tag in tags]}, 200

    def post(self):
        args = self.parser.parse_args()
        new_tag = Tag(name=args["name"], note_id=args["note_id"])
        try:
            db_session.add(new_tag)
            db_session.commit()
            return {"status": "success", "data": new_tag.to_dict()}, 200
        except Exception as e:
            db_session.rollback()
            return {"message": f"Failed to create tag: {str(e)}"}, 500

    def put(self, tag_id):
        tag = db_session.query(Tag).get(tag_id)
        if not tag:
            return {"message": "Tag not found"}, 404

        args = self.parser.parse_args()

        tag.name = args["name"]
        tag.note_id = args["note_id"]

        try:
            db_session.commit()
            return {"status": "success", "data": tag.to_dict()}, 200
        except Exception as e:
            db_session.rollback()
            return {"message": f"Failed to update tag: {str(e)}"}, 500

    def delete(self, tag_id):
        tag = db_session.query(Tag).get(tag_id)
        if not tag:
            return {"message": "Tag not found"}, 404

        try:
            db_session.delete(tag)
            db_session.commit()
            return "", 204
        except Exception as e:
            db_session.rollback()
            return {"message": f"Failed to delete tag: {str(e)}"}, 500
