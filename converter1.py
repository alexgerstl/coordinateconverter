# -*- coding: utf-8 -*-
from os.path import expanduser

import converter

home = expanduser("~")
python_path = home + '\.qgis2\python\plugins\CoordinatesConverter\lib\pyproj-1.9.5.1.egg'

import sys
sys.path.insert(0,python_path)
import pyproj
import math
import points
from ensurer import Hemisphere


class Converter:
    def __init__(self):
        pass

    @staticmethod
    def convert_based_on_epsg(point, _from, _to):
        longitude = point.long_deg
        latitude = point.lat_deg
        _from = pyproj.Proj(init='EPSG:' + _from)
        _to = pyproj.Proj(init='EPSG:' + _to)
        x, y = pyproj.transform(_from, _to, longitude, latitude)
        return x, y


