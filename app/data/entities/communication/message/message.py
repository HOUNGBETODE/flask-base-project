from datetime import datetime, timezone
from data.entities.config.entities_config import db
from commons.const.string.app_string import AppString


class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_modified = db.Column(db.Boolean, default=False, nullable=False)
    writer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True) # only True for first message
    is_first = db.Column(db.Boolean, default=False, nullable=True)

    conversation_id = db.Column(db.String(36), db.ForeignKey('conversations.id'), nullable=False)
    conversation = db.relationship('Conversation', back_populates='messages')

    attachments = db.relationship('Attachment', back_populates='message', lazy=True, cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    is_deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)


    def to_dict(self):
        return {
            'id': self.id,
            'content': "Ce message a été supprimé" if self.is_deleted else self.content if (self.content != AppString.default_message_with_attachment_value) else "",
            'is_first': self.is_first,
            'conversation_id': self.conversation_id,
            'attachment_count': len([attachment for attachment in self.attachments if not attachment.is_deleted]) if self.attachments else 0,  
            'attachments': [attachment.to_dict_for_message() for attachment in self.attachments if not attachment.is_deleted] if not self.is_deleted else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted_at': self.is_deleted_at.isoformat() if self.is_deleted_at else None,
            'is_deleted': self.is_deleted,
            'is_modified': self.is_modified
        }


    def from_dict(self, data):
        self.content = data.get('content')
        self.writer_id = data.get('writer_id')
        self.conversation_id = data.get('conversation_id')
        return self


    def from_dict_for_update_message(self, data):
        self.content = data.get('content') if data.get('content') else self.content
        return self
