# -*- coding: utf-8 -*-
import points
import math
from ensurer import Hemisphere
import exceptions
from decimal import Decimal

K0 = 0.9996

E = 0.00669438
E2 = E * E
E3 = E2 * E
E_P2 = E / (1.0 - E)

SQRT_E = math.sqrt(1 - E)
_E = (1 - SQRT_E) / (1 + SQRT_E)
_E2 = _E * _E
_E3 = _E2 * _E
_E4 = _E3 * _E
_E5 = _E4 * _E

M1 = (1 - E / 4 - 3 * E2 / 64 - 5 * E3 / 256)
M2 = (3 * E / 8 + 3 * E2 / 32 + 45 * E3 / 1024)
M3 = (15 * E2 / 256 + 45 * E3 / 1024)
M4 = (35 * E3 / 3072)

P2 = (3. / 2 * _E - 27. / 32 * _E3 + 269. / 512 * _E5)
P3 = (21. / 16 * _E2 - 55. / 32 * _E4)
P4 = (151. / 96 * _E3 - 417. / 128 * _E5)
P5 = (1097. / 512 * _E4)

R = 6378137

ZONE_LETTERS = "CDEFGHJKLMNPQRSTUVWXX"
lettertable = 'CDEFGHJKLMNPQRSTUVWX'
LETTER_VALUES = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
                 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
                 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}


def degree_to_utm(point):
    """Algorithm for the conversion of coordinate from the geographic coordinate system to UTM.

    Authors
    -------
    * Bart van Andel <bavanandel@gmail.com>
    * Tobias Bieniek <Tobias.Bieniek@gmx.de>
    * Torstein I. Bo
    """
    longitude = point.long_deg
    latitude = point.lat_deg
    force_zone_number = None

    # if not -80.0 <= latitude <= 84.0:
    #     raise exceptions.ParseException('latitude out of range (must be between 80 deg S and 84 deg N)')
    # if not -180.0 <= longitude <= 180.0:
    #     raise exceptions.ParseException('longitude out of range (must be between 180 deg W and 180 deg E)')

    lat_rad = math.radians(latitude)
    lat_sin = math.sin(lat_rad)
    lat_cos = math.cos(lat_rad)

    lat_tan = lat_sin / lat_cos
    lat_tan2 = lat_tan * lat_tan
    lat_tan4 = lat_tan2 * lat_tan2

    if force_zone_number is None:
        zone_number = latlon_to_zone_number(latitude, longitude)
    else:
        zone_number = force_zone_number

    zone_letter = latitude_to_zone_letter(latitude)

    lon_rad = math.radians(longitude)
    central_lon = zone_number_to_central_longitude(zone_number)
    central_lon_rad = math.radians(central_lon)

    n = R / math.sqrt(1 - E * lat_sin**2)
    c = E_P2 * lat_cos**2

    a = lat_cos * (lon_rad - central_lon_rad)
    a2 = a * a
    a3 = a2 * a
    a4 = a3 * a
    a5 = a4 * a
    a6 = a5 * a

    m = R * (M1 * lat_rad -
             M2 * math.sin(2 * lat_rad) +
             M3 * math.sin(4 * lat_rad) -
             M4 * math.sin(6 * lat_rad))

    easting = K0 * n * (a +
                        a3 / 6 * (1 - lat_tan2 + c) +
                        a5 / 120 * (5 - 18 * lat_tan2 + lat_tan4 + 72 * c - 58 * E_P2)) + 500000

    northing = K0 * (m + n * lat_tan * (a2 / 2 +
                                        a4 / 24 * (5 - lat_tan2 + 9 * c + 4 * c**2) +
                                        a6 / 720 * (61 - 58 * lat_tan2 + lat_tan4 + 600 * c - 330 * E_P2)))

    if latitude < 0:
        northing += 10000000

    if latitude >= 0:
        hemisphere = Hemisphere.NORTH
    else:
        hemisphere = Hemisphere.SOUTH
    point = points.UTMPoint(easting, northing, zone_number, zone_letter, hemisphere)
    return point


def utm_to_degree(point):
    """Algorithm for the conversion of coordinate from UTM to the geographic coordinate system.

    Authors
    -------
    * Bart van Andel <bavanandel@gmail.com>
    * Tobias Bieniek <Tobias.Bieniek@gmx.de>
    * Torstein I. Bo
    """
    easting = int(point.easting)
    northing = int(point.northing)
    zone_number = int(point.zone_number)
    zone_letter = None

    if point.hemisphere == Hemisphere.NORTH:
        northern = True
    else:
        northern = False

    if not zone_letter and northern is None:
        raise exceptions.ConversionException('either zone_letter or northern needs to be set')

    elif zone_letter and northern is not None:
        raise exceptions.ConversionException('set either zone_letter or northern, but not both')

    # if not 100000 <= easting < 1000000:
    #     raise exceptions.ParseException('easting out of range (must be between 100.000 m and 999.999 m)')
    # if not 0 <= northing <= 10000000:
    #     raise exceptions.ParseException('northing out of range (must be between 0 m and 10.000.000 m)')
    # if not 1 <= zone_number <= 60:
    #     raise exceptions.ParseException('zone number out of range (must be between 1 and 60)')
    #
    # if zone_letter:
    #     zone_letter = zone_letter.upper()
    #
    #     if not 'C' <= zone_letter <= 'X' or zone_letter in ['I', 'O']:
    #         raise exceptions.ParseException('zone letter out of range (must be between C and X)')

        northern = (zone_letter >= 'N')

    x = easting - 500000
    y = northing

    if not northern:
        y -= 10000000

    m = y / K0
    mu = m / (R * M1)

    p_rad = (mu +
             P2 * math.sin(2 * mu) +
             P3 * math.sin(4 * mu) +
             P4 * math.sin(6 * mu) +
             P5 * math.sin(8 * mu))

    p_sin = math.sin(p_rad)
    p_sin2 = p_sin * p_sin

    p_cos = math.cos(p_rad)

    p_tan = p_sin / p_cos
    p_tan2 = p_tan * p_tan
    p_tan4 = p_tan2 * p_tan2

    ep_sin = 1 - E * p_sin2
    ep_sin_sqrt = math.sqrt(1 - E * p_sin2)

    n = R / ep_sin_sqrt
    r = (1 - E) / ep_sin

    c = _E * p_cos**2
    c2 = c * c

    d = x / (n * K0)
    d2 = d * d
    d3 = d2 * d
    d4 = d3 * d
    d5 = d4 * d
    d6 = d5 * d

    latitude = (p_rad - (p_tan / r) *
                (d2 / 2 - d4 / 24 * (5 + 3 * p_tan2 + 10 * c - 4 * c2 - 9 * E_P2)) +
                d6 / 720 * (61 + 90 * p_tan2 + 298 * c + 45 * p_tan4 - 252 * E_P2 - 3 * c2))

    longitude = (d - d3 / 6 * (1 + 2 * p_tan2 + c) +
                 d5 / 120 * (5 - 2 * c + 28 * p_tan2 - 3 * c2 + 8 * E_P2 + 24 * p_tan4)) / p_cos

    calc_point = points.WGSPoint(Decimal(math.degrees(longitude) + zone_number_to_central_longitude(zone_number)), 0, 0,
                                 Decimal(math.degrees(latitude)), 0, 0)
    return calc_point


def convert_degree_to_DMS(degrees):
    """Algorithm for the conversion of degrees to degrees, minutes and seconds in the geographic coordinate system."""
    _deg = int(degrees)
    _min = (Decimal(degrees) - Decimal(_deg)) * Decimal(60)
    _sec = (Decimal(_min) - int(_min)) * Decimal(60)
    if abs(float(_sec)) == 60:
        _sec = 0
    return Decimal(_deg), abs(int(float(_min))), abs(float(_sec))


def convert_DMS_to_degree(degrees, minutes, seconds):
    """Algorithm for the conversion of degrees, minutes and seconds to degrees in the geographic coordinate system."""
    if degrees >= 0:
        _deg = Decimal(degrees) + Decimal(minutes) / Decimal(60.0) + Decimal(seconds) / Decimal(3600.0)
    else:
        _deg = Decimal(degrees) - Decimal(minutes) / Decimal(60.0) - Decimal(seconds) / Decimal(3600.0)
    return _deg


def convert_degree_to_decimal_minutes(degrees):
    """Algorithm for the conversion of degrees to degrees, decimal minutes in the geographic coordinate system."""
    _deg = int(degrees)
    _min = (abs(degrees) - abs(_deg)) * 60
    return _deg, _min


def convert_decimal_minutes_to_degree(degrees, minutes):
    """Algorithm for the conversion of degrees, decimal minutes to degrees in the geographic coordinate system."""
    _d = Decimal(minutes) / Decimal(60.0)
    if degrees >= 0:
        _deg = Decimal(degrees) + Decimal(_d)
    else:
        _deg = Decimal(degrees) - Decimal(_d)
    return Decimal(_deg)


def convert_dms_to_decimal_minutes(degrees, minutes, seconds):
    """Algorithm for the conversion of degrees, minutes and seconds to
    degrees, decimal minutes in the geographic coordinate system."""
    _min = Decimal(minutes) + Decimal(seconds) / Decimal(60.0)
    return Decimal(degrees), Decimal(_min)


def latitude_to_zone_letter(latitude):
    if -80 <= latitude <= 84:
        return ZONE_LETTERS[int(latitude + 80) >> 3]
    else:
        return None


def latlon_to_zone_number(latitude, longitude):
    if 56 <= latitude < 64 and 3 <= longitude < 12:
        return 32

    if 72 <= latitude <= 84 and longitude >= 0:
        if longitude <= 9:
            return 31
        elif longitude <= 21:
            return 33
        elif longitude <= 33:
            return 35
        elif longitude <= 42:
            return 37

    return int((longitude + 180) / 6) + 1


def zone_number_to_central_longitude(zone_number):
    return (zone_number - 1) * 6 - 180 + 3

def convert_MGRS_to_UTM(point):
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

    min_lat = __get_min_northing(chr(lat_zone))
    while square_y < min_lat:
        square_y += 20

    if square_y > min_lat + 15:
        square_y -= 20

    northing_temp = square_y * 100000

    result_easting = easting_temp + int(point.easting)
    result_northing = northing_temp + int(point.northing)

    return points.UTMPoint(result_easting, result_northing, zone_temp, '', hemisphere)


def convert_UTM_to_MGRS(point):
    degree_point = utm_to_degree(point)
    ltr2_low_value, ltr2_high_value, false_northing = __get_grid_values(point.zone_number)
    letter = __get_latitude_letter(float(degree_point.lat_deg))

    grid_northing = int(point.northing)
    if grid_northing == 1.E7:
        grid_northing -= 1.0

    while grid_northing >= 2000000.0:
        grid_northing -= 2000000.0

    grid_northing -= false_northing

    if grid_northing < 0.0:
        grid_northing += 2000000

    square_y = grid_northing / 100000.0

    if square_y > LETTER_VALUES['H']:
        square_y += 1

    if square_y > LETTER_VALUES['N']:
        square_y += 1

    grid_easting = int(point.easting)

    if letter == 'V' and point.zone == 31 and grid_easting == 500000.0:
        grid_easting -= 1.0

    square_x = ltr2_low_value + (grid_easting / 100000) - 1
    if ltr2_low_value == LETTER_VALUES['J'] and square_x > LETTER_VALUES['N']:
        square_x += 1

    zone = str(point.zone_number) + letter
    square = str(LETTER_VALUES.keys()[LETTER_VALUES.values().index(int(square_x))]) + \
             str(LETTER_VALUES.keys()[LETTER_VALUES.values().index(int(square_y))])
    easting = math.fmod(float(point.easting), 100000.0)
    northing = math.fmod(float(point.northing), 100000.0)
    return points.MGRSPoint(int(easting), int(northing), zone, square)


def __define_UTM_zone(point):
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


def __get_grid_values(zone):
    set_number = float(zone) % 6
    if set_number == 0:
        set_number = 6
    if set_number == 1 or set_number == 4:
        ltr2_low_value = LETTER_VALUES['A']
        ltr2_high_value = LETTER_VALUES['H']
    elif set_number == 2 or set_number == 5:
        ltr2_low_value = LETTER_VALUES['J']
        ltr2_high_value = LETTER_VALUES['R']
    elif set_number == 3 or set_number == 6:
        ltr2_low_value = LETTER_VALUES['S']
        ltr2_high_value = LETTER_VALUES['Z']

    if set_number % 2 == 0:
        false_northing = 1500000.0
    else:
        false_northing = 0.0

    return ltr2_low_value, ltr2_high_value, false_northing

def __get_latitude_letter(latitude):
    if 72.0 <= latitude < 84.5:
        letter = 'X'
    elif -80.5 < latitude < 72.0:
        temp = (latitude + 80.0) / 8.0 + 1.0E-12
        letter = lettertable[int(temp)]
    else:
        letter = 'Z'
    return letter

def __get_min_northing(letter):
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
