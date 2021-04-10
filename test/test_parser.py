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

    def test_parse_location_all_values(self):
        data = {
            'realtimeActivated': True,
            'tiploc': [
                'FIRSTTIP',
                'SECONDTIP',
                'THIRDTIP'
            ],
            'crs': 'ABC',
            'description': 'Example Station',
            'wttBookedArrival': '1251',
            'wttBookedDeparture': '1253',
            'wttBookedPass': '1255',
            'gbttBookedArrival': '1251',
            'gbttBookedDeparture': '1253',
            'origin': [
                {
                    'tiploc': 'VICTORIA',
                    'description': 'London Victoria',
                    'workingTime': '113600',
                    'publicTime': '1136'
                }
            ],
            'destination': [
                {
                    'tiploc': 'SOTON',
                    'description': 'Southampton Central',
                    'workingTime': '133700',
                    'publicTime': '1337'
                },
                {
                    'tiploc': 'BOGNOR',
                    'description': 'Bognor Regis',
                    'workingTime': '130400',
                    'publicTime': '1304'
                }
            ],
            'realtimeArrival': '1251',
            'realtimeArrivalActual': '1252',
            'realtimeArrivalNoReport': True,
            'realtimeWttArrivalLateness': '3',
            'realtimeGbttArrivalLateness': '4',
            'realtimeDeparture': '1253',
            'realtimeDepartureActual': '1253',
            'realtimeDepartureNoReport': True,
            'realtimeWttDepartureLateness': '1',
            'realtimeGbttDepartureLateness': '2',
            'platform': '2A',
            'platformConfirmed': True,
            'platformChanged': True,
            'line': 'M',
            'lineConfirmed': True,
            'path': 'UP',
            'pathConfirmed': True,
            'cancelReasonCode': 'LEA',
            'cancelReasonShortText': 'leaves on the line',
            'cancelReasonLongText': 'leaves on the line in the Havant area',
            'displayAs': 'CALL',
            'serviceLocation': 'DEP_READY'
        }

        actual = parser.parse_location(data)

        self.assertTrue(actual.realtime_activated)
        self.assertEqual(['FIRSTTIP', 'SECONDTIP','THIRDTIP'], actual.tiploc)
        self.assertEqual('ABC', actual.crs)
        self.assertEqual('Example Station', actual.description)
        self.assertEqual('1251', actual.wtt_booked_arrival)
        self.assertEqual('1253', actual.wtt_booked_departure)
        self.assertEqual('1255', actual.wtt_booked_pass)
        self.assertEqual('1251', actual.gbtt_booked_arrival)
        self.assertEqual('1253', actual.gbtt_booked_departure)

        self.assertEqual(1, len(actual.origin))
        self.assertEqual('VICTORIA', actual.origin[0].tiploc)
        self.assertEqual('London Victoria', actual.origin[0].description)
        self.assertEqual('113600', actual.origin[0].working_time)
        self.assertEqual('1136', actual.origin[0].public_time)

        self.assertEqual(2, len(actual.destination))
        self.assertEqual('SOTON', actual.destination[0].tiploc)
        self.assertEqual('Southampton Central', actual.destination[0].description)
        self.assertEqual('133700', actual.destination[0].working_time)
        self.assertEqual('1337', actual.destination[0].public_time)

        self.assertEqual('BOGNOR', actual.destination[1].tiploc)
        self.assertEqual('Bognor Regis', actual.destination[1].description)
        self.assertEqual('130400', actual.destination[1].working_time)
        self.assertEqual('1304', actual.destination[1].public_time)

        self.assertEqual('1251', actual.realtime_arrival)
        self.assertEqual('1252', actual.realtime_arrival_actual)
        self.assertTrue(actual.realtime_arrival_no_report)
        self.assertEqual('3', actual.realtime_wtt_arrival_lateness)
        self.assertEqual('4', actual.realtime_gbtt_arrival_lateness)

        self.assertEqual('1253', actual.realtime_departure)
        self.assertEqual('1253', actual.realtime_departure_actual)
        self.assertTrue(actual.realtime_departure_no_report)
        self.assertEqual('1', actual.realtime_wtt_departure_lateness)
        self.assertEqual('2', actual.realtime_gbtt_departure_lateness)

        self.assertEqual('2A', actual.platform)
        self.assertTrue(actual.platform_confirmed)
        self.assertTrue(actual.platform_changed)

        self.assertEqual('M', actual.line)
        self.assertTrue(actual.line_confirmed)

        self.assertEqual('UP', actual.path)
        self.assertTrue(actual.path_confirmed)

        self.assertEqual('LEA', actual.cancel_reason_code)
        self.assertEqual('leaves on the line', actual.cancel_reason_short_text)
        self.assertEqual('leaves on the line in the Havant area', actual.cancel_reason_long_text)

        self.assertEqual('CALL', actual.display_as)
        self.assertEqual('DEP_READY', actual.service_location)