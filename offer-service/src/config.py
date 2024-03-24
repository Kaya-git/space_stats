import os
from dotenv import load_dotenv
import logging
from dataclasses import dataclass
import pika
import time


load_dotenv()

LOGGER = logging.getLogger(__name__)


@dataclass
class RabbitMQ:
    __host = os.environ.get("RABBITMQ")
    __conn = None
    __channel = None

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
        self.__channel = self.__conn.channel()

    def exchange_declare(self):
        self.__channel.exchange_declare(
            exchange="offer_service",
            exchange_type="fanout"
        )

    def queue_declare(self, *args):
        for i in args:
            self.__channel.queue_declare(
                queue=i,
                durable=True
            )


@dataclass
class RabbitMQSender(RabbitMQ):

    def publish(
        self,
        exchange,
        routing_key,
        message,
    ):
        self.__channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            )
        )

    def close_connection(self) -> None:
        self.__conn.close()


@dataclass
class RabbitMQReciever(RabbitMQ):
    def callback(
        self,
        ch,
        method,
        properties,
        body
    ):
        time.sleep(body.count(b'.'))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consume(self):
        self.__channel.basic_qos()
        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(
            queue='task_queue',
            on_message_callback=self.callback
        )

        self.__channel.start_consuming()


@dataclass
class Config:
    rbtmqs = RabbitMQSender()
    rbtmqr = RabbitMQReciever()


conf = Config()
