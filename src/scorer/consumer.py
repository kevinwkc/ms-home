import pika, sys, os, time
from pymongo import MongoClient
from score import scoring

MONGODB_HOST=os.environ.get("MONGODB_HOST")
RABBITMQ_HOST=os.environ.get("RABBITMQ_HOST")
HOUSE_QUEUE=os.environ.get("HOUSE_QUEUE")
'''
MONGODB_HOST=RABBITMQ_HOST='localhost'
HOUSE_QUEUE="house"
'''
def main():
    client = MongoClient(MONGODB_HOST, 27017)
    db = client.house
    intake = db.intake
    score = db.score

    # rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = scoring.start(body, intake, score, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
            #negative ack to channel: no going to ack we process the msg, keep msg on the queue
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=HOUSE_QUEUE, on_message_callback=callback
        # when callback(message[-1])
    )

    print("Waiting for messages. To exit press CTRL+C")

    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
