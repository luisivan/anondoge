from cmd import Cmd
import os
import shlex
import tempfile
import random

from AnonDoge import AnonDoge

doge = AnonDoge()

class AnonDogeShell(Cmd):
    intro = 'Welcome to AnonDoge. Type help or ? to list commands\n'
    prompt = '(doge) '

    def do_image(self, arg):
        'Create an image with your pubkey or get someone pubkey by an image'

        args = parse(arg)
        if len(args):
            f = args[0]
            pubkey = doge.decode_img(f)
            if pubkey:
                doge.set_receiver(pubkey)
                print('Pubkey successfully imported')
            else:
                print('Failed to import pubkey from image')
        else:
            doge.encode_img(doge.pubkey.decode())
            print('Pubkey successfully exported')

    def do_alias(self, arg):
        'Get a new alias for you or set your receiver to an alias'

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
        'Print your public key'

        print(doge.pubkey.decode())

    def do_fetch(self, arg):
        'Fetch all the messages sent to you'

        msgs = doge.fetch()
        n = len(msgs)

        print("%d new message%s" % (n, "s"[n==1:]))

        for i, msg in enumerate(msgs):

            file_divider = b'-----BEGIN FILE-----'

            if not file_divider in msg:
                print('#%d - %s' % (i+1, msg.decode()))
            else:
                msg = msg[msg.index(file_divider)+20:]

                f, pathname = tempfile.mkstemp()
                os.write(f, msg)
                os.close(f)
                print('file://'+pathname)

    def do_send(self, arg):
        'Send a plain-text message'

        args = parse(arg)
        if len(args):
            msg = args[0]
        else:
            msg = 'Received.'

        if doge.send(msg.encode()):
            print('Message sent')

    def do_sendfile(self, arg):
        'Send a file from your filesystem'

        args = parse(arg)
        f = args[0]
        msg = open(f, 'rb').read()

        if doge.send(msg, True):
            print('File sent')

    def do_bye(self, arg):
        'Close AnonDoge'

        print('Thank you for using AnonDoge')
        return True

    def emptyline(self):
        doge = ['such command line', 'much crypto', 'very secure', 'much hacker', 'so fuck NSA', 'wow freedom', 'many messages', 'such communication', 'many keys']
        print(random.choice(doge))

def parse(arg):
    return shlex.split(arg)

if __name__ == '__main__':
    try:
        AnonDogeShell().precmd('fetch')
        AnonDogeShell().cmdloop()
    except KeyboardInterrupt:
        print('\n\nGoodbye!')
        exit()