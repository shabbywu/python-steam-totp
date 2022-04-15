import base64
import hashlib
import hmac
import json
import logging
import struct
from typing import Optional, Union
from urllib.request import urlopen

_CHARSET = "23456789BCDFGHJKMNPQRTVWXY"
_SYNC_URL = "https://api.steampowered.com:443/ITwoFactorService/QueryTime/v0001"


def _get_server_time():  # type: () -> int
    """Query timestamp in the Steam server
    :return: steam aligned timestamp
    """

    response = urlopen(_SYNC_URL, data=b"")
    response_content = response.read()
    logging.debug(
        "Sent request to '%s', and the recept response content is '%s'",
        _SYNC_URL,
        response_content,
    )
    data = json.loads(response_content)
    return int(data["response"]["server_time"])


def _hmac_sha1(secret, data):
    return hmac.new(secret, data, hashlib.sha1).digest()


def generate_twofactor_code_for_time(
    shared_secret,  # type: Union[bytes, str]
    timestamp=None,  # type: Optional[int]
):
    """Generate Steam 2FA code for timestamp
    :param shared_secret: authenticator shared secret
    :param timestamp: timestamp to use, if left out uses current time
    :return: steam two factor code
    """
    if timestamp is None:
        timestamp = _get_server_time()

    hmac = _hmac_sha1(base64.b64decode(shared_secret), struct.pack(b">Q", int(timestamp) // 30))

    start = ord(hmac[19:20]) & 0x0F
    codeint = struct.unpack(">I", hmac[start : start + 4])[0] & 0x7FFFFFFF

    code = []
    for _ in range(5):
        codeint, i = divmod(codeint, len(_CHARSET))
        code.append(_CHARSET[i])

    return "".join(code)


__ALL__ = ["generate_twofactor_code_for_time"]
