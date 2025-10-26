from data.entities.user.user import User
from commons.instances.instances import logger
from uses_cases.user_use_case import UserUseCase 
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from data.entities.config.entities_config import db
from commons.enums.user_genders.genders import UserGender


class AuthAdaptater :

    @staticmethod
    def create_user(data)-> User :
        try :
            user = User()
            user = user.from_dict(data=data)
            UserUseCase.send_account_activation_code(user)
            
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            logger.error(f"Error in create_user function adaptater: {e}")
            db.session.rollback()
            raise e 
    
    
    @staticmethod
    def create_google_user(data)-> User :
        try :
            user = User()
            user = user.from_dict_for_oauth(data=data)
            user.is_admin = True
            user.is_active = True
            user.is_verified = True
            user.is_google_authenticated = True
            user.gender = UserGender.UNDEFINED.value

            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            logger.error(f"Error in create_google_user function adaptater: {e}")
            db.session.rollback()
            raise e

        
    @staticmethod
    def verify_password(user : User, password ):
        try:
            return check_password_hash(user.password, password)
        except Exception as e:
            logger.error(f"Error in verify_password function adaptater: {e}")
            raise e
    

    @staticmethod    
    def check_password(password, old_password ):
        try:
            return check_password_hash(password, old_password)
        except Exception as e:
            logger.error(f"Error in check_password function adaptater: {e}")
            raise e


    @staticmethod
    def create_token(user : User):        
        try:
            access_token = create_access_token(identity=user.id)
            return access_token
        except Exception as e:
            logger.error(f"Error in create_token function adaptater: {e}")
            raise e
