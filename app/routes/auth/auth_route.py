from flask import Blueprint
from flasgger import swag_from
from flask_jwt_extended import jwt_required
from documentation.user_doc.user_doc import *
from commons.utils.decorators import swagger_doc
from controllers.auth.auth_controller import AuthController
from documentation.auth_doc.auth_doc import (
    signup_doc,
    login_doc,
    logout_doc, 
    reset_password_doc,
    forgot_password_doc,
    verify_user_doc,
    user_verify_resent_code
)

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
@swagger_doc(signup_doc)
@swag_from({
    "summary": "Public endpoint",
    "description": "This endpoint is accessible without authentication token.",
    "responses": {
        200: {"description": "User registered successfully."}
    },
    "security": []
})
def signup_route():
    return AuthController.signup()

@auth.route('/signin', methods=['POST'])
@swagger_doc(login_doc)
@swag_from({
    "summary": "Public endpoint",
    "description": "This endpoint is accessible without authentication token.",
    "responses": {
        200: {"description": "User login successful."}
    },
    "security": []
})
def login_route():
    return AuthController.login()

@auth.route('/password/reset', methods=['POST'])
@swagger_doc(reset_password_doc)
@swag_from({
    "summary": "Public endpoint",
    "description": "This endpoint is accessible without authentication token.",
    "responses": {
        200: {"description": "Password reset successful."}
    },
    "security": []
})
def reset_password_route():
    return AuthController.reset_password()

@auth.route('/password/forgot', methods=['POST'])
@swagger_doc(forgot_password_doc)
@swag_from({
    "summary": "Public endpoint",
    "description": "This endpoint is accessible without authentication token.",
    "responses": {
        200: {"description": "Password reset code sent successfully."}
    },
    "security": []
})
def forgot_password_route():
    return AuthController.forgot_password()

@auth.route('/account/activate', methods=['POST'])
@swagger_doc(verify_user_doc)
@swag_from({
    "summary": "Public endpoint",
    "description": "This endpoint is accessible without authentication token.",
    "responses": {
        200: {"description": "User account activated successfully."}
    },
    "security": []
})
def verify_user_account_route():
    return AuthController.verify_user_account()

@auth.route('/password/code-resent', methods=['POST'])
@swagger_doc(forgot_password_doc)
@swag_from({
    "summary": "Public endpoint",
    "description": "This endpoint is accessible without authentication token.",
    "responses": {
        200: {"description": "Password reset code resent successfully."}
    },
    "security": []
})
def resent_forgot_password_route():
    return AuthController.resent_forgot_password_code()

@auth.route('/verify/code-resent', methods=['POST'])
@swagger_doc(user_verify_resent_code)
@swag_from({
    "summary": "Public endpoint",
    "description": "This endpoint is accessible without authentication token.",
    "responses": {
        200: {"description": "Verification code resent successfully."}
    },
    "security": []
})
def resent_verification_code_route():
    return AuthController.resent_verification_code()

@auth.route('/logout', methods=['POST'])
@swagger_doc(logout_doc)
@jwt_required()
@swag_from({
    "summary": "Protected endpoint",
    "description": "This endpoint requires a valid authentication token.",
    "responses": {
        200: {"description": "User logged out successfully."},
        401: {"description": "Unauthorized. Token is missing or invalid."}
    }
})
def logout_route():
    return AuthController.logout()
