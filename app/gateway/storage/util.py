import json
import time

import pika


def upload(f, fs, channel, user_profile):
    try:
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return "internal server error - upload not successful", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": user_profile["email"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
        )
    except Exception as err:
        print(err)
        fs.delete(fid)
        return "internal server error", 500


def upload_to_cosmosdb(file, fs, retries=3):
    try:
        fid = fs.put(file, filename=file.filename)
        print(f"File uploaded successfully, file ID: {fid}")
        return fid
    except Exception as e:
        if "RetryAfterMs" in str(e) and retries > 0:
            retry_after = float(str(e).split("RetryAfterMs=")[1].split(",")[0]) / 1000
            print(f"Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
            return upload_to_cosmosdb(file, fs, retries - 1)
        else:
            raise e
