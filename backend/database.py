import pg8000
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import Config

db = SQLAlchemy()

# Define the database URI and initialize sessionmaker
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
db_session = Session()


def create_database_if_not_exists():
    # Connect to PostgreSQL with default database
    conn = pg8000.connect(
        user=Config.username,
        password=Config.password,
        host=Config.host,
        port=int(Config.port),  # pg8000 requires port as integer
        database="postgres",  # Connect to default database first
    )

    conn.autocommit = True
    cursor = conn.cursor()

    try:
        # Check if the database exists
        cursor.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
            (Config.db_name,),  # Pass parameters as a tuple
        )

        exists = cursor.fetchone()

        if exists:
            print(f"Database '{Config.db_name}' already exists. Skipping creation.")
        else:
            cursor.execute(f"CREATE DATABASE {Config.db_name}")
            print(f"Database '{Config.db_name}' created successfully!")

    except Exception as e:
        print(f"Error occurred while creating database: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()


def setup_db(app):
    # Create database if it doesn't exist
    create_database_if_not_exists()

    # Initialize the app with SQLAlchemy
    db.init_app(app)

    # Create all tables using Base.metadata.create_all(engine) in app context
    with app.app_context():
        Base.metadata.create_all(engine)  # Use Base from models to create tables
        print("All database tables created successfully!")

    return db
