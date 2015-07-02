import json
import tornado.ioloop
import tornado.web

import nltk
from cap_restore import DefaultRestorer

import traceback

restorer = DefaultRestorer()

STATUS_RESTORE_ERROR=-2
STATUS_INVALID_PARAM=-1
STATUS_OK=0

class MainHandler(tornado.web.RequestHandler):
    def write_error_msg(self, code, msg):
        self.write({"code": code, "msg": msg})

    def post(self):
        data = json.loads(self.request.body)
        text = data.get("text")
        if not text:
            self.write_error_msg(STATUS_INVALID_PARAM,
                             msg="Missing argument: text")
            return
            
        docpath = data.get("docpath")
        if not docpath:
            self.write_error_msg(STATUS_INVALID_PARAM,
                             msg="Missing argument: docpath")
            return

        ans = {}
        
        try:
            ans['result'] = restorer.restore(nltk.word_tokenize(unicode(text)), 
                                             docpath=docpath)
            ans['code'] = STATUS_OK
            self.write(ans)
        except:
            if self.settings.get("debug"):
                self.write_error_msg(STATUS_RESTORE_ERROR,
                                 msg = traceback.format_exc())
            else:
                self.write_error_msg(STATUS_RESTORE_ERROR,
                                 msg="Restoration error occurred")
            

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
