# -*- coding: utf-8 -*-
import unittest
import ensurer
import imp
exceptions = imp.load_source('exceptions','../exceptions.py')


class EnsurerTest(unittest.TestCase):

    def test_ensure_mgrs_zone_invalid1(self):
        try:
            string = ''
            erg = ensurer.ensure_it_is_a_valid_mgrs_zone(string, True)
        except exceptions.ParseException, e:
            self.assertTrue(ensurer.INPUT_NOT_COMPLETE_DE in e.message)

    def test_ensure_mgrs_zone_invalid2(self):
        try:
            string = '3'
            erg = ensurer.ensure_it_is_a_valid_mgrs_zone(string, True)
        except exceptions.ParseException, e:
            self.assertTrue(ensurer.INPUT_NOT_COMPLETE_DE in e.message)

    def test_ensure_mgrs_zone_invalid3(self):
        try:
            string = 'a'
            erg = ensurer.ensure_it_is_a_valid_mgrs_zone(string, True)
        except exceptions.ParseException, e:
            self.assertTrue(ensurer.ZONE_HAS_TO_START_WITH_NUMBER_DE in e.message)

    def test_ensure_mgrs_zone_invalid4(self):
        try:
            string = '33'
            erg = ensurer.ensure_it_is_a_valid_mgrs_zone(string, True)
        except exceptions.ParseException, e:
            self.assertTrue(ensurer.INPUT_NOT_COMPLETE_DE in e.message)

    def test_ensure_mgrs_zone_invalid5(self):
        try:
            string = '3a'
            erg = ensurer.ensure_it_is_a_valid_mgrs_zone(string, True)
        except exceptions.ParseException, e:
            self.assertTrue(ensurer.ZONE_HAS_TO_CONTAIN_TWO_NUMBERS_DE in e.message)

    def test_ensure_mgrs_zone_invalid6(self):
        try:
            string = '33!'
            erg = ensurer.ensure_it_is_a_valid_mgrs_zone(string, True)
        except exceptions.ParseException, e:
            self.assertTrue(ensurer.ZONE_HAS_TO_CONTAIN_TWO_NUMBERS_AND_A_LETTER_DE in e.message)

    def test_ensure_mgrs_zone_invalid7(self):
        try:
            string = '33I'
            erg = ensurer.ensure_it_is_a_valid_mgrs_zone(string, True)
        except exceptions.ParseException, e:
            self.assertTrue(ensurer.INVALID_LAT_GRID_ZONE_DE.format('I') in e.message)

    def test_ensure_mgrs_zone_invalid8(self):
        try:
            string = '32X'
            erg = ensurer.ensure_it_is_a_valid_mgrs_zone(string, True)
        except exceptions.ParseException, e:
            print e.message
            self.assertTrue(ensurer.INVALID_MGRS_SQUARE_LETTRES_DE.format(32, 'X') in e.message)

    def test_ensure_mgrs_zone_valid(self):
        string = '33U'
        erg = ensurer.ensure_it_is_a_valid_mgrs_zone(string, True)
        self.assertEqual(erg, '33U')

    def test_ensure_mgrs_square_invalid(self):
        try:
            string = '3'
            erg = ensurer.ensure_it_is_a_valid_mgrs_square(string, True)
        except exceptions.ParseException, e:
            print e.message
            self.assertTrue(ensurer.SQUARE_HAS_TO_START_WITH_DE in e.message)

    def test_ensure_mgrs_square_invalid2(self):
        try:
            string = 'X'
            erg = ensurer.ensure_it_is_a_valid_mgrs_square(string, True)
        except exceptions.ParseException, e:
            self.assertTrue(ensurer.INPUT_NOT_COMPLETE_DE in e.message)

    def test_ensure_mgrs_square_invalid3(self):
        try:
            string = 'X1'
            erg = ensurer.ensure_it_is_a_valid_mgrs_square(string, True)
        except exceptions.ParseException, e:
            self.assertTrue(ensurer.SQUARE_HAS_TO_BE_TWO_LETTERS_DE in e.message)

    def test_ensure_mgrs_square_invalid4(self):
        try:
            string = 'UVP'
            erg = ensurer.ensure_it_is_a_valid_mgrs_square(string, True)
        except exceptions.ParseException, e:
            self.assertTrue(ensurer.INPUT_TO_LONG_DE in e.message)

    def test_ensure_mgrs_square_valid(self):
        string = 'UV'
        erg = ensurer.ensure_it_is_a_valid_mgrs_square(string, True)
        self.assertEqual(erg, 'UV')