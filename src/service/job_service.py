from dataclasses import asdict
import json
import os
import time
import urllib.parse
from bs4 import BeautifulSoup, Tag
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from model.job import Job
from model.job_details import JobDetails
from service.extraction_service import ExtractionService
from model.search_result import SearchResult
from utils.utils import is_first_launch

class JobService:

    base_link = "https://linkedin.com"
    search_link = f"{base_link}/jobs/search/?keywords=%s"
    search_delay = 60
    jobs_chunk = 25

    def __init__(self, user_data: str, extraction_service: ExtractionService):
        self.user_data = user_data
        self.driver = webdriver.Chrome(options=self.load_options())
        self.extraction_service = extraction_service
        self.export_path = os.path.join(os.getenv('USER_DATA_DIR', os.path.join(os.getcwd(),'user_data')), 'export.json')

    def load_options(self) -> Options:
        options = Options()
        options.add_argument(f"--user-data-dir={self.user_data}")
        options.add_argument("--profile-directory=Default")
        if not is_first_launch(self.user_data):
            options.add_argument("--headless")
            self.search_delay = 5
        return options
    
    def get_html(self, job: str, start: int) -> str:
        job_to_search = urllib.parse.quote(job)
        final_link = self.search_link.replace("%s",job_to_search)
        if start > 0:
            final_link += f"&start={start}"
        self.driver.get(final_link)
        time.sleep(self.search_delay)
        return self.driver.page_source
    
    def get_job_offers(self, text_search: str, pages: int = 3) -> list[Job]:
        jobs = []
        filtered_jobs: list[SearchResult] = []

        for page_index in range(pages):
            html = self.get_html(text_search, self.jobs_chunk * page_index)
            soup = BeautifulSoup(html, 'html.parser')
            jobs += soup.find_all('div', attrs={'data-job-id': True})

        for job in jobs:
            clean_job = self.process_job(job)
            if self.extraction_service.detect_keywords(clean_job.description):
                keywords = self.extraction_service.extract_keywords(clean_job.description)
                filtered_jobs.append(SearchResult(clean_job, keywords))

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

    def process_job(self, job: Tag) -> Job:
        title = job.find("a", class_="job-card-container__link").get_text(strip=True, separator=", ")
        business = job.find("div", class_="artdeco-entity-lockup__subtitle").get_text(strip=True, separator=", ")
        url = job.find("a", class_="job-card-container__link")["href"]
        img = job.find("img")
        logo_url = img["src"] if img else None
        
        job_link = self.base_link + url
        self.driver.get(job_link)
        time.sleep(2)
        
        loaded_job_page = self.driver.page_source
        soup = BeautifulSoup(loaded_job_page, 'html.parser')
        job_details_tag = soup.find('div', id='job-details')
        description = job_details_tag.get_text(separator='\n', strip=True)
        
        job_details = self.get_details(soup)

        return Job(title,description,business,url,logo_url, job_details)
    
    def get_details(self, soup: BeautifulSoup) -> JobDetails:
        primary_desc = soup.find('div', class_='job-details-jobs-unified-top-card__primary-description-container')
        spans = primary_desc.find_all('span', class_='tvm__text tvm__text--low-emphasis')
        location = date = applications = 'Not found'
        if spans:
            if len(spans) > 0:
                location = spans[0].get_text(strip=True)
            if len(spans) > 2:
                date = spans[2].get_text(strip=True)
            if len(spans) > 4:
                applications = spans[4].get_text(strip=True)
        return JobDetails(location,date,applications)