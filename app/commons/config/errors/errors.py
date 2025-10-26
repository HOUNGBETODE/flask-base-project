from flask import jsonify
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError,
    DecodeError,
    InvalidSignatureError,
    InvalidAudienceError,
    InvalidIssuerError,
    ImmatureSignatureError,
    MissingRequiredClaimError,
    InvalidAlgorithmError
) 
from werkzeug.exceptions import HTTPException
from commons.helpers.custom_response import CustomResponse


def register_error_handlers(app):
    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_signature_error(e):
        """Handle expired JWT tokens."""
        return CustomResponse.send_serveur_error(message="Your token has expired. Please log in again.",status_code=401, error=e)

    @app.errorhandler(InvalidTokenError)
    def handle_invalid_token_error(e):
        """Handle invalid JWT tokens."""
        return CustomResponse.send_serveur_error(message="The token provided is invalid.",status_code=401, error=e)

    # Add custom errors (e.g., for your application-specific exceptions)
    @app.errorhandler(KeyError)
    def handle_key_error(e):
        """Handle missing keys in requests or data."""
        return CustomResponse.send_serveur_error(message="A required field is missing.",status_code=400, error=e)    

    @app.errorhandler(DecodeError)
    def handle_decode_error(e):
        return CustomResponse.send_serveur_error(message="Le token ne peut pas être décodé.", status_code=401, error=e)

    @app.errorhandler(InvalidSignatureError)
    def handle_invalid_signature(e):
        return CustomResponse.send_serveur_error(message="Signature du token invalide.", status_code=401, error=e)

    @app.errorhandler(InvalidAudienceError)
    def handle_invalid_audience(e):
        return CustomResponse.send_serveur_error(message="Audience invalide dans le token.", status_code=401, error=e)

    @app.errorhandler(InvalidIssuerError)
    def handle_invalid_issuer(e):
        return CustomResponse.send_serveur_error(message="Émetteur du token invalide.", status_code=401, error=e)

    @app.errorhandler(ImmatureSignatureError)
    def handle_immature_signature(e):
        return CustomResponse.send_serveur_error(message="Le token n'est pas encore actif.", status_code=401, error=e)

    @app.errorhandler(MissingRequiredClaimError)
    def handle_missing_claim(e):
        return CustomResponse.send_serveur_error(message=f"Le token est incomplet, claim requis manquant", status_code=401, error=e)

    @app.errorhandler(InvalidAlgorithmError)
    def handle_invalid_algo(e):
        return CustomResponse.send_serveur_error(message="Algorithme utilisé pour le token invalide ou non supporté.", status_code=401, error=e)


    return app
