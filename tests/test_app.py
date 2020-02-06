import os
import tempfile

import pytest

from testing_app import create_app


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_root_route(client):
    rv = client.get('/')
    assert b'Hey' in rv.data
