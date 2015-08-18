from nose.tools import (assert_true, assert_false, assert_raises)

from capitalization_restoration.feature_extractor import (DocumentRelatedFeature,
                                                          CapitalizedInDocumentFeature,
                                                          LowercaseInDocumentFeature,
                                                          CapitalizedSentenceHeadInDocumentFeature,
                                                          UppercaseInDocumentFeature)

doc = [
    'But Ben van Beurden , chief executive of Shell'.split(),
    "Shell 's oil and gas business".split(),
    "Some of them ( Shell projects ) may be put on pause IBM 12345".split(),
    "12345 , _good_".split(),
    "HAO hehe".split(),
]


def test_DocumentRelatedFeature():
    f = DocumentRelatedFeature()
    assert_raises(TypeError, f.check_doc, 1)
    assert_raises(TypeError,
                  f.check_doc, [['a', 'a'], None])

    assert_false(f.tail_token_match_predicate(
        doc,
        lambda t: t == 'but')
    )
    assert_false(f.tail_token_match_predicate(
        doc,
        lambda t: t == 'But')
    )

    assert_true(f.head_token_match_predicate(
        doc,
        lambda t: t == 'But')
    )

    assert_true(f.every_token_match_predicate(
        doc,
        lambda t: t == 'Shell')
    )


def test_capindoc():
    f = CapitalizedInDocumentFeature()
    words = ['shell', 'some']
    assert_true(f.get_value(0, words, doc=doc))
    assert_false(f.get_value(1, words, doc=doc))


def test_lowerindoc():
    f = LowercaseInDocumentFeature()
    words = ['Executive', 'Some']
    assert_true(f.get_value(0, words, doc=doc))
    assert_false(f.get_value(1, words, doc=doc))


def test_CapitalizedSentenceHeadInDocumentFeature():
    f = CapitalizedSentenceHeadInDocumentFeature()
    assert_true(f.get_value(0, ['but'], doc=doc))
    assert_false(f.get_value(0, ['them'], doc=doc))


def test_UpperInDocumentFeature():
    f = UppercaseInDocumentFeature()
    assert_true(f.get_value(0, ['ibm'], doc=doc))
    assert_true(f.get_value(0, ['hao'], doc=doc))
    assert_false(f.get_value(0, ['ben'], doc=doc))


def test_non_alpha_values():
    feats = [CapitalizedInDocumentFeature(),
             CapitalizedSentenceHeadInDocumentFeature(),
             UppercaseInDocumentFeature(),
             LowercaseInDocumentFeature()]
    words = [',', '12345', '_good_']
    for f in feats:
        for i in xrange(len(words)):
            assert_false(f.get_value(i, words, doc=doc))
