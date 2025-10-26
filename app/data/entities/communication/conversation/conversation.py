import uuid
from datetime import datetime, timezone
from data.entities.config.entities_config import db
from commons.const.string.app_string import AppString


class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    messengers = db.Column(db.JSON, nullable=False, default=[]) # [{id: '...', unread_count: '...'}, ...]

    messages = db.relationship(
        'Message',
        lazy=True,
        cascade='all, delete-orphan',
        back_populates='conversation',
        primaryjoin=f"and_(Conversation.id == Message.conversation_id, Message.is_deleted == False, Message.content != '{AppString.default_message_value}')"
    )

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    is_deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)


    def to_dict(self):
        return {
            'id': self.id,
            'messengers': self.messengers,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted_at': self.is_deleted_at.isoformat() if self.is_deleted_at else None,
            'is_deleted': self.is_deleted
        }


    def from_dict(self, data):
        self.messengers = data.get("messengers")
        return self
