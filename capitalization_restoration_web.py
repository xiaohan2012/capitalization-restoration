import sys
import urllib2
import json
import socket

TIMEOUT_THRESHOLD = 3

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Restore the sentence capitalization relying on document content')
    parser.add_argument('-s', dest="sentence", type=str, required=True,
                        help='sentence string or tokens separated by "|"')
    parser.add_argument('--docpath', type=str, required=True,
                        dest='docpath',
                        help='Path to the document associated with the sentence')
    parser.add_argument('--pos', type=str, required=False,
                        dest='pos',
                        help='POS tags separated by "|"')

    args = parser.parse_args()
    
    if '|' in args.sentence:
        sentence = args.sentence.split('|')
    else:
        sentence = args.sentence

    kwargs = {'sentence': sentence,
              'docpath': args.docpath}

    if args.pos:
        kwargs['pos'] = args.pos.split('|')

    timeout_count = 0

    while True:
        try:
            res = urllib2.urlopen("http://localhost:8888/caprestore", 
                                  json.dumps(kwargs), 1.0)
            break
        except urllib2.URLError, e:
            print "URLError: {}".format(e.reason)
            sys.exit(-1)
        except socket.timeout:
            timeout_count += 1
            if timeout_count == TIMEOUT_THRESHOLD:
                print "Timeout count reaches {}. Abandon.".format(
                    TIMEOUT_THRESHOLD)
                sys.exit(-1)

    res = json.loads(res.read())
    try:
        print " ".join(res['result'])
    except KeyError:
        print "**Error:"
        print res['msg']
