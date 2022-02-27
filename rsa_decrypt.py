import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from config import PRIVATE_KEY


def decrypt(encrypted_data: str):
    decrypted_text = ''
    try:
        key = RSA.importKey(PRIVATE_KEY)
        key = PKCS1_OAEP.new(key)
        decoded_data = base64.b64decode(encrypted_data)
        decrypted_text = key.decrypt(decoded_data).decode('utf-8')
    except:
        decrypted_text = 'decryption error'

    print(decrypted_text)
    return decrypted_text


def encode(data: str):
    new_data = data.encode('utf-8')
    base64_bytes = base64.b64encode(new_data)
    base64_message = base64_bytes.decode('utf-8')
    print(f'encode {data} -> {base64_message}')

    return base64_message
