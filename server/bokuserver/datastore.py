import sqlite3
import os
import sys
import logging
from threading import Thread
from queue import Queue

class AdapterMT(Thread):
    def __init__(self, db):
        super(AdapterMT, self).__init__()
        self.db = db
        self.reqs = Queue()

    def startThread(self):
        self.start()

    def run(self):
        conn = sqlite3.connect(self.db) 
        cursor = conn.cursor()
        while True:
            req, arg, res = self.reqs.get()
            print("Executing new execute." + req + " " + str(arg))
            if req == "--close--": break
            cursor.execute(req, arg)
            print("Rowcount: " + str(cursor.rowcount))
            if res:
                for rec in cursor:
                    res.put(rec)
                res.put("--no more--")
            conn.commit()
        conn.close()

    def execute(self, req, arg=None, res=None):
        self.reqs.put((req, arg or tuple(), res))
    
    def select(self, req, arg=None):
        res = Queue()
        self.execute(req, arg, res)
        while True:
            rec = res.get()
            if rec == "--no more--": break
            yield rec

    def close(self):
        self.execute("--close--")

class Datastore:
    def __init__(self, dbfile="datastore.db"):
        self.initialized = False
        self.db_path = dbfile
        self.adapterMT = AdapterMT(self.db_path)
        logging.debug("Created datastore instance. DB: {0}, ".format(self.db_path))

    def create(self):
        print(self.db_path);
        self.create_tables()

    def init(self):
        if self.initialized:
            logging.warn("Skipping init because Datastore was initialized.")
            return
        if not os.path.exists(self.db_path):
            logging.debug("Database not present, createding...")
            self.create()
        self.adapterMT.startThread()
        self.initialized = True

    def close(self):
        if not self.initialized:
            return
        self.adapterMT.close()
        self.initialized = False

    def create_tables(self):
        if self.initialized:
            return
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE TempCs (Timestamp INTEGER, Location TEXT, TempC REAL);")
        cur.execute("CREATE TABLE Humidities (Timestamp INTEGER, Location TEXT, Humidity REAL);")
        conn.commit()
        conn.close()

    def _put_telemetry(self, timestamp, location, table, value):
        if not self.initialized:
            return False
        print("Storing data in table " + table + ": " + str(timestamp) + ", "+ location + ", " + value)
        self.adapterMT.execute("INSERT INTO " + table + " VALUES (?, ?, ?);", (timestamp, location, value))
        return False

    def put_telemetry_tempc(self, timestamp, location, v):
        return self._put_telemetry(timestamp, location, "TempCs", v)

    def put_telemetry_humidity(self, timestamp, location, v):
        return self._put_telemetry(timestamp, location, "Humidities", v)

    def get_telemetries(self):
        if not self.initialized:
            return False
        cur = self.conn.cursor()
        rows = cur.execute("SELECT * FROM Telemetries;")
        return rows

