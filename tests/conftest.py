from fakeriak import FakeRiakClient
import pytest

@pytest.yield_fixture
def fakeriak():
    riak = FakeRiakClient()
    yield riak