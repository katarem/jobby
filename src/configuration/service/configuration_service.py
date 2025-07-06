import json
import os
from configuration.exception.configuration_file_not_found import ConfigurationFileNotFoundError
from configuration.model.config import Config
from configuration.exception.invalid_configuration_file import InvalidConfigurationError 

class ConfigurationService:
    
    def get_config(self) -> Config:
        config_path = os.path.join(os.getcwd(), 'config.json')
        if not os.path.exists(config_path):
            raise ConfigurationFileNotFoundError()
        with open(config_path, encoding='utf-8') as file:
            try:
                config = json.load(file)
            except json.JSONDecodeError as e:
                raise InvalidConfigurationError(f"Failed to parse configuration file: {e}")
        return Config(**config)