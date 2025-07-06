from unittest import TestCase
from unittest.mock import patch, mock_open

from configuration.model.config import Config
from configuration.service.configuration_service import ConfigurationService
from configuration.exception.configuration_file_not_found import ConfigurationFileNotFoundError
from configuration.exception.invalid_configuration_file import InvalidConfigurationError


class ConfigurationServiceTest(TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"title": "developer", "keywords": ["python"], "search_location": "European Union", "filter_locations": ["poland", "germany"]}')
    def test_get_configuration_ok(self, mock_open, mock_exists):
        configuration_service = ConfigurationService()
        config = configuration_service.get_config()
        self.assertIsInstance(config, Config)
        self.assertEqual(config.title, "developer")
        self.assertEqual(config.keywords, ["python"])
        self.assertEqual(config.search_location, "European Union")
        self.assertEqual(config.filter_locations, ["poland", "germany"])

    @patch("os.path.exists", return_value=False)
    def test_configuration_file_not_found_error(self, mock_exists):
        configuration_service = ConfigurationService()
        with self.assertRaises(ConfigurationFileNotFoundError):
            configuration_service.get_config()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
    def test_invalid_configuration_file_error(self, mock_open, mock_exists):
        configuration_service = ConfigurationService()
        with self.assertRaises(InvalidConfigurationError):
            configuration_service.get_config()


