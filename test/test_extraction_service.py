from unittest import TestCase

from service.extraction_service import ExtractionService

class ExtractionServiceTest(TestCase):

    extraction_service: ExtractionService

    def setUp(self):
        self.extraction_service = ExtractionService(['hello','world'])

    def test_detect_keywords_ok(self):
        description = 'Hello World!!'
        self.assertTrue(self.extraction_service.detect_keywords(description))

    def test_detect_keywords_ko(self):
        description = 'Helo Worl!!'
        self.assertFalse(self.extraction_service.detect_keywords(description))

    def test_extract_keywords_ok_contains_all(self):
        expected_keywords = ['hello', 'world']
        description = 'Hello everyone welcome to this fantastic world full of people'
        self.assertEqual(expected_keywords, self.extraction_service.extract_keywords(description))

    def test_extract_keywords_ok_contains_only_one(self):
        expected_keywords = ['world']
        description = 'Helo everyone welcome to this fantastic world full of people'
        self.assertEqual(expected_keywords, self.extraction_service.extract_keywords(description))

    def test_extract_keywords_ko(self):
        expected_keywords = []
        description = 'Helo everyone welcome to this fantastic wold full of people'
        self.assertEqual(expected_keywords, self.extraction_service.extract_keywords(description))