# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal
from os.path import expanduser
import mgrs

home = expanduser("~")
python_path = home + '\.qgis2\python\plugins\CoordinatesConverter\lib\pyproj-1.9.5.1.egg'
import sys
sys.path.insert(0,python_path)
import pyproj

import points
import converter
from ensurer import Hemisphere, CoordinateSystemString


class ConverterTest(unittest.TestCase):

    def test_conversion_of_degrees_1(self):
        point = points.WGSPoint(0, 32, 0, 0, 31, 0)
        long_deg = converter.convert_decimal_minutes_to_degree(point.long_deg, point.long_min)
        lat_deg = converter.convert_decimal_minutes_to_degree(point.lat_deg, point.lat_min)
        degree_point = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        print(degree_point.to_string(CoordinateSystemString.WGS84_Degrees.value))
        self.assertEqual(str(degree_point.long_deg)[:8], '0.533333')
        self.assertEqual(str(degree_point.lat_deg)[:8], '0.516666')
        utm_point = converter.degree_to_utm(degree_point)
        print(utm_point.to_string())
        self.assertEqual(utm_point.zone_number, 31)
        self.assertEqual(int(utm_point.easting), 225447)
        self.assertEqual(int(utm_point.northing), 57160)
        self.assertEqual(utm_point.hemisphere, Hemisphere.NORTH)
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        print(mgrs_point.to_string())
        self.assertEqual(mgrs_point.zone, '31N')
        self.assertEqual(mgrs_point.square, 'BA')
        self.assertEqual(mgrs_point.easting, 25447)
        self.assertEqual(mgrs_point.northing, 57160)

    def test_conversion_of_degrees_2(self):
        point = points.WGSPoint(12, 32, 0, 2, 31, 0)
        long_deg = converter.convert_decimal_minutes_to_degree(point.long_deg, point.long_min)
        lat_deg = converter.convert_decimal_minutes_to_degree(point.lat_deg, point.lat_min)
        degree_point = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        print(degree_point.to_string(CoordinateSystemString.WGS84_Degrees.value))
        self.assertEqual(str(degree_point.long_deg)[:8], '12.53333')
        self.assertEqual(str(degree_point.lat_deg)[:8], '2.516666')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        print(dms_point.to_string(CoordinateSystemString.WGS84_DMS.value))
        self.assertEqual(int(dms_point.long_deg), 12)
        self.assertEqual(int(dms_point.long_min), 32)
        self.assertEqual(int(dms_point.long_sec), 0)
        self.assertEqual(int(dms_point.lat_deg), 2)
        self.assertEqual(int(dms_point.lat_min), 31)
        self.assertEqual(int(dms_point.lat_sec), 0)
        utm_point = converter.degree_to_utm(degree_point)
        print(utm_point.to_string())
        self.assertEqual(utm_point.zone_number, 33)
        self.assertEqual(int(utm_point.easting), 225699)
        self.assertEqual(int(utm_point.northing), 278428)
        self.assertEqual(utm_point.hemisphere, Hemisphere.NORTH)
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        print(mgrs_point.to_string())
        self.assertEqual(mgrs_point.zone, '33N')
        self.assertEqual(mgrs_point.square, 'TC')
        self.assertEqual(mgrs_point.easting, 25699)
        self.assertEqual(mgrs_point.northing, 78428)

    def test_conversion_of_degrees_3(self):
        degree_point = points.WGSPoint(16.123456, 0, 0, 25.654321, 0, 0)
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        print(dms_point.to_string(CoordinateSystemString.WGS84_DMS.value))
        self.assertEqual(int(dms_point.long_deg), 16)
        self.assertEqual(int(dms_point.long_min), 7)
        self.assertEqual(str(dms_point.long_sec)[:5], '24.44')
        self.assertEqual(int(dms_point.lat_deg), 25)
        self.assertEqual(int(dms_point.lat_min), 39)
        self.assertEqual(str(dms_point.lat_sec)[:5], '15.55')
        utm_point = converter.degree_to_utm(degree_point)
        print(utm_point.to_string())
        self.assertEqual(utm_point.zone_number, 33)
        self.assertEqual(int(utm_point.easting), 612764)
        self.assertEqual(int(utm_point.northing), 2837881)
        self.assertEqual(utm_point.hemisphere, Hemisphere.NORTH)
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        print(mgrs_point.to_string())
        self.assertEqual(mgrs_point.zone, '33R')
        self.assertEqual(mgrs_point.square, 'XJ')
        self.assertEqual(mgrs_point.easting, 12764)
        self.assertEqual(mgrs_point.northing, 37881)

    def test_conversion_of_degrees_4(self):
        degree_point = points.WGSPoint(16.123456, 0, 0, 25.654321, 0, 0)
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(float(degree_point.long_deg))
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(float(degree_point.lat_deg))
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        print(dms_point.to_string(CoordinateSystemString.WGS84_DMS.value))
        self.assertEqual(int(dms_point.long_deg), 16)
        self.assertEqual(int(dms_point.long_min), 7)
        self.assertEqual(str(dms_point.long_sec)[:5], '24.44')
        self.assertEqual(int(dms_point.lat_deg), 25)
        self.assertEqual(int(dms_point.lat_min), 39)
        self.assertEqual(str(dms_point.lat_sec)[:5], '15.55')
        utm_point = converter.degree_to_utm(degree_point)
        print(utm_point.to_string())
        self.assertEqual(utm_point.zone_number, 33)
        self.assertEqual(int(utm_point.easting), 612764)
        self.assertEqual(int(utm_point.northing), 2837881)
        self.assertEqual(utm_point.hemisphere, Hemisphere.NORTH)
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        print(mgrs_point.to_string())
        self.assertEqual(mgrs_point.zone, '33R')
        self.assertEqual(mgrs_point.square, 'XJ')
        self.assertEqual(mgrs_point.easting, 12764)
        self.assertEqual(mgrs_point.northing, 37881)

    def test_conversion_of_degrees_5(self):
        degree_point = points.WGSPoint(-16.123456, 0, 0, 25.654321, 0, 0)
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(float(degree_point.long_deg))
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(float(degree_point.lat_deg))
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        print(dms_point.to_string(CoordinateSystemString.WGS84_DMS.value))
        self.assertEqual(int(dms_point.long_deg), -16)
        self.assertEqual(int(dms_point.long_min), 7)
        self.assertEqual(str(dms_point.long_sec)[:5], '24.44')
        self.assertEqual(int(dms_point.lat_deg), 25)
        self.assertEqual(int(dms_point.lat_min), 39)
        self.assertEqual(str(dms_point.lat_sec)[:5], '15.55')
        utm_point = converter.degree_to_utm(degree_point)
        print(utm_point.to_string())
        self.assertEqual(utm_point.zone_number, 28)
        self.assertEqual(int(utm_point.easting), 387235)
        self.assertEqual(int(utm_point.northing), 2837881)
        self.assertEqual(utm_point.hemisphere, Hemisphere.NORTH)
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        print(mgrs_point.to_string())
        self.assertEqual(mgrs_point.zone, '28R')
        self.assertEqual(mgrs_point.square, 'CP')
        self.assertEqual(mgrs_point.easting, 87235)
        self.assertEqual(mgrs_point.northing, 37881)

    def test_conversion_of_degrees_6(self):
        degree_point = points.WGSPoint(16.123456, 0, 0, -25.654321, 0, 0)
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(float(degree_point.long_deg))
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(float(degree_point.lat_deg))
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        print(dms_point.to_string(CoordinateSystemString.WGS84_DMS.value))
        self.assertEqual(int(dms_point.long_deg), 16)
        self.assertEqual(int(dms_point.long_min), 7)
        self.assertEqual(str(dms_point.long_sec)[:5], '24.44')
        self.assertEqual(int(dms_point.lat_deg), -25)
        self.assertEqual(int(dms_point.lat_min), 39)
        self.assertEqual(str(dms_point.lat_sec)[:5], '15.55')
        utm_point = converter.degree_to_utm(degree_point)
        print(utm_point.to_string())
        self.assertEqual(utm_point.zone_number, 33)
        self.assertEqual(int(utm_point.easting), 612764)
        self.assertEqual(int(utm_point.northing), 7162118)
        self.assertEqual(utm_point.hemisphere, Hemisphere.SOUTH)
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        print(mgrs_point.to_string())
        self.assertEqual(mgrs_point.zone, '33J')
        self.assertEqual(mgrs_point.square, 'XM')
        self.assertEqual(mgrs_point.easting, 12764)
        self.assertEqual(mgrs_point.northing, 62118)

    def test_conversion_of_degrees_7(self):
        point = points.WGSPoint(25, 59, 59.99, 67, 12, 58.99)
        long_deg = converter.convert_DMS_to_degree(point.long_deg, point.long_min, point.long_sec)
        lat_deg = converter.convert_DMS_to_degree(point.lat_deg, point.lat_min, point.lat_sec)
        degree_point = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        print(degree_point.to_string(CoordinateSystemString.WGS84_Degrees.value))
        self.assertEqual(str(degree_point.long_deg)[:8], '25.99999')
        self.assertEqual(str(degree_point.lat_deg)[:8], '67.21638')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        print(dms_point.to_string(CoordinateSystemString.WGS84_DMS.value))
        self.assertEqual(int(dms_point.long_deg), 25)
        self.assertEqual(int(dms_point.long_min), 59)
        self.assertEqual(str(dms_point.long_sec)[:5], '59.99')
        self.assertEqual(int(dms_point.lat_deg), 67)
        self.assertEqual(int(dms_point.lat_min), 12)
        self.assertEqual(str(dms_point.lat_sec)[:5], '58.99')
        utm_point = converter.degree_to_utm(degree_point)
        print(utm_point.to_string())
        self.assertEqual(utm_point.zone_number, 35)
        self.assertEqual(int(utm_point.easting), 456786)
        self.assertEqual(int(utm_point.northing), 7455850)
        self.assertEqual(utm_point.hemisphere, Hemisphere.NORTH)
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        print(mgrs_point.to_string())
        self.assertEqual(mgrs_point.zone, '35W')
        self.assertEqual(mgrs_point.square, 'MQ')
        self.assertEqual(mgrs_point.easting, 56786)
        self.assertEqual(mgrs_point.northing, 55850)

    def test_conversion_of_utm_1(self):
        utm_point = points.UTMPoint(123456, 1234567, 5, '', Hemisphere.NORTH)
        degree_point = converter.utm_to_degree(utm_point)
        self.assertEqual(str(degree_point.long_deg)[:9], '-156.4466')
        self.assertEqual(str(degree_point.lat_deg)[:8], '11.14828')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(int(dms_point.long_deg), -156)
        self.assertEqual(int(dms_point.long_min), 26)
        self.assertEqual(str(dms_point.long_sec)[:5], '47.86') #TODO: check
        self.assertEqual(int(dms_point.lat_deg), 11)
        self.assertEqual(int(dms_point.lat_min), 8)
        self.assertEqual(str(dms_point.lat_sec)[:5], '53.81')
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        self.assertEqual(mgrs_point.zone, '5P')
        self.assertEqual(mgrs_point.square, 'JO') #TODO: check
        self.assertEqual(mgrs_point.easting, 23456)
        self.assertEqual(mgrs_point.northing, 34567)

    def test_conversion_of_utm_2(self):
        utm_point = points.UTMPoint(123456, 1234567, 5, '', Hemisphere.SOUTH)
        degree_point = converter.utm_to_degree(utm_point)
        self.assertEqual(str(degree_point.long_deg)[:9], '-170.0987')
        self.assertEqual(str(degree_point.lat_deg)[:9], '-78.46254')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(int(dms_point.long_deg), -170)
        self.assertEqual(int(dms_point.long_min), 5)
        self.assertEqual(str(dms_point.long_sec)[:5], '55.62') #TODO: check
        self.assertEqual(int(dms_point.lat_deg), -78)
        self.assertEqual(int(dms_point.lat_min), 27)
        self.assertEqual(str(dms_point.lat_sec)[:5], '45.17')
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        self.assertEqual(mgrs_point.zone, '5C')
        self.assertEqual(mgrs_point.square, 'JO') #TODO: check
        self.assertEqual(mgrs_point.easting, 23456)
        self.assertEqual(mgrs_point.northing, 34567)

    def test_conversion_of_utm_3(self):
        utm_point = points.UTMPoint(654321, 7654321, 45, '', Hemisphere.NORTH)
        degree_point = converter.utm_to_degree(utm_point)
        self.assertEqual(str(degree_point.long_deg)[:9], '90.853072')
        self.assertEqual(str(degree_point.lat_deg)[:9], '68.956178')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(int(dms_point.long_deg), 90)
        self.assertEqual(int(dms_point.long_min), 51)
        self.assertEqual(str(dms_point.long_sec)[:5], '11.06')
        self.assertEqual(int(dms_point.lat_deg), 68)
        self.assertEqual(int(dms_point.lat_min), 57)
        self.assertEqual(str(dms_point.lat_sec)[:5], '22.24')
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        self.assertEqual(mgrs_point.zone, '45W')
        self.assertEqual(mgrs_point.square, 'XS')
        self.assertEqual(mgrs_point.easting, 54321)
        self.assertEqual(mgrs_point.northing, 54321)

    def test_conversion_of_utm_4(self):
        utm_point = points.UTMPoint(654321, 7654321, 45, '', Hemisphere.SOUTH)
        degree_point = converter.utm_to_degree(utm_point)
        self.assertEqual(str(degree_point.long_deg)[:9], '88.486799')
        self.assertEqual(str(degree_point.lat_deg)[:9], '-21.20607')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(int(dms_point.long_deg), 88)
        self.assertEqual(int(dms_point.long_min), 29)
        self.assertEqual(str(dms_point.long_sec)[:5], '12.47')
        self.assertEqual(int(dms_point.lat_deg), -21)
        self.assertEqual(int(dms_point.lat_min), 12)
        self.assertEqual(str(dms_point.lat_sec)[:5], '21.86')
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        self.assertEqual(mgrs_point.zone, '45K')
        self.assertEqual(mgrs_point.square, 'XS')
        self.assertEqual(mgrs_point.easting, 54321)
        self.assertEqual(mgrs_point.northing, 54321)

    def test_conversion_of_utm_5(self):
        utm_point = points.UTMPoint(500000, 2000000, 31, '', Hemisphere.NORTH)
        degree_point = converter.utm_to_degree(utm_point)
        self.assertEqual(str(degree_point.long_deg)[:9], '3')
        self.assertEqual(str(degree_point.lat_deg)[:9], '18.088708')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(int(dms_point.long_deg), 3)
        self.assertEqual(int(dms_point.long_min), 0)
        self.assertEqual(str(dms_point.long_sec)[:5], '0.0')
        self.assertEqual(int(dms_point.lat_deg), 18)
        self.assertEqual(int(dms_point.lat_min), 5)
        self.assertEqual(str(dms_point.lat_sec)[:5], '19.35')
        mgrs_point = converter.convert_UTM_to_MGRS(utm_point)
        self.assertEqual(mgrs_point.zone, '31Q')
        self.assertEqual(mgrs_point.square, 'EA')
        self.assertEqual(mgrs_point.easting, 0)
        self.assertEqual(mgrs_point.northing, 0)

    def test_conversion_of_mgrs_1(self):
        mgrs_point = points.MGRSPoint(55500, 72800, '33U', 'VP')
        utm_point = converter.convert_MGRS_to_UTM(mgrs_point)
        self.assertEqual(utm_point.zone_number, 33)
        self.assertEqual(int(utm_point.easting), 455500)
        self.assertEqual(int(utm_point.northing), 5372800)
        self.assertEqual(utm_point.hemisphere, Hemisphere.NORTH)
        degree_point = converter.utm_to_degree(utm_point)
        self.assertEqual(str(degree_point.long_deg)[:8], '14.39752')
        self.assertEqual(str(degree_point.lat_deg)[:8], '48.50673')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(int(dms_point.long_deg), 14)
        self.assertEqual(int(dms_point.long_min), 23)
        self.assertEqual(str(dms_point.long_sec)[:5], '51.08')
        self.assertEqual(int(dms_point.lat_deg), 48)
        self.assertEqual(int(dms_point.lat_min), 30)
        self.assertEqual(str(dms_point.lat_sec)[:5], '24.26')

    def test_conversion_of_mgrs_2(self):
        mgrs_point = points.MGRSPoint(16794, 10831, '37L', 'BM')
        utm_point = converter.convert_MGRS_to_UTM(mgrs_point)
        self.assertEqual(utm_point.zone_number, 37)
        self.assertEqual(int(utm_point.easting), 216794)
        self.assertEqual(int(utm_point.northing), 9110831)
        self.assertEqual(utm_point.hemisphere, Hemisphere.SOUTH)
        degree_point = converter.utm_to_degree(utm_point)
        self.assertEqual(str(degree_point.long_deg)[:8], '36.43065')
        self.assertEqual(str(degree_point.lat_deg)[:8], '-8.03602')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(int(dms_point.long_deg), 36)
        self.assertEqual(int(dms_point.long_min), 25)
        self.assertEqual(str(dms_point.long_sec)[:5], '50.36')
        self.assertEqual(int(dms_point.lat_deg), -8)
        self.assertEqual(int(dms_point.lat_min), 2)
        self.assertEqual(str(dms_point.lat_sec)[:5], '9.702')

    def test_conversion_of_mgrs_3(self):
        mgrs_point = points.MGRSPoint(78917, 92398, '20J', 'NM')
        utm_point = converter.convert_MGRS_to_UTM(mgrs_point)
        self.assertEqual(utm_point.zone_number, 20)
        self.assertEqual(int(utm_point.easting), 578917)
        self.assertEqual(int(utm_point.northing), 6692398)
        self.assertEqual(utm_point.hemisphere, Hemisphere.SOUTH)
        degree_point = converter.utm_to_degree(utm_point)
        self.assertEqual(str(degree_point.long_deg)[:8], '-62.1826')
        self.assertEqual(str(degree_point.lat_deg)[:8], '-29.8965')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(int(dms_point.long_deg), -62)
        self.assertEqual(int(dms_point.long_min), 10)
        self.assertEqual(str(dms_point.long_sec)[:5], '57.44')
        self.assertEqual(int(dms_point.lat_deg), -29)
        self.assertEqual(int(dms_point.lat_min), 53)
        self.assertEqual(str(dms_point.lat_sec)[:5], '47.54')

    def test_conversion_of_mgrs_4(self):
        mgrs_point = points.MGRSPoint(80363, 76750, '14S', 'MJ')
        utm_point = converter.convert_MGRS_to_UTM(mgrs_point)
        self.assertEqual(utm_point.zone_number, 14)
        self.assertEqual(int(utm_point.easting), 480363)
        self.assertEqual(int(utm_point.northing), 4376750)
        self.assertEqual(utm_point.hemisphere, Hemisphere.NORTH)
        degree_point = converter.utm_to_degree(utm_point)
        self.assertEqual(str(degree_point.long_deg)[:8], '-99.2285')
        self.assertEqual(str(degree_point.lat_deg)[:8], '39.54019')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(int(dms_point.long_deg), -99)
        self.assertEqual(int(dms_point.long_min), 13)
        self.assertEqual(str(dms_point.long_sec)[:5], '42.68')
        self.assertEqual(int(dms_point.lat_deg), 39)
        self.assertEqual(int(dms_point.lat_min), 32)
        self.assertEqual(str(dms_point.lat_sec)[:5], '24.69')

    def test_conversion_of_mgrs_5(self):
        mgrs_point = points.MGRSPoint(28166, 47695, '05Q', 'KB')
        utm_point = converter.convert_MGRS_to_UTM(mgrs_point)
        self.assertEqual(utm_point.zone_number, 5)
        self.assertEqual(int(utm_point.easting), 228166)
        self.assertEqual(int(utm_point.northing), 2147695)
        self.assertEqual(utm_point.hemisphere, Hemisphere.NORTH)
        degree_point = converter.utm_to_degree(utm_point)
        self.assertEqual(str(degree_point.long_deg)[:8], '-155.588')
        self.assertEqual(str(degree_point.lat_deg)[:8], '19.40511')
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(degree_point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(degree_point.lat_deg)
        dms_point = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(int(dms_point.long_deg), -155)
        self.assertEqual(int(dms_point.long_min), 35)
        self.assertEqual(str(dms_point.long_sec)[:5], '18.20')
        self.assertEqual(int(dms_point.lat_deg), 19)
        self.assertEqual(int(dms_point.lat_min), 24)
        self.assertEqual(str(dms_point.lat_sec)[:5], '18.42')


    #test for comma minutes to degree and dms
    def test_comma_minutes_to_other(self):
        point = points.WGSPoint(1, 32, 0, 2, 31, 0)
        long_deg = converter.convert_decimal_minutes_to_degree(float(point.long_deg), float(point.long_min))
        lat_deg = converter.convert_decimal_minutes_to_degree(float(point.lat_deg), float(point.lat_min))
        p = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        #self.assertEqual(format(p.long_deg, '.4f'), '-3.0750')
        #self.assertEqual(format(p.lat_deg, '.4f'), '10.9833')
        print('WGS_Degree_long: ' + str(p.long_deg))
        print('WGS_Degree_lat: ' + str(p.lat_deg))
        print('WGS_Degree: ' + p.to_string(CoordinateSystemString.WGS84_Degrees.value))
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(p.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(p.lat_deg)
        p_1 = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        # self.assertEqual(p_1.long_deg, 1)
        # self.assertEqual(p_1.long_min, 31)
        # self.assertEqual(format(p_1.long_sec, '06.3f')[0:5], '00.00')
        # self.assertEqual(p_1.lat_deg, 10)
        # self.assertEqual(p_1.lat_min, 59)
        # self.assertEqual('59.99', '59.99')
        print('WGS_DMS_long: ' + str(p_1.long_deg) + ' ' + str(p_1.long_min) + ' ' + str(p_1.long_sec))
        print('WGS_DMS_lat: ' + str(p_1.lat_deg) + ' ' + str(p_1.lat_min) + ' ' + str(p_1.lat_sec))
        print('WGS_DMS: ' + p_1.to_string(CoordinateSystemString.WGS84_DMS.value))

    #test for dms to degree and comma mintues
    def test_dms_to_other(self):
        point = points.WGSPoint(3, 59, Decimal(59.999), 10, 12, 30)
        long_deg = converter.convert_DMS_to_degree(point.long_deg, point.long_min, point.long_sec)
        lat_deg = converter.convert_DMS_to_degree(point.lat_deg, point.lat_min, point.lat_sec)
        p = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        self.assertEqual(str(p.long_deg)[:8], '3.999999')
        self.assertEqual(format(p.lat_deg, '.4f'), '10.2083')
        long_deg, long_min = converter.convert_degree_to_decimal_minutes(p.long_deg)
        lat_deg, lat_min = converter.convert_degree_to_decimal_minutes(p.lat_deg)
        p_1 = points.WGSPoint(long_deg, long_min, 0, lat_deg, lat_min, 0)
        self.assertEqual(p_1.long_deg, 3)
        self.assertEqual(str(p_1.long_min)[:5], '59.99')
        self.assertEqual(p_1.long_sec, 0)
        self.assertEqual(p_1.lat_deg, 10)
        self.assertEqual(format(p_1.lat_min, '.2f'), '12.50')
        self.assertEqual(p_1.lat_sec, 0)

    #test for degree to comma minutes and dms
    def test_degree_to_other(self):
        point = points.WGSPoint(-3.0750, 0, 0, 10.2083, 0, 0)
        long_deg, long_min = converter.convert_degree_to_decimal_minutes(point.long_deg)
        lat_deg, lat_min = converter.convert_degree_to_decimal_minutes(point.lat_deg)
        p = points.WGSPoint(long_deg, long_min, 0, lat_deg, lat_min, 0)
        self.assertEqual(p.long_deg, -3)
        self.assertEqual(format(p.long_min, '.2f'), '4.50')
        self.assertEqual(p.long_sec, 0)
        self.assertEqual(p.lat_deg, 10)
        self.assertEqual(format(p.lat_min, '.2f'), '12.50')
        self.assertEqual(p.lat_sec, 0)
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(point.lat_deg)
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
        self.assertEqual(p_1.zone_number, 31)
        self.assertEqual(p_1.hemisphere, Hemisphere.SOUTH)
        self.assertEqual(int(p_1.easting), 500000)
        self.assertEqual(int(p_1.northing), 8894587)

    #test for utm -> degree
    def test_utm_to_degree(self):
        point = points.UTMPoint(456331, 1562000, 33, None,  Hemisphere.NORTH)
        p_1 = converter.utm_to_degree(point)
        self.assertEqual(format(p_1.lat_deg, '.4f'), '14.1287')
        self.assertEqual(format(p_1.long_deg, '.4f'), '14.5954')

    #test for mgrs -> utm
    def test_MGRS_to_UTM(self):
        point = points.MGRSPoint(12345, 12345, '33U', 'VP')
        p_1 = converter.convert_MGRS_to_UTM(point)
        self.assertEqual(p_1.zone_number, 33)
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
        point = points.WGSPoint(16, 59, 59.9999, 10, 12, 30)
        print(point.to_string('WGS_DEGREES'))
        long_deg = converter.convert_DMS_to_degree(point.long_deg, point.long_min, point.long_sec)
        lat_deg = converter.convert_DMS_to_degree(point.lat_deg, point.lat_min, point.lat_sec)
        print(long_deg)
        p = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        print(str(p.long_deg))
        print(p.to_string('WGS_DEGREES'))

    def test_def(self):
        point = points.WGSPoint(3, 0, 0, -10, 0, 0)
        point = converter.degree_to_utm(point)
        print(point.to_string())

    def test_ghi(self):
        point = points.UTMPoint(123456, 1, 33, 'L', Hemisphere.NORTH)
        point = converter.utm_to_degree(point)
        print(point.to_string(CoordinateSystemString.WGS84_Degrees.value))
        long_deg, long_min, long_sec = converter.convert_degree_to_DMS(point.long_deg)
        lat_deg, lat_min, lat_sec = converter.convert_degree_to_DMS(point.lat_deg)
        print(str(long_deg))
        print(str(lat_deg))

    def test_deg_to_mgrs(self):
        point = points.WGSPoint(16, 0, 0, 10, 0, 0)
        p1 = self.__degree_to_mgrs(point)
        print(p1.to_string())

    def test_deg_to_mgrs3(self):
        point = points.WGSPoint(0, 32, 0, 0, 31, 0)
        long_deg = converter.convert_DMS_to_degree(point.long_deg, point.long_min, point.long_sec)
        lat_deg = converter.convert_DMS_to_degree(point.lat_deg, point.lat_min, point.lat_sec)
        deg_point = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        print('Deg point: ' + deg_point.to_string(CoordinateSystemString.WGS84_Degrees.value))
        p1 = self.__degree_to_mgrs(deg_point)
        print('With lib: ' + p1.to_string())
        p = converter.degree_to_utm(deg_point)
        print(p.to_string())
        p2 = converter.convert_UTM_to_MGRS(p)
        print('Without lib: ' + p2.to_string())

    def __degree_to_mgrs(self, point):
        m = mgrs.MGRS()
        c = m.toMGRS(point.lat_deg, point.long_deg)
        zone = c[:3]
        square = c[3:5]
        easting = c[5:10]
        northing = c[10:]

        point = points.MGRSPoint(easting, northing, zone, square)
        return point


if __name__ == '__main__':
    unittest.main()