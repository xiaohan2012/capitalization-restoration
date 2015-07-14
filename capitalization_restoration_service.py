import json
import tornado.ioloop
import tornado.web

import nltk
nltk.data.path.append('nltk_data')

from cap_restore import DefaultRestorer

import traceback

restorer = DefaultRestorer()


STATUS_RESTORE_ERROR = -2
STATUS_INVALID_PARAM = -1
STATUS_OK = 0


class MainHandler(tornado.web.RequestHandler):
    def write_error_msg(self, code, msg):
        self.write({"code": code, "msg": msg})

    def post(self):
        """
        Request parameter:
        ----------------------
        
        sentence: string|list of string

        docpath: string, document path

        pos: list of string, part of speech tags of the sentence tokens

        """
        data = json.loads(self.request.body)
        sentence = data.get("sentence")
        if not sentence:
            self.write_error_msg(STATUS_INVALID_PARAM,
                                 msg="Missing argument: sentence")
            return
        else:
            if isinstance(sentence, basestring):
                tokens = nltk.word_tokenize(unicode(sentence))
            elif isinstance(sentence, list):
                tokens = sentence
            else:
                self.write_error_msg(STATUS_INVALID_PARAM,
                                     msg="Unknown `sentence` type: `{}`".format(type(sentence)))
                return

        kwargs = {}
        docpath = data.get("docpath")
        if not docpath:
            self.write_error_msg(STATUS_INVALID_PARAM,
                                 msg="Missing argument: docpath")
            return
        else:
            kwargs['docpath'] = docpath

        pos = data.get("pos")
        if pos:
            if isinstance(pos, list) and len(pos) == len(tokens):
                kwargs['pos'] = pos
            else:
                self.write_error_msg(STATUS_INVALID_PARAM,
                                     msg="Invalid `pos`: {}".format(repr(pos)))
                return

        ans = {}
        
        try:
            ans['result'] = restorer.restore(tokens, **kwargs)
            ans['code'] = STATUS_OK
            self.write(ans)
        except:
            if self.settings.get("debug"):
                self.write_error_msg(STATUS_RESTORE_ERROR,
                                     msg=traceback.format_exc())
            else:
                self.write_error_msg(STATUS_RESTORE_ERROR,
                                     msg="Restoration error occurred")
            
        # import time
        # time.sleep(1.1)

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
