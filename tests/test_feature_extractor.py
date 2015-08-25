# -*- coding: utf-8 -*-

import os
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
            AllLowercaseFeature,
            BeginsWithAlphaFeature,
            ContainsPunctuationFeature,
            POSFeature,
            CapitalizedInDocumentFeature,
            LowercaseInDocumentFeature,
            UppercaseInDocumentFeature,
            GenericDitionaryFeature,
            FirstnameDictionaryFeature,
            MixedCaseInTailFeature,
            TokenNormalizer,
            CapitalizedWithPreviousWordInDocument,
            CapitalizedWithNextWordInDocument
    )
from capitalization_restoration.dictionary import ItemListDictionary

from capitalization_restoration.tests.data import (load_turkish_example,
                                                   load_china_example)


CURDIR = os.path.dirname(os.path.realpath(__file__))


feats_extractors = [
    WordFeature(), IsLeadingWordFeature(),
    LowercaseInDictionaryFeature(),
    UppercaseInDictionaryFeature(),
    CapitalizedInDictionaryFeature(),
    OriginalInDictionaryFeature(),
    AllUppercaseFeature(),
    BeginsWithAlphaFeature(),
    ContainsPunctuationFeature(),
    POSFeature(),
    CapitalizedInDocumentFeature(),
    LowercaseInDocumentFeature(),
    UppercaseInDocumentFeature()
]


def test_digitalize():
    n = TokenNormalizer()
    assert_equal(n.digitalize('123'), '_DIG_' * 3)
    assert_equal(n.digitalize(u'\xe9'), u'\xe9')
    

def test_FeatureExtractor():
    toks, lemmas, tags, doc = load_turkish_example()
    ext = FeatureExtractor(feats_extractors)
    feats = ext.extract(toks, pos=tags, doc=doc, lemma=lemmas)
    assert_equal(len(toks), len(feats))
    for tok in feats:
        assert_equal(len(tok), len(feats_extractors))

    assert_equal(feats[3]['word'], 'Lithuanian')
    assert_false(feats[3]['cap-in-doc'])

    assert_equal(feats[6]['word'], 'Business')
    assert_true(feats[6]['lower-in-doc'])


def test_FeatureExtractor_china_example():
    toks, lemmas, tags, doc = load_china_example()
    ext = FeatureExtractor(feats_extractors)
    feats = ext.extract(toks, pos=tags, doc=doc,
                        lemma=lemmas)
    
    # China
    assert_true(feats[0]['begins-with-alphabetic'])
    assert_true(feats[0]['cap-in-doc'])
    assert_false(feats[0]['lower-in-doc'])
    assert_true(feats[0]['upper-in-doc'])

    assert_true(feats[0]['begins-with-alphabetic'])
    assert_true(feats[0]['cap-in-doc'])
    assert_false(feats[0]['lower-in-doc'])
    assert_true(feats[0]['upper-in-doc'])

    assert_false(feats[1]['upper-in-doc'])
    assert_false(feats[1]['lower-in-doc'])
    assert_false(feats[1]['cap-in-doc'])
    
    assert_false(feats[2]['upper-in-dict'])
    assert_true(feats[2]['lower-in-dict'])
    assert_false(feats[2]['cap-in-dict'])


def test_LemmaFeature():
    words = ['I', 'love', 'those', 'games', u'\xe9', 12345, 'hao123']
    input_lemma = ['i', 'love', 'those', 'game', u'\xe9', 12345, 'hao123', ]
    expected_lemma = input_lemma[:]

    expected_lemma[-2] = '_DIG_' * 5
    expected_lemma[-1] = 'hao_DIG__DIG__DIG_'

    feat = LemmaFeature()
    assert_equal(feat.name, 'lemma')
    for i in xrange(len(expected_lemma)):
        assert_equal(expected_lemma[i],
                     feat.get_value(i, words, lemma=input_lemma))


def test_WordFeature():
    feat = WordFeature()
    assert_equal('company', feat.get_value(0, ["company"]))
    assert_equal('hao_DIG__DIG__DIG_', feat.get_value(0, ["hao123"]))


def test_POSFeature():
    feat = POSFeature()
    assert_equal('NN',
                 feat.get_value(0, ["company"], pos=["NN"]))


def test_IsLeadingWordFeature():
    f = IsLeadingWordFeature()
    assert_false(f.get_value(1, ["company", "hehe"]))
    assert_true(f.get_value(0, ["123"]))


def test_BeginsWithAlphaFeature():
    f = BeginsWithAlphaFeature()
    assert_true(f.get_value(0, ["company"]))
    assert_true(f.get_value(0, ["China"]))
    assert_false(f.get_value(0, ["123"]))


def test_LowercaseInDictionaryFeature():
    f = LowercaseInDictionaryFeature()
    assert_true(f.get_value(0, ["company"]))
    assert_false(f.get_value(0, ["ibm"]))


def test_UppercaseInDictionaryFeature():
    f = UppercaseInDictionaryFeature()
    assert_false(f.get_value(0, ["company"]))
    assert_false(f.get_value(0, ["ask"]))
    assert_false(f.get_value(0, ["occasionally"]))
    assert_true(f.get_value(0, ["ibm"]))


def test_OriginalInDictionaryFeature():
    f = OriginalInDictionaryFeature()
    assert_true(f.get_value(0, ["Belarus"]))
    assert_false(f.get_value(0, ["belarus"]))


def test_CapitalizedInDictionaryFeature():
    f = CapitalizedInDictionaryFeature()
    assert_true(f.get_value(0, ["google"]))
    assert_false(f.get_value(0, ["ibm"]))


def test_ContainsPunctuationFeature():
    f = ContainsPunctuationFeature()
    assert_true(f.get_value(0, ["A-B"]))
    assert_false(f.get_value(0, ["AB"]))


def test_AllUppercaseFeature():
    f = AllUppercaseFeature()
    assert_true(f.get_value(0, [u'U.S.']))
    assert_false(f.get_value(0, [u'Ad']))
    assert_false(f.get_value(0, [u'123..4']))
    assert_true(f.get_value(0, [u'HAO123']))
    assert_false(f.get_value(0, [u'FIIs']))


def test_GenericFilebasedDitionaryFeature():
    f = GenericDitionaryFeature(ItemListDictionary(CURDIR + '/data/dict.txt'))
    assert_false(f.get_value(0, ['c']))
    assert_false(f.get_value(0, ['adsad']))
    assert_true(f.get_value(0, ['a']))
    assert_true(f.get_value(0, ['1111111111111111']))


def test_FirstnameDictionaryFeature():
    f = FirstnameDictionaryFeature()
    assert_true(f.get_value(0, [u'Abigale']))
    assert_false(f.get_value(0, [u'Han']))


def test_MixedCaseInTailFeature():
    f = MixedCaseInTailFeature()
    assert_true(f.get_value(0, [u'iPhone']))
    assert_false(f.get_value(0, [u'Apple']))


def test_AllLowercaseFeature():
    f = AllLowercaseFeature()
    assert_false(f.get_value(0, [u'iPhone']))
    assert_false(f.get_value(0, [u'IBM']))
    assert_true(f.get_value(0, [u'apple']))
    assert_true(f.get_value(0, [u'12-year']))
    assert_false(f.get_value(0, [u'12-Century']))


def test_CapitalizedWithPreviousWordInDocument():
    f = CapitalizedWithPreviousWordInDocument()
    assert_equal(f.name, 'cap-with-prev-word-in-doc')
    
    toks, lemmas, tags, doc = load_turkish_example()

    assert_true(f.get_value(1, ['between', 'lithuania'], doc=doc))
    assert_false(f.get_value(0, ['between'], doc=doc))
    assert_false(f.get_value(1, ['three', 'agreements'], doc=doc))
    assert_false(f.get_value(1, ['between', 'china'], doc=doc))

    # artifial doc
    doc = [['Long', 'Long', 'ago']]
    assert_true(f.get_value(1, ['long', 'long'], doc=doc))


def test_CapitalizedWithCurrentWordInDocument():
    f = CapitalizedWithNextWordInDocument()
    assert_equal(f.name, 'cap-with-next-word-in-doc')

    toks, lemmas, tags, doc = load_turkish_example()

    assert_true(f.get_value(0, ['lithuania', 'and'], doc=doc))
    assert_false(f.get_value(0, ['between'], doc=doc))
    assert_false(f.get_value(0, ['three', 'agreements'], doc=doc))
    assert_false(f.get_value(0, ['china', 'open'], doc=doc))

    # artifial doc
    doc = [['Long', 'Long', 'ago']]
    assert_false(f.get_value(0, ['long', 'long'], doc=doc))
    assert_true(f.get_value(1, ['long', 'long', 'ago'], doc=doc))
