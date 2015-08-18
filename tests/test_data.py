from nose.tools import assert_equal
from data import load_example_by_id


def test_load_example_by_id():
    toks, lemmas, tags, doc = load_example_by_id(
        'BBCEC51D429DD4B06739107B121D69B7'
    )
    assert_equal(toks, ['New', 'Opportunities', 'for', 'Lithuanian',
                        'and', 'Turkish', 'Business'])
    assert_equal(lemmas, [u'new', u'opportunity', u'for', u'lithuanian',
                          u'', u'turkish', u'business'])
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
    toks, lemmas, tags, doc = load_example_by_id(
        'f4'
    )
    assert_equal(len(toks), 10)
    assert_equal(toks[0], 'China')
