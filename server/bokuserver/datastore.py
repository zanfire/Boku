import sqlite3
import os
import sys
import logging


class Datastore:

  def __init__(self):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    self.initialized = False
    self.root_directory = os.path.abspath(os.path.dirname(sys.argv[0])) + "/datastore"
    self.db_path = self.root_directory + "/datastore.db"
    self.conn = None
    self._last_tempc = -1
    self._last_humidity = -1
    logging.debug("Created datastore instance. DB: {0}, ".format(self.db_path))

  def create(self):
    # Create folder and database
    print(self.root_directory)
    os.mkdir(self.root_directory)
    self.conn = sqlite3.connect(self.db_path)
    self.create_tables()

  def init(self):
    if self.initialized:
      logging.warn("Skipping init because Datastore was initialized.")
      return

    if not os.path.exists(self.db_path):
       logging.debug("Database not present, createding...")
       self.create()
    else:
      logging.debug("Database was created, connecting...")
      self.conn = sqlite3.connect(self.db_path)
    self.initialized = True

  def close(self):
    if not self.initialized:
      return
    self.conn.close()
    self.initialized = False

  def create_tables(self):
    if self.initialized:
      return
    cur = self.conn.cursor()
    cur.execute("CREATE TABLE TempCs (Timestamp INTEGER, Location TEXT, TempC REAL);")
    cur.execute("CREATE TABLE Humidities (Timestamp INTEGER, Location TEXT, Humidity REAL);")
    self.conn.commit()


  def _put_telemetry(self, timestamp, location, table, value):
    if not self.initialized:
      return False
    print("Storing data in table " + table + ": " + str(timestamp) + ", "+ location + ", " + value)
    cur = self.conn.cursor()
    cur.execute("INSERT INTO " + table + " VALUES (?, ?, ?);", (timestamp, location, value))
    if cur.rowcount == 1:
      self.conn.commit()
      return True
    else:
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
 

