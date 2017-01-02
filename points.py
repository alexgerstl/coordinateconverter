# -*- coding: utf-8 -*-
import ensurer


class MGRSPoint:
    def __init__(self, easting, northing, zone, square):
        self.easting = easting
        self.northing = northing
        self.zone = zone
        self.square = square

    def to_string(self):
        easting = self.__format_mgrs_values(self.easting)
        northing = self.__format_mgrs_values(self.northing)
        return '{} {} {} {}'.format(self.zone, self.square, easting, northing)

    def __format_mgrs_values(self, value):
        while len(str(value)) < 5:
            value = '0' + str(value)
        return value


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

        return '{}{} {}E {}N'.format(self.zone_number, hemisphere, int(self.easting), int(self.northing))


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

    def __format_degrees_for_wgs_degrees(self, deg):
        """Formats degree value from point for presenting to user"""
        if '.' in str(deg):
            # it's a decimal
            if 'e' in str(deg).lower():
                # it's stored in exponential map
                zeros = self.__number_of_zeros(str(deg))
                # now we now the exponent
                _list = str(deg).split('.')
                before = _list[0]
                after = _list[1]
                add_zeros = self.__create_zeros(zeros)
                first_number = len(add_zeros) + len(before)
                if first_number < 7:
                    _d = '0.' + add_zeros + before + '' + after[:7-first_number]
                else:
                    _d = _d = '0.' + add_zeros[:6]
                return _d
            else:
                # it's a simple decimal
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
            # it's an integer
            _d = str(deg) + '.000000'
            return _d

    def __format_min_for_wgs_dms(self, _min):
        if '.' in str(_min):
            if 'e' in str(_min).lower():
                # it's stored in exponential map
                zeros = self.__number_of_zeros(str(_min))
                # now we now the exponent
                _list = str(_min).split('.')
                before = _list[0]
                after = _list[1]
                add_zeros = self.__create_zeros(zeros)
                first_number = len(add_zeros) + len(before)
                if first_number < 7:
                    _m = '00.' + add_zeros + before + '' + after[:7-first_number]
                else:
                    _m = _m = '00.' + add_zeros[:2]
                return _m
            else:
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
            if 'e' in str(sec).lower():
                # it's stored in exponential map
                zeros = self.__number_of_zeros(str(sec))
                # now we now the exponent
                _list = str(sec).split('.')
                before = _list[0]
                after = _list[1]
                add_zeros = self.__create_zeros(zeros)
                first_number = len(add_zeros) + len(before)
                if first_number < 7:
                    _s = '00.' + add_zeros + before + '' + after[:7-first_number]
                else:
                    _s = _s = '00.' + add_zeros[:2]
                return _s
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

    def __number_of_zeros(self, value):
        index = str(value).lower().index('e')
        zeros = int(str(value)[index + 1:]) * -1
        return zeros

    def __create_zeros(self, value):
        add_zeros = '0'
        while value - 2 > 0:
            # creating zeros based on exponent
            add_zeros += '0'
            value -= 1
        return add_zeros
