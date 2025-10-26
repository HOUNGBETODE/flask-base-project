from flask import Flask
from core.scheduler.scheduler import scheduler
from services.scheduler_job.scheduler_sample_job import sample_job


def initialize_scheduler(app : Flask):

    # Démarrage du scheduler
    scheduler.init_app(app)
    scheduler.start()

    # ajout des jobs à exécuter
    scheduler.add_job(
        id='a_sample_job_for_test_purpose',
        func=sample_job,
        trigger='interval',
        seconds=60  # Exécution toutes les minutes
    )
