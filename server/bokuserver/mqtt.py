import paho.mqtt.client as mqtt
import os
import sys
import logging
import time
from datastore import Datastore

def internal_on_connect(client, userdata, flags, rc):
    print("on_connect: " + str(rc))
    userdata._on_connect(client, userdata, flags, rc)

def internal_on_message(client, userdata, message):
    userdata._on_message(client, userdata, message)

class MQTTClient:
    def __init__(self, server_address, ds, ):
        self.initialized = False
        self.client = mqtt.Client("", True, self, mqtt.MQTTv31)
        self.server_address = server_address
        self.ds = ds

    def start(self):
        print("Starting...")
        self.client.loop_start()

    def init(self):
        self.client.on_connect = internal_on_connect
        self.client.on_message = internal_on_message
        print("Connecting to MQTT broker: " + self.server_address)
        self.client.connect(self.server_address)
    
    def _on_connect(self, client, userdata, flags, rc):
        print("Connected to the server, starting subscribe.")
        #self.client.subscribe("$SYS/#")
        #self.client.subscribe("Tel")
        self.client.subscribe("Telemetries/Room/+/+", 0)

    def _on_message(self, client, userdata, message):
        print("Payload: " + str(message.topic) + " - " + str(message.payload)) 
        tokens = message.topic.split('/')
        if (tokens[0] == "Telemetries") and (self.ds != None):
            ts = int(time.time())
            location = tokens[2]
            value = str(message.payload)
            if value.startswith("b"):
                value = value[2:(len(value)-1)]
            if tokens[3] == "TempC":
                self.ds.put_telemetry_tempc(ts, location, value)
            elif tokens[3] == "Humidity":
                self.ds.put_telemetry_humidity(ts, location, value)

