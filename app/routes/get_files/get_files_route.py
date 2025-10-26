import os
from flask_jwt_extended import jwt_required
from commons.config.config.config import Config
from flask import send_from_directory, Blueprint
from commons.utils.admin_user_required import admin_user_required
from commons.utils.update_user_activity import update_user_activity


get_files = Blueprint('files', __name__,)

@get_files.route(Config.UPLOAD_FOLDER + '/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), Config.UPLOAD_FOLDER), filename)

@get_files.route(Config.UPLOAD_USER_AVATAR + '/<filename>')
def uploaded_user_avatar(filename):
    return send_from_directory(os.path.join(os.getcwd(), Config.UPLOAD_USER_AVATAR), filename)

@get_files.route(Config.UPLOAD_ATTACHMENT + '/<filename>')
def uploaded_attachment(filename):
    return send_from_directory(os.path.join(os.getcwd(), Config.UPLOAD_ATTACHMENT), filename)

@get_files.route(Config.DELETED_ATTACHMENTS + '/<filename>')
@jwt_required()
@admin_user_required()
@update_user_activity()
def deleted_attachment(filename):
    return send_from_directory(os.path.join(os.getcwd(), Config.DELETED_ATTACHMENTS), filename)
