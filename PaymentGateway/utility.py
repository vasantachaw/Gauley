import hmac
import hashlib
import base64

def generate_signature(secret, message):
    secret = secret.encode('utf-8')
    message = message.encode('utf-8')
    hmac_sha256 = hmac.new(secret, message, hashlib.sha256)
    digest = hmac_sha256.digest()
    return base64.b64encode(digest).decode('utf-8')