# -*- coding: utf-8 -*-
# 2013.12.26 K. Kuwata
# GRASSsetup.py
import os
import grass.script as grass
import grass.script as gsetup
from grass.script import core as g

class GRASSset:
    def __init__(self, datasource, gisbase, gisdbase, location, mapset):
        self.datasource = datasource
        self.gisbase = gisbase
        self.gisdbase = gisdbase
        self.location = location
        self.mapset = mapset

    def ChangeMapset(self):
        home = os.environ['HOME'] + "/"
        setfile = home + ".grassrc6"
        content = \
"""GISDBASE: %s
LOCATION_NAME: %s
MAPSET: %s
GRASS_GUI: text\n""" % (self.datasource, self.location, self.mapset)
        f = open(setfile, 'w')
        f.write(content)
        f.close()

