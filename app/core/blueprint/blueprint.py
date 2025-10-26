
from flask import Flask
from routes.user.user_route import user
from routes.auth.auth_route import auth
from routes.public.public_route import public_bp
from routes.google.google_route import google_auth_bp
from routes.get_files.get_files_route import get_files
from routes.conversation.conversation_route import conversation_bp
from routes.notification.notification_route import notification_bp


def initialize_blueprint_route(app : Flask):

    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(user, url_prefix='/api/user')
    app.register_blueprint(get_files, url_prefix='/')
    app.register_blueprint(conversation_bp, url_prefix='/api/conversation')
    app.register_blueprint(public_bp, url_prefix='/api/public')
    app.register_blueprint(google_auth_bp, url_prefix='/api/google')
    app.register_blueprint(notification_bp, url_prefix='/api/notification')
