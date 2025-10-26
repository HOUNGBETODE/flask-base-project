from flask import request
from datetime import datetime, timezone
from data.entities.config.entities_config import db


class Attachment(db.Model):
    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=True, default='')
    file_size = db.Column(db.BigInteger, nullable=False, default=0)

    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    message = db.relationship('Message', back_populates='attachments')

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    is_deleted_at = db.Column(db.DateTime(timezone=True), nullable=True)


    def to_dict(self):
        return {
            'id': self.id,
            'file_path': request.host_url + self.file_path,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'message_id': self.message_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted_at': self.is_deleted_at.isoformat() if self.is_deleted_at else None,
            'is_deleted': self.is_deleted
        }


    def to_dict_for_message(self):
        return {
            'id': self.id,
            'file_path': request.host_url + self.file_path,
            'file_name': '_'.join(self.file_name.split('_')[1:]),
            'file_size': self.file_size
        }


    def from_dict(self, data):
        self.file_path = data.get('file_path')
        self.file_name = data.get('file_name', 'msg-attachment')
        self.file_size = data.get('file_size')
        self.message_id = data.get('message_id')
        return self


    def from_dict_for_update_attachment(self, data):
        self.file_path = data.get('file_path') if data.get('file_path') else self.file_path
        self.file_name = data.get('file_name') if data.get('file_name') else self.file_name
        self.file_size = data.get('file_size') if data.get('file_size') else self.file_size
        self.is_deleted = data.get('is_deleted', self.is_deleted)
        return self
