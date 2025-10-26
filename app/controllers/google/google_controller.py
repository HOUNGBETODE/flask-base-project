from flask import request
from commons.instances.instances import logger
from commons.utils.utils import validate_password
from commons.helpers.response_data import ResponseData
from adaptater.auth.auth_adaptater import AuthAdaptater
from adaptater.user.user_adaptater import UserAdaptater
from commons.helpers.custom_response import CustomResponse
from commons.utils.oauth_utils import (
    exchange_code_for_token, 
    get_access_token, 
    get_user_info, 
    verify_google_id_token
)


class GoogleController:

    @staticmethod
    def _handle_google_login(public_user_infos):
        email = public_user_infos.get('email')
        if not email:
            return CustomResponse.send_response(message="Impossible de récupérer l'email depuis Google", status_code=400)

        user = UserAdaptater.get_by_email(email)
        if user:
            if user.is_deleted:
                return CustomResponse.send_response(message="Nous avons rencontré un souci avec l'email fourni. Contactez le support.", status_code=400)
            final_user = user
        else:
            final_user = AuthAdaptater.create_google_user({
                "email": email,
                "firstname": public_user_infos.get('given_name'),
                "lastname": public_user_infos.get('family_name'),
                "avatar": public_user_infos.get('picture')
            })

        access_token = AuthAdaptater.create_token(user=final_user)
        return CustomResponse.send_response(message="Connexion réussie", status_code=200, data=ResponseData.login(access_token=access_token), success=True)


    @staticmethod
    def login_with_code():
        try:
            data = request.get_json()
            code = data.get('code')

            if not code:
                return CustomResponse.send_response(message="Le champ 'code' est requis", status_code=422)

            exchanges = exchange_code_for_token(code)
            access_token = exchanges.get('access_token')
            if not access_token:
                return CustomResponse.send_response(message="Échec lors de l'échange du code contre un token", status_code=400)

            public_user_infos = get_user_info(access_token)
            return GoogleController._handle_google_login(public_user_infos)

        except Exception as e:
            logger.error(f"Error in login_with_code function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)


    @staticmethod
    def login_with_refresh_token():
        try:
            data = request.get_json()
            refresh_token = data.get('refresh_token')

            if not refresh_token:
                return CustomResponse.send_response(message="Le champ 'refresh_token' est requis", status_code=422)

            access_token, _ = get_access_token(refresh_token)
            if not access_token:
                return CustomResponse.send_response(message="Impossible de générer un access token avec le refresh token fourni", status_code=400)

            public_user_infos = get_user_info(access_token)
            return GoogleController._handle_google_login(public_user_infos)

        except Exception as e:
            logger.error(f"Error in login_with_refresh_token function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)


    @staticmethod
    def login_with_id_token():
        try:
            data = request.get_json()
            id_token = data.get('id_token')

            if not id_token:
                return CustomResponse.send_response(message="Le champ 'id_token' est requis", status_code=422)

            public_user_infos = verify_google_id_token(id_token)
            if not public_user_infos:
                return CustomResponse.send_response(message="ID Token invalide", status_code=400)

            return GoogleController._handle_google_login(public_user_infos)

        except Exception as e:
            logger.error(f"Error in login_with_id_token function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)


    @staticmethod
    def set_password():
        try:
            data = request.get_json()

            required_fields = ['email', 'new_password', 'confirm_new_password']
            missing_fields = [f for f in required_fields if not data.get(f)]
            if missing_fields:
                return CustomResponse.send_response(message=f"Les champs suivants sont requis : {', '.join(missing_fields)}", status_code=422)

            email = data['email'].lower().strip()
            new_password = data['new_password']
            confirm_new_password = data['confirm_new_password']

            if not validate_password(new_password):
                message = "Le mot de passe ne respecte pas les critères de sécurité. Il doit contenir au moins 6 caractères dont une majuscule, une minuscule, un chiffre et un caractère spécial"
                return CustomResponse.send_response(message=message, status_code=422)

            if new_password != confirm_new_password:
                return CustomResponse.send_response(message="Le nouveau mot de passe et la confirmation ne correspondent pas", status_code=400)

            user = UserAdaptater.get_by_email(email)
            if (not user) or user.is_deleted:
                return CustomResponse.send_response(message="Nous avons rencontré un souci au cours de votre inscription avec l'email fourni. Veuillez contacter le support pour plus de clarté.", status_code=404)
            
            if user.is_google_authenticated:
                if user.password:
                    return CustomResponse.send_response(message="Vous avez déjà défini un mot de passe", status_code=400)
                elif UserAdaptater.update_password(user, new_password):
                    return CustomResponse.send_response(message="Mot de passe défini avec succès", success=True, status_code=200)

            return CustomResponse.send_response(message="Erreur lors de la définition du mot de passe", status_code=400)

        except Exception as e:
            logger.error(f"Error in set_password function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)
