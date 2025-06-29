import os
import time
from bs4 import BeautifulSoup, Tag
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import urllib

from model.config import Config
from model.job import Job
from model.job_details import JobDetails
from service.location_service import LocationService
from utils.utils import is_first_launch

class WebService:

    base_link = "https://linkedin.com"
    search_link = f"{base_link}/jobs/search/?keywords=%s"
    search_delay = 60
    jobs_chunk = 25

    location_service: LocationService = LocationService()

    def __init__(self, user_data: str):
        self.user_data = user_data
        self.driver = webdriver.Chrome(options=self.load_options())
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

    def load_options(self) -> Options:
        options = Options()
        options.add_argument(f"--user-data-dir={self.user_data}")
        options.add_argument("--profile-directory=Default")
        if not is_first_launch(self.user_data):
            options.add_argument("--headless")
            self.search_delay = 5
        return options
    
    def get_html(self, search_params: Config, start: int) -> str:
        job_to_search = urllib.parse.quote(str(search_params.title))
        final_link = self.search_link.replace("%s", job_to_search)
        if start > 0:
            final_link += f"&start={start}"
        location = self.location_service.parse_location(search_params.search_location)
        if location is not None:
            final_link += f"&geoId={location}"
        if self.debug_mode:
            print(f'generated URL={final_link}')
        self.driver.get(final_link)
        time.sleep(self.search_delay)
        return self.driver.page_source
    
    def get_job_tags(self, search_params: Config, pages: int) -> list[Tag]:
        jobs = []
        for page_index in range(pages):
            html = self.get_html(search_params, self.jobs_chunk * page_index)
            soup = BeautifulSoup(html, 'html.parser')
            jobs += soup.find_all('div', attrs={'data-job-id': True})
        return jobs
    
    def map_tag_to_job(self, job: Tag) -> Job:
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
    
    def get_jobs(self, search_params: Config, pages: int) -> list[Job]:
        tags = self.get_job_tags(search_params,pages)
        jobs: list[Job] = []
        for tag in tags:
            job = self.map_tag_to_job(tag)
            jobs.append(job)
        return jobs