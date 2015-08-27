import json
import tornado.ioloop
import tornado.web

import nltk
nltk.data.path.append('nltk_data')

from cap_restore import PulsRestorer

import traceback

restorer = PulsRestorer()


STATUS_RESTORE_ERROR = -2
STATUS_INVALID_PARAM = -1
STATUS_OK = 0


class MainHandler(tornado.web.RequestHandler):
    def write_error_msg(self, code, msg):
        self.write({"code": code, "msg": msg})

    def valid_data(self, data):
        fields = ['capitalizedSentences', 'otherSentences']
        for field in fields:
            if field not in data:
                return False, 'd: {} not present'.format(field)
        
        for field in fields:
            if not isinstance(data[field], list):
                return False, 'd: {} not list'.format(field)

        for field in fields:
            for sent in data[field]:
                flag, msg = self.valid_sent(sent)
                if not flag:
                    return False, msg

        return True, ''
            
    def valid_sent(self, sent):
        fields = ['no', 'tokens', 'pos']

        for f in fields:
            if f not in sent:
                return False, 's: {} not present.'.format(f)
        
        # token checking
        if not isinstance(sent['tokens'], list):
            return False, 'tokens: {} not list. {}'.format(
                sent['tokens'], sent
            )
        for tok in sent['tokens']:
            if not isinstance(tok, basestring):
                return False, 'tok: {} not string'.format(tok)

        # pos checking
        if not isinstance(sent['pos'], list):
            return False, 'pos: {} not list. {}'.format(sent['pos'], sent)

        for p in sent['pos']:
            if not (isinstance(p, basestring)
                    or p == None):
                return False, 'pos: {} not string'.format(p)

        return True, ''

    def post(self):
        """
        Request parameter:
        ----------------------
        
        json_string: string
            the dict(after parsing) should contain the following fields:
            - 'capitalizedSentences': list<dict<no, tokens, pos>>, one dict one sent
            - 'otherSentences': same format as above

        """
        try:
            data = json.loads(self.request.body)
        except ValueError:
            self.write_error_msg(STATUS_INVALID_PARAM,
                                 msg="JSON decode error")
            return
        valid, msg = self.valid_data(data)
        if not valid:
            self.write_error_msg(STATUS_INVALID_PARAM,
                                 msg=msg)
            return
            
        try:
            ans = {}
            ans['result'] = []
            ans['code'] = STATUS_OK
            
            doc = [sent['tokens'] for sent in data['otherSentences']]
            for r in data['capitalizedSentences']:
                decap_tokens = restorer.restore(r['tokens'],
                                                pos=r['pos'],
                                                doc=doc)
                ans['result'].append({'no': r['no'], 'tokens': decap_tokens})
            self.write(ans)

        except:
            if self.settings.get("debug"):
                self.write_error_msg(STATUS_RESTORE_ERROR,
                                     msg=traceback.format_exc())
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
