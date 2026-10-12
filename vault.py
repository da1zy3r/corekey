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

def add_password(master_password: str, service: str) -> str:
    file = open('./vault.json', 'r+', encoding='utf-8')
    vault = json.load(file)
    key = derive_key(master_password.encode(),
                     decode_base64(vault['kdf']['salt']),
                     vault['kdf']['time_cost'],
                     vault['kdf']['memory_cost'],
                     vault['kdf']['parallelism'],
                     vault['kdf']['hash_len'])
    nonce = vault['encryption']['nonce']
    plaintext = decrypt(decode_base64(vault['ciphertext']), key, decode_base64(nonce))
    entries = json.loads(plaintext)
    if service in entries['entries']:
        file.close()
        return "Password for '{}' already exists".format(service)
    password_options = {}
    while True:
        password_length = input('Password length [20]: ').strip()
        if not password_length:
            break
        if password_length.isdigit():
            if int(password_length) >= 8:
                password_options['length'] = int(password_length)
                break
            else:
                print('Password length must be at least 8')
        else:
            print('Password length must be a positive integer')
    include_digits = ask_yes_no('Include digits? [Y/n]: ', True)
    password_options['include_digits'] = include_digits
    include_special_chars = ask_yes_no('Include special chars? [Y/n]: ', True)
    password_options['include_special_chars'] = include_special_chars
    if include_special_chars:
        special_chars = input('Special chars [!@#$%^&*]: ').strip()
        if special_chars:
            password_options['special_chars'] = special_chars
    password = generate_password(**password_options)
    entries['entries'][service] = password
    plaintext = json.dumps(entries).encode('utf-8')
    new_nonce = generate_random_base64(12)
    vault['encryption']['nonce'] = new_nonce
    ciphertext = encrypt(plaintext, key, decode_base64(new_nonce))
    vault['ciphertext'] = encode_base64(ciphertext)
    file.seek(0)
    json.dump(vault, file, indent=4)
    file.truncate()
    file.close()
    return "Password for '{}' added".format(service)

def get_password(master_password: str, service: str) -> str:
    file = open('./vault.json', encoding='utf-8')
    vault = json.load(file)
    file.close()
    key = derive_key(master_password.encode(),
                     decode_base64(vault['kdf']['salt']),
                     vault['kdf']['time_cost'],
                     vault['kdf']['memory_cost'],
                     vault['kdf']['parallelism'],
                     vault['kdf']['hash_len'])
    nonce = vault['encryption']['nonce']
    plaintext = decrypt(decode_base64(vault['ciphertext']), key, decode_base64(nonce))
    entries = json.loads(plaintext)
    if service in entries['entries']:
        return entries['entries'][service]
    else:
        return "Password for '{}' not found".format(service)
