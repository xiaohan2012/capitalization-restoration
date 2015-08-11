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
    assert_raises(ValueError, DocumentRelatedFeature.check_doc, None)
    assert_raises(TypeError, DocumentRelatedFeature.check_doc, 1)
    assert_raises(TypeError,
                  DocumentRelatedFeature.check_doc, [['a', 'a'], None])

    assert_false(DocumentRelatedFeature.tail_token_match_predicate(
        doc,
        lambda t: t == 'but')
    )
    assert_false(DocumentRelatedFeature.tail_token_match_predicate(
        doc,
        lambda t: t == 'But')
    )


def test_capindoc():
    words = ['shell', 'some']
    assert_true(CapitalizedInDocumentFeature.get_value(0, words, doc=doc))
    assert_false(CapitalizedInDocumentFeature.get_value(1, words, doc=doc))


def test_lowerindoc():
    words = ['Executive', 'Some']
    assert_true(LowercaseInDocumentFeature.get_value(0, words, doc=doc))
    assert_false(LowercaseInDocumentFeature.get_value(1, words, doc=doc))

