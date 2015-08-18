import os
import json
from pathlib import Path
from toolz.functoolz import partial
from toolz.dicttoolz import get_in

CURDIR = os.path.dirname(os.path.realpath(__file__))

get_tokens = partial(map, partial(get_in, ['token']))
get_lemmas = partial(map, partial(get_in, ['lemma']))
get_tags = partial(map, partial(get_in, ['pos']))


def load_example_by_id(id_):
    # data preparation
    with Path(CURDIR + '/data/{}.title'.format(id_)).open(encoding='utf8') as title_f, \
         Path(CURDIR + '/data/{}.doc'.format(id_)).open(encoding='utf8') as doc_f:
        title_raw = json.loads(title_f.read())
        doc_raw = json.loads(doc_f.read())
        doc = [[doc['token'] for doc in sent['features']]
               for sent in doc_raw]

    return (get_tokens(title_raw),
            get_lemmas(title_raw),
            get_tags(title_raw),
            doc)

    
def load_turkish_example():
    return load_example_by_id('BBCEC51D429DD4B06739107B121D69B7')


def load_china_example():
    return load_example_by_id('f4')
    
