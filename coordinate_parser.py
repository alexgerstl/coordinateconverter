# -*- coding: utf-8 -*-
from os.path import expanduser
home = expanduser("~")
enum_path = home + '\.qgis2\python\plugins\CoordinatesConverter\lib\enum34-1.1.6-py2.7.egg'

import sys
sys.path.insert(0,enum_path)
import enum
import points
import exceptions
from decimal import Decimal





class Guess:
    def __init__(self, coord_format, status):
        self.coordFormat = coord_format
        self.status = status

    @staticmethod
    def invalid_unknown():
        return Guess(None, ParserStatus.INVALID)

    @staticmethod
    def new_valid(coord_format):
        return Guess(coord_format, ParserStatus.VALID)

    @staticmethod
    def new_incomplete(coord_format):
        return Guess(coord_format, ParserStatus.INCOMPLETE)

    @staticmethod
    def new_invalid(coord_format):
        return Guess(coord_format, ParserStatus.INVALID)


class Parser:
    def __init__(self):
        self.directions = ['N', 'S', 'E', 'W']
        self.white_list = ['-', ' ', '.', u'\xb0', '"', '\'']
        self.guessed_system = None
        self.format = None

    @staticmethod
    def count_letters(string):
        count = 0
        for char in string:
            if char.isalpha():
                count += 1
        return count

    @staticmethod
    def all_in(chars, char_array):
        for char1 in chars:
            found = False
            for char2 in char_array:
                if char1.lower() == char2.lower():
                    found = True
                    break
            if not found:
                return False
        return True

    @staticmethod
    def letters(input_string):
        result = []
        for char in input_string:
            if char.isalpha():
                result.append(char)
        return result

    def parse(self, to_parse):
        if to_parse is None or len(to_parse) == 0:
            raise exceptions.ParseException('Empty', 0, ParserStatus.INVALID)
        trimmed = to_parse.strip()
        if len(trimmed) == 0:
            raise exceptions.ParseException('Empty', 0, ParserStatus.INCOMPLETE)
        illegal_char_index = self.__index_of_first_illegal_char(to_parse)
        if illegal_char_index != -1:
            raise exceptions.ParseException('Invalid Symbol \'' + trimmed[illegal_char_index] + '\'', 0,
                                            ParserStatus.INCOMPLETE)

        guess = Parser.guess_system(self, to_parse)
        parse_status = guess.status
        guessed_format = guess.coordFormat
        self.guessed_system = guessed_format

        if self.guessed_system == Guess.invalid_unknown() or parse_status is None:
            raise exceptions.ParseException('Unknown coordinate system', 0, ParserStatus.INVALID)

        if parse_status == ParserStatus.INCOMPLETE:
            if guessed_format is None:
                raise exceptions.ParseException('Incomplete input', 0, ParserStatus.INCOMPLETE)
            raise exceptions.ParseException('Incomplete input. Possible format: \'' + str(guessed_format) + '\'', 0,
                                            ParserStatus.INCOMPLETE)

        if parse_status == ParserStatus.INVALID:
            if guessed_format is None:
                raise exceptions.ParseException('Unknown coordinate system', 0, ParserStatus.INVALID)
            raise exceptions.ParseException('Invalid ' + guessed_format.coordFormat(self), 0, ParserStatus.INVALID)

        if parse_status == ParserStatus.VALID:
            if guessed_format == CoordinateSystemString.MGRS:
                return Parser.parse_MGRS(self, to_parse)
            if guessed_format == CoordinateSystemString.UTM:
                return Parser.parse_UTM(self, to_parse)
            if guessed_format == CoordinateSystemString.WGS84_Degrees or guessed_format == CoordinateSystemString.WGS84_CommaMinutes or guessed_format == CoordinateSystemString.WGS84_DMS:
                return Parser.parse_WGS(self, to_parse)

    def parse_MGRS(self, to_parse):
        no_space = to_parse.upper().replace(" ", "")
        if len(no_space) >= 2:
            zone = no_space[0:3]
            zone_temp = int(zone[0:2])
            if zone_temp < 1 or zone_temp > 60:
                raise exceptions.ParseException('Invalid Zone: ' + str(zone_temp) +
                                                ' in MGRS-String (zone must be between 1 and 60)', 0,
                                                ParserStatus.INVALID)

        letter_count = Parser.count_letters(no_space)
        if letter_count < 3:
            raise exceptions.ParseException("", 0, ParserStatus.INCOMPLETE)

        if len(no_space) < 5:
            raise exceptions.ConversionException('Invalid MGRS-String: "' + no_space +
                                                 '" (valid string: e.g. 33UVP3000082000)')
        else:
            lat_zone = ord(no_space[2])
            if lat_zone >= ord('N'):
                hemisphere = Hemisphere.NORTH
            else:
                hemisphere = Hemisphere.SOUTH

            if lat_zone < 67 or lat_zone > 88 or lat_zone == 73 or lat_zone == 79:
                raise exceptions.ParseException('Invalid latitude grid-zone: ' + chr(lat_zone) +
                                                ' in MGRS-String (accepted values: C-X omitting I and O)',
                                                0, ParserStatus.INVALID)

            if lat_zone == ord('X') and (zone_temp == 32 or zone_temp == 34 or zone_temp == 36):
                raise exceptions.ParseException('Invalid grid zone designation: grid zone ' + str(zone_temp) + ' ' +
                                                chr(lat_zone) + ' does not exist.', 0, ParserStatus.INVALID)

            zone_fields = ['STUVWXYZ', 'ABCDEFGH', 'JKLMNPQR']
            zone_fields_lat = 'ABCDEFGHJKLMNPQRSTUV'

            square = no_space[3:5]
            squares_x = square[0] in zone_fields[zone_temp % 3]
            squares_y = square[1] in zone_fields_lat

            if squares_x is False:
                raise exceptions.ParseException('Invalid easting letter for 100x100km grid square: ' + square[0] +
                                                ' (value has to be one of the letters: ' +
                                                zone_fields[zone_temp % 3] + ')', 0, ParserStatus.INVALID)
            if squares_y is False:
                raise exceptions.ParseException('Invalid northing letter for 100x100km grid square: ' + square[1] +
                                                ' (value has to be one of the letters: ' + zone_fields_lat + ')', 0,
                                                ParserStatus.INVALID)

        if len(no_space) == 15:
            easting = int(no_space[5:10])
            northing = int(no_space[10:])
            return points.MGRSPoint(easting, northing, zone, square, hemisphere)
        else:
            if len(no_space) < 15:
                temp = no_space[5:]
                if len(temp) % 2 == 0:
                    easting_temp = str(temp[:len(temp)/2])
                    northing_temp = str(temp[len(temp)/2:])
                    while len(easting_temp) < 5:
                        easting_temp += '0'
                        northing_temp += '0'
                    return points.MGRSPoint(int(easting_temp), int(northing_temp), zone, square, hemisphere)
                else:
                    raise exceptions.ParseException('Missing valid easting/northing values', 0, ParserStatus.INVALID)
            raise exceptions.ParseException('Missing valid easting/northing values', 0, ParserStatus.INVALID)

    def parse_UTM(self, to_parse):
        no_space = to_parse.replace(" ", "").upper()
        hemisphere_char = ' '
        hemisphere_index = -1
        hemisphere = ''

        for i in range(0, len(no_space)):
            if no_space[i].isalpha():
                hemisphere_char = no_space[i].upper()
                hemisphere_index = i
                break

        if hemisphere_char != 'N' and hemisphere_char != 'S':
            raise exceptions.ParseException('Excepted hemisphere \'N\' or \'S\'.', 0, ParserStatus.INCOMPLETE)
        else:
            if hemisphere_char == 'N':
                hemisphere = Hemisphere.NORTH
            elif hemisphere_char == 'S':
                hemisphere = Hemisphere.SOUTH

        zone = int(no_space[0:hemisphere_index])
        if zone < 1 or zone > 60:
            raise exceptions.ConversionException('Invalid Zone: ' + str(zone) +
                                                 ' in UTM-String (zone must be between 1 and 60)')

        letter_count = Parser.count_letters(to_parse)
        if letter_count == 1:
            raise exceptions.ParseException('Expected east and north value', 0, ParserStatus.INCOMPLETE)
        else:
            if letter_count == 2:
                if 'E' in no_space:
                    raise exceptions.ParseException('Expected north value', 0, ParserStatus.INCOMPLETE)
                else:
                    raise exceptions.ParseException('Expected east value', 0, ParserStatus.INCOMPLETE)

            if 'E' in no_space:
                east_index = no_space.index('E', hemisphere_index + 1)
            else:
                raise exceptions.ConversionException('Expected \'E\'')
            if 'N' in no_space:
                north_index = no_space.index('N', hemisphere_index + 1)
            else:
                raise exceptions.ConversionException('Expected \'N\'')

            if east_index > north_index:
                northing = int(no_space[hemisphere_index + 1:north_index])
                easting = int(no_space[north_index + 1:east_index])
            else:
                easting = int(no_space[hemisphere_index + 1:east_index])
                northing = int(no_space[east_index + 1:north_index])

            if hemisphere == Hemisphere.NORTH:
                if northing < -9000000 or northing > 9400000:
                    raise exceptions.ParseException('Northing ' + str(northing) + ' is out of range', 0,
                                                    ParserStatus.INVALID)
            else:
                if northing < 1000000 or northing > 19400000:
                    raise exceptions.ParseException('Northing ' + str(northing) + ' is out of range', 0,
                                                    ParserStatus.INVALID)

            return points.UTMPoint(easting, northing, zone, hemisphere)

    def parse_WGS(self, to_parse):
        no_spaces = to_parse.replace(" ", "")
        no_spaces = no_spaces.upper()

        east_index = -1
        west_index = -1
        north_index = -1
        sout_index = -1

        if 'E' in no_spaces:
            east_index = no_spaces.index('E')
        if 'W' in no_spaces:
            west_index = no_spaces.index('W')
        if 'N' in no_spaces:
            north_index = no_spaces.index('N')
        if 'S' in no_spaces:
            sout_index = no_spaces.index('S')

        if east_index == -1 and west_index == -1:
            raise exceptions.ParseException('Expected \'E\' or \'W\'', 0, ParserStatus.INCOMPLETE)
        if north_index == -1 and sout_index == -1:
            raise exceptions.ParseException('Expected \'N\' or \'S\'', 0, ParserStatus.INCOMPLETE)
        if east_index != -1 and west_index != -1:
            raise exceptions.ParseException('Detected both \'E\' and \'W\'', 0, ParserStatus.INVALID)
        if north_index != -1 and sout_index != -1:
            raise exceptions.ParseException('Detected both \'N\' and \'S\'', 0, ParserStatus.INVALID)

        long_index = max(east_index, west_index)
        lat_index = max(north_index, sout_index)
        max_index = max(long_index, lat_index)

        if len(no_spaces) > max_index + 1:
            token = no_spaces[max_index + 1]
            raise exceptions.ParseException('Unrecognized: \'' + token + '\'', max_index + 1, ParserStatus.INVALID)

        if long_index > lat_index:
            if lat_index + 1 == long_index:
                raise exceptions.ParseException('Expected latitude value', 0, ParserStatus.INCOMPLETE)
            latitude = no_spaces[0:lat_index]
            longitude = no_spaces[lat_index + 1:long_index]
        else:
            if long_index + 1 == lat_index:
                raise exceptions.ParseException('Expected longitude value', 0, ParserStatus.INCOMPLETE)
            longitude = no_spaces[0:long_index]
            latitude = no_spaces[long_index + 1:lat_index]

        if east_index == -1:
            if len(longitude) > 0:
                if longitude[0] == '-':
                    longitude = longitude[1:]
                else:
                    longitude = '-' + longitude

        if north_index == -1:
            if len(latitude) > 0:
                if latitude[0] == '-':
                    latitude = latitude[1:]
                else:
                    latitude = '-' + latitude

        if u'\xb0' in longitude and u'\xb0' in latitude and self.guessed_system == CoordinateSystemString.WGS84_Degrees:
            deg_index = longitude.index(u'\xb0')
            long_deg = longitude[:deg_index]
            deg_index = latitude.index(u'\xb0')
            lat_deg = latitude[:deg_index]
            point = points.WGSPoint(float(long_deg), 0, 0, float(lat_deg), 0, 0)
            self.__check_values_of_WGSPoint(point)
            return point
        elif self.guessed_system == CoordinateSystemString.WGS84_Degrees:
            point = points.WGSPoint(float(longitude), 0, 0, float(latitude), 0, 0)
            self.__check_values_of_WGSPoint(point)
            return point
        elif self.guessed_system == CoordinateSystemString.WGS84_CommaMinutes:
            deg_index = longitude.index(u'\xb0')
            min_index = longitude.index('\'')
            long_deg = longitude[:deg_index]
            long_min = longitude[deg_index + 1:min_index]
            deg_index = latitude.index(u'\xb0')
            min_index = latitude.index('\'')
            lat_deg = latitude[:deg_index]
            lat_min = latitude[deg_index + 1:min_index]
            point = points.WGSPoint(float(long_deg), float(long_min), 0, float(lat_deg), float(lat_min), 0)
            self.__check_values_of_WGSPoint(point)
            return point
        elif self.guessed_system == CoordinateSystemString.WGS84_DMS:
            deg_index = longitude.index(u'\xb0')
            min_index = longitude.index('\'')
            sec_index = longitude.index('"')
            long_deg = longitude[:deg_index]
            long_min = longitude[deg_index + 1:min_index]
            long_sec = longitude[min_index + 1:sec_index]
            deg_index = latitude.index(u'\xb0')
            min_index = latitude.index('\'')
            sec_index = latitude.index('"')
            lat_deg = latitude[:deg_index]
            lat_min = latitude[deg_index + 1:min_index]
            lat_sec = latitude[min_index + 1:sec_index]
            point = points.WGSPoint(int(long_deg), int(long_min), Decimal(long_sec), int(lat_deg), int(lat_min), Decimal(lat_sec))
            self.__check_values_of_WGSPoint(point)
            return point

    def guess_system(self, input_string):
        trimmed = input_string.strip()
        no_spaces = trimmed.replace(" ", "")
        letters = self.letters(no_spaces)
        letter_count = len(letters)
        length = len(no_spaces)

        first_char = ' '
        second_char = ' '
        third_char = ' '
        fourth_char = ' '
        fifth_char = ' '

        if length >= 5:
            fifth_char = no_spaces.upper()[4]
        if length >= 4:
            fourth_char = no_spaces.upper()[3]
        if length >= 3:
            third_char = no_spaces.upper()[2]
        if length >= 2:
            second_char = no_spaces.upper()[1]
        if length >= 1:
            first_char = no_spaces.upper()[0]
        if length == 0:
            return Guess.invalid_unknown()

        if first_char == '-':
            return Parser.guess_WGS(self, trimmed)

        if first_char.isalpha():
            return Guess.invalid_unknown()

        ''' First char is digit'''
        if second_char.isdigit():
            if third_char.isalpha():
                if third_char in self.directions:
                    if length == 3:
                        return Guess.new_incomplete(None)

                    if fourth_char.isalpha():
                        if length > 4 and not fifth_char.isalpha():
                            return Guess.new_valid(CoordinateSystemString.MGRS)
                        return Guess.new_valid(CoordinateSystemString.MGRS)

                    if Parser.all_in(letters, self.directions):
                        if letter_count == 2:
                            return Parser.guess_WGS(self, trimmed)

                        if third_char == 'N' or third_char == 'S':
                            return Guess.new_valid(CoordinateSystemString.UTM)

                        return Parser.guess_WGS(self, trimmed)

                    return Guess.new_valid(CoordinateSystemString.MGRS)
                return Guess.new_valid(CoordinateSystemString.MGRS)

        if second_char == 'N' or second_char == 'S':
            if letter_count == 2 and Parser.all_in(letters, self.directions):
                return Parser.guess_WGS(self, trimmed)
            return Guess.new_valid(CoordinateSystemString.UTM)

        if u'\xb0' in no_spaces:
            return Parser.guess_WGS(self, trimmed)

        if length <= 2:
            return Guess.new_incomplete(None)

        if letter_count == 0:
            return Guess.new_incomplete(None)

        return Parser.guess_WGS(self, trimmed)

    def guess_WGS(self, input_string):
        coord_format = CoordinateSystemString.WGS84_Degrees
        contains_degree = u'\xb0' in input_string
        contains_minutes = '\'' in input_string
        contains_seconds = '"' in input_string

        if contains_degree and contains_minutes and contains_seconds:
            coord_format = CoordinateSystemString.WGS84_DMS

        if contains_degree and contains_minutes and not contains_seconds:
            coord_format = CoordinateSystemString.WGS84_CommaMinutes

        if contains_degree and contains_seconds and not contains_minutes:
            raise exceptions.ParseException('Missing minutes value', 0, ParserStatus.INVALID)

        return Guess.new_valid(coord_format)

    def __index_of_first_illegal_char(self, string):
        is_ok = True

        for i in range(0, len(string)):
            if string[i].isdigit():
                # all good
                continue
            elif string[i].isalpha():
                char_int = ord(string[i].lower())
                if char_int < ord('a') or char_int > ord('z'):
                    is_ok = False
            else:
                # no digit, no letter
                in_white_list = False
                if string[i] in self.white_list:
                    in_white_list = True
                    break
                is_ok = in_white_list
            if not is_ok:
                return i
        return -1

    def check_values_of_WGSPoint(self, point):
        if point.long_deg < -180 or point.long_deg > 180:
            raise exceptions.ParseException('Degree value of longitude ' + str(point.long_deg) +
                                            ' out of range (-180...+180)', 0, ParserStatus.INVALID)
        if point.lat_deg < -90 or point.lat_deg > 90:
            raise exceptions.ParseException('Degree value of latitude ' + str(point.lat_deg) +
                                            ' out of range (-90...+90)', 0, ParserStatus.INVALID)
        if point.long_min < 0 or point.long_min >= 60:
            raise exceptions.ParseException('Minutes value of longitude ' + str(point.long_min) +
                                            ' out of range (0...59)', 0, ParserStatus.INVALID)
        if point.lat_min < 0 or point.lat_min >= 60:
            raise exceptions.ParseException('Minutes value of latitude ' + str(point.lat_min) +
                                            ' out of range (0...59)', 0, ParserStatus.INVALID)
        if point.long_sec < 0 or point.long_sec >= 60:
            raise exceptions.ParseException('Seconds value of longitude ' + str(point.long_sec) +
                                            ' out of range (0...59)', 0, ParserStatus.INVALID)
        if point.lat_sec < 0 or point.lat_sec >= 60:
            raise exceptions.ParseException('Seconds value of latitude ' + str(point.lat_sec) +
                                            ' out of range (0...59)', 0, ParserStatus.INVALID)