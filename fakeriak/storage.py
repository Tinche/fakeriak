"""Fake Riak in-memory storage logic."""
from collections import defaultdict
import uuid


class InMemoryStorage(object):
    """An in-memory, simple implementation of the Riak storage backend."""
    def __init__(self):
        self.bucket_types = set(['default'])
        self.buckets = defaultdict(dict)  # type: Mapping[Tuple[str, str], Mapping[str, RiakObject]]

    def put(self, robj):
        bucket = robj.bucket
        bucket_type = bucket.bucket_type
        bucket_name = bucket.name
        if not robj.key:
            robj.key = str(uuid.uuid4())
        obj_key = robj.key

        if bucket_type.name not in self.bucket_types:
            raise ValueError('Unknown bucket type: {}'.format(bucket_type))
        self.buckets[(bucket_type.name, bucket_name)][obj_key] = robj
        return robj

    def get(self, robj):
        bucket = robj.bucket
        bucket_type = bucket.bucket_type
        bucket_name = bucket.name
        obj_key = robj.key

        if bucket_type.name not in self.bucket_types:
            raise ValueError('Unknown bucket type: {}'.format(bucket_type))

        stored = self.buckets[(bucket_type.name, bucket_name)].get(obj_key)
        if stored:
            robj.content_type = stored.content_type
            robj.encoded_data = stored.encoded_data
            robj.siblings[0].exists = True

        return robj

    def delete(self, robj):
        bucket = robj.bucket
        bucket_type = bucket.bucket_type
        bucket_name = bucket.name
        obj_key = robj.key

        if bucket_type.name not in self.bucket_types:
            raise ValueError('Unknown bucket type: {}'.format(bucket_type))

        self.buckets[(bucket_type.name, bucket_name)].pop(obj_key, None)

        return robj
