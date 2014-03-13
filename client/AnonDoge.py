import requests

import Crypt, DB

from base64 import b64encode, b64decode

class AnonDoge:

    server = 'https://localhost:8443'

    def __init__(self):

        try:
            self.pubkey = open('.keys/pubkey', 'r').read().decode('utf-8')
            self.hashed_pubkey = Crypt.sha256(pubkey)
            self.privkey = open('.keys/privkey', 'r').read().decode('utf-8')
        except:
            self.pubkey, self.privkey = Crypt.generate_RSA()
            Crypt.write_RSA(self.pubkey, self.privkey)
            self.hashed_pubkey = Crypt.sha256(self.pubkey)

    def send(self, receiver, msg):

        data = Crypt.encrypt(self.pubkey, self.privkey, receiver, msg)

        r = requests.post(AnonDoge.server + '/api/msgs', data=data, verify=False)

        return r.json()

        # new keys instead of that two
        DB.save('hola', receiver, None, self.pubkey, self.privkey)

    def fetch(self):

        r = requests.get(AnonDoge.server + '/api/msgs', params = { 'hashed_pubkey': self.hashed_pubkey }, verify=False)

        msgs = r.json()['msgs']

        print('You have %d new messages' % (len(msgs)))

        # download them in received (threads?)
        for msg in msgs:
            msg, newpubkey = Crypt.decrypt(self.privkey, msg)

            DB.save('hola', newpubkey, msg, self.pubkey, self.privkey)


        print(DB.list())