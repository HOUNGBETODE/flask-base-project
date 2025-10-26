from datetime import datetime, timezone
from data.entities.config.entities_config import db


class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False)
    token = db.Column(db.JSON, nullable=False)
    
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


    def from_dict(self, data):
        self.jti = data.get("jti")
        self.token = data.get("token")    
        return self
