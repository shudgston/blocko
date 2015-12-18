"""
A blocking server standing between a client and the external_server
"""

import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.gen
import tornado.web

EXTERNAL_URL = 'http://localhost:5000'


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        client = tornado.httpclient.HTTPClient()

        try:
            response = client.fetch(EXTERNAL_URL)
        except tornado.httpclient.HTTPError as ex:
            # log error
            pass

        for header in ('Content-Type', 'Content-Length'):
            self.set_header(header, response.headers.get(header))

        self.write(response.body)


class AsyncHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        response = yield client.fetch(EXTERNAL_URL)
        headers = ('Content-Type', 'Content-Length')

        for header in headers:
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
    server = tornado.httpserver.HTTPServer(APP)
    server.bind(8888)
    server.start(1)
    tornado.ioloop.IOLoop.current().start()
