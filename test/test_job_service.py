import os
import shutil
import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.chrome.options import Options
from model.config import Config
from service.job_service import JobService
from model.job import Job
from model.job_details import JobDetails
from model.search_result import SearchResult

class TestJobService(unittest.TestCase):

    def tearDown(self):
        if os.path.exists("test_user_data"):
            shutil.rmtree("test_user_data")

    def setUp(self):
        os.mkdir("test_user_data")

    @patch('service.job_service.webdriver.Chrome')
    @patch('service.job_service.is_first_launch', return_value=False)
    def test_load_options(self, mock_is_first_launch, mock_chrome):
        mock_chrome.return_value = MagicMock()
        extraction_service = MagicMock()
        job_service = JobService(user_data="test_user_data", extraction_service=extraction_service)
        options = job_service.load_options()
        self.assertIsInstance(options, Options)
        self.assertIn("--headless", options.arguments)

    @patch('service.job_service.webdriver.Chrome')
    @patch('service.job_service.time.sleep')
    def test_get_html(self, mock_sleep, mock_chrome):
        mock_chrome.return_value = MagicMock()
        extraction_service = MagicMock()
        job_service = JobService(user_data="test_user_data", extraction_service=extraction_service)
        mock_driver = mock_chrome.return_value
        mock_driver.page_source = "<html><body>Test HTML</body></html>"
        job_service.driver.get = MagicMock()
        html = job_service.get_html("developer", 0)
        job_service.driver.get.assert_called_once()
        self.assertIsInstance(html, str)

    @patch('service.job_service.webdriver.Chrome')
    @patch('service.job_service.BeautifulSoup')
    @patch('service.job_service.time.sleep')
    def test_get_job_offers(self, mock_sleep, mock_soup, mock_chrome):
        mock_chrome.return_value = MagicMock()
        extraction_service = MagicMock()
        extraction_service.detect_keywords.return_value = True
        extraction_service.extract_keywords.return_value = ["Python", "Django"]
        job_service = JobService(user_data="test_user_data", extraction_service=extraction_service)
        mock_soup.return_value.find_all.return_value = [MagicMock()]
        filtered_jobs = job_service.get_job_offers("developer", pages=1)
        self.assertGreater(len(filtered_jobs), 0)
        self.assertIsInstance(filtered_jobs[0], SearchResult)

    @patch('service.job_service.webdriver.Chrome')
    @patch('service.job_service.json.dumps')
    @patch('service.job_service.open', new_callable=unittest.mock.mock_open)
    def test_export_job_offers(self, mock_open, mock_json, mock_chrome):
        mock_chrome.return_value = MagicMock()
        extraction_service = MagicMock()
        job_service = JobService(user_data="test_user_data", extraction_service=extraction_service)
        jobs = [SearchResult(MagicMock(), ["Python"])]
        result = job_service.export_job_offers(jobs)
        self.assertTrue(result)
        mock_open.assert_called_once_with(job_service.export_path, mode='w', encoding='utf-8')

    @patch('service.job_service.webdriver.Chrome')
    @patch('service.job_service.BeautifulSoup')
    @patch('service.job_service.time.sleep')
    def test_process_job(self, mock_sleep, mock_soup, mock_chrome):
        mock_chrome.return_value = MagicMock()
        extraction_service = MagicMock()
        job_service = JobService(user_data="test_user_data", extraction_service=extraction_service)
        mock_soup.return_value.find.return_value.get_text.return_value = "Test Description"
        mock_soup.return_value.find.return_value["href"] = "/test-url"
        job = MagicMock()
        processed_job = job_service.process_job(job)
        self.assertIsInstance(processed_job, Job)

    @patch('service.job_service.webdriver.Chrome')
    @patch('service.job_service.BeautifulSoup')
    def test_get_details(self, mock_chrome, mock_soup):
        mock_chrome.return_value = MagicMock()
        extraction_service = MagicMock()
        job_service = JobService(user_data="test_user_data", extraction_service=extraction_service)
        mock_soup.return_value.find.return_value.find_all.return_value = [MagicMock(get_text=MagicMock(return_value="Test Location"))]
        details = job_service.get_details(mock_soup.return_value)
        self.assertIsInstance(details, JobDetails)
        self.assertEqual(details.location, "Test Location")

    @patch('service.job_service.webdriver.Chrome')
    @patch('service.job_service.BeautifulSoup')
    @patch('service.job_service.time.sleep')
    def test_get_job_offers_with_empty_keywords(self, mock_sleep, mock_soup, mock_chrome):
        mock_chrome.return_value = MagicMock()
        extraction_service = MagicMock()
        extraction_service.keywords = []
        job_service = JobService(user_data="test_user_data", extraction_service=extraction_service)
        
        mock_soup.return_value.find_all.return_value = [MagicMock()]
        filtered_jobs = job_service.get_job_offers("developer", pages=1)
        
        self.assertGreater(len(filtered_jobs), 0)
        self.assertIsInstance(filtered_jobs[0], SearchResult)
        self.assertEqual(filtered_jobs[0].matching_keywords, [])

    @patch('service.job_service.webdriver.Chrome')
    @patch('service.job_service.time.sleep')
    def test_get_html_with_search_location(self, mock_sleep, mock_chrome):
        mock_chrome.return_value = MagicMock()
        extraction_service = MagicMock()
        job_service = JobService(user_data="test_user_data", extraction_service=extraction_service)
        mock_driver = mock_chrome.return_value
        job_service.driver.get = MagicMock()
        config = Config(title="developer", search_location="European Union", filter_locations=[], keywords=[])
        job_service.get_html(config, 0)
        job_service.driver.get.assert_called_once()
        called_url = job_service.driver.get.call_args[0][0]
        self.assertIn("geoId=91000000", called_url)
