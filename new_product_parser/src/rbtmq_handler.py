import pika
import json


class RBTMQ:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()

    def publish(self, method, routing_key, body):
        properties = pika.BasicProperties(method)
        self.channel.basic_publish(
            exchange='', routing_key=routing_key,
            body=json.dumps(body), properties=properties
        )
        self.connection.close()

    def callback(ch, method, properties, body):
        ...

    def consume(self):
        self.channel.queue_declare(queue="parser")
        self.channel.basic_consume(
            queue="parser",
            on_message_callback=self.callback,
            auto_ack=True
        )
        self.channel.start_consuming()


rbtmq = RBTMQ()
