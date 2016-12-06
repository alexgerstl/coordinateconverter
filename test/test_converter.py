# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal
from os.path import expanduser

import coordinate_parser

home = expanduser("~")
python_path = home + '\.qgis2\python\plugins\CoordinatesConverter\lib\pyproj-1.9.5.1-py2.7-win-amd64.egg'

import mgrs
import sys
sys.path.insert(0,python_path)
import pyproj

import points
import converter
from converter1 import Converter
from ensurer import Hemisphere


class ConverterTest(unittest.TestCase):

    #test for comma minutes to degree and dms
    def test_comma_minutes_to_other(self):
        point = points.WGSPoint(-3, 4.5, 0, 10, 59.9999999999999, 0)
        long_deg = converter.convert_decimal_minutes_to_degree(float(point.long_deg), float(point.long_min))
        lat_deg = converter.convert_decimal_minutes_to_degree(float(point.lat_deg), Decimal(point.lat_min))
        p = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        #self.assertEqual(format(p.long_deg, '.4f'), '-3.0750')
        #self.assertEqual(format(p.lat_deg, '.4f'), '10.9833')
        print('WGS_Degree_long: ' + str(p.long_deg))
        print('WGS_Degree_lat: ' + str(p.lat_deg))
        print('WGS_Degree: ' + p.to_string(coordinate_parser.CoordinateSystemString.WGS84_Degrees.value))
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(p.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(p.lat_deg)
        p_1 = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(p_1.long_deg, -3)
        self.assertEqual(p_1.long_min, 4)
        self.assertEqual(format(p_1.long_sec, '06.3f')[0:5], '30.00')
        self.assertEqual(p_1.lat_deg, 10)
        self.assertEqual(p_1.lat_min, 58)
        self.assertEqual(format(p_1.lat_sec, '06.3f'), '59.99')
        print('WGS_DMS_long: ' + str(p_1.long_deg) + ' ' + str(p_1.long_min + ' ' + str(p_1.long_sec)))
        print('WGS_DMS_lat: ' + str(p_1.lat_deg) + ' ' + str(p_1.lat_min + ' ' + str(p_1.lat_sec)))
        print('WGS_DMS: ' + p_1.to_string(coordinate_parser.CoordinateSystemString.WGS84_DMS.value))

    #test for dms to degree and comma mintues
    def test_dms_to_other(self):
        f = Converter()
        point = points.WGSPoint(3, 59, Decimal(59.999), 10, 12, 30)
        long_deg = f.convert_DMS_to_degree(point.long_deg, point.long_min, point.long_sec)
        lat_deg = f.convert_DMS_to_degree(point.lat_deg, point.lat_min, point.lat_sec)
        p = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        self.assertEqual(str(p.long_deg)[:8], '3.999999')
        self.assertEqual(format(p.lat_deg, '.4f'), '10.2083')
        long_deg, long_min = f.convert_degree_to_decimal_minutes(p.long_deg)
        lat_deg, lat_min = f.convert_degree_to_decimal_minutes(p.lat_deg)
        p_1 = points.WGSPoint(long_deg, long_min, 0, lat_deg, lat_min, 0)
        self.assertEqual(p_1.long_deg, 3)
        self.assertEqual(str(p_1.long_min)[:5], '59.99')
        self.assertEqual(p_1.long_sec, 0)
        self.assertEqual(p_1.lat_deg, 10)
        self.assertEqual(format(p_1.lat_min, '.2f'), '12.50')
        self.assertEqual(p_1.lat_sec, 0)

    #test for degree to comma minutes and dms
    def test_degree_to_other(self):
        f = Converter()
        point = points.WGSPoint(-3.0750, 0, 0, 10.2083, 0, 0)
        long_deg, long_min = f.convert_degree_to_decimal_minutes(point.long_deg)
        lat_deg, lat_min = f.convert_degree_to_decimal_minutes(point.lat_deg)
        p = points.WGSPoint(long_deg, long_min, 0, lat_deg, lat_min, 0)
        self.assertEqual(p.long_deg, -3)
        self.assertEqual(format(p.long_min, '.2f'), '4.50')
        self.assertEqual(p.long_sec, 0)
        self.assertEqual(p.lat_deg, 10)
        self.assertEqual(format(p.lat_min, '.2f'), '12.50')
        self.assertEqual(p.lat_sec, 0)
        long_deg, long_min, long_sec = f.convert_degree_to_DMS(point.long_deg)
        lat_deg, lat_min, lat_sec = f.convert_degree_to_DMS(point.lat_deg)
        p_1 = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(p_1.long_deg, -3)
        self.assertEqual(p_1.long_min, 4)
        self.assertEqual(format(p_1.long_sec, '.0f'), '30')
        self.assertEqual(p_1.lat_deg, 10)
        self.assertEqual(p_1.lat_min, 12)
        self.assertEqual(format(p_1.lat_sec, '.0f'), '30')

    #test for degree -> utm
    def test_degree_to_UTM(self):
        point = points.WGSPoint(3, 0, 0, -10, 0, 0)
        p_1 = converter.degree_to_utm(point)
        print(p_1.to_string())
        self.assertEqual(p_1.zone, 31)
        self.assertEqual(p_1.hemisphere, Hemisphere.SOUTH)
        self.assertEqual(p_1.easting, 500000)
        self.assertEqual(p_1.northing, 1128443)

    #test for utm -> degree
    def test_utm_to_degree(self):
        point = points.UTMPoint(456331, 1562000, 33, None,  Hemisphere.NORTH)
        p_1 = converter.utm_to_degree(point)
        self.assertEqual(format(p_1.lat_deg, '.4f'), '14.1287')
        self.assertEqual(format(p_1.long_deg, '.4f'), '14.5954')

    #test for mgrs -> utm
    def test_MGRS_to_UTM(self):
        f = Converter()
        point = points.MGRSPoint(12345, 12345, '33U', 'VP', Hemisphere.NORTH)
        p_1 = f.convert_MGRS_to_UTM(point)
        self.assertEqual(p_1.zone, 33)
        self.assertEqual(p_1.hemisphere, Hemisphere.NORTH)
        self.assertEqual(p_1.easting, 412345)
        self.assertEqual(p_1.northing, 5312345)

    def test_MGRS(self):
        lon = 14.056128
        lat = 48.299322
        m = mgrs.MGRS()
        c = m.toMGRS(lat, lon)
        print(c)

    # test for dms to degree and comma mintues
    def test_dms_to_degree(self):
        f = Converter()
        point = points.WGSPoint(16, 59, 59.9999, 10, 12, 30)
        print(point.to_string('WGS_DEGREES'))
        long_deg = f.convert_DMS_to_degree(point.long_deg, point.long_min, point.long_sec)
        lat_deg = f.convert_DMS_to_degree(point.lat_deg, point.lat_min, point.lat_sec)
        print(long_deg)
        p = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        print(str(p.long_deg))
        print(p.to_string('WGS_DEGREES'))

    def test_abc(self):
        p2 = pyproj.Proj(proj='utm', zone=31, ellps='WGS84')
        #x, y = p2(-10.2083, 3.0750)
        x, y = p2(3, -10)
        print(x)
        print(y)

    def test_def(self):
        point = points.WGSPoint(3, 0, 0, -10, 0, 0)
        point = converter.degree_to_utm(point)
        print(point.to_string())

    def test_ghi(self):
        point = points.UTMPoint(123456, 1, 33, 'L', coordinate_parser.Hemisphere.NORTH)
        point = converter.utm_to_degree(point)
        print(point.to_string(coordinate_parser.CoordinateSystemString.WGS84_Degrees.value))
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(point.lat_deg)
        print(str(long_deg))
        print(str(lat_deg))


if __name__ == '__main__':
    unittest.main()