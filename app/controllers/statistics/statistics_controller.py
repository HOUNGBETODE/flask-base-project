from commons.instances.instances import logger
from commons.helpers.custom_response import CustomResponse
from adaptater.statistics.statistics_adaptater import StatisticsAdaptater


class StatisticController:

    @staticmethod
    def get_dashboard_statistics():
        try:
            stats = StatisticsAdaptater.get_dashboard_stats()
            return CustomResponse.send_response(message="Statistiques du dashboard récupérées avec succès.", status_code=200, success=True, data=stats)
        except Exception as e:
            logger.error(f"Error in get_dashboard_statistics function controller: {e}")
            return CustomResponse.send_serveur_error(error=e, success=False, status_code=500)
