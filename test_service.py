# coding: utf-8

from nose.tools import assert_equals, assert_true
import json
import urllib2

URL = "http://localhost:8888/caprestore"

SENTENCE = u"Kingdom € Tourism and Hospitality Sector to Draw Huge Investments"
TOKENS = SENTENCE.split()
DOCPATH = "data/test"
POS = ('NNP', ':', 'NNP', 'CC', 'NNP', 'NNP', 'TO', 'NNP', 'NNP', 'NNP')
INVALID_POS1 = ('Not', 'The', 'Same', 'Length', 'As', 'Sentence')
INVALID_POS2 = 'Invalid type: string'

EXPECTED = u"Kingdom € Tourism and hospitality sector to draw huge investments"


def _request(sent, docpath, pos=None):
    data = {"sentence": sent, "docpath": docpath}
    if pos:
        data['pos'] = pos
    return json.loads(urllib2.urlopen(URL, json.dumps(data)).read())


def test_ordinary():
    actual = ' '.join(_request(SENTENCE, DOCPATH)['result'])
    assert_equals(actual, EXPECTED)


def test_tokens():
    actual = ' '.join(_request(TOKENS, DOCPATH)['result'])
    assert_equals(actual, EXPECTED)


def test_pos():
    actual = ' '.join(_request(TOKENS, DOCPATH, pos=POS)['result'])
    assert_equals(actual, EXPECTED)    


def test_pos_err1():
    actual = _request(TOKENS, DOCPATH, pos=INVALID_POS1)['msg']
    assert_true('invalid `pos`' in actual.lower())


def test_pos_err2():
    actual = _request(TOKENS, DOCPATH, pos=INVALID_POS2)['msg']
    assert_true('invalid `pos`' in actual.lower())
