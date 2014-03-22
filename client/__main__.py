from cmd import Cmd
import shlex

from AnonDoge import AnonDoge

from base64 import b64encode, b64decode

doge = AnonDoge()

class AnonDogeShell(Cmd):
    intro = 'Welcome to AnonDoge. Type help or ? to list commands\n'
    prompt = '(doge) '

    #doge.fetch()

    def do_alias(self, arg):

        args = parse(arg)
        if len(args):
            alias = args[0]
            pubkey = doge.get_pubkey(alias)
            if pubkey:
                doge.set_receiver(pubkey)
                print('Now you can message %s' % alias)
            else:
                print('Alias %s does not exist' % alias)
        else:
            print('Your alias is %s' % doge.get_alias())

    def do_key(self, arg):

        print(doge.pubkey.decode())

    def do_fetch(self, arg):

        msgs = doge.fetch()
        n = len(msgs)

        print("%d new message%s" % (n, "s"[n==1:]))

        for i, msg in enumerate(msgs):

            file_divider = b'-----BEGIN FILE-----'

            if not file_divider in msg:
                print('#%d - %s' % (i+1, msg.decode()))
            else:
                msg = msg[msg.index(file_divider)+20:]

                f = open('blob', 'wb')
                f.write(msg)
                f.close()

    def do_send(self, arg):

        args = parse(arg)
        if len(args):
            msg = args[0]
        else:
            msg = 'Received.'

        if doge.send(msg.encode()):
            print('Message sent')

    def do_sendfile(self, arg):

        args = parse(arg)
        f = args[0]
        msg = open(f, 'rb').read()

        if doge.send(msg, True):
            print('File sent')

    def do_bye(self, arg):
        'Close AnonDoge'
        print('Thank you for using AnonDoge')
        return True

def parse(arg):
    return shlex.split(arg)

if __name__ == '__main__':
    try:
        AnonDogeShell().cmdloop()
    except KeyboardInterrupt:
        print('\n\nGoodbye!')
        exit()