import pika, json
import os
from flask import jsonify

def upload(f, fs, channel, access):
    try:

        fid = fs.insert_one(f).inserted_id
    except Exception as err:
        print(err)
        return "internal server error", 500

    message = {
        "intake_id": str(fid),
        "score_id": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("HOUSE_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

        return jsonify(message), 200

    except Exception as err:
        print(err)
        fs.delete_one({'_id': fid})
        return "internal server error", 500
