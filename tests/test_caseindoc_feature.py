from nose.tools import (assert_true, assert_false, assert_raises)

from capitalization_restoration.feature_extractor import (DocumentRelatedFeature,
                                                          CapitalizedInDocumentFeature,
                                                          LowercaseInDocumentFeature)

doc = [
    'But Ben van Beurden, chief executive of Shell'.split(),
    "Shell's oil and gas business".split(),
    "Some of them ( Shell projects ) may be put on pause".split(),
]


def test_DocumentRelatedFeature():
    feat = DocumentRelatedFeature()
    assert_raises(TypeError, feat.check_doc, 1)
    assert_raises(TypeError,
                  feat.check_doc, [['a', 'a'], None])

    assert_false(feat.tail_token_match_predicate(
        doc,
        lambda t: t == 'but')
    )
    assert_false(feat.tail_token_match_predicate(
        doc,
        lambda t: t == 'But')
    )


def test_capindoc():
    feat = CapitalizedInDocumentFeature()
    words = ['shell', 'some']
    assert_true(feat.get_value(0, words, doc=doc))
    assert_false(feat.get_value(1, words, doc=doc))


def test_lowerindoc():
    feat = LowercaseInDocumentFeature()
    words = ['Executive', 'Some']
    assert_true(feat.get_value(0, words, doc=doc))
    assert_false(feat.get_value(1, words, doc=doc))

