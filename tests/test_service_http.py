import os
import json
import urllib2
from pathlib import Path

from nose.tools import assert_equal

from capitalization_restoration.service import (STATUS_RESTORE_ERROR,
                                                STATUS_INVALID_PARAM,
                                                STATUS_OK)

CURDIR = os.path.dirname(os.path.realpath(__file__))

def make_err_msg(code, msg):
    return {"code": code, "msg": msg}


def make_request(data):
    req = urllib2.urlopen(
        "http://{}:{}/caprestore".format('localhost', '8888'),
        json.dumps(data)
    )
    return json.loads(req.read())


def make_json_data(cap_sents=[], other_sents=[]):
    return {'capitalizedSentences': cap_sents,
            'otherSentences': other_sents}


def test_missing_fields():
    # 'capitalizedSentences' shoudl be present
    assert_equal(
        make_request({'haha': None})['code'],
        STATUS_INVALID_PARAM
    )
    
    # 'otherSentences' shoudl be present
    assert_equal(
        make_request({'capitalizedSentences': None})['code'],
        STATUS_INVALID_PARAM
    )


invalid_params = [
    # missing pos, tokens and no for each case
    [{'no': 1, 'tokens': ['a', 'b']}],
    [{'no': 1, 'pos': ['a', 'b']}],
    [{'tokens': ['a', 'b'], 'pos': ['a', 'b']}],
    # not a list
    [{'tokens': ['a', 'b'], 'pos': 'a'}],
    # not a list of str
    [{'tokens': ['a', 'b', 1], 'pos': ['a']}]
]

    
def test_invalid_type():
    for param in invalid_params:
        for arg_name in ['cap_sents', 'other_sents']:
            kwargs = {arg_name: param}
            assert_equal(
                make_request(make_json_data(**kwargs))['code'],
                STATUS_INVALID_PARAM
            )
    

def test_success_case():
    with Path(CURDIR, 'data/request_data.json').open(encoding='utf8') as f:
        req_data = json.loads(f.read())
        res = make_request(req_data)
        assert_equal(res['code'], STATUS_OK)
        assert_equal(res['result'][:2], [
            {'no': 33, 'tokens': u'# # #'.split()},
            {'no': 22, 'tokens': u'About the author'.split()},
        ])
        assert_equal(len(res['result']), 9)

        # empty doc
        req_data['otherSentences'] = []  # empty docs
        res = make_request(req_data)
        assert_equal(res['code'], STATUS_OK)
        assert_equal(len(res['result']), 9)
        assert_equal(res['result'][:2], [
            {'no': 33, 'tokens': u'# # #'.split()},
            {'no': 22, 'tokens': u'About the author'.split()},
        ])

