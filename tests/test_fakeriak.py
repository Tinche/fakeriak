"""Pytest tests for fake Riak."""
from collections import namedtuple
from fakeriak import FakeRiakClient
from hypothesis import given
from hypothesis.stateful import RuleBasedStateMachine, Bundle, rule
from hypothesis.strategies import binary, text, dictionaries


@given(binary())
def test_simple_bucket_binary(fakeriak, payload):
    """Binary payloads."""
    bucket = fakeriak.bucket('default')

    riak_obj = bucket.new(content_type='binary/octet-stream')

    assert riak_obj

    riak_obj.data = payload
    riak_obj.store()
    assert riak_obj.data == payload

    fresh = bucket.get(riak_obj.key)
    assert fresh.data == payload

    fresh_through_client = fakeriak.get(riak_obj)
    assert fresh_through_client.data == payload


@given(binary())
def test_simple_binary(fakeriak, payload):
    """Binary payloads."""
    bucket = fakeriak.bucket('default')

    riak_obj = bucket.new(content_type='binary/octet-stream')

    assert riak_obj

    riak_obj.data = payload
    fakeriak.put(riak_obj)
    assert riak_obj.data == payload

    fresh = bucket.get(riak_obj.key)
    assert fresh.data == payload

    fresh_through_client = fakeriak.get(riak_obj)
    assert fresh_through_client.data == payload


RiakAndDict = namedtuple('RiakAndDict', ('riak', 'dict'))


class OpsTest(RuleBasedStateMachine):
    """Test fake Riak objects using a simple dict model."""
    states = Bundle('RiakAndDicts')

    @rule(target=states)
    def create(self):
        return RiakAndDict(FakeRiakClient(), {})

    @rule(state=states, key=text(min_size=1), payload=binary())
    def insert_object_binary(self, state, key, payload):
        riak, dict = state
        bucket = riak.bucket('default')
        riak_obj = bucket.new(key=key, content_type='binary/octet-stream')
        riak_obj.data = payload
        riak_obj.store()
        assert riak.bucket('default').get(key).exists
        assert riak.bucket('default').get(key).data == payload
        dict[key] = payload

    @rule(state=states, key=text(min_size=1),
          payload=dictionaries(keys=text(), values=text()))
    def insert_object_dict(self, state, key, payload):
        riak, dict = state
        bucket = riak.bucket('default')
        riak_obj = bucket.new(key=key)
        riak_obj.data = payload
        riak_obj.store()
        assert riak.bucket('default').get(key).exists
        assert riak.bucket('default').get(key).data == payload
        dict[key] = payload

    @rule(state=states, key=text(min_size=1))
    def delete_object_bucket(self, state, key):
        riak, dict = state
        if dict.pop(key, None):
            assert riak.bucket('default').get(key).exists
        robj = riak.bucket('default').delete(key)
        assert not robj.exists
        assert not riak.bucket('default').get(key).exists

    @rule(state=states, key=text(min_size=1))
    def delete_object_object(self, state, key):
        """Delete an object using RiakObject.delete()."""
        riak, dict = state
        if dict.pop(key, None):
            assert riak.bucket('default').get(key).exists
        robj = riak.bucket('default').get(key)
        robj.delete()
        assert not robj.exists
        assert not riak.bucket('default').get(key).exists

    @rule(state=states)
    def check_state_via_dict(self, state):
        riak, dict = state
        bucket = riak.bucket('default')
        for key in dict:
            assert bucket.get(key).exists
            assert bucket.get(key).data == dict[key]

    @rule(state=states)
    def test_multiget(self, state):
        riak, dict = state
        keys = [('default', 'default', key) for key in dict]
        results = riak.multiget(keys)
        for key_result in zip(keys, results):
            assert dict[key_result[0][2]] == key_result[1].data


SimpleOpsTest = OpsTest.TestCase
