# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

from __future__ import absolute_import, division, print_function

import os

from cryptography import exceptions, utils
from cryptography.hazmat.backends.openssl import aead
from cryptography.hazmat.backends.openssl.backend import backend


class ChaCha20Poly1305(object):
    def __init__(self, key):
        if not backend.aead_cipher_supported(self):
            raise exceptions.UnsupportedAlgorithm(
                "ChaCha20Poly1305 is not supported by this version of OpenSSL",
                exceptions._Reasons.UNSUPPORTED_CIPHER
            )
        utils._check_bytes("key", key)

        if len(key) != 32:
            raise ValueError("ChaCha20Poly1305 key must be 32 bytes.")

        self._key = key

    @classmethod
    def generate_key(cls):
        return os.urandom(32)

    def encrypt(self, nonce, data, associated_data):
        if associated_data is None:
            associated_data = b""

        self._check_params(nonce, data, associated_data)
        return aead._encrypt(
            backend, self, nonce, data, associated_data, 16
        )

    def decrypt(self, nonce, data, associated_data):
        if associated_data is None:
            associated_data = b""

        self._check_params(nonce, data, associated_data)
        return aead._decrypt(
            backend, self, nonce, data, associated_data, 16
        )

    def _check_params(self, nonce, data, associated_data):
        utils._check_bytes("nonce", nonce)
        utils._check_bytes("data", data)
        utils._check_bytes("associated_data", associated_data)
        if len(nonce) != 12:
            raise ValueError("Nonce must be 12 bytes")
