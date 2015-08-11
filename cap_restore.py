# coding: utf-8
import os
import sys
import pycrfsuite
from feature_extractor import FeatureExtractor
from feature_templates import (load_feature_templates, apply_templates)

from cap_detect import (capitalized, all_lowercase, all_uppercase)


CURDIR = os.path.dirname(os.path.realpath(__file__))


class MultiPurposeRestorer(object):
    u"""
    Capitalization restorer that captures capitalized, lowercase and uppercase sentences

    >>> import nltk
    >>> docpath = "/group/home/puls/Shared/capitalization-recovery/10/www.proactiveinvestors.co.uk.sectors.41.rss/D8B4C87CDC7862F53E6285DDC892C7C0"
    >>> r = MultiPurposeRestorer('models/cap_model.bin', 
    ... 'models/lower_model.bin', 
    ... 'models/upper_model.bin',
    ... FeatureExtractor(), load_feature_templates())
    >>> r.restore(nltk.word_tokenize(u"Cyan Holdings Represented at Heavyweight Round-table Event in India"),
    ... docpath=docpath)
    [u'Cyan', u'Holdings', u'represented', u'at', u'heavyweight', u'round-table', u'event', u'in', u'India']
    >>> r.restore(nltk.word_tokenize(u"cyan holdings represented at heavyweight round-table event in india"),
    ... docpath=docpath)
    [u'Cyan', u'Holdings', u'represented', u'at', u'heavyweight', u'round-table', u'event', u'in', u'India']
    >>> r.restore(nltk.word_tokenize(u"CYAN HOLDINGS REPRESENTED AT HEAVYWEIGHT ROUND-TABLE EVENT IN INDIA"),
    ... docpath=docpath) # doctest: +SKIP
    [u'CYAN', u'HOLDINGS', u'represented', u'at', u'heavyweight', u'round-table', u'event', u'in', u'INDIA']

    >>> docpath="/group/home/puls/Shared/capitalization-recovery/10/www.zawya.com.rssfeeds.tourism/E85D3090167053EFB118C243D9747FAC"
    >>> r.restore(u"Kingdom € Tourism and Hospitality Sector to Draw Huge Investments".split(),
    ... docpath=docpath)
    [u'Kingdom', u'\\u20ac', u'Tourism', u'and', u'hospitality', u'sector', u'to', u'draw', u'huge', u'investments']

    >>> r.restore(u"Kingdom € Tourism and Hospitality Sector to Draw Huge Investments".split(),
    ... pos=('NNP', ':', 'VBP', 'CC', 'NNP', 'NNP', 'TO', 'NNP', 'NNP', 'NNP'), # Tourism will be lowercased
    ... docpath=docpath)
    [u'Kingdom', u'\\u20ac', u'tourism', u'and', u'hospitality', u'sector', u'to', u'draw', u'huge', u'investments']
    """
    def __init__(self, cap_model_path, lower_model_path, upper_model_path,
                 feature_extractor, feature_templates):
        self.cap_restorer = Restorer(cap_model_path, feature_extractor,
                                     feature_templates)
        self.lower_restorer = Restorer(lower_model_path, feature_extractor,
                                       feature_templates)
        self.upper_restorer = Restorer(upper_model_path, feature_extractor,
                                       feature_templates)

    def _get_restorer(self, words):
        if all_lowercase(words):
            return self.lower_restorer
        elif all_uppercase(words):
            return self.upper_restorer
        elif capitalized(words):
            return self.cap_restorer
        else:
            return None

    def restore(self, words, *args, **kwargs):
        restorer = self._get_restorer(words)
        if restorer:
            return restorer.restore(words, *args, **kwargs)
        else:
            sys.stderr.write("Seems to be in proper capitalization\n")
            return words


class Restorer(object):
    def __init__(self, model_path,
                 feature_extractor=FeatureExtractor(),
                 feature_templates=load_feature_templates()):
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(model_path)
        self.extractor = feature_extractor
        self.templates = feature_templates

    def get_labels(self, sent, *args, **kwargs):
        assert isinstance(sent, list)

        words_with_features = self.extractor.extract(sent, *args, **kwargs)

        for word in words_with_features:  # accord to crfsuite 
            word["F"] = []

        return self.tagger.tag(apply_templates(words_with_features, self.templates))

    def restore(self, sent, *args, **kwargs):
        labels = self.get_labels(sent, *args, **kwargs)
        return transform_words_by_labels(sent, labels)


def transform_words_by_labels(words, labels):
    """
    Transform words capitalization by labels

    >>> words = [u'I', u'Compared', u'PaaS', u'Providers', u':', u'Heroku', u'and', u"IBM", u"'s", u'Bluemix', u'.']
    >>> transform_words_by_labels(words, [u'AU', u'AL', u'MX', u'AL', u'AN', u'IC', u'AL', u'AU', u'AL', u'IC', u'AN'])
    [u'I', u'compared', u'PaaS', u'providers', u':', u'Heroku', u'and', u'IBM', u"'s", u'Bluemix', u'.']
    """
    assert len(words) == len(labels)

    new_words = []
    for w, l in zip(words, labels):
        if l == "IC":
            new_words.append(w[0].upper() + w[1:])
        elif l == "AL":
            new_words.append(w.lower())
        elif l == "AU":
            new_words.append(w.upper())
        elif l == "MX" or l == "AN": # TODO: handle more complex cases for all uppercase or all lowercase input
            new_words.append(w)
        else:
            raise ValueError("Unknown label %s" %(l))

    return new_words


class DefaultRestorer(MultiPurposeRestorer):
    def __init__(self):
        cur_path = os.path.abspath(os.path.dirname(__file__))
        super(DefaultRestorer, self).__init__(os.path.join(cur_path, 'models/cap_model.bin'),
                                              os.path.join(cur_path, 'models/lower_model.bin'),
                                              os.path.join(cur_path, 'models/upper_model.bin'),
                                              FeatureExtractor(),
                                              load_feature_templates())


class PulsRestorer(Restorer):
    """
    Restorerer for PULS system
    """
    def __init__(self, *args, **kwargs):
        super(PulsRestorer, self).__init__(CURDIR + '/models/puls-model',
                                           *args, **kwargs)
