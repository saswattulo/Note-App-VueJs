from flask_restful import Api
from .user import UserResource, Login, FileUpload
from .note import NoteResource, TagResource


def init_api(app):
    api = Api(app)

    # Register resources
    api.add_resource(UserResource, "/users", "/users/<int:user_id>")
    api.add_resource(NoteResource, "/notes", "/notes/<int:note_id>")
    api.add_resource(TagResource, "/tags", "/tags/<int:tag_id>")
    api.add_resource(Login, "/login")
    api.add_resource(FileUpload, '/upload')

    return api
