import os
import re
import string

from dictionary import ItemListDictionary

CURDIR = os.path.dirname(os.path.realpath(__file__))


class Feature(object):
    def get_value(cls, t, words, **kwargs):
        raise NotImplementedError


class TokenNormalizer(object):
    def __init__(self):
        self.replace_digit_regexp = re.compile(r"[0-9]")
        self.replace_str = '_DIG_'

    def digitalize(self, word):
        return self.replace_digit_regexp.sub(self.replace_str, word)

        
class WordFeature(Feature, TokenNormalizer):
    """
    The word feature
    """
    def __init__(self):
        self.name = "word"
        super(WordFeature, self).__init__()

    def get_value(self, t, words, **kwargs):
        return self.digitalize(words[t])


class LemmaFeature(Feature, TokenNormalizer):
    """
    The lemma feature

    if it's empty string, return the token

    """
    def __init__(self):
        self.name = "lemma"
        super(LemmaFeature, self).__init__()

    def get_value(self, t, words, **kwargs):
        if 'lemma' in kwargs:
            l = kwargs['lemma'][t]
            if isinstance(l, basestring) and len(l) == 0:
                return words[t]
            else:
                return self.digitalize(unicode(l))
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

    def begins_with_alpha(self, word):
        return word[0].isalpha()

    def get_value(self, t, words, **kwargs):
        return self.begins_with_alpha(words[t])


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


class StripNonAlphabeticalMixin(object):
    def __init__(self):
        exclude = unicode(string.punctuation + ''.join(
            [str(i)
             for i in xrange(10)])
        )
        self.table = {ord(c): None
                      for c in exclude}


class AllUppercaseFeature(Feature, StripNonAlphabeticalMixin):
    """
    If the letters in word is all uppercased
    """
    def __init__(self):
        super(AllUppercaseFeature, self).__init__()
        self.name = "all-letter-uppercase"

    def get_value(self, t, words, **kwargs):
        word = words[t].translate(self.table)  # Remove punctuations + numbers
        if len(word) > 0:
            return (word.upper() == word)
        else:
            return False


class AllLowercaseFeature(Feature, StripNonAlphabeticalMixin):
    """
    If the letters in word is all lowercased
    """
    def __init__(self):
        super(AllLowercaseFeature, self).__init__()
        self.name = "all-letter-lowercase"

    def get_value(self, t, words, **kwargs):
        word = words[t].translate(self.table)  # Remove punctuations + numbers
        if len(word) > 0:
            return (word.lower() == word)
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
        valid_toks = [tok for sent in doc for tok in sent[1:] if func(tok)]
        return len(valid_toks) > 0

    def head_token_match_predicate(self, doc, func):
        """
        Check if any of the head tokens in the doc fulfill the `func`
        """
        valid_toks = [sent[0] for sent in doc if func(sent[0])]
        return len(valid_toks) > 0

    def every_token_match_predicate(self, doc, func):
        """
        Check if any of the tokens in the doc fulfill the `func`
        """
        valid_toks = [tok for sent in doc for tok in sent if func(tok)]
        return len(valid_toks) > 0


class CapitalizedSentenceHeadInDocumentFeature(DocumentRelatedFeature,
                                               BeginsWithAlphaFeature):
    """
    Whether the word appears capitalized at the sentence head of the document.
    """
    def __init__(self):
        super(CapitalizedSentenceHeadInDocumentFeature, self).__init__()
        self.name = 'cap-sent-head-in-doc'
        
    def _get_label_for_word(self, word, doc):
        cap_word = unicode(word.capitalize())
        return self.head_token_match_predicate(
            doc, lambda tok: cap_word == tok
        )

    def get_value(self, t, words, **kwargs):
        if self.begins_with_alpha(words[t]):
            doc = kwargs.get("doc")
            
            self.check_doc(doc)
            
            return self._get_label_for_word(words[t], doc)
        else:
            return False
        

class CapitalizedInDocumentFeature(DocumentRelatedFeature,
                                   BeginsWithAlphaFeature):
    """
    Whether the word appears capitalized in the document.

    One exception is the leading word of the sentence, which is capitalized by convention.

    In this case, we don't consider it as capitalized

    """
    def __init__(self):
        super(CapitalizedInDocumentFeature, self).__init__()
        self.name = "cap-in-doc"

    def _get_label_for_word(self, word, doc):
        cap_word = unicode(word.capitalize())
        return self.tail_token_match_predicate(
            doc, lambda tok: cap_word == tok
        )

    def get_value(self, t, words, **kwargs):
        if self.begins_with_alpha(words[t]):
            doc = kwargs.get("doc")

            self.check_doc(doc)

            return self._get_label_for_word(words[t], doc)
        else:
            return False


class UppercaseInDocumentFeature(DocumentRelatedFeature,
                                 BeginsWithAlphaFeature):
    def __init__(self):
        super(UppercaseInDocumentFeature, self).__init__()
        self.name = 'upper-in-doc'
        
    def _get_label_for_word(self, word, doc):
        upper_word = word.upper()
        return self.every_token_match_predicate(
            doc, lambda tok: upper_word == tok
        )

    def get_value(self, t, words, **kwargs):
        if self.begins_with_alpha(words[t]):
            doc = kwargs.get("doc")
            self.check_doc(doc)
            return self._get_label_for_word(words[t], doc)
        else:
            return False
    

class LowercaseInDocumentFeature(DocumentRelatedFeature,
                                 BeginsWithAlphaFeature):
    """
    Whether the word appears lower-cased in the document.

    In this case, we don't consider it as lower-cased
    """
    def __init__(self):
        super(LowercaseInDocumentFeature, self).__init__()
        self.name = "lower-in-doc"

    def _get_label_for_word(self, word, doc):
        lower_word = word.lower()
        return self.tail_token_match_predicate(
            doc, lambda tok: lower_word == tok
        )

    def get_value(self, t, words, **kwargs):
        if self.begins_with_alpha(words[t]):
            doc = kwargs.get("doc")
            self.check_doc(doc)
            return self._get_label_for_word(words[t], doc)
        else:
            return False


DEFAULT_FEATURES = [
    WordFeature(),
    IsLeadingWordFeature(),
    LowercaseInDictionaryFeature(),
    UppercaseInDictionaryFeature(),
    CapitalizedInDictionaryFeature(),
    OriginalInDictionaryFeature(),
    AllLowercaseFeature(),
    AllUppercaseFeature(),
    MixedCaseInTailFeature(),
    BeginsWithAlphaFeature(),
    ContainsPunctuationFeature(),
    POSFeature(),
    CapitalizedInDocumentFeature(),
    CapitalizedSentenceHeadInDocumentFeature(),
    LowercaseInDocumentFeature(),
    UppercaseInDocumentFeature(),
    FirstnameDictionaryFeature(),
]


class FeatureExtractor(object):
    """
    Extract features for sentence
    """
    def __init__(self, features=DEFAULT_FEATURES, convert_bool=False):
        self.features = features
        for feat in self.features:
            assert hasattr(feat, 'name')
            assert feat.name != None, \
                '{} should have a name'.format(feat.__class__)
        self.convert_bool = convert_bool
        self.bool2str_map = {True: '--T',
                             False: '--F'}

    def extract(self, sent, *args, **kwargs):
        """Expect unicode strings"""
        assert isinstance(sent, list), "sent must be a list"

        words_with_features = []
        for i in xrange(len(sent)):
            word = {}
            for feature in self.features:
                value = feature.get_value(i, sent,
                                          **kwargs)
                if self.convert_bool and isinstance(value, bool):
                    value = self.bool2str_map[value]
                word[feature.name] = value

            words_with_features.append(word)

        return words_with_features

    @property
    def feature_names(self):
        return [feature.name for feature in self.features]

if __name__ == '__main__':
    print('\t'.join([f.name for f in DEFAULT_FEATURES]))
