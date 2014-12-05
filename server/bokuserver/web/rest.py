import os, os.path
import random
import string

import cherrypy

class RESTService(object):
  exposed = True

  @cherrypy.tools.accept(media="text/plain")
  def GET(self):
    return cherrypy.session["mystring"]

  def POST(self, length = 8):
    random_string = "".join(random.sample(string.hexdigits, int(length)))
    cherrypy.sessio["mystring"] = random_string
    return random_string

  def PUT(self, string):
    cherrypy.session["mystring"] = string

  def DELETE(self):
      cherrypy.session.pop("mystring", None)
