import sys
import argparse

from web.webserver import WebServer
from store.datastore import Datastore

if __name__ == "__main__":
  print("Starting store ...")
  ds = Datastore()
  ds.init()

  print("Starting MQTT broker ...")
  print("Starting web server ...")
  websrv = WebServer()
  websrv.start()
