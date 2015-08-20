from capitalization_restoration.feature_templates import apply_templates
from capitalization_restoration.tests.data import load_turkish_example
from capitalization_restoration.feature_extractor import (FeatureExtractor,
                                                          IsLeadingWordFeature,
                                                          LowercaseInDictionaryFeature,
                                                          UppercaseInDictionaryFeature,
                                                          CapitalizedInDictionaryFeature,
                                                          OriginalInDictionaryFeature,
                                                          AllUppercaseFeature,
                                                          AllLowercaseFeature,
                                                          BeginsWithAlphaFeature,
                                                          ContainsPunctuationFeature,
                                                          POSFeature,
                                                          CapitalizedInDocumentFeature,
                                                          LowercaseInDocumentFeature,
                                                          UppercaseInDocumentFeature,
                                                          GenericDitionaryFeature,
                                                          FirstnameDictionaryFeature,
                                                          MixedCaseInTailFeature)
from nose.tools import assert_true

features = (LowercaseInDocumentFeature(),
            CapitalizedInDocumentFeature())


templates = [
    (('cap-in-doc', 0), ),
    (('cap-in-doc', -1), ),
    (('lower-in-doc', 0), ),
    (('cap-in-doc', -1), ('cap-in-doc', 0), ('lower-in-doc', 0))
]


def test_apply_templates():
    toks, lemmas, tags, doc = load_turkish_example()
    ext = FeatureExtractor(features)
    feats = ext.extract(toks, pos=tags, doc=doc, lemma=lemmas)
    templ_feats = apply_templates(feats, templates)

    assert_true(u'cap-in-doc[0]=False' in templ_feats[0])
    assert_true(u'lower-in-doc[0]=True' in templ_feats[0])
    assert_true(u'cap-in-doc[-1]=False' in templ_feats[1])
