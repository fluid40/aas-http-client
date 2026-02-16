import pytest
from aas_http_client.utilities import encoder

def test_001a_decode_base_64():
    encoded = "RW5lcmd5TW9uaXRvcmluZw"

    decoded = encoder.decode_base_64(encoded)
    assert decoded == "EnergyMonitoring"
    new_encoded = encoder.encode_base_64(decoded)
    assert new_encoded == encoded + "=="


def test_001b_decode_base_64():
    encoded = "aHR0cHM6Ly9mbHVpZDQwLmRlL2lkcy9zbS8xNTE1XzUzMDZfNzYyNF81MzY3"

    decoded = encoder.decode_base_64(encoded)
    assert decoded == "https://fluid40.de/ids/sm/1515_5306_7624_5367"
    new_encoded = encoder.encode_base_64(decoded)
    assert new_encoded == encoded

def test_002a_encode_base_64():
    decoded = "EnergyMonitoring"

    encoded = encoder.encode_base_64(decoded)
    assert encoded == "RW5lcmd5TW9uaXRvcmluZw=="
    new_decoded = encoder.decode_base_64(encoded)
    assert new_decoded == decoded

def test_002b_encode_base_64():
    decoded = "https://fluid40.de/ids/sm/1515_5306_7624_5367"

    encoded = encoder.encode_base_64(decoded)
    assert encoded == "aHR0cHM6Ly9mbHVpZDQwLmRlL2lkcy9zbS8xNTE1XzUzMDZfNzYyNF81MzY3"
    new_decoded = encoder.decode_base_64(encoded)
    assert new_decoded == decoded
