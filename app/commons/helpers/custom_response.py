from flask import jsonify
from commons.config.config.config import Config


class CustomResponse : 

    @staticmethod
    def send_serveur_error(error , status_code=500, success=False, message = None):
        """
        Fonction pour envoyer une réponse d'erreur serveur JSON avec un code HTTP spécifique.
        
        :param message: Message d'erreur à inclure dans la réponse.
        :param status_code: Code HTTP de l'erreur (par défaut 400).
        :param success: Indicateur de succès (par défaut False).
        :return: Objet JSON avec le message d'erreur et le statut.
        """

        response = {
            'message': "une erreur est survenue",
            'success': success
        }
        if Config.DEBUG:
            response.update({'error': str(error)})

        if message is not None:
            response['message'] = message

        return jsonify(response), status_code
    
    @staticmethod    
    def send_response(message, data=None , status_code=400, success=False):
        """
        Fonction pour envoyer une réponse  JSON avec un code HTTP spécifique.
        
        :param message: Message d'erreur à inclure dans la réponse.
        :param status_code: Code HTTP de l'erreur (par défaut 400).
        :param success: Indicateur de succès (par défaut False).
        :return: Objet JSON avec le message d'erreur et le statut.
        """
        response = {
            'message': message,
            'success': success
        }
        
        if data is not None:
            response['data'] = data
        
        return jsonify(response), status_code