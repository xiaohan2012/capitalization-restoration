import os
from nose.tools import assert_true, assert_false

from capitalization_restoration.dictionary import ItemListDictionary

CURDIR = os.path.dirname(os.path.realpath(__file__))


def test_ItemListDictionary():
    d = ItemListDictionary(CURDIR + '/data/dict.txt')
    assert_false('c' in d)
    assert_false(d.check('c'))
    assert_true('d' in d)
    assert_true(d.check('d'))
