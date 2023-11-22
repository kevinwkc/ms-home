import os, pika, json
from flask import Flask, request, send_file, jsonify
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId
import toolz.dicttoolz as dtz

server = Flask(__name__)

MONGODB_HOST=os.environ.get("MONGODB_HOST")
RABBITMQ_HOST=os.environ.get("RABBITMQ_HOST")

mongo_house = PyMongo(server, uri=f"mongodb://{MONGODB_HOST}:27017/house")
mongo_intake= mongo_house.db.intake
mongo_score= mongo_house.db.score


connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/booking", methods=["POST"])
def booking():

    access, status = validate.token(request)

    if status:
        return status

    access = json.loads(access)

    if access["admin"]:
        '''
        if True:
            access=dict()
            access['username']="objectdeveloper@gmail.com"
            os.environ['HOUSE_QUEUE']='house'
        '''
        if request.is_json:
            status = util.upload(request.get_json(True), mongo_intake, channel, access)

            if status:
                return status

    else:
        return "not authorized", 401


@server.route("/pricing", methods=["GET"])
def pricing():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        '''
        if True:
            access=dict()
            access['username']="objectdeveloper@gmail.com"
            os.environ['HOUSE_QUEUE']='house'
        '''
        pid_str = request.args.get("intake_id")

        if not pid_str:
            return "intake_id is required", 400

        print(pid_str)
        try:
            out = mongo_score.find_one({'intake_id': pid_str})

            score=dtz.keyfilter(lambda x: x!='_id', out)

            return jsonify(score), 200

        except Exception as err:
            print(err)
            return "internal server error", 500

    return "not authorized", 401


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
