from __future__ import with_statement
import os, os.path
import sys
import cherrypy
import threading
import json

from datastore import Datastore

class ContentGenerator(object):
    @cherrypy.expose
    def index(self):
        return file("index.html")

class RESTService(object):
    """Handle REST requests (we provide only GET) to access to TempCs and Humidity."""
    # REST request are in th4e form: host:port/api/<roomID>/[TempCs|Humidity]

    exposed = True

    def __init__(self, ds):
        self.ds = ds

    @cherrypy.tools.accept(media="text/plain")
    def GET(self, roomID = None, kind = None):
        print("Asking for " + roomID + ", kind "+ kind)
        rows = self.ds.get_tempCs() # WHERE Location = \"" + + "\";" kind, roomID)
        #return str(rows)
        list = []
        for x in rows:
            entry = {
                "timestamp" : str(x[0]),
                "location" : str(x[1]),
                "tempC" : str(x[2])
                    }
            list.append(entry)
        jsonObj =  {
                "result": list
                }
        return json.dumps(jsonObj, indent=4, sort_keys=True) 

    def POST(self, length = 8):
        return "Not implemented."

    def PUT(self, string):
        return "Not implemented."

    def DELETE(self):
        return "Not implemented."

class HTTPServer(threading.Thread):
  
    def __init__(self, ds):
        threading.Thread.__init__(self)
        self.ds = ds
        self.sync = threading.Condition()
        self.webapp = ContentGenerator()
        self.api = RESTService(ds);
        self.root_directory = os.path.abspath(os.path.dirname(sys.argv[0])) + "/../frontend"
 
    def run(self):
        with self.sync:
            cherrypy.server.server_port = 8080
            cherrypy.tree.mount(self.webapp, "/", self.conf)
            cherrypy.tree.mount(self.api, "/api", self.confAPI)
            cherrypy.engine.start()
        cherrypy.engine.block()

    def stop(self):
        with self.sync:
            cherrypy.engine.exit()
            cherrypy.server.stop()

    def init(self):
        self.conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.on': True,
            'tools.staticdir.root': self.root_directory,
            'tools.staticdir.dir': self.root_directory
            }
        }
        self.confAPI = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            #'tools.response_headers.on': True,
            #'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            }
        }

