#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dictregister
----------------------------------

Tests for `dictregister` module.
"""

import pytest

from dictregister import dictregister as dr

@pytest.fixture
def fixdr():
    return dr.DictRegister([{'x':1,'y':2},{'x':3,'y':4}])

@pytest.fixture
def fixdrmult():
    return dr.DictRegister([{'x':set([1,3]),'y':2},{'x':3,'y':4}])

def test_instance_without_parameters():
    d = dr.DictRegister()

def test_instance_with_a_list_of_dicts(fixdr):
    assert len(fixdr) == 2

def test_can_be_indexed(fixdr):
    assert fixdr[0] == {'x':1,'y':2}

def test_instance_with_an_argument():
    with pytest.raises(ValueError):
        d = dr.DictRegister([1,2,3])

def test_append_dict(fixdr):
    fixdr.append({'x':4,'y':5})
    assert len(fixdr) == 3

def test_cannot_append_non_dict(fixdr):
    with pytest.raises(ValueError):
        fixdr.append(6)

def test_add_keyword(fixdr):
    fixdr.kadd('z', 3)
    assert len(fixdr) == 2
    assert fixdr[0] == {'x':1,'y':2,'z':3}

def test_add_already_present_keyword(fixdr):
    fixdr.kadd('x', 3)
    assert len(fixdr) == 2
    assert fixdr[0] == {'x': set([1,3]),'y':2}
    
def test_replace_already_present_keyword(fixdr):
    fixdr.kreplace('x', 3)
    assert len(fixdr) == 2
    assert fixdr[0] == {'x': 3,'y':2}

def test_replace_not_present_keyword(fixdr):
    fixdr.kreplace('z', 3)
    assert len(fixdr) == 2
    assert fixdr[0] == {'x': 1,'y':2}

def test_remove_keyword(fixdr):
    fixdr.kremove('x')
    assert len(fixdr) == 2
    assert fixdr[0] == {'y':2}
    assert fixdr[1] == {'y':4}

def test_remove_keyword_with_multiple_values(fixdrmult):
    fixdrmult.kremove('x',3)
    assert len(fixdrmult) == 2
    assert fixdrmult[0] == {'x':1,'y':2}
    assert fixdrmult[1] == {'y':4}

def test_remove_not_present_keyword(fixdr):
    fixdr.kremove('z')
    assert len(fixdr) == 2
    assert fixdr[0] == {'x':1,'y':2}
    assert fixdr[1] == {'x':3,'y':4}


