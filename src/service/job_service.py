from dataclasses import asdict
import json
import os
import time
from bs4 import BeautifulSoup, Tag

from model.config import Config
from model.job import Job
from model.job_details import JobDetails
from service.extraction_service import ExtractionService
from model.search_result import SearchResult
from service.location_service import LocationService
from service.web_service import WebService

class JobService:

    base_link = "https://linkedin.com"
    search_link = f"{base_link}/jobs/search/?keywords=%s"
    search_delay = 60
    jobs_chunk = 25
    location_service: LocationService = LocationService()

    def __init__(self, user_data: str, extraction_service: ExtractionService, web_service: WebService):
        
        self.web_service = web_service
        self.extraction_service = extraction_service
        
        self.user_data = user_data
        self.export_path = os.path.join(os.getenv('USER_DATA_DIR', os.path.join(os.getcwd(),'user_data')), 'export.json')
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

    
    def get_job_offers(self, search_params: Config, pages: int = 3) -> list[Job]:
        jobs = []
        filtered_jobs: list[SearchResult] = []

        jobs = self.web_service.get_jobs(search_params,pages)

        for job in jobs:
            if not self.extraction_service.keywords:
                if search_params.filter_locations:
                    if any(location in job.job_details.location.lower() for location in search_params.filter_locations):
                        filtered_jobs.append(SearchResult(job, []))
                else:
                    filtered_jobs.append(SearchResult(job, []))
            elif self.extraction_service.detect_keywords(job.description):
                keywords = self.extraction_service.extract_keywords(job.description)
                filtered_jobs.append(SearchResult(job, keywords))

        return filtered_jobs
    
    def export_job_offers(self, jobs: list[SearchResult]) -> bool:
        try:
            export_json = json.dumps([asdict(job) for job in jobs], indent=4)
            with open(self.export_path, mode= 'w', encoding= 'utf-8') as export_file:
                export_file.write(export_json)
            return True
        except Exception as e:
            print(e)
            return False