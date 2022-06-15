from collections import defaultdict
import json
from bottle import route, run, template, request, hook, response

user_data = defaultdict(list)

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'


@route('/i')
def some_api():
    query = dict(request.query)
    if 'device_id' in query and 'events' in query:
        user_data[query['device_id']].extend(json.loads(query['events']))
        print(user_data[query['device_id']])
    return {"result": "Success"}


run(host='localhost', port=8282, )
