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