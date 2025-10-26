import pyotp
from typing import Optional
from data.entities.user.user import User
from sqlalchemy import desc, asc, exists, or_
from commons.instances.instances import logger
from commons.config.config.config import Config
from datetime import datetime, timezone, timedelta
from commons.enums.user_roles.roles import UserRole
from data.entities.config.entities_config import db
from werkzeug.security import generate_password_hash
from commons.utils.file_utils import FileUploadManager
from adaptater.revoked_token.revoked_token_adaptater import RevokeTokenAdaptater


class UserAdaptater :

    @staticmethod
    def add_admin(data)-> User :
        from uses_cases.user_use_case import UserUseCase
        try :
            user = User()
            user = user.from_dict(data=data)
            UserUseCase.send_admin_welcome_email(user.username, user.email, data["password"])
            user.is_admin = True
            user.is_active = True
            user.temporal_password_in_use = True
            user.role = UserRole.ADMIN.value

            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            logger.error(f"Error in add_admin_user function adaptater: {e}")
            db.session.rollback()
            raise e 

    
    @staticmethod
    def get_by_email_or_username(input_: str) -> Optional[User]:
        try:
            return User.query.filter(
                or_(
                    User.email.ilike(f"%{input_}%"),
                    User.username == input_
                ),
                # User.is_deleted == False
            ).first()
        except Exception as e:
            logger.error(f"Error in get_by_email_or_username function adapter: {e}")
            raise e


    @staticmethod
    def get_by_email(email) -> User:
        try:
            return User.query.filter(
                User.email.ilike(email),
                # User.is_deleted == False
            ).first()
        except Exception as e:
            logger.error(f"Error in get_by_email function adapter: {e}")
            raise e
    

    @staticmethod
    def get_admin_emails() -> list[str]:
        try:
            admins = User.query.filter(
                User.is_admin == True,
                User.is_deleted == False,
                User.is_active == True,
                User.is_verified == True
            ).all()
            return [admin.email for admin in admins]
        except Exception as e:
            logger.error(f"Error in get_admin_emails function adapter: {e}")
            raise e
    

    @staticmethod
    def check_existing_username(username: str) -> bool:
        try:
            return db.session.query(exists().where(User.username == username)).scalar()
        except Exception as e:
            logger.error(f"Error checking existing username function adaptater: {e}")
            raise e


    @staticmethod
    def get_by_id(id) -> User:
        try:
            return User.query.filter_by(id=id, is_deleted=False).first()
        except Exception as e:
            logger.error(f"Error in get_user_by_id function adaptater: {e}")
            raise e


    @staticmethod
    def get_any_by_id(id) -> User:
        try:
            return User.query.filter_by(id=id).first()
        except Exception as e:
            logger.error(f"Error in get_user_by_id function adaptater: {e}")
            raise e


    @staticmethod
    def disconnect(user_id):
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                user.is_connected = False
                db.session.commit()
        except Exception as e:
            logger.error(f"Error in disconnect_user function adaptater: {e}")
            db.session.rollback()
            raise e


    @staticmethod
    def update( user : User, data)-> User :
        try :
            user = user.from_dict_for_update_user(data)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            logger.error(f"Error in update_user function adaptater: {e}")
            db.session.rollback()
            raise e


    @staticmethod
    def generate_password_reset_secret( user: User):
        try :
            otp_secret = pyotp.random_base32()
            user.password_reset_secret = otp_secret
            db.session.commit()
            return otp_secret
        except Exception as e:
            logger.error(f"Error in generate_password_reset_secret function adaptater: {e}")
            db.session.rollback()
            raise e


    @staticmethod 
    def generate_account_activation_secret(user: User):
        try: 
            otp_secret = pyotp.random_base32()
            user.account_activation_secret = otp_secret
            db.session.commit()
            return otp_secret
        except Exception as e:
            logger.error(f"Error in generate_account_activation_secret function adaptater: {e}")
            db.session.rollback()
            raise e


    @staticmethod
    def activate_account(user: User):
        try: 
            user.is_verified = True
            user.is_active = True
            user.account_activation_secret = None
            user.password_failed_attempts = 0
            user.account_lockout_duration = 0
            user.lockout_expires_at = None
            user.is_connected = True
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error in activate_user_account function adaptater: {e}")
            db.session.rollback()
            raise e


    @staticmethod    
    def unverify_account(user: User):
        try: 
            user.is_verified = False
            user.account_activation_secret = None
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error in unverify_admin_account_on_login function adaptater: {e}")
            db.session.rollback()
            raise e


    @staticmethod    
    def update_password(user: User, new_password : str, token: str = None, token_jti : str = None):
        try: 
            hashed_password = generate_password_hash( new_password, method='pbkdf2:sha256')
            user.password = hashed_password
            user.password_reset_secret = None
            user.temporal_password_in_use = False
            user.is_connected = False
            db.session.commit()

            if token and token_jti:
                assert RevokeTokenAdaptater.revoke_token(token_jti, token)

            return True
        except Exception as e:
            logger.error(f"Error in update_user_password function adaptater: {e}")
            db.session.rollback()
            raise e
        

    @staticmethod    
    def delete(user: User):
        try: 
            user.is_deleted = True
            user.email += " - deleted"
            user.is_deleted_at = datetime.now(timezone.utc)
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error in delete user function adaptater : {e}")
            db.session.rollback()
            raise e
    

    @staticmethod    
    def restore(user: User):
        try: 
            user.is_deleted = False
            user.email = user.email.replace(" - deleted", "")
            user.is_deleted_at = None
            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error in restore user function adaptater : {e}")
            db.session.rollback()
            raise e

    
    @staticmethod    
    def get_all(user_id, page, per_page, q=None, sort_direction = None, sort_field=None, filter_field=None, filter_value=None, q_name = None, q_email = None, q_username = None, only_deleted=False):
        try:
            query = User.query.filter(User.is_deleted == only_deleted, User.id != user_id)
            
            if q:
                filtre_like = f"%{q}%"
                query = query.filter(
                    (User.email.ilike(filtre_like)) |
                    (User.firstname.ilike(filtre_like)) |
                    (User.lastname.ilike(filtre_like))
                )

            if q_name is not None:
                query = query.filter(
                    (User.firstname.ilike(f"%{q_name}%")) |
                    (User.lastname.ilike(f"%{q_name}%"))
                )

            if q_email is not None:
                query = query.filter(
                    (User.email.ilike(f"%{q_email}%"))
                )

            if q_username is not None:
                query = query.filter(
                    (User.username.ilike(f"%{q_username}%"))
                )

            if sort_field and hasattr(User, sort_field):
                sort_column = getattr(User, sort_field)
                query = query.order_by(asc(sort_column) if sort_direction == 'asc' else desc(sort_column))
            else:
                if not only_deleted:
                    query = query.order_by(desc(User.created_at))
                else:
                    query = query.order_by(desc(User.is_deleted_at))

            if filter_field and filter_value:
                if filter_field not in ("role", "is_deleted", "is_connected", "is_active", "is_verified", "gender"):
                    raise ValueError(
                        f"Le champ '{filter_field}' n'est pas autorisé pour le filtrage dynamique. "
                        "Champs autorisés : role, is_active, is_deleted, , is_connected, is_verified, gender."
                    )
                if hasattr(User, filter_field):
                    field_attr = getattr(User, filter_field)
                    if isinstance(field_attr.property.columns[0].type, db.Boolean):
                        filter_bool = filter_value.lower() == 'true'
                        query = query.filter(field_attr == filter_bool)
                    else:
                        query = query.filter(field_attr.ilike(f"%{filter_value}%"))
                else:
                    raise ValueError(f"Le champ {filter_field} n'existe pas dans le modèle User.")

            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            return pagination
        except Exception as e:
            logger.error(f"Error in get_all_users function adaptater: {e}")
            raise e

     
    @staticmethod
    def toggle_active_status(user: User) -> User:
        try:
            user.is_active = not user.is_active
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            logger.error(f"Error in toggle_user_active_status function adaptater: {e}")
            db.session.rollback()
            raise e


    @staticmethod
    def avatar(user: User, avatar_file) -> User:
        try:            
            if user.avatar:
                FileUploadManager.delete_one_file(user.avatar)
            avatar_upload_success, avatar_path  = FileUploadManager.upload_one_file(avatar_file, Config.UPLOAD_USER_AVATAR)
           
            if avatar_upload_success:
                user.avatar = avatar_path
                db.session.add(user)
                db.session.commit()
                return user
        
        except Exception as e:
            logger.error(f"Error creating user avatar: {e}")
            db.session.rollback()
            raise e
    

    @staticmethod
    def delete_avatar(user: User) -> User:
        try:
            if user.avatar:
                FileUploadManager.delete_one_file(user.avatar)              
                user.avatar = None
                db.session.add(user)
                db.session.commit()
            return user
        except Exception as e:
            logger.error(f"Error deleting user avatar: {e}")
            db.session.rollback()
            raise e


    @staticmethod
    def is_locked(user: User) -> tuple[bool, str, int]:
        now = datetime.now(timezone.utc)
        if user.lockout_expires_at and user.lockout_expires_at > now:
            remaining_seconds = (user.lockout_expires_at - now).total_seconds()
            remaining_minutes = max(0, round(remaining_seconds / 60))
            message = f"Compte verrouillé. Veuillez patienter {remaining_minutes} minutes avant de réessayer."
            return True, message, 423
        return False, None, None


    @staticmethod
    def handle_failed_attempt(user: User) -> tuple[str, int]:
        now = datetime.now(timezone.utc)
        try:
            user.password_failed_attempts += 1
            db.session.commit()

            if user.password_failed_attempts >= 3:
                exponent = user.password_failed_attempts - 3
                duration_minutes = 5 * (2 ** exponent)
                expires_at = now + timedelta(minutes=duration_minutes)
                
                user.account_lockout_duration = duration_minutes
                user.lockout_expires_at = expires_at
                db.session.commit()
                
                message = f"Compte verrouillé pour {duration_minutes} minutes suite à trop de tentatives échouées. Veuillez patienter avant de réessayer."
                return message, 423
            
            return "L'email / nom d'utilisateur ou le mot de passe est incorrect", 400
        
        except Exception as e:
            logger.error(f"Erreur lors de la gestion d'un échec de tentative pour {user.email}: {e}")
            db.session.rollback()
            raise e


    @staticmethod
    def reset_lockout(user : User):
        try:
            user.password_failed_attempts = 0
            user.account_lockout_duration = 0
            user.lockout_expires_at = None
            user.is_connected = True
            db.session.commit()
            logger.info(f"Verrouillage réinitialisé pour l'utilisateur {user.email}")
        except Exception as e:
            logger.error(f"Erreur lors de la réinitialisation du verrouillage pour {user.email}: {e}")
            db.session.rollback()
            raise e
    

    @staticmethod
    def grade_connectivity_status(obj_id: str) -> int:
        """
        Retourne le statut de connectivité de l'utilisateur :
        0 -> is_connected False
        1 -> is_connected True et last_activity_at récent (moins de 5 minutes)
        2 -> is_connected True mais last_activity_at vieux de plus de 5 minutes
        """
        try:
            user = db.session.query(User).filter(User.id == obj_id).first()

            if not user:
                logger.warning(f"User with id {obj_id} not found")
                return 0

            if not user.is_connected:
                return 0

            if user.last_activity_at:
                now = datetime.now(timezone.utc)
                delta = now - user.last_activity_at
                if delta <= timedelta(minutes=5):
                    return 1
                else:
                    return 2
            else:
                return 2

        except Exception as e:
            logger.error(f"Error checking connectivity status for user {obj_id}: {e}")
            raise e
