# -*- coding: utf-8 -*-
import sys
import exceptions
from os.path import expanduser
home = expanduser("~")
enum_path = home + '\.qgis2\python\plugins\CoordinatesConverter\lib\enum34-1.1.6-py2.7.egg'
sys.path.insert(0, enum_path)
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
INVALID_SYMBOL_ERROR_DE = "ung" + u'\xFC' + "ltiges Symbol".decode('UTF-8')
INVALID_SYMBOL_ERROR_EN = "invalid symbol"
VALUE_HAS_TO_BE_INTEGER_DE = "Wert muss ganzzahlig sein"
VALUE_HAS_TO_BE_INTEGER_EN = "Value has to be an integer"
INPUT_TO_LONG_DE = "Eingabe ist zu lange"
INPUT_TO_LONG_EN = "input is too long"
ZONE_HAS_TO_START_WITH_NUMBER_DE = "Zone muss mit einer Zahl beginnen"
ZONE_HAS_TO_START_WITH_NUMBER_EN = "zone has to start with a number"
ZONE_HAS_TO_CONTAIN_TWO_NUMBERS_DE = "Zone muss aus zwei Ziffern bestehen"
ZONE_HAS_TO_CONTAIN_TWO_NUMBERS_EN = "first two numbers of zone has to be numbers"
ZONE_HAS_TO_CONTAIN_TWO_NUMBERS_AND_A_LETTER_DE = "Zone muss aus zwei Ziffern und einem Buchstaben bestehen"
ZONE_HAS_TO_CONTAIN_TWO_NUMBERS_AND_A_LETTER_EN = "zone has to contain two numbers and a letter"
SQUARE_HAS_TO_START_WITH_DE = "Gitterquadrat muss mit Buchstaben beginnen"
SQUARE_HAS_TO_START_WITH_EN = "square has to start with a letter"
SQUARE_HAS_TO_BE_TWO_LETTERS_DE = "Gitterquadrat muss aus zwei Buchstaben bestehen"
SQUARE_HAS_TO_BE_TWO_LETTERS_EN = "square has to be two letters"
INPUT_NOT_COMPLETE_DE = "Eingabe noch nicht vollst" + u'\xE4' +"ndig"
INPUT_NOT_COMPLETE_EN = "input not completed"
INVALID_LAT_GRID_ZONE_DE = "Ung" + u'\xFC' + "ltige MGRS-Zone: {0} (g" + u'\xFC' + "ltige Werte: C-X außer I und O)".decode('UTF-8')
INVALID_LAT_GRID_ZONE_EN = "Invalid MGRS zone: {0} (accepted values: C-X omitting I and O)"
INVALID_MGRS_SQUARE_LETTRES_DE = "Ung" + u'\xFC' + "ltige Zone-Gitterquadrat-Kombination. Zone: '{0}' ung" + u'\xFC' + "ltig: '{1}'"
INVALID_MGRS_SQUARE_LETTRES_EN = "Invalid grid zone designation: grid zone '{0}' with '{1}' does not exist."
LONGITUDE_OUT_OF_RANGE_DE = "Wer f" + u'\xFC' + "r L" + u'\xE4' +"ngengrad au" + u'\xDF' + "erhalb des Wertebereiches (-180...+180)"
LONGITUDE_OUT_OF_RANGE_EN = "Degree value of longitude out of range (-180...+180)"
LATITUDE_OUT_OF_RANGE_DE = "Wer f" + u'\xFC' + "r Breitengrad au" + u'\xDF' + "erhalb Wertebereich (-90...+90)"
LATITUDE_OUT_OF_RANGE_EN = "Degree value of latitude out of range (-90...+90)"
MINUTES_OUT_OF_RANGE_DE = "Gradminuten au" + u'\xDF' + "erhalb des Wertebereiches (0...59)"
MINUTES_OUT_OF_RANGE_EN = "Minutes value out of range (0...59)"
SECONDS_OUT_OF_RANGE_DE = "Gradsekunden au" + u'\xDF' + "erhalb des Wertebereiches (0...59)"
SECONDS_OUT_OF_RANGE_EN = "Seconds value out of range (0...59)"
ZONE_OUT_OF_RANGE_DE = "Zone au" + u'\xDF' + "erhalb des Wertebereiches (0...60)"
ZONE_OUT_OF_RANGE_EN = "zone out of range (0...60)"
UTM_EASTING_OUT_OF_RANGE_DE = "Ostwert au" + u'\xDF' + "erhalb des Wertebereiches (100 000 m ... 999 999 m)"
UTM_EASTING_OUT_OF_RANGE_EN = "easting out of range (100 000 m ... 999 999 m)"
UTM_NORTHING_OUT_OF_RANGE_DE = "Nordwert au" + u'\xDF' + "erhalb des Wertebereiches (0 m ... 10 000 000 m)"
UTM_NORTHING_OUT_OF_RANGE_EN = "northing out of range (0 m ... 10 000 000 m)"
MGRS_EASTING_OUT_OF_RANGE_DE = "Ostwert au" + u'\xDF' + "erhalb des Wertebereiches (0 m ... 99 999 m)"
MGRS_EASTING_OUT_OF_RANGE_EN = "easting out of range (0 m ... 99 999 m)"
MGRS_NORTHING_OUT_OF_RANGE_DE = "Nordwert au" + u'\xDF' + "erhalb des Wertebereiches (0 m ... 99 999 m)"
MGRS_NORTHING_OUT_OF_RANGE_EN = "northing out of range (0 m ... 99 999 m)"


def ensure_it_is_a_number(string, german):
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
        if german:
            raise exceptions.ParseException(INVALID_SYMBOL_ERROR_DE + " '" + replaced[illegal_char_index] + "'")
        else:
            raise exceptions.ParseException(INVALID_SYMBOL_ERROR_EN + " '" + replaced[illegal_char_index] + "'")

    if len(replaced) > 10:
        replaced = replaced[:11]
    if not __is_positive(replaced):
        final = replaced.replace('-', '0')
        return float(final) * -1
    return float(replaced)


def ensure_it_is_a_positive_number(string, german):
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
        if german:
            raise exceptions.ParseException(INVALID_SYMBOL_ERROR_DE + " '" + replaced[illegal_char_index] + "'")
        else:
            raise exceptions.ParseException(INVALID_SYMBOL_ERROR_EN + " '" + replaced[illegal_char_index] + "'")
    if len(replaced) > 10:
        replaced = replaced[:11]
    return float(replaced)


def ensure_it_is_an_integer(string, german):
    """Ensures string can be parsed to a positive or negative integer."""
    trimmed = string.strip()
    if len(trimmed) == 0:
        trimmed = '0'
    no_space = trimmed.replace(' ', '')
    if ',' in no_space or '.' in no_space:
        raise exceptions.ParseException('Wert muss ganzzahlig sein')
    illegal_char_index = __index_of_first_illegal_char_number_only(no_space, 1)
    if illegal_char_index != -1:
        if german:
            raise exceptions.ParseException(INVALID_SYMBOL_ERROR_DE + " '" + no_space[illegal_char_index] + "'")
        else:
            raise exceptions.ParseException(INVALID_SYMBOL_ERROR_EN + " '" + no_space[illegal_char_index] + "'")

    if not __is_positive(no_space):
        final = no_space.replace('-', '0')
        return int(final) * -1
    return int(no_space)


def ensure_it_is_a_positive_integer(string, german):
    """Ensures string can be parsed to a positive integer."""
    trimmed = string.strip()
    if len(trimmed) == 0:
        trimmed = '0'
    no_space = trimmed.replace(' ', '')
    if ',' in no_space or '.' in no_space:
        if german:
            raise exceptions.ParseException(VALUE_HAS_TO_BE_INTEGER_DE)
        else:
            raise exceptions.ParseException(VALUE_HAS_TO_BE_INTEGER_EN)
    illegal_char_index = __index_of_first_illegal_char_number_only(no_space, 2)
    if illegal_char_index != -1:
        if german:
            raise exceptions.ParseException(INVALID_SYMBOL_ERROR_DE + " '" + no_space[illegal_char_index] + "'")
        else:
            raise exceptions.ParseException(INVALID_SYMBOL_ERROR_EN + " '" + no_space[illegal_char_index] + "'")
    return int(no_space)


def ensure_it_is_a_valid_mgrs_zone(string, german):
    """Ensures string consists of 2 digits and a letter"""
    trimmed = string.strip()
    no_space = trimmed.replace(' ', '').upper()
    if len(no_space) > 3:
        if german:
            raise exceptions.ParseException(INPUT_TO_LONG_DE)
        else:
            raise exceptions.ParseException(INPUT_TO_LONG_EN)
    for i in range(0, len(no_space)):
        if i == 0:
            if no_space[i].isdigit():
                continue
            else:
                if german:
                    raise exceptions.ParseException(ZONE_HAS_TO_START_WITH_NUMBER_DE)
                else:
                    raise exceptions.ParseException(ZONE_HAS_TO_START_WITH_NUMBER_EN)
        elif i == 1:
            if no_space[i].isdigit():
                continue
            else:
                if german:
                    raise exceptions.ParseException(ZONE_HAS_TO_CONTAIN_TWO_NUMBERS_DE)
                else:
                    raise exceptions.ParseException(ZONE_HAS_TO_CONTAIN_TWO_NUMBERS_EN)
        else:
            if no_space[i].isalpha():
                char_int = ord(no_space[i].lower())
                if char_int < ord('a') or char_int > ord('z'):
                    if german:
                        raise exceptions.ParseException(INVALID_SYMBOL_ERROR_DE + " '" + no_space[i] + "'")
                    else:
                        raise exceptions.ParseException(INVALID_SYMBOL_ERROR_EN + " '" + no_space[i] + "'")

                lat_zone = ord(no_space[2])
                zone_temp = int(no_space[:2])
                if lat_zone < 67 or lat_zone > 88 or lat_zone == 73 or lat_zone == 79:
                    if german:
                        raise exceptions.ParseException(INVALID_LAT_GRID_ZONE_DE.format(chr(lat_zone)))
                    else:
                        raise exceptions.ParseException(INVALID_LAT_GRID_ZONE_EN.format(chr(lat_zone)))
                if lat_zone == ord('X') and (zone_temp == 32 or zone_temp == 34 or zone_temp == 36):
                    if german:
                        raise exceptions.ParseException(INVALID_MGRS_SQUARE_LETTRES_DE.format(str(zone_temp), chr(lat_zone)))
                    else:
                        raise exceptions.ParseException(INVALID_MGRS_SQUARE_LETTRES_EN.format(str(zone_temp), chr(lat_zone)))
            else:
                if german:
                    raise exceptions.ParseException(ZONE_HAS_TO_CONTAIN_TWO_NUMBERS_AND_A_LETTER_DE)
                else:
                    raise exceptions.ParseException(ZONE_HAS_TO_CONTAIN_TWO_NUMBERS_AND_A_LETTER_EN)
    if len(no_space) != 3:
        if german:
            raise exceptions.ParseException(INPUT_NOT_COMPLETE_DE)
        else:
            raise exceptions.ParseException(INPUT_NOT_COMPLETE_EN)
    return no_space


def ensure_it_is_a_valid_mgrs_square(string, german):
    """Ensures string consists of 2 letters"""
    trimmed = string.strip()
    no_space = trimmed.replace(' ', '').upper()
    if len(no_space) > 2:
        if german:
            raise exceptions.ParseException(INPUT_TO_LONG_DE)
        else:
            raise exceptions.ParseException(INPUT_TO_LONG_EN)
    for i in range(0, len(no_space)):
        if i == 0:
            if no_space[i].isalpha():
                continue
            else:
                if german:
                    raise exceptions.ParseException(SQUARE_HAS_TO_START_WITH_DE)
                else:
                    raise exceptions.ParseException(SQUARE_HAS_TO_START_WITH_EN)
        elif i == 1:
            if no_space[i].isalpha():
                continue
            else:
                if german:
                    raise exceptions.ParseException(SQUARE_HAS_TO_BE_TWO_LETTERS_DE)
                else:
                    raise exceptions.ParseException(SQUARE_HAS_TO_BE_TWO_LETTERS_EN)
        else:
            if no_space[i].isalpha() or no_space[i].isdigit():
                char_int = ord(no_space[i].lower())
                if char_int < ord('a') or char_int > ord('z'):
                    if german:
                        raise exceptions.ParseException(INVALID_SYMBOL_ERROR_DE + no_space[i])
                    else:
                        raise exceptions.ParseException(INVALID_SYMBOL_ERROR_EN + no_space[i])
    if len(no_space) != 2:
        if german:
            raise exceptions.ParseException(INPUT_NOT_COMPLETE_DE)
        else:
            raise exceptions.ParseException(INPUT_NOT_COMPLETE_EN)
    return no_space


def ensure_longitude_in_range(longitude, german):
    if longitude < -180 or longitude > 180:
        if german:
            raise exceptions.ParseException(LONGITUDE_OUT_OF_RANGE_DE)
        else:
            raise exceptions.ParseException(LONGITUDE_OUT_OF_RANGE_EN)


def ensure_latitude_in_range(latitude, german):
    if latitude < -90 or latitude > 90:
        if german:
            raise exceptions.ParseException(LATITUDE_OUT_OF_RANGE_DE)
        else:
            raise exceptions.ParseException(LATITUDE_OUT_OF_RANGE_EN)


def ensure_minutes_in_range(minutes, german):
    if minutes < 0 or minutes >= 60:
        if german:
            raise exceptions.ParseException(MINUTES_OUT_OF_RANGE_DE)
        else:
            raise exceptions.ParseException(MINUTES_OUT_OF_RANGE_EN)


def ensure_seconds_in_range(seconds, german):
    if seconds < 0 or seconds >= 60:
        if german:
            raise exceptions.ParseException(SECONDS_OUT_OF_RANGE_DE)
        else:
            raise exceptions.ParseException(SECONDS_OUT_OF_RANGE_EN)


def ensure_zone_in_range(zone, german):
    if not 1 <= zone <= 60:
        if german:
            raise exceptions.ParseException(ZONE_OUT_OF_RANGE_DE)
        else:
            raise exceptions.ParseException(ZONE_OUT_OF_RANGE_EN)


def ensure_utm_easting_in_range(easting, german):
    if not 100000 <= easting < 1000000:
        if german:
            raise exceptions.ParseException(UTM_EASTING_OUT_OF_RANGE_DE)
        else:
            raise exceptions.ParseException(UTM_EASTING_OUT_OF_RANGE_EN)


def ensure_utm_northing_in_range(northing, german):
    if not 0 <= northing <= 10000000:
        if german:
            raise exceptions.ParseException(UTM_NORTHING_OUT_OF_RANGE_DE)
        else:
            raise exceptions.ParseException(UTM_NORTHING_OUT_OF_RANGE_EN)


def ensure_mgrs_easting_in_range(easting, german):
    if not 0 <= easting < 100000:
        if german:
            raise exceptions.ParseException(MGRS_EASTING_OUT_OF_RANGE_DE)
        else:
            raise exceptions.ParseException(MGRS_EASTING_OUT_OF_RANGE_EN)


def ensure_mgrs_northing_in_range(northing, german):
    if not 0 <= northing < 100000:
        if german:
            raise exceptions.ParseException(MGRS_NORTHING_OUT_OF_RANGE_DE)
        else:
            raise exceptions.ParseException(MGRS_NORTHING_OUT_OF_RANGE_EN)


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
