from datetime import datetime, timezone
from data.entities.config.entities_config import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    unread = db.Column(db.Boolean, nullable=True, default=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
