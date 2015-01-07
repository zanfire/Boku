import sys
import argparse
import logging

from mqtt import MQTTClient
from webserver import HTTPServer
from datastore import Datastore

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Bokuserver", None, "Home automation server.")
    parser.add_argument("-m", "--mqttbroker", help="The MQTT broker address.", action="store", type=str, default="127.0.0.1")
    parser.add_argument("-d", "--datastore", help="The datastore location.", action="store", type=str, default="datastore.db")
    parser.add_argument("-v", "--verbose", help="Enable verbose output.", action="store_true")
    args = parser.parse_args()


    print("Boku server, Copyright Matteo Valdina 2014.\n")

    print("Starting store ...")
    ds = Datastore(args.datastore)
    ds.init()
    print(" ... done")

    rooms = ds.get_rooms()

    for x in rooms:
        print("Loaded room ID:" + x.id + " desc: " + x.description)


    print("Starting MQTT Client ...")
    mqttcli = MQTTClient(args.mqttbroker, ds)
    #mqttcli.server_address = "192.168.1.99"
    mqttcli.init()
    mqttcli.start()
    print(" ... done")

    print("Starting web server ...")
    websrv = HTTPServer(ds)
    websrv.init()
    websrv.start()
    # TODO: Unblock call to start and wait in a LOOP here.
    while True:
        resp = input("Press q to exit ...")
        if resp == "q":
            break;
  
    print("Shutdown ...")
    ds.close()
    websrv.stop()
    print(" ... done")

    print("Process terminated.")
    exit(0)
