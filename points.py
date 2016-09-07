# -*- coding: utf-8 -*-
import exceptions


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
    def __init__(self, easting, northing, zone, hemisphere):
        self.easting = easting
        self.northing = northing
        self.zone = zone
        self.hemisphere = hemisphere

    def to_string(self):
        if self.hemisphere.name == 'NORTH':
            hemisphere = 'N'
        else:
            hemisphere = 'S'

        return '{}{} {}E {}N'.format(self.zone, hemisphere, self.easting, self.northing)


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
            self.long_deg *= -1
        else:
            long_identifier = 'E'
        if self.lat_deg < 0:
            lat_identifier = 'S'
            self.lat_deg *= -1
        else:
            lat_identifier = 'N'

        long_deg = self.long_deg
        long_min = self.long_min
        long_sec = self.long_sec
        lat_deg = self.lat_deg
        lat_min = self.lat_min
        lat_sec = self.lat_sec

        if guessed_system == 'WGS_DEGREES':
            return '{}\xb0 {} {}\xb0 {}'.format(format(long_deg, '.6f'), long_identifier, format(lat_deg, '.6f'),
                                                lat_identifier)

        if guessed_system == 'WGS_COMMA':
            return '{}\xb0 {}\' {} {}\xb0 {}\' {}'.format(int(long_deg), format(float(long_min), '05.2f'),
                                                          long_identifier, int(lat_deg), format(float(lat_min), '05.2f'),
                                                          lat_identifier)

        if guessed_system == 'WGS_DMS':
            return '{}\xb0 {}\' {}" {} {}\xb0 {}\' {}" {}'.format(int(long_deg), format(int(long_min), '02d'),
                                                                  format(float(long_sec), '05.2f'), long_identifier,
                                                                  int(lat_deg), format(int(lat_min), '02d'),
                                                                  format(float(lat_sec), '05.2f'), lat_identifier)
