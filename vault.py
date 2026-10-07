import json

from utils import *

def init_vault(
        master_password: str,
        time_cost: int = 3,
        memory_cost: int = 2 ** 16,
        parallelism: int = 4,
        hash_len: int = 32
) -> None:
    vault = {
        'kdf': {
            'algorithm': 'argon2id',
            'salt': '',
            'time_cost': time_cost,
            'memory_cost': memory_cost,
            'parallelism': parallelism,
            'hash_len': hash_len
        },
        'encryption': {
            'algorithm': 'aes-gcm',
            'nonce': ''
        },
        'ciphertext': ''
    }
    salt = generate_random_base64(16)
    nonce = generate_random_base64(12)
    vault['kdf']['salt'] = salt
    vault['encryption']['nonce'] = nonce
    key = derive_key(master_password.encode(),
                     decode_base64(salt),
                     time_cost,
                     memory_cost,
                     parallelism,
                     hash_len)
    entries = {'entries': {}}
    plaintext = json.dumps(entries).encode('utf-8')
    ciphertext = encrypt(plaintext, key, decode_base64(nonce))
    vault['ciphertext'] = encode_base64(ciphertext)
    file = open('./vault.json', 'w', encoding='utf-8')
    json.dump(vault, file, indent=4)
    file.close()
