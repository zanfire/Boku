import sqlite3
import os
import sys
import logging
from model import Room
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

    def execute(self, req, arg = None, res = None):
        print("Execute SQL.")
        self.reqs.put((req, arg or tuple(), res))
    
    def get(self, req, arg = None):
        print("Select invoke ...")
        res = Queue()
        output = []
        self.execute(req, arg, res)
        while True:
            rec = res.get()
            print(rec)
            if rec == "--no more--": break
            output.append(rec)
        return output

    def close(self):
        self.execute("--close--")

class Datastore:
    def __init__(self, dbfile="datastore.db"):
        self.initialized = False
        self.db_path = dbfile
        self._adapterMT = AdapterMT(self.db_path)
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
        self._adapterMT.startThread()
        self.initialized = True

    def close(self):
        if not self.initialized:
            return
        self._adapterMT.close()
        self.initialized = False

    def create_tables(self):
        if self.initialized:
            return
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("CREATE TABLE Rooms (id TEXT, description TEXT);")
        cur.execute("CREATE TABLE TempCs (Timestamp INTEGER, Location TEXT, TempC REAL);")
        cur.execute("CREATE TABLE Humidities (Timestamp INTEGER, Location TEXT, Humidity REAL);")
        conn.commit()
        conn.close()

    def _put_telemetry(self, timestamp, location, table, value):
        if not self.initialized:
            return False
        print("Storing data in table " + table + ": " + str(timestamp) + ", "+ location + ", " + value)
        self._adapterMT.execute("INSERT INTO " + table + " VALUES (?, ?, ?);", (timestamp, location, value))
        return False

    def put_telemetry_tempc(self, timestamp, location, v):
        return self._put_telemetry(timestamp, location, "TempCs", v)

    def put_telemetry_humidity(self, timestamp, location, v):
        return self._put_telemetry(timestamp, location, "Humidities", v)

    def get_tempCs(self, loc):
        if not self.initialized:
            return False
        print("Get ... started")
        rows = self._adapterMT.get("SELECT * FROM TempCs WHERE Location = ? ORDER BY Timestamp DESC;", (loc,))
        print("Get ... ended")
        return rows

    def get_last_tempCs(self, loc):
        if not self.initialized:
            return False
        print("Get ... started")
        rows = self._adapterMT.get("SELECT * FROM TempCs WHERE Location = ? LIMIT 1;", (loc,))
        print("Get ... ended")
        return rows[0]

    def get_rooms(self):
        if not self.initialized:
            return False
        rows = self._adapterMT.get("SELECT * FROM Rooms;")
        rooms = []
        for x in rows:
            rooms.append(Room(self, x[0], x[1]))
        return rooms

