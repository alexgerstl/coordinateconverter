# -*- coding: utf-8 -*-
from os.path import expanduser
home = expanduser("~")
python_path = home + '\.qgis2\python\plugins\CoordinatesConverter\lib\pyproj-1.9.5.1-py2.7-win-amd64.egg'

import sys
sys.path.insert(0,python_path)
import pyproj
import math
import points
from ensurer import Hemisphere


class Converter:
    def __init__(self):
        self.lettertable = 'CDEFGHJKLMNPQRSTUVWX'
        self.lettervalues = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
                             'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
                             'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}

    @staticmethod
    def convert_based_on_epsg(point, _from, _to):
        longitude = point.long_deg
        latitude = point.lat_deg
        _from = pyproj.Proj(init='EPSG:' + _from)
        _to = pyproj.Proj(init='EPSG:' + _to)
        x, y = pyproj.transform(_from, _to, longitude, latitude)
        return x, y

    def convert_MGRS_to_UTM(self, point):
        lat_zone = ord(point.zone[2].upper())
        if lat_zone >= ord('N'):
            hemisphere = Hemisphere.NORTH
        else:
            hemisphere = Hemisphere.SOUTH

        zone_fields = ['STUVWXYZ', 'ABCDEFGH', 'JKLMNPQR']
        zone_fields_lat = 'ABCDEFGHJKLMNPQRSTUV'
        zone_temp = int(point.zone[0:2])
        square = point.square.upper()
        square_x = zone_fields[zone_temp % 3].index(square[0])
        square_y = zone_fields_lat.index(square[1])

        square_x += 1
        easting_temp = square_x * 100000

        if zone_temp % 2 == 0:
            square_y = (square_y - 5) % 20

        min_lat = self.__get_min_northing(chr(lat_zone))
        while square_y < min_lat:
            square_y += 20

        if square_y > min_lat + 15:
            square_y -= 20

        northing_temp = square_y * 100000

        result_easting = easting_temp + int(point.easting)
        result_northing = northing_temp + int(point.northing)

        return points.UTMPoint(result_easting, result_northing, zone_temp, hemisphere)

    def convert_UTM_to_MGRS(self, point):
        degree_point = self.convert_UTM_to_degree(point)
        ltr2_low_value, ltr2_high_value, false_northing = self.__get_grid_values(point.zone)
        letter = self.__get_latitude_letter(degree_point.lat_deg)

        grid_northing = int(point.northing)
        if grid_northing == 1.E7:
            grid_northing -= 1.0

        while grid_northing >= 2000000.0:
            grid_northing -= 2000000.0

        grid_northing -= false_northing

        if grid_northing < 0.0:
            grid_northing += 2000000

        square_y = grid_northing / 100000.0

        if square_y > self.lettervalues['H']:
            square_y += 1

        if square_y > self.lettervalues['N']:
            square_y += 1

        grid_easting = int(point.easting)

        if letter == 'V' and point.zone == 31 and grid_easting == 500000.0:
            grid_easting -= 1.0

        square_x = ltr2_low_value + (grid_easting / 100000) - 1
        if ltr2_low_value == self.lettervalues['J'] and square_x > self.lettervalues['N']:
            square_x += 1

        zone = str(point.zone) + letter
        square = str(self.lettervalues.keys()[self.lettervalues.values().index(int(square_x))]) + \
                 str(self.lettervalues.keys()[self.lettervalues.values().index(int(square_y))])
        easting = math.fmod(float(point.easting), 100000.0)
        northing = math.fmod(float(point.northing), 100000.0)
        return points.MGRSPoint(int(easting), int(northing), zone, square, point.hemisphere)


    def __define_UTM_zone(self, point):
        long_deg = float(point.long_deg)
        lat_deg = float(point.lat_deg)

        #long_temp = (long_deg + 180) - (long_deg + 180)/360 *360 - 180
        #zone = (long_temp + 180)/6 + 1
        long_temp = (long_deg + 180) - math.floor((long_deg + 180)/360)*360-180
        zone = math.floor((long_temp + 180)/6) + 1

        if 56.0 <= lat_deg < 64.0 and 3.0 <= long_temp < 12.0:
            zone = 32

        #specila zone for Svalbard
        if 72.0 <= lat_deg < 84.0:
            if 0.0 <= long_temp < 9.0:
                zone = 31
            elif 9.0 <= long_temp < 21.0:
                zone = 33
            elif 21.0 <= long_temp < 33.0:
                zone = 35
            elif 33.0 <= long_temp < 42.0:
                zone = 37

        if 84 >= lat_deg >= 72:
            letter = 'X'
        elif 72 > lat_deg >= 64:
            letter = 'W'
        elif 64 > lat_deg >= 56:
            letter = 'V'
        elif 56 > lat_deg >= 48:
            letter = 'U'
        elif 48 > lat_deg >= 40:
            letter = 'T'
        elif 40 > lat_deg >= 32:
            letter = 'S'
        elif 32 > lat_deg >= 24:
            letter = 'R'
        elif 24 > lat_deg >= 16:
            letter = 'Q'
        elif 16 > lat_deg >= 8:
            letter = 'P'
        elif 8 > lat_deg >= 0:
            letter = 'N'
        elif 0 > lat_deg >= -8:
            letter = 'M'
        elif -8 > lat_deg >= -16:
            letter = 'L'
        elif -16 > lat_deg >= -24:
            letter = 'K'
        elif -24 > lat_deg >= -32:
            letter = 'J'
        elif -32 > lat_deg >= -40:
            letter = 'H'
        elif -40 > lat_deg >= -48:
            letter = 'G'
        elif -48 > lat_deg >= -56:
            letter = 'F'
        elif -56 > lat_deg >= -64:
            letter = 'E'
        elif -64 > lat_deg >= -72:
            letter = 'D'
        elif -72 > lat_deg >= -80:
            letter = 'C'
        else:
            letter = 'Z'

        return zone, letter

    def __get_grid_values(self, zone):
        set_number = zone % 6
        if set_number == 0:
            set_number = 6
        if set_number == 1 or set_number == 4:
            ltr2_low_value = self.lettervalues['A']
            ltr2_high_value = self.lettervalues['H']
        elif set_number == 2 or set_number == 5:
            ltr2_low_value = self.lettervalues['J']
            ltr2_high_value = self.lettervalues['R']
        elif set_number == 3 or set_number == 6:
            ltr2_low_value = self.lettervalues['S']
            ltr2_high_value = self.lettervalues['Z']

        if set_number % 2 == 0:
            false_northing = 1500000.0
        else:
            false_northing = 0.0

        return ltr2_low_value, ltr2_high_value, false_northing

    def __get_latitude_letter(self, latitude):
        if 72.0 <= latitude < 84.5:
            letter = 'X'
        elif -80.5 < latitude < 72.0:
            temp = (latitude + 80.0) / 8.0 + 1.0E-12
            letter = self.lettertable[int(temp)]
        else:
            letter = 'Z'
        return letter

    def __get_min_northing(self, letter):
        if letter == 'C':
            return 11.0
        elif letter == 'D':
            return 20.0
        elif letter == 'E':
            return 28.0
        elif letter == 'F':
            return 37.0
        elif letter == 'G':
            return 46.0
        elif letter == 'H':
            return 55.0
        elif letter == 'J':
            return 64.0
        elif letter == 'K':
            return 73.0
        elif letter == 'L':
            return 82.0
        elif letter == 'M':
            return 91.0
        elif letter == 'N':
            return 0.0
        elif letter == 'P':
            return 8.0
        elif letter == 'Q':
            return 17.0
        elif letter == 'R':
            return 26.0
        elif letter == 'S':
            return 35.0
        elif letter == 'T':
            return 44.0
        elif letter == 'U':
            return 53.0
        elif letter == 'V':
            return 62.0
        elif letter == 'W':
            return 70.0
        elif letter == 'X':
            return 79.0
