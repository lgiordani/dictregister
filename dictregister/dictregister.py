#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import six

class DictRegister(list):
    def __init__(self, iterable=[]):
        """This class accepts an iterable of dictionary-like objects.
        If an element is not a dictionary-like object raises ValueError.
        """
        for elem in iterable:
            self._check_elem(elem)
        super(DictRegister, self).__init__(iterable)

    def _check_elem(self, elem):
        # Check if the given element is a dictionary-like object
        if not isinstance(elem, collections.Mapping):
            raise ValueError(
                "Given element %s is not a dictionary-like object" % (elem))

    def append(self, elem):
        self._check_elem(elem)
        super(DictRegister, self).append(elem)

    def kadd(self, key, value):
        """Adds the given key/value to all elements.
        Single values for a key are stored directly, as key:value, multiple
        values for the same key are stored as key,set(values).
        """
        for item in self:
            try:
                # Use the key as a set
                item[key].add(value)
            except KeyError:
                # This happens if the key is not present
                item[key] = value
            except AttributeError:
                # This happens if the key is present but is not a set
                item[key] = set([item[key], value])

    def kreplace(self, key, value):
        """Replaces the given key/value for each element.
        If the key is not present silently passes.
        """
        for item in self:
            if key in item:
                item[key] = value

    def kremove(self, key, value=None):
        """Removes the given key/value from all elements.
        If value is not specified, the whole key is removed.
        If value is not None and the key is present but with a
        different value, or if the key is not present, silently passes.
        """
        for item in self:
            if value is None:
                # Just pop the key if present,
                # otherwise return None
                # (shortcut to ignore the exception)
                item.pop(key, None)
            else:
                try:
                    # Use the key as a set
                    item[key].remove(value)
                    # If the set contains a single element
                    # just store the latter
                    if len(item[key]) == 1:
                        item[key] = item[key].pop()
                except KeyError:
                    # This happens when the item
                    # does not contain the key
                    pass
                except AttributeError:
                    # This happens when the key is not a set
                    # and shall be removed only if values match
                    if item[key] == value:
                        item.pop(key)

    def _match(self, item, keyop, value):
        # Split key and operator
        if '__' not in keyop:
            keyop = keyop + '__eq'
        key, op = keyop.split('__')

        if op == "eq":
            try:
                return item[key] == value
            except KeyError:
                return False
        elif op == "ne":
            try:
                return item[key] != value
            except KeyError:
                return True
        elif op == "in":
            try:
                if isinstance(item[key], collections.Iterable):
                    return value in item[key]
                else:
                    return item[key] == value
            except KeyError:
                return False
        elif op == "nin":
            try:
                if isinstance(item[key], collections.Iterable):
                    return value not in item[key]
                else:
                    return item[key] != value
            except KeyError:
                return True
        elif op == "iskey":
            return (key in item) == value
        else:
            return False

    def dfilter(self, **kwds):
        """Returns a DictRegister which contains only the
        elements that match the given specifications.
        """
        starting_list = self[:]
        filtered_list = []
        for key, value in six.iteritems(kwds):
            for item in starting_list:
                if self._match(item, key, value):
                    filtered_list.append(item)
            starting_list = filtered_list
            filtered_list = []
        return DictRegister(starting_list)

    def dget(self, **kwds):
        """Returns the first element that matches the
        given specification. If no elements are found
        raises IndexError.
        """
        return self.dfilter(**kwds)[0]

    def dpop(self, **kwds):
        """Pops and returns the first element that matches the
        given specification. If no elements are found
        raises IndexError.
        """
        item = self.dget(**kwds)
        self.remove(item)
        return item

    def dremove(self, **kwds):
        """Removes from the object any element that matches the
        given specification.
        """
        filtered_dr = self.dfilter(**kwds)
        for item in filtered_dr:
            self.remove(item)
        return filtered_dr

    def dremove_copy(self, **kwds):
        """Returns a copy of the object without any element that
        matches the given specification.
        """
        copy_dr = DictRegister(self)
        copy_dr.dremove(**kwds)
        return copy_dr
