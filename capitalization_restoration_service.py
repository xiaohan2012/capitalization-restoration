import json
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def write_error_msg(self, code, msg):
        self.write({"code": code, "msg": msg})

    def post(self):
        data = json.loads(self.request.body)
        new_data = []
        for r in data:
            new_data.append({'no': r['no'], 'tokens': r['tokens']})
        self.write(json.dumps(new_data))

settings = {
    'debug': True,
}

handlers = [
    (r"/caprestore", MainHandler),
]

application = tornado.web.Application(handlers, **settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
