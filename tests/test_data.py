from nose.tools import assert_equal
from data import load_turkish_example


def test_load_turkish_example():
    toks, tags, doc = load_turkish_example()
    assert_equal(toks, ['New', 'Opportunities', 'for', 'Lithuanian',
                        'and', 'Turkish', 'Business'])
    assert_equal(tags, ['adj', 'n', 'p', 'adj', None, 'adj', 'n'])
    assert_equal(doc, [[u'Three', u'agreements', u'will', u'be', u'signed',
                        u'with', u'a', u'view', u'to', u'strengthening',
                        u'cooperation', u'between', u'the', u'two',
                        u'countries', u'-', u'memorandum', u'of',
                        u'understanding', u'on', u'railway', u'project',
                        u'Viking', u'and', u'agreements', u'among',
                        u'business', u'associations', u'and', u'national',
                        u'broadcasters', u'.'],
                       [u'According', u'to', u'the', u'President', u',',
                        u'a', u'new', u'stage', u'of', u'cooperation',
                        u'between', u'Lithuania', u'and', u'Turkey', u'opens',
                        u'up', u'new', u'opportunities', u'for', u'their',
                        u'business', u'people', u'.'],
                       [u'Our', u'countries', u'are', u'\u2026']
    ])
