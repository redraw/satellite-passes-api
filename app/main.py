import json
import logging
from datetime import timedelta

from flask import Flask, Response, request, abort, jsonify
from marshmallow import ValidationError
import markdown

from schemas import PassesQuery
from tracker import SatTracker
from utils import cache, get_cache_key, filter_next_passes
from tle import TLENotFound


api = Flask('api')
api.logger.setLevel(logging.INFO)


@api.route('/passes/<int:norad_id>')
def passes(norad_id):
    try:
        query = PassesQuery().load(request.args)
    except ValidationError as err:
        return jsonify(err.messages), 400

    limit = query.pop('limit')
    cache_key = get_cache_key(norad_id, query, prefix="passes")
    cache_response = cache.get(cache_key)

    # Return results from cache if hit
    if cache_response:
        passes = json.loads(cache_response)
        next_passes = filter_next_passes(passes)
        return Response(json.dumps(next_passes[:limit]), headers={
            "x-api-cache": "HIT",
            "x-api-cache-ttl": f"{cache.ttl(cache_key)}",
            "content-type": "application/json"
        })

    # Calculate next passes
    try:
        tracker = SatTracker(query["lat"], query["lon"], norad_id=norad_id)
    except TLENotFound:
        return jsonify({"error": "TLE not found"}), 400

    passes = tracker.next_passes(
        days=query["days"],
        visible_only=query["visible_only"]
    )

    # Cache passes for 1 day
    content = json.dumps(passes)
    cache.set(cache_key, content, ex=timedelta(days=1))

    return Response(json.dumps(passes[:limit]), headers={
        "x-api-cache": "MISS",
        "content-type": "application/json"
    })


@api.route('/')
def docs():
    with open('README.md') as f:
        return markdown.markdown(f.read(), extensions=['fenced_code'])


if __name__ == '__main__':
    api.run(port=8000, debug=True)