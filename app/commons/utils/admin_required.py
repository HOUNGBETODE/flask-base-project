from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt, exceptions
from adaptater.user.user_adaptater import UserAdaptater
from adaptater.auth.auth_adaptater import AuthAdaptater
from commons.helpers.custom_response import CustomResponse
from commons.instances.instances import logger


def admin_required():
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                # Récupérer le token d'authentification
                token = request.headers.get('Authorization')
                if not token:

                    return CustomResponse.send_response(message=  "Token requis!", success= False, status_code= 401)

                # Vérifier si le token est valide et récupérer l'identité de l'utilisateur
                user_id = get_jwt_identity()
      
                user = UserAdaptater.get_user_by_id(user_id)
                logger.debug(user)
                if not user:
                    return CustomResponse.send_response(message=  "Utilisateur non trouvé", success= False, status_code= 403)
                #vérifier si le compte n'a pas été supprimer
                if user.is_deleted:
                    return CustomResponse.send_response(message="L'utilisateur n'esxiste pas!", success=False, status_code=403)
                
                # Vérifier si l'utilisateur a le rôle d'administrateur
                if not user.is_admin:
                     return CustomResponse.send_response(message=  "Vous n'êtes pas autorisé à consulter cette ressource, Rôle admin requis!", success= False, status_code= 403)

                # Si tout est en ordre, exécuter la fonction de route
                return func(*args, **kwargs)

            except Exception as e:
               return CustomResponse.send_serveur_error( error = e,  success= False, status_code= 500)

        return decorated_function
    return decorator
