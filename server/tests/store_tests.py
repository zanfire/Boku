import logging

from nose.tools import *
from bokuserver.store.datastore import Datastore


ds = Datastore()

def setup_func():
  ds.init()

def teardown_func():
  ds.close()
  print("TEARDOWN")

@with_setup(setup_func, teardown_func)
def test_insert():
  print("Starting insert test.")
  ds.put_telemetry(0, "Home\Room1\sensor1", 19.8, 55)
  ds.put_telemetry(1, "Home\Room1\sensor1", 19.8, 55)
  ds.put_telemetry(1, "Home\Room1\sensor1", 19.8, 55)

