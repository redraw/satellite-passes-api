import json
from datetime import timedelta

from flask import Flask, Response, request, abort, jsonify
from marshmallow import ValidationError
import markdown

from schemas import PassesQuery
from tracker import SatTracker
from utils import cache, get_cache_key


api = Flask(__name__)


@api.route('/passes/<int:norad_id>')
def passes(norad_id):
    try:
        query = PassesQuery().load(request.args)
    except ValidationError as err:
        abort(jsonify(err.messages))

    cache_key = get_cache_key(norad_id, query, prefix="passes")
    cache_response = cache.get(cache_key)

    if cache_response:
        return Response(cache_response, headers={
            "x-api-cache": "HIT",
            "x-api-cache-ttl": f"{cache.ttl(cache_key)}",
            "content-type": "application/json"
        })

    tracker = SatTracker(query["lat"], query["lon"], norad_id=norad_id)
    limit = query["limit"]

    passes = tracker.next_passes(
        days=query["days"],
        visible_only=query["visible_only"]
    )[:limit]

    content = json.dumps(passes)
    cache.set(cache_key, content, ex=timedelta(days=1))

    return Response(content, headers={
        "x-api-cache": "MISS",
        "content-type": "application/json"
    })


@api.route('/')
def docs():
    with open('README.md') as f:
        return markdown.markdown(f.read(), extensions=['fenced_code'])


if __name__ == '__main__':
    api.run(port=8000, debug=True)