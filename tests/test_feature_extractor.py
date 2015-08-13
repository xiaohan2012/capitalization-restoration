from nose.tools import assert_equal, assert_false, assert_true

from capitalization_restoration.feature_extractor \
    import (FeatureExtractor,
            LemmaFeature,
            WordFeature, IsLeadingWordFeature,
            LowercaseInDictionaryFeature,
            UppercaseInDictionaryFeature,
            CapitalizedInDictionaryFeature,
            OriginalInDictionaryFeature,
            AllUppercaseFeature,
            BeginsWithAlphaFeature,
            ContainsPunctuationFeature,
            POSFeature,
            CapitalizedInDocumentFeature,
            LowercaseInDocumentFeature)

from capitalization_restoration.tests.data import load_turkish_example


feats_extractors = [
    WordFeature, IsLeadingWordFeature,
    LowercaseInDictionaryFeature,
    UppercaseInDictionaryFeature,
    CapitalizedInDictionaryFeature,
    OriginalInDictionaryFeature,
    AllUppercaseFeature,
    BeginsWithAlphaFeature,
    ContainsPunctuationFeature,
    POSFeature,
    CapitalizedInDocumentFeature,
    LowercaseInDocumentFeature
]


def test_FeatureExtractor():
    toks, tags, doc = load_turkish_example()
    ext = FeatureExtractor(feats_extractors)
    feats = ext.extract(toks, pos=tags, doc=doc)
    assert_equal(len(toks), len(feats))
    for tok in feats:
        assert_equal(len(tok), len(feats_extractors))

    assert_equal(feats[3]['word'], 'Lithuanian')
    assert_false(feats[3]['indoccap'])

    assert_equal(feats[6]['word'], 'Business')
    assert_true(feats[6]['indoclower'])


def test_LemmaFeature():
    words = ['I', 'love', 'those', 'game']
    lemma = ['i', 'love', 'those', 'games']
    for i in xrange(len(lemma)):
        assert_equal(lemma[i],
                     LemmaFeature.get_value(i, words, lemma=lemma))
