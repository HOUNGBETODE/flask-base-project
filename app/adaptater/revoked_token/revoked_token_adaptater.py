from commons.instances.instances import logger
from data.entities.config.entities_config import db
from data.entities.revoked_token.revoked_token import RevokedToken


class RevokeTokenAdaptater :

    @staticmethod
    def token_is_revoked(jti)-> RevokedToken | None:
        try:
            return RevokedToken.query.filter_by(jti = jti).first()
        except Exception as e:
            logger.error(f"Error checking token revocation status: {e}")
            raise e


    @staticmethod
    def revoke_token(jti: str, token: str) -> RevokedToken:
        try:
            revoked_token = RevokedToken().from_dict({
                "jti": jti,
                "token": token
            })
            db.session.add(revoked_token)
            db.session.commit()
            return revoked_token
        except Exception as e:
            logger.error(f"Error revoking token: {e}")
            raise e
