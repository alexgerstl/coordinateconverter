# -*- coding: utf-8 -*-
from decimal import Decimal
import ensurer


class MGRSPoint:
    def __init__(self, easting, northing, zone, square, hemisphere):
        self.easting = easting
        self.northing = northing
        self.zone = zone
        self.square = square
        self.hemisphere = hemisphere

    def to_string(self):
        return '{} {} {} {}'.format(self.zone, self.square, self.easting, self.northing)


class UTMPoint:
    def __init__(self, easting, northing, zone_number, zone_letter, hemisphere):
        self.easting = easting
        self.northing = northing
        self.zone_number = zone_number
        self.zone_letter = zone_letter
        self.hemisphere = hemisphere

    def to_string(self):
        if self.hemisphere == ensurer.Hemisphere.NORTH:
            hemisphere = 'N'
        else:
            hemisphere = 'S'

        return '{}{} {}E {}N'.format(self.zone_number, hemisphere, int(self.easting), format(int(self.northing), '08d'))


class WGSPoint:
    def __init__(self, long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec):
        self.long_deg = long_deg
        self.long_min = long_min
        self.long_sec = long_sec
        self.lat_deg = lat_deg
        self.lat_min = lat_min
        self.lat_sec = lat_sec

    def to_string(self, guessed_system):
        if self.long_deg < 0:
            long_identifier = 'W'
            long_deg = self.long_deg * -1
        else:
            long_identifier = 'E'
            long_deg = self.long_deg
        if self.lat_deg < 0:
            lat_identifier = 'S'
            lat_deg = self.lat_deg * -1
        else:
            lat_identifier = 'N'
            lat_deg = self.lat_deg

        long_min = self.long_min
        long_sec = self.long_sec
        lat_min = self.lat_min
        lat_sec = self.lat_sec

        if guessed_system == 'WGS_DEGREES':
            _long_d = self.__format_degrees_for_wgs_degrees(long_deg)
            _lat_d = self.__format_degrees_for_wgs_degrees(lat_deg)
            return '{}\xb0 {} {}\xb0 {}'.format(_long_d, long_identifier, _lat_d, lat_identifier)

        if guessed_system == 'WGS_COMMA':
            _long_m = self.__format_min_for_wgs_dms(long_min)
            _lat_m = self.__format_min_for_wgs_dms(lat_min)
            return '{}\xb0 {}\' {} {}\xb0 {}\' {}'.format(int(long_deg), _long_m[:5],
                                                          long_identifier, int(lat_deg), _lat_m[:5],
                                                          lat_identifier)

        if guessed_system == 'WGS_DMS':
            _long_s = self.__format_sec(long_sec)
            _lat_s = self.__format_sec(lat_sec)
            return '{}\xb0 {}\' {}" {} {}\xb0 {}\' {}" {}'.format(int(long_deg), format(int(long_min), '02d'),
                                                                  _long_s, long_identifier,
                                                                  int(lat_deg), format(int(lat_min), '02d'),
                                                                  _lat_s, lat_identifier)

            # TODO
            # format degrees in a private method
            # check if < 0 or > 0 because if < 0 values are stores in e- style
            # also consider handling formating min and sec this way

    def __format_degrees_for_wgs_degrees(self, deg):
        if '.' in str(deg):
            if 'E' in str(deg):
                index = str(deg).index('E')
                zeros = int(str(deg)[index + 1: index + 3]) * -1
                _list = str(deg).split('.')
                before = _list[0]
                after = _list[1]
                add_zeros = '0'
                while zeros - 2 > 0:
                    add_zeros += '0'
                    zeros -= 1

                first_number = len(add_zeros) + len(before)
                if first_number < 7:
                    _d = '0.' + add_zeros + before + '' + after[:7-first_number]
                else:
                    _d = _d = '0.' + add_zeros
                return _d
            else:
                _list = str(deg).split('.')
                before = _list[0]
                after = _list[1]
                if len(after) < 6:
                    while len(after) < 6:
                        after += '0'
                else:
                    after = after[:6]
                _d = before + '.' + after
                return _d
        else:
            _d = str(deg) + '.000000'
            return _d

    def __format_min_for_wgs_dms(self, _min):
        if '.' in str(_min):
            _list = str(_min).split('.')
            before = _list[0]
            after = _list[1]
            if len(before) < 2:
                before = '0' + before
            if len(after) < 2:
                after += '0'
            else:
                after = after[:2]

            return before + '.' + after
        else:
            _s = format(_min, '06.3f')
            _s = _s[:5]
        return _s

    def __format_sec(self, sec):
        if '.' in str(sec):
            _list = str(sec).split('.')
            before = _list[0]
            after = _list[1]
            if len(before) < 2:
                before = '0' + before
            if len(after) < 2:
                after += '0'
            else:
                after = after[:2]

            return before + '.' + after
        else:
            _s = format(sec, '06.3f')
            _s = _s[:5]
            return _s