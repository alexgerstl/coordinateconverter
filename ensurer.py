# -*- coding: utf-8 -*-
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


white_list_1 = ['-', ' ', '.', ',']
white_list_2 = [' ', '.', ',']


def ensure_it_is_a_number(string):
    """Ensures string can be parsed to a positive or negative number."""
    trimmed = string.strip()
    if len(trimmed) == 0:
        trimmed = '0'
    no_space = trimmed.replace(' ', '')
    if ',' in no_space:
        replaced = no_space.replace(',', '.')
    else:
        replaced = no_space
    illegal_char_index = __index_of_first_illegal_char_number_only(replaced, 1)
    if illegal_char_index != -1:
        raise exceptions.ParseException('Invalid Symbol \'' + replaced[illegal_char_index] + '\'')

    if len(replaced) > 10:
        replaced = replaced[:11]
    if not __is_positive(replaced):
        final = replaced.replace('-', '0')
        return float(final) * -1
    return float(replaced)


def ensure_it_is_a_positive_number(string):
    """Ensures string can be parsed to a positive number."""
    trimmed = string.strip()
    if len(trimmed) == 0:
        trimmed = '0'
    no_space = trimmed.replace(' ', '')
    if ',' in no_space:
        replaced = no_space.replace(',', '.')
    else:
        replaced = no_space
    illegal_char_index = __index_of_first_illegal_char_number_only(replaced, 2)
    if illegal_char_index != -1:
        raise exceptions.ParseException('Invalid Symbol \'' + replaced[illegal_char_index] + '\'')
    if len(replaced) > 10:
        replaced = replaced[:11]
    return float(replaced)


def ensure_it_is_an_integer(string):
    """Ensures string can be parsed to a positive or negative integer."""
    trimmed = string.strip()
    if len(trimmed) == 0:
        trimmed = '0'
    no_space = trimmed.replace(' ', '')
    if ',' in no_space or '.' in no_space:
        raise exceptions.ParseException('Wert muss ganzzahlig sein')
    illegal_char_index = __index_of_first_illegal_char_number_only(no_space, 1)
    if illegal_char_index != -1:
        raise exceptions.ParseException('Invalid Symbol \'' + no_space[illegal_char_index] + '\'')

    if not __is_positive(no_space):
        final = no_space.replace('-', '0')
        return int(final) * -1
    return int(no_space)


def ensure_it_is_a_positive_integer(string):
    """Ensures string can be parsed to a positive integer."""
    trimmed = string.strip()
    if len(trimmed) == 0:
        trimmed = '0'
    no_space = trimmed.replace(' ', '')
    if ',' in no_space or '.' in no_space:
        raise exceptions.ParseException('Wert muss ganzzahlig sein')
    illegal_char_index = __index_of_first_illegal_char_number_only(no_space, 2)
    if illegal_char_index != -1:
        raise exceptions.ParseException('Invalid Symbol \'' + no_space[illegal_char_index] + '\'')
    return int(no_space)


def ensure_it_is_a_valid_mgrs_zone(string):
    """Ensures string consists of 2 digits and a letter"""
    trimmed = string.strip()
    no_space = trimmed.replace(' ', '').upper()
    if len(no_space) > 3:
        raise exceptions.ParseException('Eingabe zu lange')
    for i in range(0, len(no_space)):
        if i == 0:
            if no_space[i].isdigit():
                continue
            else:
                raise exceptions.ParseException('Zone muss mit Zahl beginnen.')
        elif i == 1:
            if no_space[i].isdigit():
                continue
            else:
                raise exceptions.ParseException('Zone muss aus zwei Ziffern bestehen.')
        else:
            if no_space[i].isalpha():
                char_int = ord(no_space[i].lower())
                if char_int < ord('a') or char_int > ord('z'):
                    raise exceptions.ParseException('Ungültiges Zeichen: ' + no_space[i])

                lat_zone = ord(no_space[2])
                zone_temp = int(no_space[:2])
                if lat_zone < 67 or lat_zone > 88 or lat_zone == 73 or lat_zone == 79:
                    raise exceptions.ParseException('Invalid latitude grid-zone: ' + chr(lat_zone) +
                                                    ' in MGRS-String (accepted values: C-X omitting I and O)')
                if lat_zone == ord('X') and (zone_temp == 32 or zone_temp == 34 or zone_temp == 36):
                    raise exceptions.ParseException(
                        'Invalid grid zone designation: grid zone ' + str(zone_temp) + ' ' +
                        chr(lat_zone) + ' does not exist.')
            else:
                raise exceptions.ParseException('Zone muss aus zwei Ziffern und einem Buchstaben bestehen.')
    if len(no_space) != 3:
        raise exceptions.ParseException('Eingabe noch nicht vollzählig')
    return no_space


def ensure_it_is_a_valid_mgrs_square(string):
    """Ensures string consists of 2 letters"""
    trimmed = string.strip()
    no_space = trimmed.replace(' ', '').upper()
    if len(no_space) > 2:
        raise exceptions.ParseException('Eingabe zu lange')
    for i in range(0, len(no_space)):
        if i == 0:
            if no_space[i].isalpha():
                continue
            else:
                raise exceptions.ParseException('Gitterquadrat muss mit Buchstaben beginnen.')
        elif i == 1:
            if no_space[i].isalpha():
                continue
            else:
                raise exceptions.ParseException('Gitterquadrat muss aus zwei Buchstaben bestehen.')
        else:
            if no_space[i].isalpha() or no_space[i].isdigit():
                char_int = ord(no_space[i].lower())
                if char_int < ord('a') or char_int > ord('z'):
                    raise exceptions.ParseException('Ungültiges Zeichen: ' + no_space[i])
    if len(no_space) != 2:
        raise exceptions.ParseException('Eingabe noch nicht vollzählig')
    return no_space


def ensure_longitude_in_range(longitude):
    if longitude < -180 or longitude > 180:
        raise exceptions.ParseException('Degree value of longitude out of range (-180...+180)')


def ensure_latitude_in_range(latitude):
    if latitude < -90 or latitude > 90:
        raise exceptions.ParseException('Degree value of latitude out of range (-90...+90)')


def ensure_minutes_in_range(minutes):
    if minutes < 0 or minutes >= 60:
        raise exceptions.ParseException('Minutes value of longitude out of range (0...59)')


def ensure_seconds_in_range(seconds):
    if seconds < 0 or seconds >= 60:
        raise exceptions.ParseException('Seconds value of longitude out of range (0...59)')


def ensure_zone_in_range(zone):
    if not 1 <= zone <= 60:
        raise exceptions.ParseException('UTM zone value out of range (1...60)')


def ensure_utm_easting_in_range(easting):
    if not 100000 <= easting < 1000000:
        raise exceptions.ParseException('easting out of range (must be between 100 000 m and 999 999 m)')


def ensure_utm_northing_in_range(northing):
    if not 0 <= northing <= 10000000:
        raise exceptions.ParseException('northing out of range (must be between 0 m and 10 000 000 m)')


def ensure_mgrs_easting_in_range(easting):
    if not 0 <= easting < 100000:
        raise exceptions.ParseException('easting out of range (must be between 0 m and 999 99 m)')


def ensure_mgrs_northing_in_range(northing):
    if not 0 <= northing < 100000:
        raise exceptions.ParseException('northing out of range (must be between 0 m and 999 99 m)')


def __is_positive(string):
    if string.startswith('-'):
        return False
    return True


def __index_of_first_illegal_char_number_only(string, list_number):
    is_ok = True
    if list_number == 1:
        _list = white_list_1
    else:
        _list = white_list_2

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
            if string[i] in _list:
                in_white_list = True
                continue
            is_ok = in_white_list

    if not is_ok:
        return i
    return -1
