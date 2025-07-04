import os
from dotenv import load_dotenv
from service.job_service import JobService
from service.extraction_service import ExtractionService
from service.configuration_service import ConfigurationService
from model.config import Config
from service.web_service import WebService

load_dotenv()

if __name__ == "__main__":
    
    user_data_dir = os.getenv('USER_DATA_DIR', os.path.join(os.getcwd(),'user_data','browser_data'))
    configuration_service = ConfigurationService()
    config: Config = configuration_service.get_config()

    extraction_service = ExtractionService(config.keywords)
    web_service = WebService(user_data_dir)
    job_service = JobService(user_data_dir, extraction_service, web_service)
    jobs = job_service.get_job_offers(config, 1)
    print(f"jobs with one or more keywords: {len(jobs)}")
    job_service.export_job_offers(jobs)