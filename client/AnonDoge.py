import requests
from base64 import b64encode, b64decode

import Crypt

class AnonDoge:

    server = 'https://localhost:8443'

    def __init__(self):
        try:
            self.pubkey = open('.pubkey', 'r').read().encode()
            self.hashed_pubkey = Crypt.sha256(self.pubkey)
            self.privkey = open('.privkey', 'r').read().encode()
        except IOError:
            self.pubkey, self.privkey = Crypt.generate_RSA()
            Crypt.write_RSA(self.pubkey, self.privkey)
            self.hashed_pubkey = Crypt.sha256(self.pubkey)

    def get_receiver(self):

        return open('.receiver', 'r').read()

    def set_receiver(self, pubkey):

        f = open('.receiver', 'w')
        f.write(pubkey)
        f.close()

    def save_msg(self, msg):

        f = open('received.txt', 'w')
        f.write(msg)
        f.close()

    def get_alias(self):

        r = requests.post(AnonDoge.server + '/api/alias', data= { 'pubkey': self.pubkey }, verify=False)

        alias = r.json()['alias']

        return alias

    def get_pubkey(self, alias):

        r = requests.get(AnonDoge.server + '/api/alias', params = { 'alias': alias }, verify=False)

        pubkey = r.json()['pubkey']

        return pubkey

    def send(self, msg, is_file=False):

        data, newpubkey, newprivkey = Crypt.encrypt(self.pubkey, self.privkey, self.get_receiver(), msg, is_file)

        r = requests.post(AnonDoge.server + '/api/msgs', data=data, verify=False)

        Crypt.write_RSA(newpubkey, newprivkey)
        self.pubkey = newpubkey
        self.hashed_pubkey = Crypt.sha256(newpubkey)
        self.privkey = newprivkey

        return r.json()

    def fetch(self):

        r = requests.get(AnonDoge.server + '/api/msgs', params = { 'hashed_pubkey': self.hashed_pubkey }, verify=False)

        msgs = r.json()['msgs']

        arr = list()
        for msg in msgs:
            try:
                msg, newpubkey = Crypt.decrypt(self.privkey, msg)
                arr.append(msg)
                self.set_receiver(newpubkey)

            except:
                return 'Incorrect decryption'

        return arr