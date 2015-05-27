import nltk
from cap_restore import DefaultRestorer

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Restore the sentence capitalization relying on document content')
    parser.add_argument('-s', dest="sentence", type=str, required=True,
                        help='an integer for the accumulator')
    parser.add_argument('--docpath', type=str, required=True,
                        dest='docpath',
                        help='Path to the document associated with the sentence')

    args = parser.parse_args()

    kwargs={}
    kwargs['docpath'] = args.docpath

    r = DefaultRestorer()
    print " ".join(r.restore(nltk.word_tokenize(unicode(args.sentence)), **kwargs))    
