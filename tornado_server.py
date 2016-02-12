"""
A blocking server standing between a client and the external_server
"""

import logging
import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import tornado.web
from settings import EXTERNAL_URL

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('tornado.access')


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        LOGGER.info('Handling sync request to %s', EXTERNAL_URL)
        client = tornado.httpclient.HTTPClient()

        try:
            response = client.fetch(EXTERNAL_URL)
        except tornado.httpclient.HTTPError as ex:
            LOGGER.error(ex)

        for header in ('Content-Type',):
            self.set_header(header, response.headers.get(header))

        self.write(response.body)


class AsyncHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        LOGGER.info('Handling async request to %s', EXTERNAL_URL)
        client = tornado.httpclient.AsyncHTTPClient(max_clients=1000)
        response = yield client.fetch(EXTERNAL_URL)

        for header in ('Content-Type',):
            self.set_header(header, response.headers.get(header))

        self.write(response.body)


def make_app():
    return tornado.web.Application([
        (r'/sync', MainHandler),
        (r'/async', AsyncHandler),
    ])


if __name__ == '__main__':
    APP = make_app()
    # APP.listen(8888)
    # tornado.ioloop.IOLoop.current().start()
    SERVER = tornado.httpserver.HTTPServer(APP)
    SERVER.bind(8888)
    SERVER.start(1)
    tornado.ioloop.IOLoop.current().start()
