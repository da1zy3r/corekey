import secrets
import base64
import string

from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_random_base64(length: int) -> str:
    random_bytes = secrets.token_bytes(length)
    return base64.b64encode(random_bytes).decode('ascii')

def decode_base64(s: str) -> bytes:
    return base64.b64decode(s)

def generate_password(
        length: int = 20,
        include_digits: bool = True,
        include_hash: bool = True,
        include_dollar: bool = True
) -> str:
    alphabet = string.ascii_letters
    if include_digits:
        alphabet += string.digits
    if include_hash:
        alphabet += '#'
    if include_dollar:
        alphabet += '$'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def encrypt(plaintext: bytes, key: bytes, nonce: bytes) -> bytes:
    aes = AESGCM(key)
    return aes.encrypt(nonce, plaintext, None)

def decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    aes = AESGCM(key)
    return aes.decrypt(nonce, ciphertext, None)

def derive_key(
        master_password: bytes,
        salt: bytes,
        time_cost: int,
        memory_cost: int,
        parallelism: int,
        hash_len: int
) -> bytes:
    return hash_secret_raw(
        secret=master_password,
        salt=salt,
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
        hash_len=hash_len,
        type=Type.ID
    )
