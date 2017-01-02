# -*- coding: utf-8 -*-
import unittest
import ensurer
import imp
exceptions = imp.load_source('exceptions','../exceptions.py')

class EnsurerTest(unittest.TestCase):

    def test_ensure_mgrs_zone_invalid1(self):
        try:
            string = ''
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_zone(string)
        except exceptions.ParseException, e:
            self.assertTrue('Eingabe noch nicht vollzählig' in e.message)

    def test_ensure_mgrs_zone_invalid2(self):
        try:
            string = '3'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_zone(string)
        except exceptions.ParseException, e:
            self.assertTrue('Eingabe noch nicht vollzählig' in e.message)

    def test_ensure_mgrs_zone_invalid3(self):
        try:
            string = 'a'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_zone(string)
        except exceptions.ParseException, e:
            self.assertTrue('Zone muss mit Zahl beginnen.' in e.message)

    def test_ensure_mgrs_zone_invalid4(self):
        try:
            string = '33'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_zone(string)
        except exceptions.ParseException, e:
            self.assertTrue('Eingabe noch nicht vollzählig' in e.message)

    def test_ensure_mgrs_zone_invalid5(self):
        try:
            string = '3a'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_zone(string)
        except exceptions.ParseException, e:
            self.assertTrue('Zone muss aus zwei Ziffern bestehen.' in e.message)

    def test_ensure_mgrs_zone_invalid6(self):
        try:
            string = '33!'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_zone(string)
        except exceptions.ParseException, e:
            self.assertTrue('Zone muss aus zwei Ziffern und einem Buchstaben bestehen.' in e.message)

    def test_ensure_mgrs_zone_invalid7(self):
        try:
            string = '33I'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_zone(string)
        except exceptions.ParseException, e:
            self.assertTrue('Invalid latitude grid-zone: I in MGRS-String (accepted values: C-X omitting I and O)'
                            in e.message)

    def test_ensure_mgrs_zone_invalid8(self):
        try:
            string = '32X'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_zone(string)
        except exceptions.ParseException, e:
            self.assertTrue('Invalid grid zone designation: grid zone 32 X does not exist.' in e.message)

    def test_ensure_mgrs_zone_valid(self):
        string = '33U'
        e = ensurer.Ensurer()
        erg = e.ensure_it_is_a_valid_mgrs_zone(string)
        self.assertEqual(erg, '33U')

    def test_ensure_mgrs_square_invalid(self):
        try:
            string = '3'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_square(string)
        except exceptions.ParseException, e:
            self.assertTrue('Gitterquadrat muss mit Buchstaben beginnen.' in e.message)

    def test_ensure_mgrs_square_invalid2(self):
        try:
            string = 'X'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_square(string)
        except exceptions.ParseException, e:
            self.assertTrue('Eingabe noch nicht vollzählig' in e.message)

    def test_ensure_mgrs_square_invalid3(self):
        try:
            string = 'X1'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_square(string)
        except exceptions.ParseException, e:
            self.assertTrue('Gitterquadrat muss aus zwei Buchstaben bestehen.' in e.message)

    def test_ensure_mgrs_square_invalid4(self):
        try:
            string = 'UVP'
            e = ensurer.Ensurer()
            erg = e.ensure_it_is_a_valid_mgrs_square(string)
        except exceptions.ParseException, e:
            self.assertTrue('Eingabe zu lange' in e.message)

    def test_ensure_mgrs_square_valid(self):
        string = 'UV'
        e = ensurer.Ensurer()
        erg = e.ensure_it_is_a_valid_mgrs_square(string)
        self.assertEqual(erg, 'UV')