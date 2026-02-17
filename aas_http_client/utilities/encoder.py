"""Encoder module.

Provides some helper methods for base 64 encoding.
"""

import base64


def decode_base_64(text: str) -> str:
    """Decode a Base64 encoded string.

    :param text: Base64 encoded string to decode
    :return:  Decoded string
    """
    missing_padding = len(text) % 4
    if missing_padding:
        text += "=" * (4 - missing_padding)

    decoded = base64.urlsafe_b64decode(text)
    return decoded.decode("utf-8")


def encode_base_64(text: str) -> str:
    """Encode a string to Base64.

    :param text: String to encode
    :return: Base64 encoded string
    """
    encoded_bytes = base64.urlsafe_b64encode(text.encode("utf-8")).rstrip(b"=")
    return encoded_bytes.decode("utf-8")
