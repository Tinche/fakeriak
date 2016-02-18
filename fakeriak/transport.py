"""Fake Riak transport."""

class InMemoryTransport(object):
    def __init__(self, storage):
        self._storage = storage

    def put(self, robj, w=None, dw=None, pw=None, return_body=None,
            if_none_match=None, timeout=None):
        return self._storage.put(robj)

    def get(self, robj, r=None, pr=None, timeout=None, basic_quorum=None,
            notfound_ok=None):
        return self._storage.get(robj)

    def delete(self, robj, rw=None, r=None, w=None, dw=None, pr=None, pw=None,
               timeout=None):
        return self._storage.delete(robj)


class InMemoryPool(object):
    def __init__(self, storage):
        self._storage = storage

    def transaction(self, *args, **kwargs):
        return self

    def __enter__(self):
        return InMemoryTransport(self._storage)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
