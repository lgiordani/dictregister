#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dictregister
----------------------------------

Tests for `dictregister` module.
"""

import pytest

import dictregister as dr


@pytest.fixture
def fixdr():
    return dr.DictRegister([{'x': 1, 'y': 2}, {'x': 3, 'y': 4}])


@pytest.fixture
def fixdrmult():
    return dr.DictRegister([{'x': set([1, 3]), 'y': 2}, {'x': 3, 'y': 4}])


def test_instance_without_parameters():
    dr.DictRegister()


def test_instance_with_a_list_of_dicts(fixdr):
    assert len(fixdr) == 2


def test_can_be_indexed(fixdr):
    assert fixdr[0] == {'x': 1, 'y': 2}


def test_instance_with_an_argument():
    with pytest.raises(ValueError):
        dr.DictRegister([1, 2, 3])


def test_append_dict(fixdr):
    fixdr.append({'x': 4, 'y': 5})
    assert len(fixdr) == 3


def test_cannot_append_non_dict(fixdr):
    with pytest.raises(ValueError):
        fixdr.append(6)


def test_add_keyword(fixdr):
    fixdr.kadd('z', 3)
    assert len(fixdr) == 2
    assert fixdr[0] == {'x': 1, 'y': 2, 'z': 3}


def test_add_already_present_keyword(fixdr):
    fixdr.kadd('x', 3)
    assert len(fixdr) == 2
    assert fixdr[0] == {'x':  set([1, 3]), 'y': 2}


def test_replace_already_present_keyword(fixdr):
    fixdr.kreplace('x', 3)
    assert len(fixdr) == 2
    assert fixdr[0] == {'x':  3, 'y': 2}


def test_replace_not_present_keyword(fixdr):
    fixdr.kreplace('z', 3)
    assert len(fixdr) == 2
    assert fixdr[0] == {'x':  1, 'y': 2}


def test_remove_keyword(fixdr):
    fixdr.kremove('x')
    assert len(fixdr) == 2
    assert fixdr[0] == {'y': 2}
    assert fixdr[1] == {'y': 4}


def test_remove_keyword_with_multiple_values(fixdrmult):
    fixdrmult.kremove('x', 3)
    assert len(fixdrmult) == 2
    assert fixdrmult[0] == {'x': 1, 'y': 2}
    assert fixdrmult[1] == {'y': 4}


def test_remove_not_present_keyword(fixdr):
    fixdr.kremove('z')
    assert len(fixdr) == 2
    assert fixdr[0] == {'x': 1, 'y': 2}
    assert fixdr[1] == {'x': 3, 'y': 4}


def test_dfilter_eq(fixdr):
    filtdr = fixdr.dfilter(x__eq=1)
    assert len(filtdr) == 1
    assert filtdr[0] == {'x': 1, 'y': 2}


def test_dfilter_implicit_eq(fixdr):
    filtdr = fixdr.dfilter(x=1)
    assert len(filtdr) == 1
    assert filtdr[0] == {'x': 1, 'y': 2}


def test_dfilter_ne(fixdr):
    filtdr = fixdr.dfilter(x__ne=3)
    assert len(filtdr) == 1
    assert filtdr[0] == {'x': 1, 'y': 2}
    filtdr = fixdr.dfilter(x__ne=5)
    assert len(filtdr) == 2
    assert filtdr[0] == fixdr[0]
    assert filtdr[1] == fixdr[1]


def test_dfilter_in(fixdrmult):
    filtdr = fixdrmult.dfilter(x__in=1)
    assert len(filtdr) == 1
    assert filtdr[0] == {'x': set([1, 3]), 'y': 2}
    filtdr = fixdrmult.dfilter(x__in=3)
    assert len(filtdr) == 2
    assert filtdr[0] == fixdrmult[0]
    assert filtdr[1] == fixdrmult[1]


def test_dfilter_nin(fixdrmult):
    filtdr = fixdrmult.dfilter(x__nin=3)
    assert len(filtdr) == 0
    filtdr = fixdrmult.dfilter(x__nin=1)
    assert len(filtdr) == 1
    assert filtdr[0] == {'x': 3, 'y': 4}


def test_dfilter_iskey(fixdr):
    filtdr = fixdr.dfilter(x__iskey=True)
    assert len(filtdr) == 2
    assert filtdr[0] == fixdr[0]
    assert filtdr[1] == fixdr[1]


def test_chain_filter(fixdr):
    filtdr = fixdr.dfilter(x__eq=1).dfilter(y__eq=2)
    assert len(filtdr) == 1
    assert filtdr[0] == fixdr[0]


def test_multiple_filter(fixdr):
    filtdr = fixdr.dfilter(x__eq=1, y__eq=2)
    assert len(filtdr) == 1
    assert filtdr[0] == fixdr[0]


def test_dget_eq(fixdr):
    elem = fixdr.dget(x__eq=1)
    assert elem == {'x': 1, 'y': 2}
    with pytest.raises(IndexError):
        elem == fixdr.dget(x__eq=7)


def test_dpop_eq(fixdr):
    elem = fixdr.dpop(x__eq=1)
    assert elem == {'x': 1, 'y': 2}
    assert len(fixdr) == 1
    assert fixdr[0] == {'x': 3, 'y': 4}
    with pytest.raises(IndexError):
        elem == fixdr.dpop(x__eq=7)


def test_dremove_iskey(fixdr):
    filtdr = fixdr.dremove(x__iskey=True)
    assert len(filtdr) == 2
    assert len(fixdr) == 0


def test_dremove_copy_iskey(fixdr):
    filtdr = fixdr.dremove_copy(x__iskey=True)
    assert len(filtdr) == 0
    assert len(fixdr) == 2
