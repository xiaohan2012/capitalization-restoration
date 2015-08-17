import os
import string

from dictionary import ItemListDictionary

CURDIR = os.path.dirname(os.path.realpath(__file__))


class Feature(object):
    def get_value(cls, t, words, **kwargs):
        raise NotImplementedError


class WordFeature(Feature):
    """
    The word feature
    """
    def __init__(self):
        self.name = "word"

    def get_value(cls, t, words, **kwargs):
        return words[t]


class LemmaFeature(Feature):
    """
    The lemma feature

    if it's empty string, return the token

    """
    def __init__(self):
        self.name = "lemma"

    def get_value(self, t, words, **kwargs):
        if 'lemma' in kwargs:
            l = kwargs['lemma'][t]
            if isinstance(l, basestring) and len(l) == 0:
                return words[t]
            else:
                return l
        else:
            raise KeyError("'lemma' is not in arguments")


class MixedCaseInTailFeature(Feature):
    """
    Check if tail substring is mixed case
    """
    def __init__(self):
        self.name = 'mixed-in-tail'

    def get_value(self, t, words, **kwargs):
        tail = words[t][1:]
        return (tail.lower() != tail and
                tail.upper() != tail)


class GenericDitionaryFeature(Feature):
    """
    Check if token is in dictionary
    """
    def __init__(self, dict_):
        self.dict_ = dict_

    def get_value(self, t, words, **kwargs):
        return words[t] in self.dict_
        

class FirstnameDictionaryFeature(GenericDitionaryFeature):
    def __init__(self):
        dict_ = ItemListDictionary(CURDIR + '/data/dict/dict-first-names.txt')
        super(FirstnameDictionaryFeature, self).__init__(dict_)
        self.name = 'first-name-in-dict'


class POSFeature(Feature):
    """
    The word Part-of-speech tag
    """
    def __init__(self):
        self.name = "pos-tag"

    def get_value(self, t, words, **kwargs):
        if 'pos' in kwargs:
            return kwargs['pos'][t]
        else:
            raise KeyError("'pos' is not in arguments")


class IsLeadingWordFeature(Feature):
    """
    If the word is the first one of the sentence or not
    """
    def __init__(self):
        self.name = "is-leading-word"

    def get_value(self, t, words, **kwargs):
        return t == 0


class BeginsWithAlphaFeature(Feature):
    """
    If the word begins with alpha
    """
    def __init__(self):
        self.name = "begins-with-alphabetic"

    def get_value(self, t, words, **kwargs):
        return words[t][0].isalpha()


unix_dictionary = ItemListDictionary(CURDIR + "/data/dict/unix.txt")


class LowercaseInDictionaryFeature(Feature):
    """
    If the uppercase word is in dictionary
    """
    def __init__(self):
        self.name = "lower-in-dict"

    def get_value(self, t, words, **kwargs):
        return unix_dictionary.check(words[t].lower())


class UppercaseInDictionaryFeature(Feature):
    """
    If the uppercase word is in dictionary
    """
    def __init__(self):
        self.name = "upper-in-dict"

    def get_value(self, t, words, **kwargs):
        return unix_dictionary.check(words[t].upper())


class OriginalInDictionaryFeature(Feature):
    """
    If the original word is in dictionary
    """
    def __init__(self):
        self.name = "orig-in-dict"

    def get_value(self, t, words, **kwargs):
        return unix_dictionary.check(words[t])


class CapitalizedInDictionaryFeature(Feature):
    """
    If the capitalized word is in dictionary
    """
    def __init__(self):
        self.name = "cap-in-dict"
        
    def get_value(self, t, words, **kwargs):
        return unix_dictionary.check(words[t].capitalize())


class ContainsPunctuationFeature(Feature):
    """
    If the word has punctuations
    """
    def __init__(self):
        self.name = "has-punct"
        self.punct = set(string.punctuation)

    def get_value(self, t, words, **kwargs):
        for l in words[t]:
            if l in self.punct:
                return True
        return False


class AllUppercaseFeature(Feature):
    """
    If the letters in word is all uppercased
    """
    def __init__(self):
        exclude = unicode(string.punctuation + ''.join(
            [str(i)
             for i in xrange(10)])
        )
        self.table = {ord(c): None
                      for c in exclude}
        self.name = "all-letter-uppercase"

    def get_value(self, t, words, **kwargs):
        word = words[t].translate(self.table)  # Remove punctuations + numbers
        if len(word) > 0:
            return (word.upper() == word)
        else:
            return False


class DocumentRelatedFeature(Feature):
    def check_doc(self, doc):
        try:
            assert isinstance(doc, list)
            for sent in doc:
                assert isinstance(sent, list)
        except AssertionError:
            raise TypeError('doc/sent type should be list, is {} instead'
                            .format(type(doc)))

    def tail_token_match_predicate(self, doc, func):
        """
        Check if any of the tail tokens in the doc fulfill the `func`
        """
        for sent in doc:
            for tok in sent[1:]:  # ignore the heading word
                if func(tok):
                    return True
        return False


class CapitalizedInDocumentFeature(DocumentRelatedFeature):
    """
    Whether the word appears capitalized in the document.

    One exception is the leading word of the sentence, which is capitalized by convention.

    In this case, we don't consider it as capitalized

    """
    def __init__(self):
        self.name = "cap-in-doc"
    
    def _get_label_for_word(self, word, doc):
        cap_word = unicode(word[0].upper() + word[1:])
        return self.tail_token_match_predicate(
            doc, lambda tok: cap_word == tok
        )

    def get_value(self, t, words, **kwargs):
        doc = kwargs.get("doc")

        self.check_doc(doc)

        return self._get_label_for_word(words[t], doc)


class LowercaseInDocumentFeature(DocumentRelatedFeature):
    """
    Whether the word appears lower-cased in the document.

    In this case, we don't consider it as lower-cased
    """
    def __init__(self):
        self.name = "lower-in-doc"

    def _get_label_for_word(self, word, doc):
        lower_word = word.lower()
        return self.tail_token_match_predicate(
            doc, lambda tok: lower_word == tok
        )

    def get_value(self, t, words, **kwargs):
        doc = kwargs.get("doc")
        self.check_doc(doc)
        return self._get_label_for_word(words[t], doc)


DEFAULT_FEATURES = [
    LemmaFeature(), IsLeadingWordFeature(),
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
    FirstnameDictionaryFeature()
]


class FeatureExtractor(object):
    """
    Extract features for sentence
    """
    def __init__(self, features=DEFAULT_FEATURES):
        self.features = features
        for feat in self.features:
            assert hasattr(feat, 'name')
            assert feat.name != None, \
                '{} should have a name'.format(feat.__class__)

    def extract(self, sent, *args, **kwargs):
        """Expect unicode strings"""
        assert isinstance(sent, list), "sent must be a list"

        words_with_features = []
        for i in xrange(len(sent)):
            word = {}
            for feature in self.features:
                word[feature.name] = feature.get_value(i, sent,
                                                       **kwargs)

            words_with_features.append(word)

        return words_with_features

    @property
    def feature_names(self):
        return [feature.name for feature in self.features]
