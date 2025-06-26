from service.job_service import JobService
from service.extraction_service import ExtractionService

if __name__ == "__main__":
    user_data_dir = "C:\\Users\\elson\\Desktop\\linkedin"
            
    extraction_service = ExtractionService(keywords = ['maven'])
    job_service = JobService(user_data=user_data_dir, extraction_service=extraction_service)
    jobs = job_service.get_job_offers("java developer")
    for job in jobs:
        print(job)