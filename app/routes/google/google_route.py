from flask import Blueprint
from flasgger import swag_from
from flask_jwt_extended import jwt_required
from commons.utils.decorators import swagger_doc
from documentation.google_doc.google_doc import *
from commons.utils.valid_user_required import valid_user_required
from controllers.google.google_controller import GoogleController
from commons.utils.update_user_activity import update_user_activity

google_auth_bp = Blueprint('google_auth_bp', __name__)

@google_auth_bp.route('/signin/code', methods=['POST'])
@swagger_doc(login_with_code_doc)
@swag_from({
    "summary": "Google OAuth2 Login (Authorization Code)",
    "description": "Public endpoint - allows login using a Google authorization code.",
    "responses": {
        200: {"description": "Login successful with Google authorization code."},
        400: {"description": "Invalid or expired authorization code."}
    },
    "security": []
})
def login_with_code_route():
    return GoogleController.login_with_code()


@google_auth_bp.route('/signin/refresh', methods=['POST'])
@swagger_doc(login_with_refresh_token_doc)
@swag_from({
    "summary": "Google OAuth2 Login (Refresh Token)",
    "description": "Public endpoint - allows login using a Google refresh token.",
    "responses": {
        200: {"description": "Login successful using Google refresh token."},
        400: {"description": "Invalid or expired refresh token."}
    },
    "security": []
})
def login_with_refresh_token_route():
    return GoogleController.login_with_refresh_token()


@google_auth_bp.route('/signin/token', methods=['POST'])
@swagger_doc(login_with_id_token_doc)
@swag_from({
    "summary": "Google OAuth2 Login (ID Token)",
    "description": "Public endpoint - allows login using a Google ID token.",
    "responses": {
        200: {"description": "Login successful with Google ID token."},
        400: {"description": "Invalid or expired ID token."}
    },
    "security": []
})
def login_with_id_token_route():
    return GoogleController.login_with_id_token()


@google_auth_bp.route('/password/set', methods=['POST'])
@swagger_doc(set_password_doc)
@jwt_required()
@valid_user_required()
@update_user_activity()
@swag_from({
    "summary": "Set User Password",
    "description": "Protected endpoint - allows an authenticated and verified user to set or update their password.",
    "responses": {
        200: {"description": "Password set successfully."},
        400: {"description": "Invalid password or validation failed."},
        401: {"description": "Unauthorized. JWT token missing or invalid."},
        403: {"description": "User not authorized to set password."}
    }
})
def set_password_route():
    return GoogleController.set_password()
