from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, exceptions
from adaptater.user.user_adaptater import UserAdaptater
from adaptater.auth.auth_adaptater import AuthAdaptater
from commons.helpers.custom_response import CustomResponse
from commons.instances.instances import logger
from uses_cases.token_revoqued import revoked_tokens

def user_existing_required():
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                # Récupérer le token d'authentification
                token = request.headers.get('Authorization')
                if not token:
                    return CustomResponse.send_response(message="Token requis!", success=False, status_code=401)
                

                identity = get_jwt()

            # Récupérer l'ID du JWT (jti) pour marquer le token comme révoqué
                jti = identity.get('jti')
                if jti in revoked_tokens : 
                    return CustomResponse.send_response(message="Token revoqué ", success=False, status_code=401)

                # Vérifier si le token est valide et récupérer les revendicat
                user_id = get_jwt_identity()

                user = UserAdaptater.get_user_by_id(user_id)
                #logger.debug(user)
                if not user:
                    return CustomResponse.send_response(message="Utilisateur non trouvé", success=False, status_code=404)

                # Vérifier si l'utilisateur a vérifié son compte
                if not user.is_verified:
                    return CustomResponse.send_response(message="Veuillez vérifier votre compte !", success=False, status_code=403)
                
                # Vérifier si compte le compte de l'utilisateur est active
                if not user.is_active:
                    return CustomResponse.send_response(message="Votre compte est desactiver!", success=False, status_code=403)
                
                # Vérifier si compte le compte de l'utilisateur n'est pas supprimer
                if user.is_deleted:
                    return CustomResponse.send_response(message="L'utilisateur n'esxiste pas!", success=False, status_code=403)
                
                # Si tout est en ordre, exécuter la fonction de route
                return func(*args, **kwargs)

            except Exception as e:
                logger.error(f"error on user existing required : {e}")
                return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)

        return decorated_function
    return decorator