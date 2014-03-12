from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256 
from base64 import b64encode, b64decode 

def generate_RSA(bits=2048):
    new_key = RSA.generate(bits, e=65537) 
    public_key = new_key.publickey().exportKey("PEM") 
    private_key = new_key.exportKey("PEM") 
    return public_key, private_key

def encrypt_RSA(public_key, message):
    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted = rsakey.encrypt(message)
    return b64encode(encrypted)

def decrypt_RSA(private_key, package):
    rsakey = RSA.importKey(private_key) 
    rsakey = PKCS1_OAEP.new(rsakey) 
    decrypted = rsakey.decrypt(b64decode(package)) 
    return decrypted

def sign_data(private_key, data):
    rsakey = RSA.importKey(private_key) 
    signer = PKCS1_v1_5.new(rsakey) 
    digest = SHA256.new() 
    digest.update(b64decode(data)) 
    sign = signer.sign(digest) 
    return b64encode(sign)

def verify_sign(public_key, signature, data):
    rsakey = RSA.importKey(public_key) 
    signer = PKCS1_v1_5.new(rsakey) 
    digest = SHA256.new() 
    digest.update(b64decode(data)) 
    if signer.verify(digest, b64decode(signature)):
        return True
    return False

def encrypt_AES(message, key=None, key_size=256):
    def pad(s):
        x = AES.block_size - len(s) % AES.block_size
        return s + (bytes([x]) * x)
 
    padded_message = pad(message)
 
    if key is None:
        key = Random.OSRNG.posix.new().read(key_size // 8)
 
    iv = Random.OSRNG.posix.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
 
    return (iv + cipher.encrypt(padded_message), key)

def decrypt_AES(ciphertext, key):
    unpad = lambda s: s[:-s[-1]]
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))[AES.block_size:]
 
    return plaintext