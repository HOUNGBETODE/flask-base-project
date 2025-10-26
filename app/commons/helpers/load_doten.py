import os
from pathlib import Path
from dotenv import load_dotenv
from commons.instances.instances import logger


env_path = Path(__file__).resolve().parent.parent / 'const' / 'const' / '.env'


logger.info(env_path)
if not env_path.exists():
    raise FileNotFoundError(f"Le fichier .env est introuvable : {env_path}")

env_is_load = load_dotenv(env_path)


class Dotenv:
    SMTPSERVEUR = os.getenv('smtp_server')
    SMTPPORT = int(os.getenv('smtp_port'))
    SMTPUSER = os.getenv('smtp_user')
    SMTPPASSWORD = os.getenv('smtp_password')
    SQLALCHEMY_DATABASE_URI = os.getenv('data_base_uri')
    ADMIN_USER_FIRSTNAME = os.getenv('admin_user_firstname')
    ADMIN_USER_LASTNAME = os.getenv('admin_user_lastname')
    ADMIN_USER_EMAIL = os.getenv('admin_user_email')
    ADMIN_USERNAME = os.getenv('admin_username')
    ADMIN_USER_PASSWORD = os.getenv('admin_user_password')
    ADMIN_FRONT_BASE_URL = os.getenv('admin_front_base_url')
    GOOGLE_MAPS_API_KEY = os.getenv('google_maps_api_key')
    APP_SECRET_KEY = os.getenv('app_secret_key')
    JWT_SECRET_KEY = os.getenv('jwt_secret_key')
    X_RAPID_API_HOST = os.getenv('x_rapidapi_host')
    X_RAPID_API_KEY = os.getenv('x_rapidapi_key')
    FCM_SERVICE_ACCOUNT_KEY_JSON_PATH = os.getenv('fcm_service_account_key_json_path')
    OAUTH_CLIENT_ID = os.getenv('oauth_client_id')
    OAUTH_CLIENT_SECRET = os.getenv('oauth_client_secret')
    OAUTH_REDIRECT_URI = os.getenv('oauth_redirect_uri')
    FCM_PUBLIC_TOPIC = os.getenv('fcm_public_topic')
    BACK_OFFICE_URL = os.getenv('back_office_url')
    DEBUG_STATUS = bool(os.getenv('debug_status') == '1')
