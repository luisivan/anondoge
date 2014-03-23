# AnonDoge


![](http://24.media.tumblr.com/6435dd24615de9bb439d7aaa34b07d8e/tumblr_mvwwxvLLTE1szim6vo1_400.jpg)


## What it does

AnonDoge lets two users communicate in a 100% anonymous, encrypted way.

Now you may be thinking *That already exists!*. Well, yeah, you can already communicate with other person encrypting messages so the NSA won't ever know what are you talking about.

And you can already use Tor so the NSA won't (hopefully) know to whom are you talking.

But I wanted to develop something easier that keeps users anonymous and messages encrypted without having to use Tor.

The main use case is for when you want to email someone and the message is so important that you gotta be a freakin' paranoid.


## Usage

Create a new directory that identifies your conversation. Each time you want to access to that conversation, you'll have to run AnonDoge in that dir.

User A:

```
(doge) alias
Your alias is william
```

(User A tells their alias to User B - *cool way to do this coming soon*)

User B:

```
(doge) alias william
Now you can message william
(doge) send "hey, this is secret"
Message sent
```

User A:

```
(doge) fetch
1 new message
1 - "hey, this is secret"
(doge) sendfile document.pdf
```

## What can be tracked


Let's be paranoid and think that your ISP is tracking the data you send to AnonDoge and that they can crack SSL or they control the server running AnonDoge. They could know:

- If you use `alias xxx`, the first public key of your receiver.

- If they know that, they can track your first message to him.

- If your receiver's ISP is also spying on him, they may be able to know if you're in the same timezone and your IPs. However, since they don't know the content of the messages they can't do anything at all.

Although this scenario it's very unlikely and the system is totally untraceable per se, using Tor erases any possibility of traceability.

However I'm not on that level of paranoia (yet)


## How it works

Each time you open AnonDoge for the first time on a new directory, it creates both a public key and a private key.

If user A runs the command `alias`, then a new keypair is created and the pubkey is uploaded to the server running AnonDoge using SSL.

When user B runs `alias xxx` he downloads A's pubkey, which is automatically erased from the server.

[1] User B then generates a random key and a new keypair and encrypts both his message and his new public key using the random key he previously generated (AES).

Then B encrypts the key to unlock the message using A's public key, and he also signs the message using his private key so A will be able to verify that in fact B is B (RSA).

The old keypair is destroyed (so reading any possible previous message becomes impossible) and the whole encrypted message is then sent to the server running AnonDoge using SSL, although the messages are public so that doesn't matter. There's also a subject in the message, that is A's hashed public key (SHA256).

When A fetches new messages, he'll query the server for messages which subject is his public key's SHA256 hash. Once downloaded, the messages are deleted from the server.

Then A unencrypts the messages, and when he decides to reply A the whole process from [1] to here is repeated.