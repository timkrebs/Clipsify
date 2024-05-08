import os
import sys
from os import environ as env

import gridfs
import pika
import pymongo
from convert import to_mp3
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


def main():
    CONNECTION_STRING = env.get("MONGO_CONNECTION_STRING")
    client = pymongo.MongoClient(CONNECTION_STRING)
    try:
        client.server_info()  # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError(
            "Invalid API for MongoDB connection string or timed out when attempting to connect"
        )
    video_db = client["videos"]
    mp3_db = client["mp3"]
    fs_videos = gridfs.GridFS(video_db)
    fs_mp3s = gridfs.GridFS(mp3_db)

    # rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback)

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
