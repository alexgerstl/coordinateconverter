# -*- coding: utf-8 -*-
import unittest
import imp
from coordinate_parser import Parser, Hemisphere, ParserStatus, CoordinateSystemString
from ensurer import Ensurer

exceptions = imp.load_source('exceptions','../exceptions.py')


class CoordinateParserTest(unittest.TestCase):

    def test_unknownSystem(self):
        with self.assertRaises(exceptions.ParseException):
            Parser().parse('#')

    def test_incomplete(self):
        try:
            parser = Parser()
            coordinate = '3'
            point = parser.parse(coordinate)
        except exceptions.ParseException, e:
            self.assertTrue(e.status, ParserStatus.INCOMPLETE)

    def test_incomplete2(self):
        try:
            parser = Parser()
            coordinate = '33UVP1'
            point = parser.parse(coordinate)
        except exceptions.ParseException, e:
                self.assertTrue('Missing valid easting/northing values' in e.message)

    def test_valid_MGRS(self):
        parser = Parser()
        point = parser.parse('33UVP1234567890')
        self.assertEqual(parser.guessed_system, CoordinateSystemString.MGRS)
        self.assertEqual(point.hemisphere,Hemisphere.NORTH)
        self.assertEqual(point.zone, '33U')
        self.assertEqual(point.square, 'VP')
        self.assertEqual(point.easting, 12345)
        self.assertEqual(point.northing, 67890)

    def test_valid_MGRS_completed(self):
        parser = Parser()
        point = parser.parse('33UVP11')
        self.assertEqual(point.zone, '33U')
        self.assertEqual(point.square, 'VP')
        self.assertEqual(point.easting, 10000)
        self.assertEqual(point.northing, 10000)

    def test_invalid_MGRS(self):
        with self.assertRaises(exceptions.ParseException):
            Parser().parse('77UVP1234567890')

    def test_valid_UTM(self):
        parser = Parser()
        point = parser.parse('12N123456E1234567N')
        self.assertEqual(parser.guessed_system, CoordinateSystemString.UTM)
        self.assertEqual(point.hemisphere, Hemisphere.NORTH)
        self.assertEqual(point.zone, 12)
        self.assertEqual(point.easting, 123456)
        self.assertEqual(point.northing, 1234567)

    def test_valid_UTM_2(self):
        parser = Parser()
        point = parser.parse('12N1234567N123456E')
        self.assertEqual(parser.guessed_system, CoordinateSystemString.UTM)
        self.assertEqual(point.hemisphere, Hemisphere.NORTH)
        self.assertEqual(point.zone, 12)
        self.assertEqual(point.easting, 123456)
        self.assertEqual(point.northing, 1234567)

    def test_invalid_UTM(self):
        with self.assertRaises(exceptions.ConversionException):
            Parser().parse('99N123456E1234567N')

    def test_invalid_UTM_2(self):
        with self.assertRaises(exceptions.ParseException):
            Parser().parse('12X123456E1234567N')

    def test_invalid_UTM_3(self):
        with self.assertRaises(exceptions.ConversionException):
            Parser().parse('12N123456W1234567N')

    def test_valid_WGS(self):
        parser = Parser()
        coordinate = '12.345678'u'\xb0''E12.345678'u'\xb0''N'
        point = parser.parse(coordinate)
        self.assertEqual(point.long_deg,12.345678)
        self.assertEqual(point.lat_deg,12.345678)

    def test_valid_WGS2(self):
        parser = Parser()
        coordinate = '12.345678E12.345678N'
        point = parser.parse(coordinate)
        self.assertEqual(point.long_deg, 12.345678)
        self.assertEqual(point.lat_deg, 12.345678)

    def test_valid_WGS_3(self):
        parser = Parser()
        coordinate = '12'u'\xb0''23\'45"E23'u'\xb0''15\'32"N'
        point = parser.parse(coordinate)
        self.assertEqual(point.long_deg, 12)
        self.assertEqual(point.long_min, 23)
        self.assertEqual(point.long_sec, 45)
        self.assertEqual(point.lat_deg, 23)
        self.assertEqual(point.lat_min, 15)
        self.assertEqual(point.lat_sec, 32)

    def test_valid_WGS_4(self):
        parser = Parser()
        coordinate = '12'u'\xb0''23.45\'E23'u'\xb0''15.32\'N'
        point = parser.parse(coordinate)
        self.assertEqual(point.long_deg, 12)
        self.assertEqual(point.long_min, 23.45)
        self.assertEqual(point.lat_deg, 23)
        self.assertEqual(point.lat_min, 15.32)


if __name__ == '__main__':
    unittest.main()