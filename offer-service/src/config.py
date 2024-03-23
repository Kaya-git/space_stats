import os
from dotenv import load_dotenv
import logging
from dataclasses import dataclass
import pika


load_dotenv()

LOGGER = logging.getLogger(__name__)


@dataclass
class RabbitMQ:
    __host = os.environ.get("RABBITMQ")
    __conn = None

    def build_connection(self) -> None:
        LOGGER.info("Создаем соединение с RbtMQ")
        self.__conn = pika.BlockingConnection(
            pika.ConnectionParameters(f'{self.__host}')
        )

    def get_channel(
        self,
        connection: pika.BlockingConnection = None
    ) -> pika.adapters.blocking_connection.BlockingChannel:
        LOGGER.info("Получаем канал для работы")

        if self.__conn is None:
            self.build_connection()
        return self.__conn.channel()

    def close_connection(self) -> None:
        self.__conn.close()


@dataclass
class Config:
    rbtmq = RabbitMQ()


conf = Config()
