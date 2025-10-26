from datetime import datetime, timezone
from commons.instances.instances import logger
from data.entities.config.entities_config import db
from commons.utils.file_utils import FileUploadManager
from data.entities.communication.message.message import Message
from data.entities.communication.attachment.attachment import Attachment


class AttachmentAdaptater:

    @staticmethod
    def get_by_id(attachment_id) -> Attachment:
        try:
            return Attachment.query.filter_by(id=attachment_id, is_deleted=False).first()
        except Exception as e:
            logger.error(f"Error fetching attachment by id function adaptater: {e}")
            raise e
    

    @staticmethod
    def get_by_message_id(message_id):
        try:
            return Attachment.query.filter_by(message_id=message_id, is_deleted=False).all()
        except Exception as e:
            logger.error(f"Error fetching attachments by message_id function adaptater: {e}")
            raise e
    

    @staticmethod
    def create(data) -> Attachment:
        try:
            attachment = Attachment().from_dict(data)
            db.session.add(attachment)
            db.session.commit()
            return attachment
        except Exception as e:
            logger.error(f"Error creating attachment function adaptater: {e}")
            db.session.rollback()
            raise e
    

    @staticmethod
    def update(attachment: Attachment, data) -> Attachment:
        try:
            attachment = attachment.from_dict_for_update_attachment(data)
            db.session.add(attachment)
            db.session.commit()
            return attachment
        except Exception as e:
            logger.error(f"Error updating attachment function adaptater: {e}")
            db.session.rollback()
            raise e
    

    @staticmethod
    def delete(attachment_id : int, is_lonely: bool):
        try:
            attachment = db.session.get(Attachment, attachment_id)
            new_path = FileUploadManager.delete_one_attachment_file(attachment.file_path)
            if new_path: 
                attachment.file_path = new_path
            attachment.is_deleted = True
            attachment.is_deleted_at = datetime.now(timezone.utc)
            if is_lonely:
                db.session.flush()
                message = db.session.get(Message, attachment.message_id)
                message.is_deleted = True
                message.is_deleted_at = datetime.now(timezone.utc)
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting attachment function adaptater: {e}")
            db.session.rollback()
            raise e
        
    
    @staticmethod
    def restore(attachment_id : int):
        try:
            attachment = db.session.get(Attachment, attachment_id)
            new_path = FileUploadManager.restore_one_attachment_file(attachment.file_path)
            if new_path: 
                attachment.file_path = new_path
            attachment.is_deleted = False
            attachment.is_deleted_at = None
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error restoring attachment function adaptater: {e}")
            db.session.rollback()
            raise e
