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

def write_RSA(pubkey, privkey):
    fpubkey = open('.keys/pubkey', 'wb')
    fpubkey.write(pubkey)
    fpubkey.close()

    fprivkey = open('.keys/privkey', 'wb')
    fprivkey.write(privkey)
    fprivkey.close()

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

def sha256(data):
    h = SHA256.new()
    h.update(data)
    return h.hexdigest()

def encrypt(pubkey, privkey, receiver_pubkey, msg):

    newkeys = generate_RSA()
    
    newpubkey = newkeys[0]
    msg = msg.encode()
    msg += pubkey + newpubkey

    encrypted_msg, key = encrypt_AES(msg)
    encrypted_key = encrypt_RSA(receiver_pubkey, key)
    signature = sign_data(privkey, encrypted_key)

    receiver = sha256(receiver_pubkey.encode())
    data = {
        'hashed_pubkey': receiver,
        'encrypted_key': encrypted_key,
        'encrypted_msg': b64encode(encrypted_msg),
        'signature': signature
    }

    # TODO: change to newkeys
    write_RSA(pubkey, privkey)

    return data

def decrypt(privkey, data):

    encrypted_key = data['encrypted_key']
    encrypted_msg = data['encrypted_msg']
    signature = data['signature']

    decrypted_key = decrypt_RSA(privkey, encrypted_key)
    decrypted_msg = decrypt_AES(b64decode(encrypted_msg), decrypted_key)

    divider = '-----BEGIN PUBLIC KEY-----'

    msg, oldpubkey, pubkey = str(decrypted_msg).split(divider)

    oldpubkey = (divider + oldpubkey).encode('utf_8').decode('unicode_escape')
    pubkey = (divider + pubkey).encode('utf_8').decode('unicode_escape')

    isverified = verify_sign(oldpubkey, signature, encrypted_key)

    if isverified:
        return msg, pubkey
    else:
        return False