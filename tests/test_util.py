from nose.tools import assert_equal
from capitalization_restoration.util import filter_word_by_shape
from capitalization_restoration.tests.data import load_turkish_example


def test_filter_word_by_shape():
    pass
    toks, lemmas, tags, doc = load_turkish_example()
    filter_word_by_shape(toks, lemmas, tags)
