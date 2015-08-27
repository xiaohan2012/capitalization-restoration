from nose.tools import assert_equal

from capitalization_restoration.cap_restore import (PulsRestorer,
                                                    transform_words_by_labels,
                                                    filter_words)
from capitalization_restoration.tests.data import load_turkish_example


def test_transform_words_by_labels():
    words = [u'I', u'Compared', u'PaaS', u'Providers', u':',
             u'Heroku', u'and', u"IBM", u"'s", u'Bluemix', u'.']
    actual = transform_words_by_labels(words,
                                       [u'AL', u'IC', u'AL', u'IC'],
                                       [1, 5, 6, 9]
    )
    expected = [u'I', u'compared', u'PaaS', u'Providers', u':',
                u'Heroku', u'and', u'IBM', u"'s", u'Bluemix', u'.']
    assert_equal(actual, expected)


def test_filter_words():
    words_with_features = [{'word': 'Feng'}, {'word': 'MiX'}, {'word': ','},
                           {'word': ','}, {'word': 'UPPER'},
                           {'word': 'normal'}, {'word': 'God'}]
    templates = range(len(words_with_features))
    actual = filter_words(words_with_features,
                          templates,
                          excluded_labels=set(['MX', 'AU', 'AN']))
    expected = [5, 6]
    assert_equal(actual, (expected, expected))

    
def test_puls_cap_restorer():
    r = PulsRestorer()
    toks, lemmas, tags, doc = load_turkish_example()

    actual = r.restore(toks, pos=tags, doc=doc)
    expected = [u'New', u'opportunities', u'for', u'Lithuanian',
                'and', u'Turkish', u'business']
    print(actual)
    assert_equal(actual, expected)
