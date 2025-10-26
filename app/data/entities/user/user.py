import uuid
from flask import request
from datetime import datetime, timezone
from commons.config.config.config import Config
from data.entities.config.entities_config import db
from commons.enums.user_roles.roles import UserRole
from werkzeug.security import generate_password_hash
from commons.const.string.app_string import AppString
from adaptater.notification.notification_adaptater import NotificationAdaptater


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    password_reset_secret = db.Column(db.String(50), nullable=True)
    account_activation_secret = db.Column(db.String(50), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    is_verified = db.Column(db.Boolean, nullable=False, default=False)
    avatar = db.Column(db.String(200), nullable=True)

    role = db.Column(db.String(15), nullable=False, default=UserRole.USER.value)
    username = db.Column(db.String(200), unique=True, nullable=False)
    temporal_password_in_use = db.Column(db.Boolean, nullable=False, default=False)
    password_failed_attempts = db.Column(db.Integer, nullable=False, default=0)
    account_lockout_duration = db.Column(db.Integer, nullable=False, default=0) # in minutes
    lockout_expires_at = db.Column(db.DateTime(timezone=True), nullable=True)
    is_connected = db.Column(db.Boolean, nullable=True, default=False)

    is_google_authenticated = db.Column(db.Boolean, default=False, nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    is_deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    last_activity_at = db.Column(db.DateTime(timezone=True), nullable=True)


    def to_dict(self, user_id: str = None, is_admin: bool = False):
        from adaptater.user.user_adaptater import UserAdaptater
        from adaptater.communication.conversation.conversation_adaptater import ConversationAdaptater
        user_base_dict = {
            'id': self.id,
            'gender': self.gender,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'is_admin': self.is_admin,
            'username': self.username,
            'role': self.role,
            'is_verified': self.is_verified,
            'is_active': self.is_active,
            'is_deleted': self.is_deleted,
            'temporal_password_in_use': bool(self.temporal_password_in_use),
            'notifications_count': NotificationAdaptater.get_unread_count(self.id),
            'is_password_set': bool(self.password),
            'is_google_authenticated': bool(self.is_google_authenticated),
            'avatar': (request.host_url + AppString.default_user_avatar) if (not self.avatar) else (request.host_url + self.avatar) if (Config.UPLOAD_USER_AVATAR in self.avatar) else self.avatar,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_activity_at': self.last_activity_at.isoformat() if self.last_activity_at else None,
            'is_deleted_at': self.is_deleted_at.isoformat() if self.is_deleted_at else None
        }
        if user_id and is_admin and (user_id != self.id):
            user_base_dict.update({
                "online_code": UserAdaptater.grade_connectivity_status(self.id)
            })
        if user_id and not is_admin:
            user_base_dict.update({
                "has_conversation_with": bool(ConversationAdaptater.get_between(self.id, user_id))
            })
        return user_base_dict
    

    def to_small_dict(self):
        return {
            'id': self.id,
            'gender': self.gender,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'is_active': self.is_active,
            'is_deleted': self.is_deleted,
            'avatar': (request.host_url + AppString.default_user_avatar) if (not self.avatar) else (request.host_url + self.avatar) if (Config.UPLOAD_USER_AVATAR in self.avatar) else self.avatar
        }


    def from_dict(self, data):
        hashed_password = generate_password_hash(data.get('password'), method='pbkdf2:sha256')
        self.firstname = data.get('firstname')
        self.lastname = data.get('lastname')
        self.email = data.get('email')
        self.username = data.get('username')
        self.gender = data.get('gender')
        self.password = hashed_password
        return self
    

    def from_dict_for_oauth(self, data):
        self.firstname = data.get('firstname')
        self.lastname = data.get('lastname')
        self.email = data.get('email')
        self.username = data.get('email').split('@')[0]
        self.gender = data.get('gender')
        self.avatar = data.get('avatar')
        return self


    def from_dict_for_update_user(self, data):
        self.firstname = data.get('firstname') if data.get('firstname') else self.firstname
        self.lastname = data.get('lastname') if data.get('lastname') else self.lastname
        self.email = data.get('email') if data.get('email') else self.email
        self.gender = data.get('gender') if data.get('gender') else self.gender
        self.username = data.get('username') if data.get('username') else self.username
        self.role = data.get('role') if data.get('role') else self.role
        return self
