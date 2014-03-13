import cherrypy
from bson.json_util import dumps

import db

class Home:

    @cherrypy.tools.json_out()
    def GET(self):

        return {'you': 'modafoca'}

class Msgs:

    @cherrypy.tools.json_out()
    def GET(self, hashed_pubkey):

        msgs = db.get(hashed_pubkey)

        return {'msgs': msgs}

    @cherrypy.tools.json_out()
    def POST(self, hashed_pubkey, encrypted_key, encrypted_msg, signature):

        msg_id = db.post(hashed_pubkey, encrypted_key, encrypted_msg, signature)

        return {'id': str(msg_id)}

def expose(routes):

    for (path, theclass) in routes.items():

        theclass.exposed = True
        cherrypy.tree.mount(
            theclass, path, {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()} }
        )

if __name__ == '__main__':

    routes = {
        '/': Home(),
        '/api/msgs': Msgs()
    }
    expose(routes)

    server_config = {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8443,

        'server.ssl_module': 'builtin',
        'server.ssl_certificate': 'certs/cert.pem',
        'server.ssl_private_key': 'certs/privkey.pem'
    }
    cherrypy.config.update(server_config)
    cherrypy.engine.start()
    cherrypy.engine.block()