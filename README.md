Home Pricing Microservice with Python, Kubernetes  RabbitMQ, MongoDB, and MySQL.
=======================================================================
login -> submit(home) -> rabbitmq -> xgboost(home) -> rabbitmq -> notification

### Microservice Design Pattern
Database per Service
Saga
Domain Event

### Security
Access Token

Instruction
================
#### ADD RABBITMQ
![img.png](img.png)

login
---------------
```
curl --resolve 'home.kevin:80:127.0.0.1' -X POST http://home.kevin/login -u objectdeveloper@gmail.com:HireMe88!
```
RETURN:
hash token
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im9iamVjdGRldmVsb3BlckBnbWFpbC5jb20iLCJleHAiOjE3MDA3MDkzNDIsImlhdCI6MTcwMDYyMjk0MiwiYWRtaW4iOnRydWV9.hvDq9JTG_lYvs8tLeS27WiBkHqCTSC0F8LXEAduAvTw

booking: send out home data for scoring
---------------
curl --resolve 'home.kevin:80:127.0.0.1' -X POST \
  'http://home.kevin/booking' \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im9iamVjdGRldmVsb3BlckBnbWFpbC5jb20iLCJleHAiOjE3MDA3MDkzNDIsImlhdCI6MTcwMDYyMjk0MiwiYWRtaW4iOnRydWV9.hvDq9JTG_lYvs8tLeS27WiBkHqCTSC0F8LXEAduAvTw' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "age": 1.1,
  "dist_subway": 193.5845,
  "dist_stores": 6,
  "lat": 24.96571,
  "long": 121.54089
}'

RETURN:
{"intake_id":"655d5d3c22435ed1b6ab27aa","score_id":null,"username":"objectdeveloper@gmail.com"}


### mongodb
```commandline
house> db.intake.find()
[
  {
    _id: ObjectId("655d4ec7667d6118eaa95474"),
    age: 1.1,
    dist_subway: 193.5845,
    dist_stores: 6,
    lat: 24.96571,
    long: 121.54089
  }
]
house> db.score.find()
[
  {
    _id: ObjectId("655d5d3c882a67964976126b"),
    intake_id: '655d5d3c22435ed1b6ab27aa',
    price: 49.13243865966797
  }
]

```
pricing: using xgboost to predict house price using the intake_id
---------------

curl --resolve 'home.kevin:80:127.0.0.1' -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im9iamVjdGRldmVsb3BlckBnbWFpbC5jb20iLCJleHAiOjE3MDA3MDY2MDEsImlhdCI6MTcwMDYyMDIwMSwiYWRtaW4iOnRydWV9.T2n3eAUlLE-tyW9BGzCL2gNM2LaNyIrWfE2xwgKO_dU" "http://home.kevin/pricing?intake_id=655d72792e62ed5f25572f2c"

RETURN:
{"intake_id":"655d72792e62ed5f25572f2c","price":49.13243865966797}










debug
==================

curl --resolve 'home.kevin:8080:127.0.0.1' -X POST \
  'http://home.kevin:8080/booking' \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im9iamVjdGRldmVsb3BlckBnbWFpbC5jb20iLCJleHAiOjE3MDA3MDY2MDEsImlhdCI6MTcwMDYyMDIwMSwiYWRtaW4iOnRydWV9.T2n3eAUlLE-tyW9BGzCL2gNM2LaNyIrWfE2xwgKO_dU' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "age": 1.1,
  "dist_subway": 193.5845,
  "dist_stores": 6,
  "lat": 24.96571,
  "long": 121.54089
}'


curl --resolve 'home.kevin:8080:127.0.0.1' -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im9iamVjdGRldmVsb3BlckBnbWFpbC5jb20iLCJleHAiOjE3MDA3MDY2MDEsImlhdCI6MTcwMDYyMDIwMSwiYWRtaW4iOnRydWV9.T2n3eAUlLE-tyW9BGzCL2gNM2LaNyIrWfE2xwgKO_dU" "http://home.kevin:8080/pricing?intake_id=655d6f058e6828528b973d10"
