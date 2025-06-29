import os
import shutil
import unittest
from unittest.mock import MagicMock, patch
from model.config import Config
from model.search_result import SearchResult
from service.job_service import JobService

class TestJobService(unittest.TestCase):

    def tearDown(self):
        if os.path.exists("test_user_data"):
            shutil.rmtree("test_user_data")

    def setUp(self):
        os.mkdir("test_user_data")

    @patch('service.job_service.FilterService.apply_filters')
    @patch('service.job_service.WebService.get_jobs')
    def test_get_job_offers(self, mock_get_jobs, mock_apply_filters):
        mock_get_jobs.return_value = [MagicMock()]
        mock_apply_filters.return_value = [SearchResult(MagicMock(), ["Python"])]
        extraction_service = MagicMock()
        web_service = MagicMock()
        web_service.get_jobs = mock_get_jobs
        job_service = JobService(user_data="test_user_data", extraction_service=extraction_service, web_service=web_service)
        config = Config(title="developer", search_location="European Union", filter_locations=[], keywords=[])
        filtered_jobs = job_service.get_job_offers(config, pages=1)
        mock_get_jobs.assert_called_once_with(config, 1)
        mock_apply_filters.assert_called_once_with(mock_get_jobs.return_value, config)
        self.assertGreater(len(filtered_jobs), 0)
        self.assertIsInstance(filtered_jobs[0], SearchResult)

    @patch('service.job_service.open', new_callable=unittest.mock.mock_open)
    @patch('service.job_service.json.dumps')
    def test_export_job_offers(self, mock_json, mock_open):
        extraction_service = MagicMock()
        web_service = MagicMock()
        job_service = JobService(user_data="test_user_data", extraction_service=extraction_service, web_service=web_service)
        jobs = [SearchResult(MagicMock(), ["Python"])]
        result = job_service.export_job_offers(jobs)
        self.assertTrue(result)
        mock_json.assert_called_once_with([{"job": jobs[0].job, "matching_keywords": jobs[0].matching_keywords}], indent=4)
        mock_open.assert_called_once_with(job_service.export_path, mode='w', encoding='utf-8')