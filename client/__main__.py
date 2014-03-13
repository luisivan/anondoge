from cmd import Cmd
import shlex

from AnonDoge import AnonDoge

from base64 import b64encode, b64decode

doge = AnonDoge()

class AnonDogeShell(Cmd):
    intro = 'Welcome to AnonDoge. Type help or ? to list commands\n'
    prompt = '(doge) '

    def do_key(self, arg):

        print(doge.pubkey.decode())

    def do_fetch(self, arg):

        print(doge.fetch())

    def do_list(self, arg):

        print(doge.fetch())

    def do_send(self, arg):

        receiver = open('.receiver', 'r').read()

        string = parse(arg)[0]
        print(string)
        if string:
            msg = string

        print(doge.send(receiver, msg))

        # move msg to sent as {timestamp}.txt

    def do_bye(self, arg):
        'Close AnonDoge'
        print('Thank you for using AnonDoge')
        return True

def parse(arg):
    return shlex.split(arg)

if __name__ == '__main__':
    AnonDogeShell().cmdloop()