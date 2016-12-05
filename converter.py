from os.path import expanduser

home = expanduser("~")
enum_path = home + '\.qgis2\python\plugins\CoordinatesConverter\lib\utm.egg'

import sys
sys.path.insert(0,enum_path)
import utm
import points
from coordinate_parser import Hemisphere
from decimal import Decimal


class UtmConverter:

    @staticmethod
    def degree_to_utm(point):
        long_deg = point.long_deg
        lat_deg = point.lat_deg
        easting, northing, zone_number, zone_letter = utm.from_latlon(lat_deg, long_deg)
        if lat_deg > 0:
            hemisphere = Hemisphere.NORTH
        else:
            hemisphere = Hemisphere.SOUTH
        point = points.UTMPoint(easting, northing, zone_number, zone_letter, hemisphere)
        return point

    @staticmethod
    def utm_to_degree(point):
        easting = int(point.easting)
        northing = int(point.northing)
        zone = int(point.zone_number)
        if point.hemisphere == Hemisphere.NORTH:
            northern = True
        else:
            northern = False

        lat_deg, long_deg = utm.to_latlon(easting, northing, zone, northern=northern)
        point = points.WGSPoint(Decimal(long_deg), 0, 0, Decimal(lat_deg), 0, 0)
        return point

class DegreeConverter:

    @staticmethod
    def convert_degree_to_DMS(degrees):
        _deg = int(degrees)
        _min = (Decimal(degrees) - Decimal(_deg)) * Decimal(60)
        _sec = (Decimal(_min) - int(_min)) * Decimal(60)
        return Decimal(_deg), abs(int(_min)), abs(Decimal(_sec))

    @staticmethod
    def convert_DMS_to_degree(degrees, minutes, seconds):
        if degrees > 0:
            _deg = Decimal(degrees) + Decimal(minutes) / Decimal(60.0) + Decimal(seconds) / Decimal(3600.0)
        else:
            _deg = Decimal(degrees) - Decimal(minutes) / Decimal(60.0) - Decimal(seconds) / Decimal(3600.0)
        return _deg

    @staticmethod
    def convert_degree_to_decimal_minutes(degrees):
        _deg = int(degrees)
        _min = (abs(degrees) - abs(_deg)) * 60
        return _deg, _min

    @staticmethod
    def convert_decimal_minutes_to_degree(degrees, minutes):
        _d = Decimal(minutes) / Decimal(60.0)
        if degrees > 0:
            _deg = Decimal(degrees) + Decimal(_d)
        else:
            _deg = Decimal(degrees) - Decimal(_d)
        return Decimal(_deg)

    @staticmethod
    def convert_dms_to_decimal_minutes(degrees, minutes, seconds):
        _min = Decimal(minutes) + Decimal(seconds) / Decimal(60.0)
        return Decimal(degrees), Decimal(_min)