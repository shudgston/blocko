"""
A blocking server standing between a client and the external_server
"""

import tornado.httpclient
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        client = tornado.httpclient.HTTPClient()

        try:
            response = client.fetch('http://localhost:5000')
            print(response.headers.get('Content-Type'))
        except tornado.httpclient.HTTPError as ex:
            # log error
            pass

        headers = ('Content-Type', 'Content-Length')

        for header in headers:
            self.set_header(header, response.headers.get(header))
        self.write(response.body)


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
    ])


if __name__ == '__main__':
    APP = make_app()
    APP.listen(8888)
    tornado.ioloop.IOLoop.current().start()
