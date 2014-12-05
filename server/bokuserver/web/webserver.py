import os, os.path
import sys
import cherrypy

import web.content
import web.rest

class WebServer(object):
  
  def __init__(self):
    self.webapp = web.content.ContentGenerator()
    self.webapp.generator = web.rest.RESTService();
    self.root_directory = os.path.abspath(os.path.dirname(sys.argv[0])) + "/frontend"
  
  def start(self):
    conf = {
      '/': {
        'tools.sessions.on': True,
        'tools.staticdir.on': True,
        'tools.staticdir.root': self.root_directory,
        'tools.staticdir.dir': self.root_directory
        },
      '/generator': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [('Content-Type', 'text/plain')],
      },
      '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './public'
      }
    }
    print(self.root_directory)
    cherrypy.quickstart(self.webapp, "/", conf)
