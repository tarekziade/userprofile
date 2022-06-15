from collections import defaultdict
import json
import os
from bottle import route, run, template, request, hook, response
from elasticsearch import Elasticsearch

HERE = os.path.dirname(__file__)
INDEX = "search-countly"


class ElasticDB:
    def __init__(self):
        self.db = Elasticsearch(
            "http://localhost:9200", basic_auth=("elastic", "changeme")
        )
        with open(os.path.join(HERE, "mapping.json")) as f:
            self.mapping = json.loads(f.read())
        self.create_index()

    def create_index(self):
        if self.db.indices.exists(index=INDEX):
            return
        data = {"mappings": self.mapping}
        self.db.indices.create(index=INDEX, body=data)

    def push_event(self, event):
        # XXX use bulk
        print(self.db.index(index=INDEX, document=event))


db = ElasticDB()


@hook("after_request")
def enable_cors():
    response.headers["Access-Control-Allow-Origin"] = "*"


@route("/i")
def some_api():
    query = dict(request.query)
    if "device_id" in query and "events" in query:
        events = json.loads(query["events"])
        for event in events:
            event["device_id"] = query["device_id"]
            db.push_event(event)
    return {"result": "Success"}


run(
    host="localhost",
    port=8282,
)
