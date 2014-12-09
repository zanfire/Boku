import sys
import argparse
import logging

from mqtt import MQTTReceiver
from web.webserver import WebServer
from store.datastore import Datastore

if __name__ == "__main__":
  print("Starting store ...")
  ds = Datastore()
  ds.init()

  print("Starting MQTT broker ...")
  mqttrecv = MQTTReceiver()
  mqttrecv.init()
  mqttrecv.start()

  print("Starting web server ...")
  websrv = WebServer()
  websrv.start()
# TODO: Unblock call to start and wait in a LOOP here.
