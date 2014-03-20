import cherrypy
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket

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

class Msgs:

    @cherrypy.tools.json_out()
    def GET(self, hashed_pubkey):

        msgs = db.get(hashed_pubkey)

        return {'msgs': msgs}

    @cherrypy.tools.json_out()
    def POST(self, hashed_pubkey, encrypted_key, encrypted_msg, signature):

        msg_id = db.post(hashed_pubkey, encrypted_key, encrypted_msg, signature)

        return {'id': str(msg_id)}

class WSocket(WebSocket):

    def received_message(self, message):
        self.send(message.data, message.is_binary)

class Socket(object):

    @cherrypy.expose
    def ws(self):
        '''handler = cherrypy.request.ws_handler
        print(handler)'''
        pass

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
        'server.ssl_private_key': 'certs/privkey.pem'
    }
    cherrypy.config.update(server_config)
    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    routes = {
        '/': Home(),
        '/api/alias': Alias(),
        '/api/msgs': Msgs()
    }
    expose(routes)
    cherrypy.tree.mount(Socket(), '/', config={'/ws': {'tools.websocket.on': True, 'tools.websocket.handler_cls': WSocket}})

    cherrypy.engine.start()
    cherrypy.engine.block()