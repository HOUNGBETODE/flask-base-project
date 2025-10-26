from flask import Blueprint
from flask_jwt_extended import jwt_required
from commons.utils.decorators import swagger_doc
# from commons.utils.none_admin_required import none_admin_required
from commons.utils.valid_user_required import valid_user_required
from commons.utils.update_user_activity import update_user_activity
from controllers.conversation.conversation_controller import ConversationController
from documentation.conversation_doc.conversation_doc import conversation_controller_doc


conversation_bp = Blueprint('conversation_bp', __name__)

@conversation_bp.route('/create', methods=['POST'])
@swagger_doc(conversation_controller_doc['create'])
@jwt_required()
@valid_user_required()
@update_user_activity()
def create_conversation_route():
    return ConversationController.create()

@conversation_bp.route('/user/history', methods=['GET'])
@swagger_doc(conversation_controller_doc['get_all_for_user'])
@jwt_required()
@valid_user_required()
@update_user_activity()
def get_all_user_conversations_route():
    return ConversationController.get_user_history()

@conversation_bp.route('/<string:conversation_id>/messages', methods=['GET'])
@swagger_doc(conversation_controller_doc['get_all_messages'])
@jwt_required()
@valid_user_required()
@update_user_activity()
def get_all_messages_route(conversation_id):
    return ConversationController.get_messages(conversation_id)

@conversation_bp.route('/<string:conversation_id>/message/create', methods=['POST'])
@swagger_doc(conversation_controller_doc['send_message_with_attachments'])
@jwt_required()
@valid_user_required()
@update_user_activity()
def send_message_with_attachments_route(conversation_id):
    return ConversationController.send_message_with_attachments(conversation_id)

@conversation_bp.route('/<string:conversation_id>/message/<int:message_id>/update', methods=['PUT'])
@swagger_doc(conversation_controller_doc['update_message_content'])
@jwt_required()
@valid_user_required()
@update_user_activity()
def update_message_route(conversation_id, message_id):
    return ConversationController.update_message(conversation_id, message_id)

@conversation_bp.route('/<string:conversation_id>/message/<int:message_id>/delete', methods=['DELETE'])
@swagger_doc(conversation_controller_doc['delete_message'])
@jwt_required()
@valid_user_required()
@update_user_activity()
def delete_message_route(conversation_id, message_id):
    return ConversationController.delete_message(conversation_id, message_id)

@conversation_bp.route('/<string:conversation_id>/attachment/<int:attachment_id>/delete', methods=['DELETE'])
@swagger_doc(conversation_controller_doc['attachment_delete'])
@jwt_required()
@valid_user_required()
@update_user_activity()
def delete_attachment_route(conversation_id, attachment_id):
    return ConversationController.delete_attachment(conversation_id, attachment_id)
