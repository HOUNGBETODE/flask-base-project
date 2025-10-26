from commons.instances.instances import logger
from adaptater.user.user_adaptater import UserAdaptater
from commons.helpers.custom_response import CustomResponse
from commons.utils.utils import validate_username, validate_ifu


class PublicController:

    @staticmethod
    def find_username(username):
        try:
            is_valid, message = validate_username(username)
            if not is_valid:
                return CustomResponse.send_response(message=message, success=False, status_code=422)

            if UserAdaptater.check_existing_username(username):
                return CustomResponse.send_response(message="Nom d'utilisateur déjà pris.", success=False, status_code=400)

            return CustomResponse.send_response(success=True, status_code=200, message="Nom d'utilisateur valide et disponible.")
        except Exception as e:
            logger.error(f"Error on find_username function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)
