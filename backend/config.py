class Config:
    username = "postgres"
    password = "postgres"
    host = "localhost"
    port = "5432"
    db_name = "notes_app"

    # Use pg8000 instead
    SQLALCHEMY_DATABASE_URI = f"postgresql+pg8000://{username}:{password}@{host}:{port}/{db_name}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your-secret-key-here"
