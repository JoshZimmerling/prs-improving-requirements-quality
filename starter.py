# -*- coding: utf-8 -*-

from flask import (
    Flask, request, abort, jsonify, render_template
)
from flask_cors import CORS
from app.requirement_improver import RequirementChecker
from app.lib.requirement import Requirement

amb_api = Flask(__name__, template_folder='./demos/iframe/templates', static_folder='./demos/iframe/static')

CORS(amb_api)  # So we can run and test locally. May be production necessary as well.

def check_json_conformance_and_create_objects():
    json_data = {}
    try:
        # Check that the request can be read
        json_data = request.get_json(force=True)
    except:
        abort(400, 'Unable to load data. Please refer to documentation on how to send JSON data in a POST request')

    # Transform data into appropriate format, checking conformance along the way
    try:
        # Extract requirements from JSON
        reqs = json_data['requirements']
        # Transform JSON
        reqs = [Requirement(id=req['id'], text=req['text']) for req in reqs]
        # Return the wrapped function, passing through reqs
        return reqs
    except KeyError:
        abort(400, """Improper body sent. Body should resemble the following example input:
            {
                "requirements": [{
                    "id": 1,
                    "text": "This is actually a good requirement."
                },{
                    "id": 2,
                    "text": "The system shall read HTML and PDF or DOC files."
                }]
            }""")


# These initial routes are to enable the demo to function properly.
# You can remove these these routes if you do not need the demo.
@amb_api.route('/')
@amb_api.route('/<requirement>')
@amb_api.route('/index/<requirement>')
def index(requirement=None):
    # Render page with ambiguities labelled
    return render_template('index.html')


# This is the main route for checking requirement(s) quality
@amb_api.route("/check-quality", methods=['POST'])
def check_quality():
    reqs = check_json_conformance_and_create_objects()
    return jsonify(RequirementChecker(reqs).check_quality())


if __name__ == "__main__":
    # amb_api.run(debug=True, host='127.0.0.1', port=9799)
    amb_api.run(debug=True, host='0.0.0.0', port=9799)