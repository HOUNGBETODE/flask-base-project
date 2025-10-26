import threading
from pytz import utc
from flask import request, current_app
from datetime import datetime, timedelta
from commons.instances.instances import logger
from flask_jwt_extended import get_jwt_identity
from commons.const.string.app_string import AppString
from commons.helpers.response_data import ResponseData
from adaptater.user.user_adaptater import UserAdaptater
from commons.helpers.custom_response import CustomResponse
from commons.enums.notification_tags.tags import NotificationTag
from adaptater.communication.message.message_adaptater import MessageAdaptater
from adaptater.notification.notification_adaptater import NotificationAdaptater
from adaptater.communication.attachment.attachment_adaptater import AttachmentAdaptater
from adaptater.communication.conversation.conversation_adaptater import ConversationAdaptater


class ConversationController:

    @staticmethod
    def create():
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            requester_id = get_jwt_identity()

            if not user_id:
                return CustomResponse.send_response(message="Le champ user_id est requis.", status_code=422)
            
            existing_conversation = ConversationAdaptater.get_between(user_id, requester_id)
            if existing_conversation:
                return CustomResponse.send_response(message="Cette conversation existe déjà.", success=False, status_code=400)

            data["messengers"] = [{"id": user_id, "unread_count": 0}, {"id": requester_id, "unread_count": 0}]
            conversation = ConversationAdaptater.create(data)
            return CustomResponse.send_response(message="Conversation créée avec succès.", status_code=201, success=True, data=conversation.to_dict())
        except Exception as e:
            logger.error(f"Error in create conversation function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)


    @staticmethod
    def get_messages(conversation_id):
        try:
            existing_conversation = ConversationAdaptater.get_by_id(conversation_id)
            if not existing_conversation:
                return CustomResponse.send_response(message="Conversation non trouvée", success=False, status_code=404)

            existing_user = UserAdaptater.get_by_id(id=get_jwt_identity())
            user_ids = [m['id'] for m in existing_conversation.messengers]
            if existing_user.id not in user_ids:
                return CustomResponse.send_response(message="Impossible de lire les messages : vous ne faites pas partie de cette conversation", success=False, status_code=403)

            ConversationAdaptater.reset_unread_for_reader(existing_conversation, existing_user.id)

            # Fetch the other user (conversation partner)
            other_user_id = next(m['id'] for m in existing_conversation.messengers if m['id'] != existing_user.id)
            other_user = UserAdaptater.get_by_id(other_user_id)

            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            pagination = MessageAdaptater.get_all(page, per_page, conversation_id)
            messages = pagination.items
            
            messages_data = [msg.to_dict() for msg in messages]
            data = ResponseData.get_all_messages(
                other_user_data=other_user.to_small_dict(),
                messages_data=messages_data, 
                page=page,
                per_page=per_page, 
                current_page=pagination.page, 
                total_pages=pagination.pages, 
                total=pagination.total,
                has_next=pagination.has_next,
                has_prev=pagination.has_prev
            )
            return CustomResponse.send_response(message="Messages récupérés avec succès", status_code=200, data=data, success=True)
                        
        except Exception as e:
            logger.error(f"Error on get_conversation_messages function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)


    @staticmethod
    def get_user_history():
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)

            pagination = ConversationAdaptater.get_history_per_user(get_jwt_identity(), page, per_page)
            conversations = pagination.items
            
            conversations_data = [
                {
                    "id": row.id,
                    "unread_count": row.user_unread_count,
                    "last_message": {
                        "id": row.last_message_id,
                        "content": row.last_message_content,
                        "is_first": row.last_message_first_status,
                        "is_modified": row.last_message_modification_status,
                        "date": row.last_message_date.isoformat() if row.last_message_date else None
                    },
                    "other_user": UserAdaptater.get_by_id(row.other_user_id).to_small_dict() if UserAdaptater.get_by_id(row.other_user_id) else None
                }
                for row in conversations
            ]
            data = ResponseData.get_all_conversations(
                conversations_data=conversations_data, 
                page=page, 
                per_page=per_page, 
                current_page=pagination.page, 
                total_pages=pagination.pages, 
                total=pagination.total,
                has_next=pagination.has_next,
                has_prev=pagination.has_prev
            )
            return CustomResponse.send_response(message="Conversations récupérées avec succès", status_code=200, data=data, success=True)
                          
        except Exception as e:
            logger.error(f"Error on get_user_conversation_history function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)
    

    @staticmethod
    def send_message_with_attachments(conversation_id):
        try: 
            files = request.files.getlist('files')
            content = request.form.get('content', '')

            if files and not content:
                content = AppString.default_message_with_attachment_value

            if not any([files, content]):
                return CustomResponse.send_response(message="'Erreur de validation : Champs requis' !", success=False, status_code=400)

            existing_conversation = ConversationAdaptater.get_by_id(conversation_id)
            if not existing_conversation:
                return CustomResponse.send_response(message='Conversation non trouvée', status_code=404, success=False)
            
            requester = UserAdaptater.get_by_id(get_jwt_identity())
            user_ids = [m['id'] for m in existing_conversation.messengers]
            if requester.id not in user_ids:
                return CustomResponse.send_response(message="Impossible d'envoyer un message au sein de cette conversation : vous n'en êtes pas un membre.", status_code=403, success=False)
            
            data = {
                "conversation_id": conversation_id,
                "conversation": existing_conversation,
                "content": content, 
                "files": files,
                "writer_id": requester.id
            }
            if MessageAdaptater.create(data):

                # Find recipient (the other user)
                recipient_id = next(m['id'] for m in existing_conversation.messengers if m['id'] != requester.id)

                if recipient_id != requester.id:
                    threading.Thread(target=NotificationAdaptater.create_notification, args=(
                        current_app._get_current_object(),
                        "Nouveau message",
                        f"Vous avez reçu un nouveau message de {requester.firstname} {requester.lastname} "
                        "dans une de vos conversations.",
                        NotificationTag.SEND_MESSAGE.value,
                        recipient_id,
                    )).start()

                return CustomResponse.send_response(message='Message envoyé avec succès', status_code=201, success=True)  
            
        except Exception as e:
            logger.error(f"Error on send_message_with_attachment function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)
    

    @staticmethod
    def update_message(conversation_id, message_id):
        try: 
            requester = UserAdaptater.get_by_id(get_jwt_identity())

            data = request.get_json()
            content = data.get("content").strip()
            data["content"] = content
            if not content:
                return CustomResponse.send_response(message="Le champ content est requis.", status_code=422, success=False, data=None)

            existing_conversation = ConversationAdaptater.get_by_id(conversation_id=conversation_id)
            if not existing_conversation:
                return CustomResponse.send_response(message='Conversation non trouvée.', status_code=404, success=False, data=None)

            user_ids = [m['id'] for m in existing_conversation.messengers]
            if requester.id not in user_ids:
                return CustomResponse.send_response(message="Impossible d'accéder à cette conversation : vous n'en êtes pas un membre.", status_code=403, success=False, data=None)

            existing_message = MessageAdaptater.get_by_id(message_id=message_id)
            if not existing_message:
                return CustomResponse.send_response(message='Message non trouvé', status_code=404, success=False, data=None)

            if existing_message.writer_id != requester.id:
                return CustomResponse.send_response(message="Impossible de modifier le message : vous n'en êtes pas l'auteur.e", status_code=403, success=False, data=None)

            if existing_message.content in (AppString.default_message_value, AppString.default_message_with_attachment_value):
                return CustomResponse.send_response(message='Ce message est dépourvu de contenu textuels. Impossible de le modifier.', status_code=400, success=False, data=None)

            if existing_message.content == content:
                return CustomResponse.send_response(message='Le contenu du message n\'a pas été modifié.', status_code=400, success=False, data=None)

            if datetime.now(utc) > (existing_message.created_at + timedelta(seconds=AppString.time_limit_for_message)):
                return CustomResponse.send_response(message=f'Expiration de la marge temporelle de modification du message : {AppString.time_limit_for_message} secondes se sont écoulées depuis son envoi.', status_code=400, success=False, data=None)

            updated_message = MessageAdaptater.update(existing_message, data)
            if updated_message:
                return CustomResponse.send_response(message='Message a été mis à jour avec succès.', success=True, status_code=200)
            
            return CustomResponse.send_response(message='Erreur lors de la mise à jour du message !', status_code=400, success=False, data=None)  
            
        except Exception as e:
            logger.error(f"Error on update_message function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)
    

    @staticmethod
    def delete_message(conversation_id, message_id):
        try: 
            requester = UserAdaptater.get_by_id(get_jwt_identity())

            existing_conversation = ConversationAdaptater.get_by_id(conversation_id=conversation_id)
            if not existing_conversation:
                return CustomResponse.send_response(message='Conversation non trouvée.', status_code=404, success=False, data=None)

            user_ids = [m['id'] for m in existing_conversation.messengers]
            if requester.id not in user_ids:
                return CustomResponse.send_response(message="Impossible d'accéder à cette conversation : vous n'en êtes pas un membre.", status_code=403, success=False, data=None)

            existing_message = MessageAdaptater.get_by_id(message_id=message_id)
            if not existing_message:
                return CustomResponse.send_response(message='Message non trouvé', status_code=404, success=False, data=None)

            if existing_message.writer_id != requester.id:
                return CustomResponse.send_response(message="Impossible de supprimer le message : vous n'en êtes pas l'auteur.e", status_code=403, success=False, data=None)

            if datetime.now(utc) > (existing_message.created_at + timedelta(seconds=AppString.time_limit_for_message)):
                return CustomResponse.send_response(message=f'Expiration de la marge temporelle de suppression du message : {AppString.time_limit_for_message} secondes se sont écoulées depuis son envoi.', status_code=400, success=False, data=None)

            if MessageAdaptater.delete(message_id, existing_conversation, existing_message.writer_id):
                return CustomResponse.send_response(message='Message supprimé avec succès', success=True, status_code=200)
            
            return CustomResponse.send_response(message='Erreur lors de la suppression du message !', status_code=400, success=False, data=None)  
        except Exception as e:
            logger.error(f"Error on delete_message function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)
    

    @staticmethod
    def delete_attachment(conversation_id, attachment_id):
        try: 
            requester = UserAdaptater.get_by_id(get_jwt_identity())

            existing_conversation = ConversationAdaptater.get_by_id(conversation_id=conversation_id)
            if not existing_conversation:
                return CustomResponse.send_response(message='Conversation non trouvée.', status_code=404, success=False, data=None)

            user_ids = [m['id'] for m in existing_conversation.messengers]
            if requester.id not in user_ids:
                return CustomResponse.send_response(message="Impossible d'accéder à cette conversation : vous n'en êtes pas un membre.", status_code=403, success=False, data=None)

            existing_attachment = AttachmentAdaptater.get_by_id(attachment_id=attachment_id)
            if not existing_attachment:
                return CustomResponse.send_response(message='Pièce jointe non trouvée.', status_code=404, success=False, data=None)

            is_attachment_lonely = (existing_attachment.message.content == AppString.default_message_with_attachment_value)
            if existing_attachment.message.writer_id != requester.id:
                return CustomResponse.send_response(message="Impossible de supprimer la pièce jointe : vous n'avez pas les droits requis", status_code=403, success=False, data=None)

            if datetime.now(utc) > (existing_attachment.created_at + timedelta(seconds=AppString.time_limit_for_message)):
                return CustomResponse.send_response(message=f'Expiration de la marge temporelle de suppression de la pièce jointe : {AppString.time_limit_for_message} secondes se sont écoulées depuis son envoi.', status_code=400, success=False, data=None)

            if AttachmentAdaptater.delete(attachment_id, is_attachment_lonely):
                return CustomResponse.send_response(message='Pièce jointe supprimée avec succès', success=True, status_code=200)
            
            return CustomResponse.send_response(message='Erreur lors de la suppression de la pièce jointe !', status_code=400, success=False, data=None)  
        except Exception as e:
            logger.error(f"Error on delete_attachment function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)
