import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from config import PRIVATE_KEY


async def decrypt(encrypted_data: str):
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
