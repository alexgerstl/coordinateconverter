import sys
import exceptions
from os.path import expanduser
home = expanduser("~")
enum_path = home + '\.qgis2\python\plugins\CoordinatesConverter\lib\enum34-1.1.6-py2.7.egg'

sys.path.insert(0,enum_path)
import enum


class CoordinateSystemString(enum.Enum):
    MGRS = 'MGRS'
    UTM = 'UTM'
    WGS84_Degrees = 'WGS_DEGREES'
    WGS84_DMS = 'WGS_DMS'
    WGS84_CommaMinutes = 'WGS_COMMA'


class Hemisphere(enum.Enum):
    NORTH = 'N'
    SOUTH = 'S'


class Ensurer:
    def __init__(self):
        self.white_list_1 = ['-', ' ', '.', ',']
        self.white_list_2 = [' ', '.', ',']

    def ensure_it_is_a_number(self, string):
        """Ensures string can be parsed to a positive or negative number."""
        trimmed = string.strip()
        if len(trimmed) == 0:
            trimmed = '0'
        no_space = trimmed.replace(' ', '')
        if ',' in no_space:
            replaced = no_space.replace(',', '.')
        else:
            replaced = no_space
        illegal_char_index = self.__index_of_first_illegal_char(replaced, 1)
        if illegal_char_index != -1:
            raise exceptions.ParseException('Invalid Symbol \'' + replaced[illegal_char_index] + '\'')

        if len(replaced) > 10:
            replaced = replaced[:11]
        if not self.__is_positive(replaced):
            final = replaced.replace('-', '0')
            return float(final) * -1
        return float(replaced)

    def ensure_it_is_a_positive_number(self, string):
        """Ensures string can be parsed to a positive number."""
        trimmed = string.strip()
        if len(trimmed) == 0:
            trimmed = '0'
        no_space = trimmed.replace(' ', '')
        if ',' in no_space:
            replaced = no_space.replace(',', '.')
        else:
            replaced = no_space
        illegal_char_index = self.__index_of_first_illegal_char(replaced, 2)
        if illegal_char_index != -1:
            raise exceptions.ParseException('Invalid Symbol \'' + replaced[illegal_char_index] + '\'')
        if len(replaced) > 10:
            replaced = replaced[:11]
        return float(replaced)

    def ensure_it_is_an_integer(self, string):
        """Ensures string can be parsed to a positive or negative integer."""
        trimmed = string.strip()
        if len(trimmed) == 0:
            trimmed = '0'
        no_space = trimmed.replace(' ', '')
        if ',' in no_space or '.' in no_space:
            raise exceptions.ParseException('Wert muss ganzzahlig sein')
        illegal_char_index = self.__index_of_first_illegal_char(no_space, 1)
        if illegal_char_index != -1:
            raise exceptions.ParseException('Invalid Symbol \'' + no_space[illegal_char_index] + '\'')

        if not self.__is_positive(no_space):
            final = no_space.replace('-', '0')
            return int(final) * -1
        return int(no_space)

    def ensure_it_is_a_positive_integer(self, string):
        """Ensures string can be parsed to a positive integer."""
        trimmed = string.strip()
        if len(trimmed) == 0:
            trimmed = '0'
        no_space = trimmed.replace(' ', '')
        if ',' in no_space or '.' in no_space:
            raise exceptions.ParseException('Wert muss ganzzahlig sein')
        illegal_char_index = self.__index_of_first_illegal_char(no_space, 2)
        if illegal_char_index != -1:
            raise exceptions.ParseException('Invalid Symbol \'' + no_space[illegal_char_index] + '\'')
        return int(no_space)

    def ensure_longitude_in_range(self, longitude):
        if longitude < -180 or longitude > 180:
            raise exceptions.ParseException('Degree value of longitude out of range (-180...+180)')

    def ensure_latitude_in_range(self, latitude):
        if latitude < -90 or latitude > 90:
            raise exceptions.ParseException('Degree value of latitude out of range (-90...+90)')

    def ensure_minutes_in_range(self, minutes):
        if minutes < 0 or minutes >= 60:
            raise exceptions.ParseException('Minutes value of longitude out of range (0...59)')

    def ensure_seconds_in_range(self, seconds):
        if seconds < 0 or seconds >= 60:
            raise exceptions.ParseException('Seconds value of longitude out of range (0...59)')

    def ensure_utm_zone_in_range(self, zone):
        if not 1 <= zone <= 60:
            raise exceptions.ParseException('UTM zone value out of range (1...60)')

    def ensure_utm_easting_in_range(self, easting):
        if not 100000 <= easting < 1000000:
            raise exceptions.ParseException('easting out of range (must be between 100 000 m and 999 999 m)')

    def ensure_utm_northing_in_range(self, northing):
        if not 0 <= northing <= 10000000:
            raise exceptions.ParseException('northing out of range (must be between 0 m and 10 000 000 m)')

    def __is_positive(self, string):
        if string.startswith('-'):
            return False
        return True

    def __index_of_first_illegal_char(self, string, list_number):
        is_ok = True
        if list_number == 1:
            list = self.white_list_1
        else:
            list = self.white_list_2

        for i in range(0, len(string)):
            if string[i].isdigit():
                # all good
                continue
            elif string[i].isalpha():
                char_int = ord(string[i].lower())
                if char_int < ord('a') or char_int > ord('z'):
                    return i
                return i
            else:
                # no digit, no letter
                in_white_list = False
                if string[i] in list:
                    in_white_list = True
                    continue
                is_ok = in_white_list

        if not is_ok:
            return i
        return -1
