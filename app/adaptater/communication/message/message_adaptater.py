import copy
from datetime import datetime, timezone
from commons.instances.instances import logger
from commons.config.config.config import Config
from data.entities.config.entities_config import db
from commons.const.string.app_string import AppString
from commons.utils.file_utils import FileUploadManager
from data.entities.communication.message.message import Message
from data.entities.communication.attachment.attachment import Attachment
from data.entities.communication.conversation.conversation import Conversation
from adaptater.communication.attachment.attachment_adaptater import AttachmentAdaptater


class MessageAdaptater:

    @staticmethod
    def get_by_id(message_id) -> Message:
        try:
            return Message.query.filter_by(id=message_id, is_deleted=False).first()
        except Exception as e:
            logger.error(f"Error fetching message by id function adaptater: {e}")
            raise e


    @staticmethod
    def get_by_conversation(conversation_id):
        try:
            return Message.query.filter_by(conversation_id=conversation_id, is_deleted=False).all()
        except Exception as e:
            logger.error(f"Error fetching messages by conversation_id function adaptater: {e}")
            raise e


    @staticmethod
    def create(data) -> Message:
        try:
            writer_id = data['writer_id']
            message = Message().from_dict(data)
            conversation = data["conversation"]
            db.session.add(message)
            db.session.flush()
            # attachment registrations
            for file in data["files"]:
                upload_success, file_url, file_size = FileUploadManager.upload_one_file(file, Config.UPLOAD_ATTACHMENT)
                assert upload_success
                data["message_id"] = message.id
                data["file_path"] = file_url
                data["file_name"] = file_url.split("/")[-1]
                data["file_size"] = file_size
                attachment = Attachment().from_dict(data)
                db.session.add(attachment)
                db.session.flush()
            # updating conversation unread statistics
            conversation_messengers = copy.deepcopy(conversation.messengers)
            for messenger in conversation_messengers:
                if messenger['id'] != writer_id:
                    messenger['unread_count'] += 1
                    break
            conversation.messengers = conversation_messengers
            db.session.add(conversation)
            db.session.commit()
            return message
        except Exception as e:
            logger.error(f"Error creating message function adapter: {e}")
            db.session.rollback()
            raise e
    

    @staticmethod
    def update(message: Message, data) -> Message:
        try:
            message = message.from_dict_for_update_message(data)
            message.is_modified = True
            db.session.add(message)
            db.session.commit()
            return message
        except Exception as e:
            logger.error(f"Error updating message function adapter: {e}")
            db.session.rollback()
            raise e
    

    @staticmethod
    def delete(message_id: int, conversation: Conversation, writer_id: str):
        try:
            message = db.session.get(Message, message_id)
            message.is_deleted = True
            message.is_deleted_at = datetime.now(timezone.utc)
            db.session.flush()
            # updating conversation unread statistics
            conversation_messengers = copy.deepcopy(conversation.messengers)
            for messenger in conversation_messengers:
                if messenger['id'] != writer_id and messenger['unread_count'] > 0:
                    messenger['unread_count'] -= 1
                    break
            conversation.messengers = conversation_messengers
            db.session.add(conversation)
            db.session.commit()
            # deleting attachments
            for attachment in message.attachments:
                assert AttachmentAdaptater.delete(attachment.id)
            return True
        except Exception as e:
            logger.error(f"Error deleting message function adapter: {e}")
            db.session.rollback()
            raise e
    

    @staticmethod
    def restore(message_id: int):
        try:
            message = db.session.get(Message, message_id)
            message.is_deleted = False
            message.is_deleted_at = None
            db.session.commit()
            for attachment in message.attachments:
                assert AttachmentAdaptater.restore(attachment.id)
            return True
        except Exception as e:
            logger.error(f"Error restoring message function adapter: {e}")
            db.session.rollback()
            raise e


    @staticmethod
    def get_all(page, per_page, conversation_id):
        try:
            query = Message.query.filter(
                Message.conversation_id == conversation_id,
                Message.content != AppString.default_message_value
            ).order_by(
                Message.created_at.desc()
            )

            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            return pagination

        except Exception as e:
            logger.error(f"Error getting paginated messages by conversation of ID {conversation_id} function adaptater: {e}")
            raise e
