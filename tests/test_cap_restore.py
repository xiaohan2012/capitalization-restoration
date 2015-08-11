from nose.tools import assert_equal

from capitalization_restoration.cap_restore import PulsRestorer
from capitalization_restoration.tests.data import load_turkish_example


def test_puls_cap_restorer():
    r = PulsRestorer()
    toks, tags, doc = load_turkish_example()

    actual = r.restore(toks, pos=tags, doc=doc)
    expected = [u'New', u'opportunities', u'for', u'Lithuanian',
                'and', u'Turkish', u'business']
    assert_equal(actual, expected)
