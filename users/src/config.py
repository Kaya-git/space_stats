import logging
import logging.handlers
import os
from dataclasses import dataclass
import sys
from dotenv import load_dotenv
from sqlalchemy.engine import URL

sys.path.append(os.path.join(sys.path[0], 'users'))

load_dotenv()


@dataclass
class DataBaseConfig:
    """ Database connection variables """
    name: str = os.environ.get("DB_NAME")
    user: str = os.environ.get("DB_USER")
    passwd: str = os.environ.get("DB_PASS")
    port: str = os.environ.get("DB_PORT")
    host: str = os.environ.get("DB_HOST")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def build_connection_str(self) -> str:
        """ This function build a connection string """
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass
class Auth:
    "JWT secret"
    jwt_token = os.environ.get("SECRET_JWT")
    algorithm = os.environ.get("ALGORITHM")
    user_menager = os.environ.get("SECRET_USER_MENAGER")


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
        log_file = "../logs/users.log"
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
    logging_level = int(os.environ.get("LOGGING_LEVEL"))
    debug = bool(os.environ.get("DEBUG"))
    auth = Auth()
    db = DataBaseConfig()
    logger_setup = LoggerSetup()


conf = Configuration()
