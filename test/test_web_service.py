import unittest
from unittest.mock import MagicMock, patch
from model.config import Config
from service.web_service import WebService

class TestWebService(unittest.TestCase):

    @patch('service.web_service.webdriver.Chrome')
    @patch('service.web_service.time.sleep')
    def test_get_html(self, mock_sleep, mock_chrome):
        mock_chrome.return_value = MagicMock()
        web_service = WebService(user_data="test_user_data")
        mock_driver = mock_chrome.return_value
        mock_driver.page_source = "<html><body>Test HTML</body></html>"
        web_service.driver.get = MagicMock()
        config = Config(title="developer", search_location="European Union", filter_locations=[], keywords=[])
        html = web_service.get_html(config, 0)
        web_service.driver.get.assert_called_once()
        self.assertIsInstance(html, str)

    @patch('service.web_service.webdriver.Chrome')
    @patch('service.web_service.BeautifulSoup')
    @patch('service.web_service.time.sleep')
    def test_get_job_offers(self, mock_sleep, mock_soup, mock_chrome):
        mock_chrome.return_value = MagicMock()
        web_service = WebService(user_data="test_user_data")
        mock_soup.return_value.find_all.return_value = [MagicMock()]
        config = Config(title="developer", search_location="European Union", filter_locations=[], keywords=[])
        jobs = web_service.get_jobs(config, pages=1)
        self.assertGreater(len(jobs), 0)
