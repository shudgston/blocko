"""
Simulates an external service that can respond to a simple HTTP GET request,
taking a somewhat unknown amount of time to respond.
"""

import logging
import random
import time
from flask import Flask, jsonify

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
APP = Flask(__name__)
APP.debug = True


@APP.route('/')
def index():
    """Reply with a dummy JSON message after sleeping a random amount of time"""
    # seconds = random.randint(3, 6)
    seconds = 1
    LOGGER.info('Handling some request for %s second(s)', seconds)
    time.sleep(seconds)
    return jsonify({u'message': u'Hello world'})


if __name__ == '__main__':
    APP.run()
