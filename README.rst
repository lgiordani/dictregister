DictRegister
============

|Build Status| |Version| |PyPi Downloads|

Documentation
-------------

`dictregister
documentation <https://dictregister.readthedocs.org/en/latest/>`__

**dictregister** provides an object that contains an ordered list of
dictionaries with some functions to search and manage them.

Dictionaries are useful objects, as they can easily represent complex
objects; being a basic language structure in Python they are very handy:
as an instance, they are serialiable, and if you ever worked with JSON
you are accustomed to see them around.

When dealing with more than one dictionary, namely a list of them, a
problem arises: searching the list for dictionaries is complex and you
usually write a bunch of repeated code to get the information you need.

**dictregister** acts as a standard Python list but can contain only
dictionaries (actually objects implementing collections.Mapping);
additionally, it provides functions to search and manage dictionaries by
key, to manage single keys and to store more than one value for each
key.

**dictregister** is a pure Python package, but its syntax has been
heavily influenced by Django's query syntax, so Django users will find
at home.

Indeed, **dictregister** acts like a small key/value database. Please
note that there it stores values in memory and there is no optimization,
so use it for small collections.

Basic usage
-----------

The ``DictRegister`` object acts as a ``list``, so you can either
initialize it empty

.. code:: python

    import dictregister
    dr = dictregister.DictRegister()

or with an iterable object as an argument

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}])

and you can use any method of ``list`` like ``append()``

.. code:: python

    import dictregister
    dr = dictregister.DictRegister()
    dr.append({'x':1, 'y':2})

``DictRegister`` accepts only objects that inherit fromt the
``collections.Mapping`` Abstract Base Class. If you try to insert an
object that does not stick with this rule you will receive a
``ValueError``.

Managing keys
-------------

You can manage keys in batch mode with ``kadd()``, ``kreplace()``, and
``kremove()``.

Adding a key to each element is easy with ``kadd()``

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}])
    dr == [{'x':1, 'y':2}, {'x':3, 'y':4}]
    dr.kadd('z', 5)
    dr == [{'x':1, 'y':2, 'z':5}, {'x':3, 'y':4, 'z':5}]

Please note that if you add more than a value to the same key you get a
multiple-value element, which is treated in a special way. See the
Multiple values section below.

When you remove keys you can do it unconditionally

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}])
    dr == [{'x':1, 'y':2}, {'x':3, 'y':4}]
    dr.kremove('y')
    dr == [{'x':1}, {'x':3}]

which removes all keys with that name. or you can specify a value, in
which case only the elments that match both the key and the value will
be removed.

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}])
    dr == [{'x':1, 'y':2}, {'x':3, 'y':4}]
    dr.kremove('y',4)
    dr == [{'x':1, 'y':2}, {'x':3}]

Last, you can replace the value of a key

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}])
    dr == [{'x':1, 'y':2}, {'x':3, 'y':4}]
    dr.kreplace('x',6)
    dr == [{'x':6, 'y':2}, {'x':6, 'y':4}]

Advanced usage
--------------

You can find a subset of dictionaries using ``dfilter()``

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}])
    filtdr = dr.dfilter(x=1)
    filtdr == [{'x':1, 'y':2}]

You can pass as many conditions as you want to ``dfilter()``

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}, {'x':1, 'y':6}])
    filtdr = dr.dfilter(x=1)
    filtdr == [{'x':1, 'y':2}, {'x':1, 'y':6}]
    filtdr = dr.dfilter(x=1, y=2)
    filtdr == [{'x':1, 'y':2}]

You can easily get only the first element of the filtering with
``dget()``. Remember that while ``dfilter()`` silently accepts a search
that returns no values, returning an empty ``DictRegister``, ``dget()``
raises an ``IndexError`` exception.

You can remove elements from a ``DictRegister`` object with
``dremove()``, which returns a ``DictRegister`` containing the removed
elements.

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}, {'x':1, 'y':6}])
    filtdr = dr.dremove(x=1)
    dr == [{'x':3, 'y':4}]
    filtdr == [{'x':1, 'y':2}, {'x':1, 'y':6}]

Otherwise you obtain a new object with the elements removed
``dremove_copy()``

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}, {'x':1, 'y':6}])
    filtdr = dr.dremove_copy(x=1)
    dr == [{'x':1, 'y':2}, {'x':3, 'y':4}, {'x':1, 'y':6}]
    filtdr == [{'x':3, 'y':4}]

Last you can pop an element with ``dpop()``, which returns the first
element matching the given conditions. Remember that ``dpop()`` raises
``IndexError`` if no matching element is found.

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}, {'x':1, 'y':6}])
    filtdr = dr.dpop(x=1)
    dr == [{'x':3, 'y':4}, {'x':1, 'y':6}]

Remember that, being a list, ``DictRegister`` also provides you a
``pop([i])`` method that pops the element at index ``i`` or the first
element if ``i`` is not specified.

Note that ``dfilter()``, ``dremove()``, and ``dremove_copy()`` return a
``DictRegister`` so you can easily chain calls.

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}, {'x':1, 'y':6}])
    filtdr = dr.dfilter(x=1).dremove_copy(y=2)
    dr == [{'x':1, 'y':2}, {'x':3, 'y':4}, {'x':1, 'y':6}]
    filtdr == [{'x':1, 'y':6}]

Matching elements
-----------------

When using the advanced features of ``DictRegister`` like filtering you
can use a special syntax for keys, namely a ``key__operator`` syntax.

The implicit operator is ``eq``, which matches all dictionaries with the
given key with the given value.

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}, {'x':1, 'y':6}])
    filtdr = dr.dfilter(x__eq=3)
    filtdr == [{'x':3, 'y':4}]
    filtdr = dr.dfilter(x=3)
    filtdr == [{'x':3, 'y':4}]

The inequality can be matched with ``ne``

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}, {'x':1, 'y':6}])
    filtdr = dr.dfilter(x__ne=1)
    filtdr == [{'x':3, 'y':4}]

You can match dictionaries that contain or not a given key

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}, {'x':1, 'y':6, 'z':8}])
    filtdr = dr.dfilter(z__iskey=True)
    filtdr == [{'x':1, 'y':6, 'z':8}]
    filtdr = dr.dfilter(z__iskey=False)
    filtdr == [{'x':1, 'y':2}, {'x':3, 'y':4}]

Multiple values
---------------

The ``DictRegister`` object can contain any dictionary with a single
value for each key, like

.. code:: python

    import dictregister
    dr = dictregister.DictRegister()
    dr.append({'x':1, 'y':2})

If you store more than a value for a key, ``DictRegister`` uses a set to
host the values. You are free to append dictionaries with generic
sequences, most notably lists and sets, as values. However remeber that
``DictRegister`` does not consider the sequence itself as the value of
the key, but the contained elements; so if you need to store a sequence
as a value you have to store a ``set`` that contains the sequence.

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':1, 'y':2}, {'x':3, 'y':4}])
    dr == [{'x':1, 'y':2}, {'x':3, 'y':4}]
    dr.kadd('x', 2)
    dr == [{'x':set([1, 2]), 'y':2}, {'x':set([2, 3]), 'y':4}]

You can match multiple values with the ``in`` and ``nin`` operators. The
first matches all dictionaries that contain the given key with the given
value among its values, while ``nin`` performs the opposite match.

.. code:: python

    import dictregister
    dr = dictregister.DictRegister([{'x':set([1, 2]), 'y':2}, {'x':2, 'y':4}])
    filtdr = dr.dfilter(x__in=2)
    filtdr == [{'x':set([1, 2]), 'y':2}, {'x':2, 'y':4}]

As you can see ``DictRegister`` treats keys with a single value and with
multiple values in the same way.

Installation
------------

.. code:: sh

    pip install dictregister

Contributions
-------------

Any form of contribution is warmly welcomed. Feel free to submit issues
of to make changes and submit a pull request. being the first Python
package I ship with all the bells and whistles like distutils, tests and
friends, I gladly accept suggestions or corrections on this topic.

Thanks
------

Many thanks to `Jeff Knupp <http://www.jeffknupp.com/about-me/>`__ for
his post `Open Sourcing a Python Project the Right
Way <http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/>`__.

Many thanks to `Audrey M. Roy <http://www.audreymroy.com/>`__ for her
`cookiecutter <https://github.com/audreyr/cookiecutter>`__ and
`cookiecutter-pypackage <https://github.com/audreyr/cookiecutter-pypackage>`__
tools, which heavily simplified the implementation of the whole thing.

.. |Build Status| image:: https://travis-ci.org/lgiordani/dictregister.png?branch=master
   :target: https://travis-ci.org/lgiordani/dictregister
.. |Version| image:: https://badge.fury.io/py/dictregister.png
   :target: http://badge.fury.io/py/dictregister
.. |PyPi Downloads| image:: https://pypip.in/d/dictregister/badge.png
   :target: https://crate.io/packages/dictregister?version=latest
