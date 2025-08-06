import pytest
from pathlib import Path
from aas_http_client.client import create_client_by_config, AasHttpClient

@pytest.fixture(scope="module")
def cloud_client() -> AasHttpClient:
    try:
        file = Path("./server_config.json")
        client = create_client_by_config(file, password="")
    except Exception as e:
        raise RuntimeError("Unable to connect to server.")

    return client

def test_001_connect(cloud_client: AasHttpClient):
    print("Testing connection to the server...")
    assert cloud_client is not None