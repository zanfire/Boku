import os, os.path

import cherrypy

class ContentGenerator(object):

  @cherrypy.expose
  def index(self):
    return file("index.html")
