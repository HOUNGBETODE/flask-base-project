from datetime import timedelta
from commons.helpers.load_doten import Dotenv

class Config:
    DEBUG = Dotenv.DEBUG_STATUS
    SQLALCHEMY_DATABASE_URI = Dotenv.SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = Dotenv.APP_SECRET_KEY
    JWT_SECRET_KEY = Dotenv.JWT_SECRET_KEY
    OTP_DIGITS_NUMBER = 6
    OTP_EXPIRATION_TIMEOUT = 300 # in secondes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=3)
    UPLOAD_FOLDER = 'files'
    UPLOAD_USER_AVATAR = 'files/user-avatars'
    UPLOAD_ATTACHMENT = "files/attachments"
    DELETED_ATTACHMENTS = "files/deleted/attachments"
