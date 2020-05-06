from flask import Flask, Response, request, abort, jsonify
from marshmallow import ValidationError
import markdown

from schemas import PassesQuery
from tracker import SatTracker


api = Flask(__name__)


@api.route('/passes/<int:norad_id>')
def passes(norad_id):
    try:
        query = PassesQuery().load(request.args)
    except ValidationError as err:
        abort(jsonify(err.messages))
    
    tracker = SatTracker(query["lat"], query["lon"], norad_id=norad_id)
    passes = tracker.get_next_passes(query["limit"])

    return jsonify(passes)


@api.route('/')
def docs():
    with open('README.md') as f:    
        return markdown.markdown(f.read(), extensions=['fenced_code'])


if __name__ == '__main__':
    api.run(port=8000, debug=True)