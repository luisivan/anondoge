from cmd import Cmd
import shlex

import Crypt

pubkey = None
privkey = None

class AnonDogeShell(Cmd):
    intro = 'Welcome to AnonDoge. Type help or ? to list commands\n'
    prompt = '(doge) '    
    global pubkey
    global privkey

    try:
        pubkey = open('pubkey', 'r').read()
        privkey = open('privkey', 'r').read()
    except:
        keys = Crypt.generate_RSA()
        pubkey = keys[0].decode("utf-8")
        privkey = keys[1].decode("utf-8")

        pubkey = open('pubkey', 'w')
        pubkey.write(pubkey)
        pubkey.close()

        privkey = open('privkey', 'w')
        privkey.write(privkey)
        privkey.close()

    def do_pubkey(self, arg):
        "Print your pubkey"
        print(pubkey)

    def do_fetch(self, arg):
        'Turn turtle right by given number of degrees:  RIGHT 20'
        to = parse(arg)

        # http get

        isverified = Crypt.verify_sign(from_public_key, signature, encrypted)

        if isverified:
            decrypted_key = Crypt.decrypt_RSA(privkey, encrypted)
            decrypted_msg = Crypt.decrypt_AES(encrypted_msg, decrypted_key)
            print(decrypted_msg)

    def do_send(self, arg):
        'Encrypt a message, sign it and broadcast it to a pubkey'
        # file = parse(arg)[0]
        msg = open('msg.txt', 'r').read().split('-----END PUBLIC KEY-----')

        receiver = msg[0] + '-----END PUBLIC KEY-----'

        encrypted_msg, key = Crypt.encrypt_AES(msg[1].encode())
        encrypted = Crypt.encrypt_RSA(receiver, key)
        sign = Crypt.sign_data(privkey, encrypted)

        # http post that

        # move msg to sent as {timestamp}.txt

        print(sign)
        print(encrypted_msg)

    def do_bye(self, arg):
        'Close AnonDoge'
        print('Thank you for using AnonDoge')
        return True

def parse(arg):
    return shlex.split(arg)

if __name__ == '__main__':
    AnonDogeShell().cmdloop()