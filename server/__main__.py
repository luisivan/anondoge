import cherrypy

import names

import db

class Home:

    @cherrypy.tools.json_out()
    def GET(self):

        return {'you': 'modafoca'}

class Alias:

    @cherrypy.tools.json_out()
    def GET(self, alias):

        pubkey = db.get_alias(alias)

        return {'pubkey': pubkey}

    @cherrypy.tools.json_out()
    def POST(self, pubkey):

        return {'alias': available_alias(pubkey)}

import time
import json
from cherrypy import tools

listening = dict()

def pa(hashed_pubkey, res):
    time.sleep(2)
    msgs = db.get(hashed_pubkey)
    res.headers['Content-Type'] = 'application/json'
    yield json.dumps({'msgs': []}).encode()

class Msgs:

    #@cherrypy.tools.json_out()
    def GET(self, hashed_pubkey):

        msgs = db.get(hashed_pubkey)
        if (len(msgs) > 0):
            cherrypy.response.headers['Content-Type'] = 'application/json'
            return json.dumps({'msgs': msgs}).encode()
        else:
            return pa(hashed_pubkey, cherrypy.response)

    GET._cp_config = {'response.stream': True}

    @cherrypy.tools.json_out()
    def POST(self, hashed_pubkey, encrypted_key, encrypted_msg, signature):

        msg_id = db.post(hashed_pubkey, encrypted_key, encrypted_msg, signature)

        if hashed_pubkey in listening.keys():
            print('wWAAA')

        return {'id': str(msg_id)}

def available_alias(pubkey):

    name = names.get_first_name().lower()
    if db.save_alias(name, pubkey):
        return name
    else:
        return available_alias(pubkey)

def expose(routes):

    for (path, theclass) in routes.items():

        theclass.exposed = True
        cherrypy.tree.mount(
            theclass, path, {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()} }
        )

if __name__ == '__main__':

    server_config = {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8443,

        'server.ssl_module': 'builtin',
        'server.ssl_certificate': 'certs/cert.pem',
        'server.ssl_private_key': 'certs/privkey.pem',

        'tools.encode.on': True,
        'tools.encode.encoding': 'utf-8'
    }
    cherrypy.config.update(server_config)

    routes = {
        '/': Home(),
        '/api/alias': Alias(),
        '/api/msgs': Msgs()
    }
    expose(routes)

    cherrypy.engine.start()
    cherrypy.engine.block()