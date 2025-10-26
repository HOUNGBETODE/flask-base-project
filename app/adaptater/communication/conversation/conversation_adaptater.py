import copy
from sqlalchemy.orm import aliased
from sqlalchemy.types import Integer
from datetime import datetime, timezone
from commons.instances.instances import logger
from data.entities.config.entities_config import db
from commons.const.string.app_string import AppString
from sqlalchemy import func, case, text, desc, or_, and_
from data.entities.communication.message.message import Message
from data.entities.communication.conversation.conversation import Conversation


class ConversationAdaptater:

    @staticmethod
    def get_by_id(conversation_id) -> Conversation:
        try:
            conversation = Conversation.query.filter_by(id=conversation_id, is_deleted=False).first()
            if conversation:
                return conversation
        except Exception as e:
            logger.error(f"Error fetching conversation by conversation_id function adaptater: {e}")
            raise e


    @staticmethod
    def get_between(user1_id: str, user2_id: str) -> Conversation:
        try:
            conversation = Conversation.query.filter(
                Conversation.is_deleted == False,
                or_(
                    and_(
                        Conversation.messengers[0].op('->>')('id') == user1_id,
                        Conversation.messengers[1].op('->>')('id') == user2_id
                    ),
                    and_(
                        Conversation.messengers[0].op('->>')('id') == user2_id,
                        Conversation.messengers[1].op('->>')('id') == user1_id
                    )
                )
            ).first()
            if conversation:
                return conversation
        except Exception as e:
            logger.error(f"Error fetching conversation by user1_id and user2_id function adaptater: {e}")
            raise e


    @staticmethod
    def create(data) -> Conversation:
        try:
            conversation = Conversation().from_dict(data)
            db.session.add(conversation)
            db.session.flush()
            data["content"] = AppString.default_message_value
            data["conversation_id"] = conversation.id
            message = Message().from_dict(data)
            message.is_first = True
            db.session.add(message)
            db.session.commit()
            return conversation
        except Exception as e:
            logger.error(f"Error creating conversation function adaptater: {e}")
            db.session.rollback()
            raise e


    @staticmethod
    def delete(conversation_id):
        try:
            conversation = db.session.get(Conversation, conversation_id)
            conversation.is_deleted = True
            conversation.is_deleted_at = datetime.now(timezone.utc)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting conversation function adaptater: {e}")
            raise e


    @staticmethod
    def restore(conversation_id):
        try:
            conversation = db.session.get(Conversation, conversation_id)
            conversation.is_deleted = False
            conversation.is_deleted_at = None
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error restoring conversation function adaptater: {e}")
            raise e
    

    @staticmethod
    def reset_unread_for_reader(conversation: Conversation, reader_id: str) -> Conversation:
        try:
            conversation_messengers = copy.deepcopy(conversation.messengers)
            for messenger in conversation_messengers:
                if messenger['id'] == reader_id:
                    messenger['unread_count'] = 0
                    break
            else:
                raise ValueError(f"Reader ID '{reader_id}' not found in conversation messengers")
            
            conversation.messengers = conversation_messengers
            db.session.commit()
            return conversation
        except Exception as e:
            logger.error(f"Error resetting unread for reader in conversation function adaptater: {e}")
            db.session.rollback()
            raise e


    @staticmethod
    def get_history_per_user(user_id: str, page: int = 1, per_page: int = 10):
        LastMessage = aliased(Message)

        last_message_subquery = (
            db.session.query(
                Message.conversation_id,
                func.max(
                    case(
                        (Message.is_modified == True, Message.updated_at),
                        else_=Message.created_at
                    )
                ).label("last_message_date")
            )
            .filter(Message.is_deleted == False)
            .group_by(Message.conversation_id)
            .subquery()
        )

        messenger_0_id = Conversation.messengers[0].op('->>')('id')
        messenger_1_id = Conversation.messengers[1].op('->>')('id')
        is_position_0 = messenger_0_id == user_id
        user_unread_count = case(
            (is_position_0, func.cast(Conversation.messengers[0].op('->>')('unread_count'), Integer)),
            else_=func.cast(Conversation.messengers[1].op('->>')('unread_count'), Integer)
        ).label("user_unread_count")

        other_user_id = case(
            (is_position_0, messenger_1_id),
            else_=messenger_0_id
        ).label("other_user_id")

        query = (
            db.session.query(
                Conversation.id,
                user_unread_count,
                other_user_id,
                LastMessage.id.label("last_message_id"),
                LastMessage.content.label("last_message_content"),
                LastMessage.is_first.label("last_message_first_status"),
                LastMessage.is_modified.label('last_message_modification_status'),
                case(
                    (LastMessage.updated_at != None, LastMessage.updated_at),
                    else_=LastMessage.created_at
                ).label("last_message_date")
            )
            .join(last_message_subquery, Conversation.id == last_message_subquery.c.conversation_id)
            .join(
                LastMessage,
                (LastMessage.conversation_id == Conversation.id)
                & (
                    case(
                        (LastMessage.updated_at != None, LastMessage.updated_at),
                        else_=LastMessage.created_at
                    )
                    == last_message_subquery.c.last_message_date
                )
            )
            .filter(
                Conversation.is_deleted == False,
                or_(
                    messenger_0_id == user_id,
                    messenger_1_id == user_id
                )
            )
            .order_by(desc("last_message_date"))
        )

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return pagination
