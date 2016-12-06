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
        self.listN = [0]*61
        self.listS = [0]*61
        p_wgs84 = pyproj.Proj(init='EPSG:4326')

        p_1N = pyproj.Proj(init='EPSG:32601')
        p_2N = pyproj.Proj(init='EPSG:32602')
        p_3N = pyproj.Proj(init='EPSG:32603')
        p_4N = pyproj.Proj(init='EPSG:32604')
        p_5N = pyproj.Proj(init='EPSG:32605')
        p_6N = pyproj.Proj(init='EPSG:32606')
        p_7N = pyproj.Proj(init='EPSG:32607')
        p_8N = pyproj.Proj(init='EPSG:32608')
        p_9N = pyproj.Proj(init='EPSG:32609')
        p_10N = pyproj.Proj(init='EPSG:32610')
        p_11N = pyproj.Proj(init='EPSG:32611')
        p_12N = pyproj.Proj(init='EPSG:32612')
        p_13N = pyproj.Proj(init='EPSG:32613')
        p_14N = pyproj.Proj(init='EPSG:32614')
        p_15N = pyproj.Proj(init='EPSG:32615')
        p_16N = pyproj.Proj(init='EPSG:32616')
        p_17N = pyproj.Proj(init='EPSG:32617')
        p_18N = pyproj.Proj(init='EPSG:32618')
        p_19N = pyproj.Proj(init='EPSG:32619')
        p_20N = pyproj.Proj(init='EPSG:32620')
        p_21N = pyproj.Proj(init='EPSG:32621')
        p_22N = pyproj.Proj(init='EPSG:32622')
        p_23N = pyproj.Proj(init='EPSG:32623')
        p_24N = pyproj.Proj(init='EPSG:32624')
        p_25N = pyproj.Proj(init='EPSG:32625')
        p_26N = pyproj.Proj(init='EPSG:32626')
        p_27N = pyproj.Proj(init='EPSG:32627')
        p_28N = pyproj.Proj(init='EPSG:32628')
        p_29N = pyproj.Proj(init='EPSG:32629')
        p_30N = pyproj.Proj(init='EPSG:32630')
        p_31N = pyproj.Proj(init='EPSG:32631')
        p_32N = pyproj.Proj(init='EPSG:32632')
        p_33N = pyproj.Proj(init='EPSG:32633')
        p_34N = pyproj.Proj(init='EPSG:32634')
        p_35N = pyproj.Proj(init='EPSG:32635')
        p_36N = pyproj.Proj(init='EPSG:32636')
        p_37N = pyproj.Proj(init='EPSG:32637')
        p_38N = pyproj.Proj(init='EPSG:32638')
        p_39N = pyproj.Proj(init='EPSG:32639')
        p_40N = pyproj.Proj(init='EPSG:32640')
        p_41N = pyproj.Proj(init='EPSG:32641')
        p_42N = pyproj.Proj(init='EPSG:32642')
        p_43N = pyproj.Proj(init='EPSG:32643')
        p_44N = pyproj.Proj(init='EPSG:32644')
        p_45N = pyproj.Proj(init='EPSG:32645')
        p_46N = pyproj.Proj(init='EPSG:32646')
        p_47N = pyproj.Proj(init='EPSG:32647')
        p_48N = pyproj.Proj(init='EPSG:32648')
        p_49N = pyproj.Proj(init='EPSG:32649')
        p_50N = pyproj.Proj(init='EPSG:32650')
        p_51N = pyproj.Proj(init='EPSG:32651')
        p_52N = pyproj.Proj(init='EPSG:32652')
        p_53N = pyproj.Proj(init='EPSG:32653')
        p_54N = pyproj.Proj(init='EPSG:32654')
        p_55N = pyproj.Proj(init='EPSG:32655')
        p_56N = pyproj.Proj(init='EPSG:32656')
        p_57N = pyproj.Proj(init='EPSG:32657')
        p_58N = pyproj.Proj(init='EPSG:32658')
        p_59N = pyproj.Proj(init='EPSG:32659')
        p_60N = pyproj.Proj(init='EPSG:32660')

        p_1S = pyproj.Proj(init='EPSG:32701')
        p_2S = pyproj.Proj(init='EPSG:32702')
        p_3S = pyproj.Proj(init='EPSG:32703')
        p_4S = pyproj.Proj(init='EPSG:32704')
        p_5S = pyproj.Proj(init='EPSG:32705')
        p_6S = pyproj.Proj(init='EPSG:32706')
        p_7S = pyproj.Proj(init='EPSG:32707')
        p_8S = pyproj.Proj(init='EPSG:32708')
        p_9S = pyproj.Proj(init='EPSG:32709')
        p_10S = pyproj.Proj(init='EPSG:32710')
        p_11S = pyproj.Proj(init='EPSG:32711')
        p_12S = pyproj.Proj(init='EPSG:32712')
        p_13S = pyproj.Proj(init='EPSG:32713')
        p_14S = pyproj.Proj(init='EPSG:32714')
        p_15S = pyproj.Proj(init='EPSG:32715')
        p_16S = pyproj.Proj(init='EPSG:32716')
        p_17S = pyproj.Proj(init='EPSG:32717')
        p_18S = pyproj.Proj(init='EPSG:32718')
        p_19S = pyproj.Proj(init='EPSG:32719')
        p_20S = pyproj.Proj(init='EPSG:32720')
        p_21S = pyproj.Proj(init='EPSG:32721')
        p_22S = pyproj.Proj(init='EPSG:32722')
        p_23S = pyproj.Proj(init='EPSG:32723')
        p_24S = pyproj.Proj(init='EPSG:32724')
        p_25S = pyproj.Proj(init='EPSG:32725')
        p_26S = pyproj.Proj(init='EPSG:32726')
        p_27S = pyproj.Proj(init='EPSG:32727')
        p_28S = pyproj.Proj(init='EPSG:32728')
        p_29S = pyproj.Proj(init='EPSG:32729')
        p_30S = pyproj.Proj(init='EPSG:32730')
        p_31S = pyproj.Proj(init='EPSG:32731')
        p_32S = pyproj.Proj(init='EPSG:32732')
        p_33S = pyproj.Proj(init='EPSG:32733')
        p_34S = pyproj.Proj(init='EPSG:32734')
        p_35S = pyproj.Proj(init='EPSG:32735')
        p_36S = pyproj.Proj(init='EPSG:32736')
        p_37S = pyproj.Proj(init='EPSG:32737')
        p_38S = pyproj.Proj(init='EPSG:32738')
        p_39S = pyproj.Proj(init='EPSG:32739')
        p_40S = pyproj.Proj(init='EPSG:32740')
        p_41S = pyproj.Proj(init='EPSG:32741')
        p_42S = pyproj.Proj(init='EPSG:32742')
        p_43S = pyproj.Proj(init='EPSG:32743')
        p_44S = pyproj.Proj(init='EPSG:32744')
        p_45S = pyproj.Proj(init='EPSG:32745')
        p_46S = pyproj.Proj(init='EPSG:32746')
        p_47S = pyproj.Proj(init='EPSG:32747')
        p_48S = pyproj.Proj(init='EPSG:32748')
        p_49S = pyproj.Proj(init='EPSG:32749')
        p_50S = pyproj.Proj(init='EPSG:32750')
        p_51S = pyproj.Proj(init='EPSG:32751')
        p_52S = pyproj.Proj(init='EPSG:32752')
        p_53S = pyproj.Proj(init='EPSG:32753')
        p_54S = pyproj.Proj(init='EPSG:32754')
        p_55S = pyproj.Proj(init='EPSG:32755')
        p_56S = pyproj.Proj(init='EPSG:32756')
        p_57S = pyproj.Proj(init='EPSG:32757')
        p_58S = pyproj.Proj(init='EPSG:32758')
        p_59S = pyproj.Proj(init='EPSG:32759')
        p_60S = pyproj.Proj(init='EPSG:32760')
        
        self.listN[0] = p_wgs84
        self.listN[1] = p_1N
        self.listN[2] = p_2N
        self.listN[3] = p_3N
        self.listN[4] = p_4N
        self.listN[5] = p_5N
        self.listN[6] = p_6N
        self.listN[7] = p_7N
        self.listN[8] = p_8N
        self.listN[9] = p_9N
        self.listN[10] = p_10N
        self.listN[11] = p_11N
        self.listN[12] = p_12N
        self.listN[13] = p_13N
        self.listN[14] = p_14N
        self.listN[15] = p_15N
        self.listN[16] = p_16N
        self.listN[17] = p_17N
        self.listN[18] = p_18N
        self.listN[19] = p_19N
        self.listN[20] = p_20N
        self.listN[21] = p_21N
        self.listN[22] = p_22N
        self.listN[23] = p_23N
        self.listN[24] = p_24N
        self.listN[25] = p_25N
        self.listN[26] = p_26N
        self.listN[27] = p_27N
        self.listN[28] = p_28N
        self.listN[29] = p_29N
        self.listN[30] = p_30N
        self.listN[31] = p_31N
        self.listN[32] = p_32N
        self.listN[33] = p_33N
        self.listN[34] = p_34N
        self.listN[35] = p_35N
        self.listN[36] = p_36N
        self.listN[37] = p_37N
        self.listN[38] = p_38N
        self.listN[39] = p_39N
        self.listN[40] = p_40N
        self.listN[41] = p_41N
        self.listN[42] = p_42N
        self.listN[43] = p_43N
        self.listN[44] = p_44N
        self.listN[45] = p_45N
        self.listN[46] = p_46N
        self.listN[47] = p_47N
        self.listN[48] = p_48N
        self.listN[49] = p_49N
        self.listN[50] = p_50N
        self.listN[51] = p_51N
        self.listN[52] = p_52N
        self.listN[53] = p_53N
        self.listN[54] = p_54N
        self.listN[55] = p_55N
        self.listN[56] = p_56N
        self.listN[57] = p_57N
        self.listN[58] = p_58N
        self.listN[59] = p_59N
        self.listN[60] = p_60N

        self.listS[0] = p_wgs84
        self.listS[1] = p_1S
        self.listS[2] = p_2S
        self.listS[3] = p_3S
        self.listS[4] = p_4S
        self.listS[5] = p_5S
        self.listS[6] = p_6S
        self.listS[7] = p_7S
        self.listS[8] = p_8S
        self.listS[9] = p_9S
        self.listS[10] = p_10S
        self.listS[11] = p_11S
        self.listS[12] = p_12S
        self.listS[13] = p_13S
        self.listS[14] = p_14S
        self.listS[15] = p_15S
        self.listS[16] = p_16S
        self.listS[17] = p_17S
        self.listS[18] = p_18S
        self.listS[19] = p_19S
        self.listS[20] = p_20S
        self.listS[21] = p_21S
        self.listS[22] = p_22S
        self.listS[23] = p_23S
        self.listS[24] = p_24S
        self.listS[25] = p_25S
        self.listS[26] = p_26S
        self.listS[27] = p_27S
        self.listS[28] = p_28S
        self.listS[29] = p_29S
        self.listS[30] = p_30S
        self.listS[31] = p_31S
        self.listS[32] = p_32S
        self.listS[33] = p_33S
        self.listS[34] = p_34S
        self.listS[35] = p_35S
        self.listS[36] = p_36S
        self.listS[37] = p_37S
        self.listS[38] = p_38S
        self.listS[39] = p_39S
        self.listS[40] = p_40S
        self.listS[41] = p_41S
        self.listS[42] = p_42S
        self.listS[43] = p_43S
        self.listS[44] = p_44S
        self.listS[45] = p_45S
        self.listS[46] = p_46S
        self.listS[47] = p_47S
        self.listS[48] = p_48S
        self.listS[49] = p_49S
        self.listS[50] = p_50S
        self.listS[51] = p_51S
        self.listS[52] = p_52S
        self.listS[53] = p_53S
        self.listS[54] = p_54S
        self.listS[55] = p_55S
        self.listS[56] = p_56S
        self.listS[57] = p_57S
        self.listS[58] = p_58S
        self.listS[59] = p_59S
        self.listS[60] = p_60S

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

    def convert_UTM_to_degree(self, point):
        zone = point.zone
        if point.hemisphere == Hemisphere.NORTH:
            longitude, latitude = self.listN[zone](point.easting, point.northing, inverse=True)
        else:
            longitude, latitude = self.listN[zone](point.easting, point.northing, inverse=True)
        return points.WGSPoint(longitude, 0, 0, latitude, 0, 0)

    def convert_degree_to_UTM(self, point):
        long_deg = point.long_deg
        lat_deg = point.lat_deg

        zone, letter = self.__define_UTM_zone(point)

        p = pyproj.Proj(proj='utm', zone=zone, ellps='WGS84')
        easting, northing = p(long_deg, lat_deg)
        if lat_deg > 0:
            hemisphere = Hemisphere.NORTH
        else:
            hemisphere = Hemisphere.SOUTH
        return points.UTMPoint(int(easting), int(northing), int(zone), hemisphere)

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
