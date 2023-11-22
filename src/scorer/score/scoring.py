import pika, json, tempfile, os
from bson.objectid import ObjectId
import pandas as pd
import toolz.dicttoolz as dtz
import xgboost as xgb


bst = xgb.Booster({'nthread': 4})  # init model
bst.load_model('score/xgb.model')  # load data

HPRICE_QUEUE=os.environ.get("HPRICE_QUEUE")

def start(message, intake, score, channel):
    message = json.loads(message)

    out = intake.find_one({'_id': ObjectId(message["intake_id"])})

    out_clean = dtz.keyfilter(lambda x: x != '_id', out)
    X_test = pd.read_json(f"[{json.dumps(out_clean)}]", orient='records')
    dtest = xgb.DMatrix(X_test)
    ypred = bst.predict(dtest)
    fid = score.insert_one({'intake_id':message["intake_id"],
                           'price': float(ypred[0])})

    #TODO: schema check
    message["score_id"] = str(fid)

    try:
        channel.basic_publish(
            exchange="",
            routing_key=HPRICE_QUEUE,
            body=json.dumps(message), #covert python obj to json
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ), #ensure persist until process
        )
    except Exception as err:
        score.delete(fid)
        return "failed to publish message"
