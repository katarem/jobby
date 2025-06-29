from model.config import Config
from model.job import Job
from model.search_result import SearchResult
from service.extraction_service import ExtractionService
from service.location_service import LocationService


class FilterService:

    def __init__(self, extraction_service: ExtractionService, location_service: LocationService):
        self.extraction_service = extraction_service
        self.location_service = location_service

    def apply_filters(self, jobs: list[Job], search_params: Config) -> list[SearchResult]:
        results: list[Job] = []
        for job in jobs:
            
            if search_params.filter_locations and not self.matches_location(job, search_params.filter_locations):
                continue

            keywords = []
            if search_params.keywords:
                if not self.extraction_service.detect_keywords(job.description):
                    continue
                keywords = self.extraction_service.extract_keywords(job.description)
                
            results.append(SearchResult(job, keywords))

        return results

    def matches_location(self, job: Job, locations: list[str]) -> bool:
        return any(location.lower() in job.job_details.location.lower() for location in locations)
    
    def matches_keywords(self, job: Job) -> bool:
        return self.extraction_service.detect_keywords(job)
