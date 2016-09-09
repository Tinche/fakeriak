from riak.client import (binary_encoder_decoder, binary_json_decoder,
                         binary_json_encoder, bytes_to_str, str_to_bytes)
from weakref import WeakValueDictionary

from riak import RiakClient

from .storage import InMemoryStorage
from .transport import InMemoryPool


class FakeRiakClient(RiakClient):

    def __init__(self, multiget_pool_size=None, **unused_kwargs):
        self._encoders = {'application/json': binary_json_encoder,
                          'text/json': binary_json_encoder,
                          'text/plain': str_to_bytes,
                          'binary/octet-stream': binary_encoder_decoder}
        self._decoders = {'application/json': binary_json_decoder,
                          'text/json': binary_json_decoder,
                          'text/plain': bytes_to_str,
                          'binary/octet-stream': binary_encoder_decoder}
        self._multiget_pool_size = multiget_pool_size
        self._pool = InMemoryPool(InMemoryStorage())
        self._buckets = WeakValueDictionary()
        self._bucket_types = WeakValueDictionary()

    def _choose_pool(self, protocol=None):
        return self._pool

    def __hash__(self):
        return id(self)

    def close(self):
        """Do nothing.

        This is called from the finalizer, so we override it.
        """
        pass
