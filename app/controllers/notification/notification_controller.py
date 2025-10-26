from flask import request
from commons.instances.instances import logger
from flask_jwt_extended import get_jwt_identity
from commons.helpers.response_data import ResponseData
from commons.helpers.custom_response import CustomResponse
from adaptater.notification.notification_adaptater import NotificationAdaptater


class NotificationController:

    @staticmethod
    def get_unread_notifications():
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            user_id = get_jwt_identity()
            
            pagination = NotificationAdaptater.get_unread_notifications(user_id, page, per_page)
            notifications = pagination.items
            notifications_data = [notif.to_dict() for notif in notifications]

            data = ResponseData.get_all_notifications(
                notifications_data=notifications_data, 
                page= page, 
                per_page=per_page, 
                current_page=pagination.page, 
                total_pages=pagination.pages, 
                total=pagination.total,
                has_next=pagination.has_next,
                has_prev=pagination.has_prev
            )
            
            return CustomResponse.send_response(message="Notifications non lues récupérées avec succès.", status_code=200, data=data, success=True)
        except Exception as e:
            logger.error(f"Error in get_unread_notifications function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)


    @staticmethod
    def mark_notifications_as_read():
        try:
            data = request.get_json()
            target = data.get('target')
            user_id = get_jwt_identity()

            if not target:
                return CustomResponse.send_response(message="Le champ 'target' est requis.", status_code=400, success=False)

            if target == 'all':
                NotificationAdaptater.mark_notifications_as_read(user_id, target)
                return CustomResponse.send_response(message="Toutes les notifications ont été marquées comme lues.", status_code=200, success=True)
            
            try:
                target = int(target)
            except Exception:
                return CustomResponse.send_response(message="Le champ 'target' est invalide.", status_code=400, success=False)
            
            marking = NotificationAdaptater.mark_notifications_as_read(user_id, target)
            if not marking:
                return CustomResponse.send_response(message="Notification non trouvée ou déjà lue.", status_code=200, success=True)
                
            return CustomResponse.send_response(message=f"Notification marquée comme lue.", status_code=200, success=True)
        except Exception as e:
            logger.error(f"Error in mark_notifications_as_read function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)
