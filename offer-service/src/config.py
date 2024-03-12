import os
from dotenv import load_dotenv
import logging
from dataclasses import dataclass
import pika


load_dotenv()

LOGGER = logging.getLogger(__name__)


@dataclass
class RabbitMQ:
    host = os.environ.get("RABBITMQ")
    conn = None

    def build_connection(self) -> None:
        LOGGER.info("Создаем соединение с RbtMQ")
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(f'{self.host}')
        )

    def get_channel(
        self,
        connection: pika.BlockingConnection = None
    ) -> pika.adapters.blocking_connection.BlockingChannel:
        LOGGER.info("Получаем канал для работы")
        if self.conn is None:
            self.build_connection()
        return self.conn.channel()


@dataclass
class Config:
    rbtmq = RabbitMQ()


conf = Config()
