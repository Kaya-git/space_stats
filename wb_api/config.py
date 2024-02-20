# import os
from dotenv import load_dotenv
import logging
import logging.handlers
from dataclasses import dataclass


load_dotenv()


@dataclass
class LoggerSetup:

    def __init__(self) -> None:
        self.logger = logging.getLogger('')
        self.setup_logging()

    def setup_logging(self):
        # add log format
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(
            level=logging.INFO,
            format=LOG_FORMAT
        )

        # configure formatter for logger
        formatter = logging.Formatter(LOG_FORMAT)

        # configure console handler
        console = logging.StreamHandler()
        console.setFormatter(formatter)

        # configure TimeRotatingFileHandler
        log_file = "logs/exchange.log"
        file = logging.handlers.TimedRotatingFileHandler(
            filename=log_file,
            when="midnight",
            backupCount=5
        )
        file.setFormatter(formatter)

        # add handlers
        self.logger.addHandler(console)
        self.logger.addHandler(file)


@dataclass
class Configuration:
    loggersetup = LoggerSetup()


conf = Configuration()
