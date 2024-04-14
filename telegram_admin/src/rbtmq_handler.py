import pika
import json


class RBTMQ:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()

    def publish(self, method: str, routing_key: str, body: dict | str):
        properties = pika.BasicProperties(method)
        self.channel.basic_publish(
            exchange='', routing_key=routing_key,
            body=json.dumps(body), properties=properties
        )
        self.connection.close()


rbtmq_handler = RBTMQ()
