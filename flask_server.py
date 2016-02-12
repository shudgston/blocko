"""
flask_server

gunicorn --bind 127.0.0.1:5001 flask_server:APP \
  --workers=4 \
  --worker-class gevent \
  --log-level=debug

"""

import logging
import requests
from flask import Flask, make_response
from settings import EXTERNAL_URL

APP = Flask(__name__)
LOGGER = logging.getLogger('gunicorn.error')
# LOGGER.setLevel(logging.DEBUG)


@APP.route('/sync')
def index():
    LOGGER.info('Handling sync request to %s', EXTERNAL_URL)
    session = requests.Session()
    response = session.get(EXTERNAL_URL)
    resp = make_response(response.text)

    for header in ('Content-Type',):
        resp.headers[header] = resp.headers.get(header)

    return resp
