import urllib
import json

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Restore the sentence capitalization relying on document content')
    parser.add_argument('-s', dest="sentence", type=str, required=True,
                        help='an integer for the accumulator')
    parser.add_argument('--docpath', type=str, required=True,
                        dest='docpath',
                        help='Path to the document associated with the sentence')

    args = parser.parse_args()

    kwargs={"sentence": args.sentence,
            "docpath": args.docpath}

    res = urllib.urlopen("http://localhost:8888/caprestore", json.dumps(kwargs))
    res = json.loads(res.read())
    try:
        print " ".join(res['result'])
    except KeyError:
        print "**Error:"
        print res['msg']
