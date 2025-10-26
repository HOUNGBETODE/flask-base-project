from sqlalchemy import exists
from data.entities.user.user import User
from commons.helpers.load_doten import Dotenv
from commons.instances.instances import logger
from commons.enums.user_roles.roles import UserRole
from data.entities.config.entities_config import db
from werkzeug.security import generate_password_hash
from commons.enums.user_genders.genders import UserGender


class SuperAdminAdaptater:

    @staticmethod
    def check_existing_super_admin() -> bool:
        try:
            return db.session.query(
                exists().where(
                    User.is_admin == True,
                    User.is_deleted == False,
                    User.role == UserRole.SUPER_ADMIN.value
                )
            ).scalar()
        except Exception as e:
            logger.error(f"Error checking existing super admin: {e}")
            raise e


    @staticmethod
    def create_super_admin() -> User:
        try:
            super_admin = User(
                gender=UserGender.MALE.value,
                firstname=Dotenv.ADMIN_USER_FIRSTNAME,
                lastname=Dotenv.ADMIN_USER_LASTNAME,
                username=Dotenv.ADMIN_USERNAME,
                is_admin=True,
                password=generate_password_hash(Dotenv.ADMIN_USER_PASSWORD),
                email=Dotenv.ADMIN_USER_EMAIL,
                role=UserRole.SUPER_ADMIN.value,
                is_verified=True,
                is_active=True,
            )
            db.session.add(super_admin)
            db.session.commit()
            return super_admin
        except Exception as e:
            logger.error(f"Error creating super admin user: {e}")
            raise e
