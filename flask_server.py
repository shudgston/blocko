"""
flask_server

gunicorn --bind 127.0.0.1:5001 flask_server:APP \
  --workers=4 \
  --worker-class gevent

"""

import requests
from flask import Flask, make_response

EXTERNAL_URL = 'http://localhost:5000'
APP = Flask(__name__)


@APP.route('/sync')
def index():
    session = requests.Session()
    response = session.get(EXTERNAL_URL)
    resp = make_response(response.text)

    for header in ('Content-Length', 'Content-Type'):
        resp.headers[header] = resp.headers.get(header)

    return resp
