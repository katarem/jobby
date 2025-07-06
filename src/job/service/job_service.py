from dataclasses import asdict
import json
import os

from configuration.model.config import Config
from extraction.service.extraction_service import ExtractionService
from job.model.search_result import SearchResult
from filters.service.filter_service import FilterService
from location.service.location_service import LocationService
from web.service.web_service import WebService

class JobService:

    location_service: LocationService = LocationService()

    def __init__(self, user_data: str, extraction_service: ExtractionService, web_service: WebService):

        self.web_service = web_service
        self.extraction_service = extraction_service
        self.filter_service: FilterService = FilterService(self.extraction_service, self.location_service)
        
        self.user_data = user_data
        self.export_path = os.path.join(os.getenv('USER_DATA_DIR', os.path.join(os.getcwd(),'user_data')), 'export.json')
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

    
    def get_job_offers(self, search_params: Config, pages: int = 3) -> list[SearchResult]:
        jobs = self.web_service.get_jobs(search_params,pages)
        return self.filter_service.apply_filters(jobs, search_params)
    
    def export_job_offers(self, jobs: list[SearchResult]) -> bool:
        try:
            export_json = json.dumps([asdict(job) for job in jobs], indent=4)
            with open(self.export_path, mode= 'w', encoding= 'utf-8') as export_file:
                export_file.write(export_json)
            return True
        except Exception as e:
            print(e)
            return False