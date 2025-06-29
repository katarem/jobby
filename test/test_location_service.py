import unittest
from service.location_service import LocationService

class TestLocationService(unittest.TestCase):

    def setUp(self):
        self.location_service = LocationService()

    def test_parse_location_valid(self):
        result = self.location_service.parse_location("European Union")
        self.assertEqual(result, 91000000)

    def test_parse_location_invalid(self):
        result = self.location_service.parse_location("Unknown Location")
        self.assertIsNone(result)

    def test_parse_location_case_insensitive(self):
        result = self.location_service.parse_location("european union")
        self.assertEqual(result, 91000000)

    def test_parse_location_with_spaces(self):
        result = self.location_service.parse_location("  european union  ")
        self.assertEqual(result, 91000000)
