import sys
import urllib2
import socket

TIMEOUT_THRESHOLD = 3

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Dummy service')
    parser.add_argument('--json_string', dest="json_string", type=str,
                        required=True, help='The json data string')

    parser.add_argument('--host', dest="host", type=str, required=False,
                        default='localhost', help='Host name of the service')
    parser.add_argument('--port', dest="port", type=str, required=False,
                        default='8888', help='Port of the service')

    args = parser.parse_args()
    
    timeout_count = 0

    while True:
        try:
            res = urllib2.urlopen(
                "http://{}:{}/caprestore".format(args.host, args.port),
                args.json_string, 1.0)
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

    print res.read()
