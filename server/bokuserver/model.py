import os
import sys
import logging

class Room:
    def __init__(self, ds, id, desc):
        self.ds = ds
        self.id = id
        self.description = desc

    def get_last_tempC(self):
        return self.ds.get_last_tempc(self.id)
