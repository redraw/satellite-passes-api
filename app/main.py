import os
import json
import logging
from datetime import timedelta

from flask import Flask, Response, request, jsonify, redirect
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from marshmallow import ValidationError
import markdown

from schemas import PassesQuery
from tracker import SatTracker
from utils import cache, get_cache_key, filter_next_passes
from tle import TLENotFound


api = Flask("api")
api.logger.setLevel(logging.INFO)
CORS(api)


@api.before_request
def redirect_to_custom_domain():
    custom_domain = os.getenv("CUSTOM_DOMAIN")
    if custom_domain and "FLY_APP_NAME" in os.environ and request.host == f"{os.getenv('FLY_APP_NAME')}.fly.dev":
        return redirect(f"https://{custom_domain}{request.full_path}", code=301)


@api.route("/passes/<int:norad_id>")
def passes(norad_id):
    try:
        query = PassesQuery().load(request.args)
    except ValidationError as err:
        return jsonify(err.messages), 400

    limit = query.pop("limit")
    cache_key = get_cache_key(norad_id, query, prefix="passes")
    cache_response = cache.get(cache_key)

    # Return results from cache if hit
    if cache_response:
        passes = json.loads(cache_response)
        next_passes = filter_next_passes(passes)
        return Response(
            json.dumps(next_passes[:limit]),
            headers={
                "x-api-cache": "HIT",
                "x-api-cache-ttl": f"{cache.ttl(cache_key)}",
                "cache-control": f"public, max-age={cache.ttl(cache_key)}",
                "content-type": "application/json",
            },
        )

    # Calculate next passes
    try:
        tracker = SatTracker(query["lat"], query["lon"], norad_id=norad_id)
    except TLENotFound:
        return jsonify({"error": "TLE not found"}), 400

    passes = tracker.next_passes(days=query["days"], visible_only=query["visible_only"])

    # Cache passes for 1 day
    content = json.dumps(passes)
    cache.set(cache_key, content, ex=timedelta(days=1))

    return Response(json.dumps(passes[:limit]), headers={"x-api-cache": "MISS", "content-type": "application/json"})


@api.route("/")
def index():
    with open("README.md") as f:
        html = markdown.markdown(f.read(), extensions=["fenced_code"])
        content = html + "<style>body {font-family: sans-serif}</style>"
        return content


@api.route("/openapi.json")
def api_spec():
    return api.send_static_file("openapi.json")


swaggerui_blueprint = get_swaggerui_blueprint(
    base_url="/docs", api_url="/openapi.json", config={"app_name": "Satellite Passes API"}
)

api.register_blueprint(swaggerui_blueprint)

if __name__ == "__main__":
    api.run(port=8000, debug=True)
