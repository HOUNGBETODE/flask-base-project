import pyotp
import threading
from flask import request, current_app
from commons.instances.instances import logger
from commons.config.config.config import Config
from uses_cases.user_use_case import UserUseCase
from uses_cases.send_mail_use_case import SendMail
from commons.enums.user_roles.roles import UserRole
from commons.helpers.response_data import ResponseData
from adaptater.auth.auth_adaptater import AuthAdaptater
from adaptater.user.user_adaptater import UserAdaptater
from flask_jwt_extended import get_jwt, get_jwt_identity
from commons.enums.user_genders.genders import UserGender
from commons.helpers.custom_response import CustomResponse
from adaptater.revoked_token.revoked_token_adaptater import RevokeTokenAdaptater
from commons.utils.utils import (
    get_empty_keys, validate_password, check_mail, is_valid_email, validate_username
)


class AuthController  :

    @staticmethod
    def signup():
        try: 
            data = request.get_json()
            email = data.get('email')
            username = data.get('username')
            gender = data.get('gender')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            required_fields = ['firstname', 'lastname', 'email', 'username', 'password', 'confirm_password']            
            validation_data = {field: data.get(field) for field in required_fields}            
            missing_fields = get_empty_keys(validation_data)
            
            if missing_fields:
                message = f"Erreur de validation : les champs suivants sont requis : {', '.join(missing_fields)}"
                return CustomResponse.send_response(message=message, status_code=422)
            
            if not is_valid_email(email):
                return CustomResponse.send_response(message="Email invalide", status_code=422, success=False)

            is_username_valid, _message = validate_username(username)
            if not is_username_valid:
                return CustomResponse.send_response(message=_message, status_code=422)

            if UserAdaptater.check_existing_username(username):
                return CustomResponse.send_response(message="Ce nom d'utilisateur a dejà été pris", status_code=422, success=False)

            if not validate_password(password):
                message = "Le mot de passe ne respecte pas les critères de sécurité. Il doit contenir au moins 6 caractères dont une majuscule, une minuscule, un chiffre et un caractère spécial"
                return CustomResponse.send_response(message=message, status_code=422)

            if password != confirm_password:
                return CustomResponse.send_response(message="Les mots de passes ne correspondent pas", status_code=422)
            
            if gender not in UserGender.list():
                return CustomResponse.send_response(message="La valeur du gender est aberrante", status_code = 422)
            
            email = email.lower().strip()
            data['email'] = email
            check_mail_result = check_mail(email)
            is_mail_disposable = check_mail_result['disposable']
            if is_mail_disposable:
                return CustomResponse.send_response(message="Adresse e-mail invalide : les adresses temporaires ne sont pas autorisées.", status_code=400, success=False)

            existing_user = UserAdaptater.get_by_email(email)
            if existing_user :
                return CustomResponse.send_response(message= "Nous avons rencontré un souci au cours de votre inscription avec l'email fourni. Veuillez contacter le support pour plus de clarté.", status_code= 400)
            
            user = AuthAdaptater.create_user(data=data)
            if user :
                return CustomResponse.send_response(message="Compte créé avec succès. Veuillez l'activer en renseignant le code reçu par mail.", success=True, status_code=201)
            
            return CustomResponse.send_response(message="Erreur lors de la création du compte", status_code=400)
        except Exception as e:
            logger.error(f"Error on signup function controller: {e}")
            return CustomResponse.send_serveur_error( error = e, status_code= 500)
    

    @staticmethod
    def resent_verification_code():
        try:
            data = request.get_json()
            email = data.get('email')

            if not email:
                return CustomResponse.send_response(message="L'e-mail est requis", status_code=400)
            
            email = email.lower().strip()
            data['email'] = email
            user = UserAdaptater.get_by_email(email=email)
            if user and (not user.is_deleted):
                if user.is_verified:
                    return CustomResponse.send_response(message="Compte déjà vérifié", status_code=400, success=False)

                new_verification_code = UserUseCase.send_admin_verification_code(email) if user.is_admin else UserUseCase.resend_account_verification_code(email)
                if new_verification_code:
                    return CustomResponse.send_response( message="Nouveau code envoyé avec succès", success=True,  status_code=200 )
            
            return CustomResponse.send_response(message="Erreur lors de l'envoi du code de vérification", status_code=500)
        except Exception as e:
            logger.error(f"Error in resent_verification_code function controller: {e}")
            return CustomResponse.send_serveur_error(error=e,  success=False,  status_code=500 )
        
    
    @staticmethod
    def verify_user_account():
        try:
            data = request.get_json()
            email = data.get('email')
            otp_code = data.get('otp_code')
            
            if not email or not otp_code:
                return CustomResponse.send_response(message="Email et code otp sont requis",status_code=400)

            email = email.lower().strip()
            data['email'] = email
            user = UserAdaptater.get_by_email(email)
            if user and (not user.is_deleted):
                if user.is_verified:
                    return CustomResponse.send_response(message="Compte déjà vérifié", status_code=400, success=False)

                if pyotp.TOTP(
                    s=user.account_activation_secret,
                    digits=Config.OTP_DIGITS_NUMBER,
                    interval=Config.OTP_EXPIRATION_TIMEOUT
                ).verify(otp_code):
                    UserAdaptater.activate_account(user)
                    access_token = AuthAdaptater.create_token(user=user)
                    return CustomResponse.send_response(message="Compte vérifié avec succès", success=True, status_code=200, data=ResponseData.login(access_token=access_token))
                else:
                    return CustomResponse.send_response(message="Code expiré ou incorrect", status_code=400)

            return CustomResponse. send_response(message ='Erreur lors de la vérification du compte utilisateur', status_code=400)
        except Exception as e:
            logger.error(f"Error in verify_user_account function controller: {e}")
            return CustomResponse.send_serveur_error( error=e, status_code=500)
        

    @staticmethod
    def login():
        try:
            device_info = {}
            device_info['device'] = request.headers.get('User-Agent', 'Non spécifié')
            if request.headers.getlist("X-Forwarded-For"):
                ip = request.headers.getlist("X-Forwarded-For")[0]
            else:
                ip = request.remote_addr
            device_info['remote_ip'] = ip

            data = request.get_json()
            credential = data.get('credential')
            password = data.get('password')

            required_fields = ['credential', 'password']            
            validation_data = {field: data.get(field) for field in required_fields}            
            missing_fields = get_empty_keys(validation_data)
            
            if missing_fields:
                message = f"Erreur de validation : les champs suivants sont requis : {', '.join(missing_fields)}"
                return CustomResponse.send_response(message=message, status_code=422)

            user = UserAdaptater.get_by_email_or_username(credential.strip())
            if not user:
                return CustomResponse.send_response(message="L'email / nom d'utilisateur ou le mot de passe est incorrect", status_code=400)

            if user.is_deleted:
                return CustomResponse.send_response(message="Nous avons rencontré un souci au cours de votre inscription avec l'email fourni. Veuillez contacter le support pour plus de clarté.", status_code=400)

            is_locked_flag, lock_message, lock_status = UserAdaptater.is_locked(user)
            if is_locked_flag:
                return CustomResponse.send_response(message=lock_message, status_code=lock_status, success=False)

            if not AuthAdaptater.verify_password(user, password):
                failed_message, failed_status = UserAdaptater.handle_failed_attempt(user)
                return CustomResponse.send_response(message=failed_message, status_code=failed_status, success=False)
            
            if user.is_admin and (user.role != UserRole.SUPER_ADMIN.value):
                UserAdaptater.unverify_account(user)
                UserUseCase.send_admin_verification_code(user.email)
                infos = {"firstname": user.firstname, "lastname": user.lastname, "gender": user.gender}
                return CustomResponse.send_response(message="Connexion réussie. Veuillez vérifier votre identité en renseignant le code reçu par mail.", status_code=200, data={"user": infos}, success=True)

            UserAdaptater.reset_lockout(user)
            access_token = AuthAdaptater.create_token(user=user)
            threading.Thread(
                target=SendMail.send_login_notification, 
                args=(current_app._get_current_object(), user, device_info)
            ).start()
            return CustomResponse.send_response(message="Connexion réussie", status_code=200, data=ResponseData.login(access_token=access_token), success=True)

        except Exception as e:
            logger.error(f"Error on login function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)


    @staticmethod
    def logout():
        try:
            token = get_jwt()
            if not token:
                return CustomResponse.send_response(message="Token introuvable ou invalide", success=False, status_code=401)

            jti = token.get('jti')
            if not jti:
                return CustomResponse.send_response(message="JWT ID (jti) introuvable", success=False, status_code=400)

            if RevokeTokenAdaptater.revoke_token(jti, token):
                identity = get_jwt_identity()
                if identity:
                    UserAdaptater.disconnect(identity)
                
                return CustomResponse.send_response(message="Déconnexion réussie", success=True, status_code=200)
        
            return CustomResponse.send_response(message="Erreur lors de la déconnexion de l'utilisateur", success=False, status_code=400)
        except Exception as e:
            logger.error(f"Error on logout function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)


    @staticmethod
    def forgot_password():
        try :
            data = request.get_json()
            email = data.get('email')

            if not email:
                return CustomResponse.send_response(message="L'e-mail est requis", status_code=422)
            
            email = email.lower().strip()
            data['email'] = email
            user = UserAdaptater.get_by_email(email)
            if user and (not user.is_deleted):            
                reset_code = UserUseCase.forgot_password_code(email)
                if reset_code:
                    return CustomResponse.send_response(message='Code envoyé avec succès',status_code=200, success=True)
            
            return CustomResponse.send_response(message ="Erreur lors de l'envoi du code", status_code=400)
        except Exception as e:
            logger.error(f"Error in forgot_password function controller: {e}")
            return CustomResponse.send_serveur_error(error = e, status_code= 500)
    
    
    @staticmethod
    def resent_forgot_password_code():
        try:
            data = request.get_json()
            email = data.get('email')

            if not email:
                return CustomResponse.send_response( message="Email est requis", success=False, status_code=400)

            email = email.lower().strip()
            data['email'] = email
            user = UserAdaptater.get_by_email(email=email)
            if user and (not user.is_deleted):
                new_verification_code = UserUseCase.resend_forgot_password_code(email)
                if new_verification_code:
                    return CustomResponse.send_response( message="Nouveau code envoyé avec succès", success=True,  status_code=200 )
            
            return CustomResponse.send_response(message="Erreur lors de l'envoi du code de réinitialisation", status_code=500)
        except Exception as e:
            logger.error(f"Error in resent_forgot_password_code function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)

    
    @staticmethod
    def reset_password():
        try:   
            data = request.get_json()
            email = data.get('email')
            otp_code = data.get('otp_code')
            new_password = data.get('new_password')
            confirm_new_password = data.get('confirm_new_password')

            required_fields = ['email', 'otp_code', 'new_password', 'confirm_new_password']            
            validation_data = {field: data.get(field) for field in required_fields}            
            missing_fields = get_empty_keys(validation_data)
            
            if missing_fields:
                message = f"Erreur de validation : les champs suivants sont requis : {', '.join(missing_fields)}"
                return CustomResponse.send_response(message=message, status_code=422)
            
            if not validate_password(new_password):
                message = "Le mot de passe ne respecte pas les critères de sécurité. Il doit contenir au moins 6 caractères dont une majuscule, une minuscule, un chiffre et un caractère spécial"
                return CustomResponse.send_response(message=message, status_code=422)

            if not (new_password == confirm_new_password):
                return CustomResponse. send_response(message ="Le nouveau mot de passe et celui de confirmation ne correspondent pas", status_code=400)

            email = email.lower().strip()
            data['email'] = email
            user = UserAdaptater.get_by_email(email)
            if user and (not user.is_deleted):
                if pyotp.TOTP(
                        s=user.password_reset_secret, 
                        digits=Config.OTP_DIGITS_NUMBER, 
                        interval=Config.OTP_EXPIRATION_TIMEOUT
                    ).verify(otp_code):
                    if UserAdaptater.update_password(user, new_password):
                        return CustomResponse.send_response(message='Mot de passe mis à jour avec succès', success=True, status_code=200)
                else:
                    return CustomResponse. send_response(message ='Code expiré ou incorrect', status_code=400)
            
            return CustomResponse.send_response(message='Erreur lors de la réinitialisation du mot de passe', status_code=500)
        except Exception as e:
            logger.error(f"Error in reset_password function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)
