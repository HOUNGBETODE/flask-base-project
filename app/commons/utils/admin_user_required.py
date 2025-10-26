from flask import request
from functools import wraps
from commons.instances.instances import logger
from commons.enums.user_roles.roles import UserRole
from adaptater.user.user_adaptater import UserAdaptater
from flask_jwt_extended import get_jwt_identity, get_jwt
from commons.helpers.custom_response import CustomResponse
from adaptater.revoked_token.revoked_token_adaptater import RevokeTokenAdaptater


def admin_user_required():
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                if not token:
                    return CustomResponse.send_response(message="Token requis!", success=False, status_code=401)
                
                identity = get_jwt()
                jti = identity.get('jti')
                if RevokeTokenAdaptater.token_is_revoked(jti): 
                    return CustomResponse.send_response(message="Token revoqué ", success=False, status_code=401)

                user_id = get_jwt_identity()

                user = UserAdaptater.get_by_id(user_id)
                if not user:
                    return CustomResponse.send_response(message="Token invalide", status_code=401)

                if not user.is_active:
                    return CustomResponse.send_response(message="Compte utilisateur inactif", status_code=403)

                if not user.is_verified:
                    return CustomResponse.send_response(message="Veuillez vérifier votre compte", success=False, status_code=403)
                
                if not (user.role in [UserRole.SUPER_ADMIN.value, UserRole.ADMIN.value]) and not user.is_admin:
                    return CustomResponse.send_response(message="Rôle admin requis", success=False, status_code=403)
                
                return func(*args, **kwargs)

            except Exception as e:
                logger.error(f"Error on admin_user_required function decorator: {e}")
                return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)

        return decorated_function
    return decorator
