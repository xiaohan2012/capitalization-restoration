# coding: utf-8
import os
import time
import calendar
import sys
import pycrfsuite
from feature_extractor import FeatureExtractor
from feature_templates import (load_feature_templates, apply_templates)

from cap_detect import (capitalized, all_lowercase, all_uppercase)
from label import get_label

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
        
        start = calendar.timegm(time.gmtime())
        self.tagger.open(model_path)

        self.extractor = feature_extractor
        self.templates = feature_templates

        self.dump = self.tagger.info()
        
        print("loading model takes {}".format(
            calendar.timegm(time.gmtime()) - start)
        )

    def get_labels(self, sent, *args, **kwargs):
        assert isinstance(sent, list)

        words_with_features = self.extractor.extract(sent, *args, **kwargs)
            
        templated_features = apply_templates(words_with_features,
                                             self.templates)
        
        # exclude the first token
        # as well as those that are uppercase, mixed-case and non-alphabetic
        token_ids, templated_features = filter_words(words_with_features,
                                                     templated_features,
                                                     excluded_labels=set(['MX', 'AU', 'AN']))

        # DEBUG START
        # rows = []
        # feats = []
        # pos = 0
        # if len(templated_features) > 1 and \
        #    'word[0]=Decisions' in templated_features[pos]:
        #     for feat in templated_features[pos]:
        #         feats.append(feat)
        #         rows.append((self.dump.state_features.get((feat, 'AL'), 0.0),
        #                      self.dump.state_features.get((feat, 'IC'), 0.0))
        #         )
        #     import pandas as pds
        #     df = pds.DataFrame(rows, index=feats, columns=('AL', 'IC'))
        #     print(df)
        #     print(df.sum(axis=0))
        # DEBUG END

        return token_ids, self.tagger.tag(templated_features)

    def restore(self, sent, *args, **kwargs):
        token_inds, labels = self.get_labels(sent, *args, **kwargs)
        return transform_words_by_labels(sent, labels, token_inds)


def filter_words(words_with_features,
                 templated_features,
                 excluded_labels=set(['MX', 'AU', 'AN'])):
    """
    Filter out words by their shape and position

    Return:
    the corresponding template values
    """
    inds = []
    template_values = []
    for i, (w, t) in enumerate(zip(words_with_features,
                                   templated_features)):
        if i != 0 and get_label(w['word']) not in excluded_labels:
            inds.append(i)
            template_values.append(t)

    return inds, template_values


def transform_words_by_labels(words, labels, token_inds):
    """
    Transform words capitalization by labels
    """
    # print(words)
    # print(labels)
    # print(token_inds)
    assert len(token_inds) == len(labels)

    token_inds = set(token_inds)
    new_words = []
    acc = 0
    for i, w in enumerate(words):
        if i in token_inds:
            l = labels[acc]
            if l == "IC":
                new_words.append(w.capitalize())
            elif l == "AL":
                new_words.append(w.lower())
            else:
                raise ValueError("Unknown label %s" % (l))
            acc += 1
        else:
            new_words.append(w)

    return new_words


class DefaultRestorer(MultiPurposeRestorer):
    def __init__(self):
        cur_path = os.path.abspath(os.path.dirname(__file__))
        super(DefaultRestorer, self).__init__(
            os.path.join(cur_path, 'models/cap_model.bin'),
            os.path.join(cur_path, 'models/lower_model.bin'),
            os.path.join(cur_path, 'models/upper_model.bin'),
            FeatureExtractor(),
            load_feature_templates()
        )


class PulsRestorer(Restorer):
    """
    Restorerer for PULS system
    """
    def __init__(self, *args, **kwargs):
        super(PulsRestorer, self).__init__(
            CURDIR + '/models/puls-model',
            feature_templates=load_feature_templates([1, 3, 4, 6]),
            **kwargs
        )
