from nose.tools import assert_equal

from capitalization_restoration.cap_restore import (PulsRestorer,
                                                    transform_words_by_labels)
from capitalization_restoration.tests.data import load_turkish_example


def test_transform_words_by_labels():
    words = [u'I', u'Compared', u'PaaS', u'Providers', u':',
             u'Heroku', u'and', u"IBM", u"'s", u'Bluemix', u'.']
    actual = transform_words_by_labels(words,
                                       [u'AU', u'AL', u'MX', u'AL', u'AN', u'IC',
                                        u'AL', u'AU', u'AL', u'IC', u'AN']
    )
    expected = [u'I', u'compared', u'PaaS', u'providers', u':',
                u'Heroku', u'and', u'IBM', u"'s", u'Bluemix', u'.']
    assert_equal(actual, expected)


def test_puls_cap_restorer():
    r = PulsRestorer()
    toks, lemmas, tags, doc = load_turkish_example()

    actual = r.restore(toks, pos=tags, doc=doc)
    expected = [u'New', u'opportunities', u'for', u'Lithuanian',
                'and', u'Turkish', u'business']
    assert_equal(actual, expected)
