import sys
import argparse
import logging

from mqtt import MQTTClient
from web.webserver import WebServer
from datastore import Datastore

if __name__ == "__main__":
  print("Starting store ...")
  ds = Datastore()
  ds.init()
  print(" ... done")

  print("Starting MQTT Client ...")
  mqttcli = MQTTClient()
  mqttcli.server_address = "192.168.1.99"
  mqttcli.ds = ds 
  mqttcli.init()
  mqttcli.start()
  print(" ... done")

  print("Starting web server ...")
  #websrv = WebServer()
  #websrv.start()
# TODO: Unblock call to start and wait in a LOOP here.
  while True:
    pass
