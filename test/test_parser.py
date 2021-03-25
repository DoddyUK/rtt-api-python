import rttapi.parser as parser
import unittest

class ParserTest(unittest.TestCase):

    def test_parse_pair(self):
        data = {
            'tiploc': 'SOTON',
            'description': 'Southampton Central',
            'workingTime': '125100',
            'publicTime': '1251'
        }

        actual = parser.parse_pair(data)

        self.assertEqual('SOTON', actual.tiploc)
        self.assertEqual('Southampton Central', actual.description)
        self.assertEqual('125100', actual.working_time)
        self.assertEqual('1251', actual.public_time)

    def test_parse_pair_without_tiploc_fails(self):
        data = {
            'description': 'Southampton Central',
            'workingTime': '125100',
            'publicTime': '1251'
        }

        with self.assertRaises(ValueError):
            parser.parse_pair(data)

    def test_parse_pair_without_description_fails(self):
        data = {
            'tiploc': 'SOTON',
            'workingTime': '125100',
            'publicTime': '1251'
        }

        with self.assertRaises(ValueError):
            parser.parse_pair(data)

    def test_parse_pair_without_working_time_fails(self):
        data = {
            'tiploc': 'SOTON',
            'description': 'Southampton Central',
            'publicTime': '1251'
        }

        with self.assertRaises(ValueError):
            parser.parse_pair(data)

    def test_parse_pair_without_public_time_fails(self):
        data = {
            'tiploc': 'SOTON',
            'description': 'Southampton Central',
            'workingTime': '125100',
        }

        with self.assertRaises(ValueError):
            parser.parse_pair(data)

    def test_parse_location_detail_single_tiploc(self):
        data = {
            'name': 'Southampton Central',
            'crs': 'SOU',
            'tiploc': 'SOTON'
        }

        actual = parser.parse_location_detail(data)

        self.assertEqual('Southampton Central', actual.name)
        self.assertEqual('SOU', actual.crs)
        self.assertEqual('SOTON', actual.tiploc)

    def test_parse_location_detail_array_tiploc(self):
        data = {
            'name': 'Clapham Junction',
            'crs': 'CLJ',
            'tiploc': ["CLPHMJ1", "CLPHMJ2", "CLPHMJC", "CLPHMJM", "CLPHMJN", "CLPHMJW"]
        }

        actual = parser.parse_location_detail(data)

        self.assertEqual('Clapham Junction', actual.name)
        self.assertEqual('CLJ', actual.crs)
        self.assertEqual(
            ["CLPHMJ1", "CLPHMJ2", "CLPHMJC", "CLPHMJM", "CLPHMJN", "CLPHMJW"],
            actual.tiploc
        )

    def test_parse_location_detail_without_name_fails(self):
        data = {
            'crs': 'SOU',
            'tiploc': 'SOTON'
        }

        with self.assertRaises(ValueError):
            parser.parse_pair(data)

    def test_parse_location_detail_without_crs_fails(self):
        data = {
            'name': 'Southampton Central',
            'tiploc': 'SOTON'
        }

        with self.assertRaises(ValueError):
            parser.parse_pair(data)

    def test_parse_location_detail_without_tiploc_fails(self):
        data = {
            'name': 'Southampton Central',
            'crs': 'SOU'
        }

        with self.assertRaises(ValueError):
            parser.parse_pair(data)


    def test_parse_search_without_filter(self):
        data = {
            'location': {
                'name': 'Southampton Central',
                'crs': 'SOU',
                'tiploc': 'SOTON'
            },
            'filter': None,
            'services': []
        }

        actual = parser.parse_search(data)

        self.assertEqual('Southampton Central', actual.location.name)
        self.assertEqual('SOU', actual.location.crs)
        self.assertEqual('SOTON', actual.location.tiploc)
        self.assertIsNone(actual.filter)
        self.assertEqual(0, len(actual.services))

    def test_parse_search_with_filter(self):
        data = {
            'location': {
                'name': 'Southampton Central',
                'crs': 'SOU',
                'tiploc': 'SOTON'
            },
            'filter': {
                'name': 'Basingstoke',
                'crs': 'BSK',
                'tiploc': 'BSNGSTK'
            },
            'services': None
        }

        actual = parser.parse_search(data)

        self.assertEqual('Southampton Central', actual.location.name)
        self.assertEqual('SOU', actual.location.crs)
        self.assertEqual('SOTON', actual.location.tiploc)
        self.assertEqual('Basingstoke', actual.filter.name)
        self.assertEqual('BSK', actual.filter.crs)
        self.assertEqual('BSNGSTK', actual.filter.tiploc)
        self.assertEqual(0, len(actual.services))

    def test_parse_search_with_null_location_fails(self):
        data = {
            'location': None,
            'filter': None,
            'services': None
        }

        with self.assertRaises(ValueError):
            parser.parse_search(data)

    def test_parse_search_with_missing_location_fails(self):
        data = {
            'filter': None,
            'services': None
        }

        with self.assertRaises(ValueError):
            parser.parse_search(data)

    def test_parse_search_with_missing_filter_fails(self):
        data = {
            'location': {
                'name': 'Southampton Central',
                'crs': 'SOU',
                'tiploc': 'SOTON'
            },
            'services': None
        }

        with self.assertRaises(ValueError):
            parser.parse_search(data)

    def test_parse_search_with_missing_services_fails(self):
        data = {
            'location': {
                'name': 'Southampton Central',
                'crs': 'SOU',
                'tiploc': 'SOTON'
            },
            'filter': None
        }

        with self.assertRaises(ValueError):
            parser.parse_search(data)