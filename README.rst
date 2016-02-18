Fakeriak: a fake Riak client for testing
==================================

.. image:: https://img.shields.io/pypi/v/fakeriak.svg
    :target: https://pypi.python.org/pypi/fakeriak
.. image:: https://travis-ci.org/Tinche/fakeriak.svg?branch=master
    :target: https://travis-ci.org/Tinche/fakeriak
.. image:: https://coveralls.io/repos/Tinche/fakeriak/badge.svg?branch=master
    :target: https://coveralls.io/r/Tinche/fakeriak?branch=master

Fakeriak is an Apache2 licensed library, written in Python, for testing code
that uses the Python Riak client.

A Fakeriak client contains a very simple, in-memory storage backend. An
ordinary Riak client can simply be replaced with a Fakeriak client during unit
testing, thus enabling the testing of components that depend on Riak.


.. code-block:: python

    test_payload = b'test'

    riak_client = FakeRiakClient()
    obj = riak_client.bucket('default').new(content_type='binary/octet-stream')
    obj.data = test_payload
    obj.store()

    assert riak_client.bucket('default').get(obj.key).data == test_payload


Features
--------

- only default, simple buckets
- ``RiakBucket.new``, ``RiakBucket.get``, ``RiakBucket.delete``,
``RiakBucket.multiget``
- ``RiakObject.store()``, ``RiakObject.delete()``, ``RiakObject.exists``
- no concurrency (sibling) support

Installation
------------

To install Fakeriak (preferably in a virtualenv), simply:

.. code-block:: bash

    $ pip install fakeriak


Contributing
~~~~~~~~~~~~
Contributions are very welcome. Tests can be run with ``tox``, please ensure
the coverage at least stays the same before you submit a pull request.

