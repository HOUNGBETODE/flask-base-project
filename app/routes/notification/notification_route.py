from flask import Blueprint
from flask_jwt_extended import jwt_required
from commons.utils.decorators import swagger_doc
from documentation.notification_doc.notification_doc import *
from commons.utils.valid_user_required import valid_user_required
from commons.utils.update_user_activity import update_user_activity
from controllers.notification.notification_controller import NotificationController


notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/unread/all', methods=['GET'])
@jwt_required()
@valid_user_required()
@update_user_activity()
@swagger_doc(get_unread_notifications_doc)
def get_unread_notifications_route():
    return NotificationController.get_unread_notifications()

@notification_bp.route('/mark-as-read', methods=['PUT'])
@jwt_required()
@valid_user_required()
@update_user_activity()
@swagger_doc(mark_notifications_as_read_doc)
def mark_notifications_as_read_route():
    return NotificationController.mark_notifications_as_read()
