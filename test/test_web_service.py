import unittest
from unittest.mock import MagicMock, patch
from configuration.model.config import Config
from web.service.web_service import WebService

class TestWebService(unittest.TestCase):

    @patch('web.service.web_service.webdriver.Chrome')
    @patch('web.service.web_service.time.sleep')
    def test_get_html(self, mock_sleep, mock_chrome):
        mock_chrome.return_value = MagicMock()
        web_service = WebService(user_data="test_user_data")
        mock_driver = mock_chrome.return_value
        mock_driver.page_source = "<html><body>Test HTML</body></html>"
        web_service.driver.get = MagicMock()
        config = Config(title="developer", search_location="European Union", filter_locations=[], keywords=[],pages=1)
        html = web_service.get_html(config, 0)
        web_service.driver.get.assert_called_once()
        self.assertIsInstance(html, str)

    @patch('web.service.web_service.webdriver.Chrome')
    @patch('web.service.web_service.BeautifulSoup')
    @patch('web.service.web_service.time.sleep')
    @patch('web.service.web_service.WebService.map_tag_to_job')
    def test_get_job_offers(self, mock_map_tag_to_job, mock_sleep, mock_soup, mock_chrome):
        mock_chrome.return_value = MagicMock()
        web_service = WebService(user_data="test_user_data")
        mock_soup.return_value.find_all.return_value = [MagicMock()]
        mock_map_tag_to_job.return_value = MagicMock(title="Dummy Job", link="http://dummy.link")
        config = Config(title="developer", search_location="European Union", filter_locations=[], keywords=[],pages=1)
        jobs = web_service.get_jobs(config, pages=1)
        self.assertGreater(len(jobs), 0)
        self.assertEqual(jobs[0].title, "Dummy Job")
        self.assertEqual(jobs[0].link, "http://dummy.link")
