import json
from toolz.functoolz import partial
from toolz.dicttoolz import get_in

from nose.tools import assert_equal

from capitalization_restoration.cap_restore import PulsRestorer


data = json.loads('[{"lemma":"new","pos":"adj","token":"New"},{"lemma":"opportunity","pos":"n","token":"Opportunities"},{"lemma":"for","pos":"p","token":"for"},{"lemma":"lithuanian","pos":"adj","token":"Lithuanian"},{"lemma":"","pos":null,"token":"and"},{"lemma":"turkish","pos":"adj","token":"Turkish"},{"lemma":"business","pos":"n","token":"Business"}]')


get_tokens = partial(map, partial(get_in, ['token']))
get_tags = partial(map, partial(get_in, ['pos']))


def test_puls_cap_restorer():
    r = PulsRestorer()
    toks = get_tokens(data)
    tags = get_tags(data)
    docpath = '/cs/taatto/home/hxiao/capitalization-recovery/corpus/puls-format/BBCEC51D429DD4B06739107B121D69B7'
    actual = r.restore(toks, pos=tags, docpath=docpath)
    expected = [u'New', u'opportunities', u'for', u'Lithuanian',
                'and', u'Turkish', u'business']
    assert_equal(actual, expected)
