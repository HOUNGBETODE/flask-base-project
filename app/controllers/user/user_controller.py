from flask import request
from commons.instances.instances import logger
from commons.helpers.response_data import ResponseData
from adaptater.auth.auth_adaptater import AuthAdaptater
from adaptater.user.user_adaptater import UserAdaptater
from commons.enums.user_genders.genders import UserGender
from services.smtp_function.send_mail import EmailService
from commons.helpers.custom_response import CustomResponse
from flask_jwt_extended import get_jwt_identity, get_jti, get_jwt
from commons.utils.utils import (
    get_empty_keys, validate_password, 
    is_valid_email, check_mail, generate_strong_password, validate_username
)


email_service = EmailService()

class UserController  :

    @staticmethod
    def add_admin():
        try: 
            data = request.get_json()
            email = data.get('email')
            username = data.get('username')

            required_fields = ['firstname', 'lastname', 'email', 'username']            
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

            email = email.lower().strip()
            data['email'] = email
            data['password'] = generate_strong_password(email)
            check_mail_result = check_mail(email)
            is_mail_disposable = check_mail_result['disposable']
            if is_mail_disposable:
                return CustomResponse.send_response(message="Adresse e-mail invalide : les adresses temporaires ne sont pas autorisées.", status_code=400, success=False)

            existing_user = UserAdaptater.get_by_email(email)
            if existing_user :
                return CustomResponse.send_response(message= "Nous avons rencontré un souci au cours de votre inscription avec l'email fourni. Veuillez contacter le support pour plus de clarté.", status_code= 400)
            
            user = UserAdaptater.add_admin(data=data)
            if user :
                return CustomResponse.send_response(message="Compte administrateur ajouté avec succès.", success=True, status_code=201)
            
            return CustomResponse.send_response(message="Erreur lors de l'ajout de l'administrateur", status_code=400)
        except Exception as e:
            logger.error(f"Error on add_admin function controller: {e}")
            return CustomResponse.send_serveur_error( error = e, status_code= 500)
    

    @staticmethod
    def update_user():
        try: 
            data = request.get_json()
            email =  data.get('email').lower().strip()
            gender = data.get('gender')
            username = data.get('username')
            user_id = get_jwt_identity()

            if gender and (gender not in [type_.value for type_ in UserGender]):
                return CustomResponse.send_response(message = "La valeur du gender est aberrante", status_code = 422)

            if username:
                is_username_valid, _message = validate_username(username)
                if not is_username_valid:
                    return CustomResponse.send_response(message=_message, status_code=422)

            existing_user = UserAdaptater.get_by_id(id= user_id)
            if existing_user :
                existing_user_with_mail = UserAdaptater.get_by_email(email=email)
                if username and (existing_user_with_mail.username != username) and UserAdaptater.check_existing_username(username):
                    return CustomResponse.send_response(message="Ce nom d'utilisateur a dejà été pris", status_code=422, success=False)

                if existing_user_with_mail and (existing_user_with_mail.id != user_id): 
                    return CustomResponse.send_response(message="Cette action n'est pas autorisée", status_code=403, data=None)
        
                data["role"] = None
                data["stand_id"] = None
                user = UserAdaptater.update(data=data, user=existing_user)
                return CustomResponse.send_response(message='Mise à jour effectuée avec succès', success=True, status_code=200, data= user.to_dict() )
            
            return CustomResponse.send_response(message='Erreur lors de la mise à jour du compte', status_code=400, data=None)
        except Exception as e:
            logger.error(f"Error in update_user function controller: {e}")
            return CustomResponse.send_serveur_error(error = e, status_code= 500)


    @staticmethod
    def get_user_profile():
        try:
            user = UserAdaptater.get_by_id(id = get_jwt_identity())
            if user:            
                user_data = user.to_dict()
                return CustomResponse.send_response(message="Données utilisateur recupérées avec succes.",status_code=200, data=user_data, success=True)

            return CustomResponse.send_response(message="Erreur lors de la récupération des détails de l'utilisateur", status_code=400)
        except Exception as e:
            logger.error(f"Error in get_user_profile function controller: {e}")
            return CustomResponse.send_serveur_error( error = e, status_code= 500)
    

    @staticmethod
    def get_storage_details():
        try:
            user = UserAdaptater.get_by_id(id = get_jwt_identity())
            if user:            
                return CustomResponse.send_response(message="Données de stockage recupérées avec succes.",status_code=200, data=user.to_dict_for_storage(), success=True)

            return CustomResponse.send_response(message="Erreur lors de la récupération des données de stockage relative à l'utilisateur", status_code=400)
        except Exception as e:
            logger.error(f"Error in get_storage_details function controller: {e}")
            return CustomResponse.send_serveur_error( error = e, status_code= 500)
    

    @staticmethod
    def get_one_user(user_id):
        try:
            user = UserAdaptater.get_any_by_id(user_id)
            if user:            
                user_data = user.to_dict()
                return CustomResponse.send_response(message="Données utilisateur recupérées avec succes.",status_code=200, data=user_data, success=True)

            return CustomResponse.send_response(message="Erreur lors de la récupération des détails de l'utilisateur", status_code=400)
        except Exception as e:
            logger.error(f"Error in get_one_user function controller: {e}")
            return CustomResponse.send_serveur_error( error = e, status_code= 500)
        

    @staticmethod
    def change_password():
        try :
            data = request.get_json()
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            confirm_new_password = data.get('confirm_new_password')
            user_id = get_jwt_identity()
            user = UserAdaptater.get_by_id(user_id)
            token = get_jwt()
            token_jti = get_jti()

            required_fields = ['current_password', 'new_password', 'confirm_new_password']     
            validation_data = {field: data.get(field) for field in required_fields}            
            missing_fields = get_empty_keys(validation_data)
            
            if missing_fields and not (token or token_jti):
                message = f"Erreur de validation : les champs suivants sont requis : {', '.join(missing_fields)}"
                return CustomResponse.send_response(message=message, status_code=422)
            
            if user:            
                if not AuthAdaptater.check_password(user.password, current_password):
                    return CustomResponse. send_response(message ="L'ancien mot de passe est incorrect", status_code=400)

                if not validate_password(new_password):
                    message = "Le mot de passe ne respecte pas les critères de sécurité. Il doit contenir au moins 6 caractères dont une majuscule, une minuscule, un chiffre et un caractère spécial"
                    return CustomResponse.send_response(message=message, status_code=422)

                if not (new_password == confirm_new_password):
                    return CustomResponse. send_response(message ="Le nouveau mot de passe et celui de confirmation ne correspondent pas", status_code=400)

                if UserAdaptater.update_password(user, new_password, token, token_jti):
                    return CustomResponse. send_response(message ='Mot de passe mis à jour avec succès. Veuillez vous connecter à nouveau.', success= True, status_code=200)
            
            return CustomResponse. send_response(message ='Erreur lors de la mise à jour du mot de passe', status_code=400)
        except Exception as e:
            logger.error(f"Error in change_password function controller: {e}")
            return CustomResponse.send_serveur_error( error = e, status_code= 500)


    @staticmethod
    def delete_my_account():
        try:
            user_id = get_jwt_identity()
            user = UserAdaptater.get_by_id(user_id)

            if user:
                success = UserAdaptater.delete(user)
                if success:
                    return CustomResponse.send_response(message='Utilisateur supprimé avec succès', success=True, status_code=200)
            
            return CustomResponse.send_response(message="Erreur lors de la suppression du compte", status_code=400)
        except Exception as e:
            logger.error(f"Error in delete_my_account function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)
        
    
    @staticmethod
    def delete_user_account(user_id):
        try:
            user = UserAdaptater.get_any_by_id(user_id)
            if not user.is_deleted:
                success = UserAdaptater.delete(user)
                if success:
                    return CustomResponse.send_response(message='Utilisateur supprimé avec succès', success=True, status_code=200)
            
            return CustomResponse.send_response(message="Erreur lors de la suppression du compte", status_code=400)
        except Exception as e:
            logger.error(f"Error in delete_user_account function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)
    
    
    @staticmethod
    def restore_user_account(user_id):
        try:
            user = UserAdaptater.get_any_by_id(user_id)
            if user.is_deleted:
                success = UserAdaptater.restore(user)
                if success:
                    return CustomResponse.send_response(message='Compte restauré avec succès', success=True, status_code=200)
            
            return CustomResponse.send_response(message="Erreur lors de la restauration du compte", status_code=400)
        except Exception as e:
            logger.error(f"Error in restore_my_account function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)


    @staticmethod
    def user_avatar():
        try:
            if 'avatar' not in request.files:
                return CustomResponse.send_response(message='Aucun fichier avatar fourni', status_code=422)
            
            avatar_file = request.files.get('avatar')            
            user_id = get_jwt_identity()
            user = UserAdaptater.get_by_id(id = user_id)            
            updated_user = UserAdaptater.avatar(user, avatar_file)
            
            return CustomResponse.send_response(message='Avatar créé avec succès', status_code=201, success=True, data=updated_user.to_dict())
        except Exception as e:
            logger.error(f"Error in user_avatar function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)


    @staticmethod
    def delete_avatar():
        try:
            user_id = get_jwt_identity()
            user = UserAdaptater.get_by_id(user_id)
            
            if not user:
                return CustomResponse.send_response(message='Utilisateur non trouvé', status_code=404)
            
            if not user.avatar:
                return CustomResponse.send_response(message='Aucun avatar à supprimer', status_code=400)
            
            updated_user = UserAdaptater.delete_avatar(user)
            return CustomResponse.send_response(message='Avatar supprimé avec succès', status_code=200, success=True, data=updated_user.to_dict())
        except Exception as e:
            logger.error(f"Error in delete_avatar function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)
        
    
    @staticmethod    
    def get_all_users(only_deleted = False):
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            sort_field  = request.args.get('sort_field', type=str)
            filter_field  = request.args.get('filter_field', type=str)
            filter_value  = request.args.get('filter_value', type=str)
            sort_direction = request.args.get('sort_direction', type=str)
            q = request.args.get('q', type=str)
            q_name = request.args.get('q_name', type=str)
            q_email = request.args.get('q_email', type=str)
            q_username = request.args.get('q_username', type=str)
            requester = UserAdaptater.get_by_id(get_jwt_identity())

            pagination = UserAdaptater.get_all(requester.id, page, per_page, q, sort_direction, sort_field, filter_field, filter_value, q_name, q_email, q_username, only_deleted)
            users = pagination.items
            
            users_data = [user.to_dict(requester.id, requester.is_admin) for user in users]
            data= ResponseData.get_all_users(
                users_data=users_data, 
                page= page, 
                per_page=per_page, 
                current_page=pagination.page, 
                sort_direction=sort_direction, 
                sort_field=sort_field, 
                q=q, 
                total_pages=pagination.pages, 
                total=pagination.total,
                filter_field=filter_field,
                filter_value=filter_value,
                q_name=q_name,
                q_email=q_email,
                q_username=q_username,
                has_next=pagination.has_next,
                has_prev=pagination.has_prev
            )
            return CustomResponse.send_response(message="Utilisateurs récupérés avec succès",status_code=200, data=data, success=True)
               
        except Exception as e:
            logger.error(f"Error in get_all_users controller: {e}")
            return CustomResponse.send_serveur_error(error=e, status_code=500)


    @staticmethod
    def toggle_user_active_status(user_id):
        try:
            requester_id = get_jwt_identity()            
            existing_user = UserAdaptater.get_by_id(user_id)

            if not existing_user:
                return CustomResponse.send_response(message="Compte introuvable ou supprimé", status_code=404, success=False)
            
            if requester_id == existing_user.id:
                return CustomResponse.send_response(message="Action non autorisée", success=False, status_code=403)
                        
            updated_user = UserAdaptater.toggle_active_status(existing_user)
            if not updated_user.is_active :
                email_service.send_email(to_email=updated_user.email, subject= "Votre compte a été desactivé", message= f"Bonjour {updated_user.firstname} {updated_user.lastname},<br/><br/>Votre compte a été desactivé,  Veuillez vous connecter pour jouir pleinement de l'application")
                return CustomResponse.send_response(message="Compte  desactivé avec succès", success=True, status_code=200)
            else:
                email_service.send_email(to_email=updated_user.email, subject= "Votre compte a été activé", message= f"Bonjour {updated_user.firstname} {updated_user.lastname},<br/><br/>Votre compte a été activé, Veuillez contactez notre service pour plus d'informations.")
                return CustomResponse.send_response(message="Compte activé avec succès", success=True, status_code=200) 
            
        except Exception as e:
            logger.error(f"Error in toggle_user_active_status controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)    
