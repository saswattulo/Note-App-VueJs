from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    f_name = Column(String, nullable=False)
    l_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    # Relationship to Note
    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "f_name": self.f_name,
            "l_name": self.l_name,
            "email": self.email,
        }


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="notes")
    tags = relationship("Tag", back_populates="note", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": [tag.to_dict()["name"] for tag in self.tags],
            "user_id": self.user_id,
        }


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)

    # Relationship
    note = relationship("Note", back_populates="tags")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "note_id": self.note_id,
        }
