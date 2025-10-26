from flask import request
from functools import wraps
from datetime import datetime, timezone
from commons.instances.instances import logger
from flask_jwt_extended import get_jwt_identity
from data.entities.config.entities_config import db
from adaptater.user.user_adaptater import UserAdaptater
from commons.helpers.custom_response import CustomResponse


def update_user_activity():
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                if not token:
                    return func(*args, **kwargs)
                
                user_id = get_jwt_identity()
                user = UserAdaptater.get_by_id(user_id)
                if not user:
                    return CustomResponse.send_response(message="Token invalide", status_code=401)

                user.last_activity_at = datetime.now(timezone.utc)
                db.session.commit()
                logger.info(f"Activité mise à jour pour l'utilisateur {user.email}")

                return func(*args, **kwargs)

            except Exception as e:
                logger.error(f"Error in update_user_activity decorator: {e}")
                db.session.rollback()
                return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)

        return decorated_function
    return decorator
