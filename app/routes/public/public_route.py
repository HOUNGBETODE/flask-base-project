from flask import Blueprint
from flasgger import swag_from
from commons.utils.decorators import swagger_doc
from controllers.public.public_controller import PublicController
from documentation.public_doc.public_doc import public_controller_doc

public_bp = Blueprint('public', __name__)

@public_bp.route('/username/<string:username>/find', methods=['GET'])
@swagger_doc(public_controller_doc['find_username'])
@swag_from({
    "tags": [
        "Public"
    ],
    "summary": "Check Username Availability",
    "description": "Public endpoint to check if a username is already taken. Accessible without authentication token.",
    "responses": {
        200: {"description": "Username is available."},
        400: {"description": "Username is already taken."},
        422: {"description": "Invalid username format."},
        500: {"description": "Server error."}
    },
    "security": []
})
def find_username_route(username):
    return PublicController.find_username(username)
