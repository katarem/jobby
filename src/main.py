import os
from dotenv import load_dotenv
from injection.service.injector_service import InjectorService
from job.service.job_service import JobService
from extraction.service.extraction_service import ExtractionService
from configuration.service.configuration_service import ConfigurationService
from configuration.model.config import Config
from presentation_card.service.pdf_service import PdfService
from web.service.web_service import WebService

load_dotenv()

if __name__ == "__main__":
    
    user_data_dir = os.getenv('USER_DATA_DIR', os.path.join(os.getcwd(),'user_data','browser_data'))
    configuration_service = ConfigurationService()
    config: Config = configuration_service.get_config()

    extraction_service = ExtractionService(config.keywords)
    web_service = WebService(user_data_dir)
    job_service = JobService(user_data_dir, extraction_service, web_service)
    results = job_service.get_job_offers(config, 1)
    print(f"jobs with one or more keywords: {len(results)}")
    job_service.export_job_offers(results)
    pdf_service = PdfService()
    injector_service = InjectorService()
    for i, result in enumerate(results):
        final_content = injector_service.inject_variables(config, result)
        pdf_service.generate_card(final_content, f'{config.card_name}_{i}.pdf')