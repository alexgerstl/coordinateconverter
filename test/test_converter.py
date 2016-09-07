# -*- coding: utf-8 -*-
import unittest
import points
from coordinate_parser import Parser, Hemisphere, CoordinateSystemString
from converter import Converter


class ConverterTest(unittest.TestCase):

    #test for comma minutes to degree and dms
    def test_comma_minutes_to_other(self):
        f = Converter()
        point = points.WGSPoint(3, 4.5, 0, 10, 12.5, 0)
        long_deg = f.convert_decimal_minutes_to_degree(point.long_deg, point.long_min)
        lat_deg = f.convert_decimal_minutes_to_degree(point.lat_deg, point.lat_min)
        p = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        self.assertEqual(format(p.long_deg, '.4f'), '3.0750')
        self.assertEqual(format(p.lat_deg, '.4f'), '10.2083')
        long_deg, long_min, long_sec = f.convert_degree_to_DMS(p.long_deg)
        lat_deg, lat_min, lat_sec = f.convert_degree_to_DMS(p.lat_deg)
        p_1 = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(p_1.long_deg, 3)
        self.assertEqual(p_1.long_min, 4)
        self.assertEqual(format(p_1.long_sec, '.0f'), '30')
        self.assertEqual(p_1.lat_deg, 10)
        self.assertEqual(p_1.lat_min, 12)
        self.assertEqual(format(p_1.lat_sec, '.0f'), '30')

    #test for dms to degree and comma mintues
    def test_dms_to_other(self):
        f = Converter()
        point = points.WGSPoint(3, 4, 30, 10, 12, 30)
        long_deg = f.convert_DMS_to_degree(point.long_deg, point.long_min, point.long_sec)
        lat_deg = f.convert_DMS_to_degree(point.lat_deg, point.lat_min, point.lat_sec)
        p = points.WGSPoint(long_deg, 0, 0, lat_deg, 0, 0)
        self.assertEqual(format(p.long_deg, '.4f'), '3.0750')
        self.assertEqual(format(p.lat_deg, '.4f'), '10.2083')
        long_deg, long_min = f.convert_degree_to_decimal_minutes(p.long_deg)
        lat_deg, lat_min = f.convert_degree_to_decimal_minutes(p.lat_deg)
        p_1 = points.WGSPoint(long_deg, long_min, 0, lat_deg, lat_min, 0)
        self.assertEqual(p_1.long_deg, 3)
        self.assertEqual(format(p_1.long_min, '.2f'), '4.50')
        self.assertEqual(p_1.long_sec, 0)
        self.assertEqual(p_1.lat_deg, 10)
        self.assertEqual(format(p_1.lat_min, '.2f'), '12.50')
        self.assertEqual(p_1.lat_sec, 0)

    #test for degree to comma minutes and dms
    def test_degree_to_other(self):
        f = Converter()
        point = points.WGSPoint(3.0750, 0, 0, 10.2083, 0, 0)
        long_deg, long_min = f.convert_degree_to_decimal_minutes(point.long_deg)
        lat_deg, lat_min = f.convert_degree_to_decimal_minutes(point.lat_deg)
        p = points.WGSPoint(long_deg, long_min, 0, lat_deg, lat_min, 0)
        self.assertEqual(p.long_deg, 3)
        self.assertEqual(format(p.long_min, '.2f'), '4.50')
        self.assertEqual(p.long_sec, 0)
        self.assertEqual(p.lat_deg, 10)
        self.assertEqual(format(p.lat_min, '.2f'), '12.50')
        self.assertEqual(p.lat_sec, 0)
        long_deg, long_min, long_sec = f.convert_degree_to_DMS(point.long_deg)
        lat_deg, lat_min, lat_sec = f.convert_degree_to_DMS(point.lat_deg)
        p_1 = points.WGSPoint(long_deg, long_min, long_sec, lat_deg, lat_min, lat_sec)
        self.assertEqual(p_1.long_deg, 3)
        self.assertEqual(p_1.long_min, 4)
        self.assertEqual(format(p_1.long_sec, '.0f'), '30')
        self.assertEqual(p_1.lat_deg, 10)
        self.assertEqual(p_1.lat_min, 12)
        self.assertEqual(format(p_1.lat_sec, '.0f'), '30')

    #test for degree -> utm
    def test_degree_to_UTM(self):
        f = Converter()
        point = points.WGSPoint(3.0750, 0, 0, 10.2083, 0, 0)
        p_1 = f.convert_degree_to_UTM(point)
        self.assertEqual(p_1.zone, 31)
        self.assertEqual(p_1.hemisphere, Hemisphere.NORTH)
        self.assertEqual(p_1.easting, 508214)
        self.assertEqual(p_1.northing, 1128443)

    #test for utm -> degree
    def test_utm_to_degree(self):
        f = Converter()
        point = points.UTMPoint(123456, 1234567, 12, Hemisphere.NORTH)
        p_1 = f.convert_UTM_to_degree(point)
        self.assertEqual(format(p_1.long_deg, '.4f'), '-114.4466')
        self.assertEqual(format(p_1.lat_deg, '.4f'), '11.1483')

    #test for mgrs -> utm
    def test_MGRS_to_UTM(self):
        f = Converter()
        point = points.MGRSPoint(12345, 12345, '33U', 'VP', Hemisphere.NORTH)
        p_1 = f.convert_MGRS_to_UTM(point)
        self.assertEqual(p_1.zone, 33)
        self.assertEqual(p_1.hemisphere, Hemisphere.NORTH)
        self.assertEqual(p_1.easting, 412345)
        self.assertEqual(p_1.northing, 5312345)

if __name__ == '__main__':
    unittest.main()