import unittest
from configuration.model.config import Config
from job.model.job import Job
from job.model.job_details import JobDetails
from filters.service.filter_service import FilterService
from extraction.service.extraction_service import ExtractionService
from location.service.location_service import LocationService

class TestFilterService(unittest.TestCase):

    def setUp(self):
        self.extraction_service = ExtractionService(["Python", "Django"])
        self.location_service = LocationService()
        self.filter_service = FilterService(self.extraction_service, self.location_service)

    def test_apply_filters_with_keywords(self):
        job = Job("Title", "Description with Python", "Company", "URL", None, JobDetails("Location", "Date", "Applications"))
        config = Config(title="developer", search_location="European Union", filter_locations=[], keywords=["python"])
        filtered_jobs = self.filter_service.apply_filters([job], config)
        self.assertEqual(len(filtered_jobs), 1)
        self.assertEqual(filtered_jobs[0].matching_keywords, ["python"])

    def test_apply_filters_without_keywords(self):
        job = Job("Title", "Description without keywords", "Company", "URL", None, JobDetails("Location", "Date", "Applications"))
        config = Config(title="developer", search_location="European Union", filter_locations=[], keywords=[])
        filtered_jobs = self.filter_service.apply_filters([job], config)
        self.assertEqual(len(filtered_jobs), 1)
        self.assertEqual(filtered_jobs[0].matching_keywords, [])

    def test_apply_filters_with_location(self):
        job = Job("Title", "Description", "Company", "URL", None, JobDetails("Germany", "Date", "Applications"))
        config = Config(title="developer", search_location="European Union", filter_locations=["Germany"], keywords=[])
        filtered_jobs = self.filter_service.apply_filters([job], config)
        self.assertEqual(len(filtered_jobs), 1)

    def test_apply_filters_with_non_matching_location(self):
        job = Job("Title", "Description", "Company", "URL", None, JobDetails("France", "Date", "Applications"))
        config = Config(title="developer", search_location="European Union", filter_locations=["Germany"], keywords=[])
        filtered_jobs = self.filter_service.apply_filters([job], config)
        self.assertEqual(len(filtered_jobs), 0)
