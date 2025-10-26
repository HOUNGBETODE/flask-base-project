import logging
from termcolor import colored

class ColoredFormatter(logging.Formatter):
    def __init__(self, fmt):
        super().__init__(fmt, datefmt='%Y-%m-%d %H:%M:%S')

    def format(self, record):
        log_message = super().format(record)
        colors = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'magenta'
        }
        return colored(log_message, colors.get(record.levelname, 'white'))

class SetLogger:
    @staticmethod
    def init_logger():
        logger = logging.Logger("mon_logger", level=logging.DEBUG)
        
        # Gestionnaire pour la console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Gestionnaire pour le fichier log
        file_handler = logging.FileHandler("app.log", mode='a', encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Ajout des gestionnaires au logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger

# Utilisation du logger
logger = SetLogger.init_logger()
logger.debug("C'est un message DEBUG")
logger.info("C'est un message INFO")
logger.warning("C'est un message WARNING")
logger.error("C'est un message ERROR")
logger.critical("C'est un message CRITICAL")
