import paho.mqtt.client as mqtt
import os
import sys
import logging

def internal_on_connect(client, userdata, flags, rc):
  userdata._on_connect(client, userdata, flags, rc)

def internal_on_message(client, userdata, message):
  userdata._on_message(client, userdata, message)

class MQTTClient:

  def __init__(self):
    self.initialized = False
    self.client = mqtt.Client("pythoncli", True, self)
    self.server_address = "iot.eclipse.org"

  def start(self):
    print("Starting...")
    self.client.loop_start()

  def init(self):
    self.client.on_connect = internal_on_connect
    self.client.on_message = internal_on_message
    self.client.connect(self.server_address)
    
  def _on_connect(self, client, userdata, flags, rc):
    print("Connected to the server, starting subscribe.")
    self.client.subscribe("$SYS/#")
    self.client.subscribe("Telemetries/Room/+/+", 0)

  def _on_message(self, client, userdata, message):
    print("Payload: " + str(message.topic) + " - " +str(message.payload)) 
