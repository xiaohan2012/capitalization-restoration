import string
import enchant
import nltk


class Feature(object):
    def __init__(self):
        self.name = None

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
    """
    def __init__(self):
        self.name = "lemma"

    def get_value(self, t, words, **kwargs):
        if 'lemma' in kwargs:
            return kwargs['lemma'][t]
        else:
            raise KeyError("'lemma' is not in arguments")


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


d = enchant.Dict("en_US")


class LowercaseInDictionaryFeature(Feature):
    """
    If the uppercase word is in dictionary
    """
    def __init__(self):
        self.name = "lower-in-dict"

    def get_value(self, t, words, **kwargs):
        return d.check(words[t].lower())


class UppercaseInDictionaryFeature(Feature):
    """
    If the uppercase word is in dictionary
    """
    def __init__(self):
        self.name = "upper-in-dict"

    def get_value(self, t, words, **kwargs):
        return d.check(words[t].upper())


class OriginalInDictionaryFeature(Feature):
    """
    If the original word is in dictionary
    """
    def __init__(self):
        self.name = "orig-in-dict"

    def get_value(self, t, words, **kwargs):
        return d.check(words[t])


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


class CapitalizedInDictionaryFeature(Feature):
    """
    If the capitalized word is in dictionary
    """
    def __init__(self):
        self.name = "cap-in-dict"
        
    def get_value(self, t, words, **kwargs):
        return d.check(words[t].capitalize())


class AllUppercaseFeature(Feature):
    """
    If the letters in word is all uppercased


    """
    def __init__(self):
        exclude = unicode(string.punctuation + ''.join([str(i) for i in xrange(10)]))
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
            raise TypeError('Invalid doc type: {}'.format(doc))

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

    >>> from util import get_document_content_paf, get_document_content
    >>> doc = get_document_content_paf("/group/home/puls/Shared/capitalization-recovery/10/www.cnbc.com.id.10000030.device.rss.rss/90792FEF7ACEE693A7A87BF5F3D341A1")
    >>> CapitalizedInDocumentFeature.get_value(0, [u"Shell"], doc=doc)
    True
    >>> CapitalizedInDocumentFeature.get_value(0, [u"Van Beurden"], doc=doc)
    False
    >>> CapitalizedInDocumentFeature.get_value(0, [u"Getty"], doc=doc)
    False
    >>> CapitalizedInDocumentFeature.get_value(0, [u"'Getty"], doc=doc) #some trick
    False
    >>> doc = get_document_content_paf("/group/home/puls/Shared/capitalization-recovery/12/www.sacbee.com.business.index/A33DCBDA991E786734BCA02B01B9DB04")
    >>> CapitalizedInDocumentFeature.get_value(0, [u'Shinjiro'], doc=doc)
    False
    >>> CapitalizedInDocumentFeature.get_value(0, [u'Valley'], doc=doc)
    False
    >>> CapitalizedInDocumentFeature.get_value(0, [u'Robertson'], doc=doc)
    True
    """
    def __init__(self):
        self.name = "indoccap"
    
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

    >>> from util import get_document_content_paf, get_document_content
    >>> doc = get_document_content_paf("/group/home/puls/Shared/capitalization-recovery/10/www.cnbc.com.id.10000030.device.rss.rss/90792FEF7ACEE693A7A87BF5F3D341A1")
    >>> LowercaseInDocumentFeature.get_value(0, [u"decline"], doc=doc)
    True
    >>> LowercaseInDocumentFeature.get_value(0, [u"Buerden"], doc=doc)
    False
    >>> LowercaseInDocumentFeature.get_value(0, [u"Getty"], doc=doc)
    False
    >>> LowercaseInDocumentFeature.get_value(0, [u"'Getty"], doc=doc) #some trick
    False
    >>> doc = get_document_content_paf("/group/home/puls/Shared/capitalization-recovery/12/www.sacbee.com.business.index/A33DCBDA991E786734BCA02B01B9DB04")
    >>> LowercaseInDocumentFeature.get_value(0, [u'Shinjiro'], doc=doc)
    False
    >>> LowercaseInDocumentFeature.get_value(0, [u'Valley'], doc=doc)
    False
    >>> LowercaseInDocumentFeature.get_value(0, [u'Robertson'], doc=doc)
    False
    """
    def __init__(self):
        self.name = "indoclower"

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
    LowercaseInDocumentFeature()
]


class FeatureExtractor(object):
    """
    Extract features for sentence
    """
    def __init__(self, features=DEFAULT_FEATURES):
        self.features = features

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
