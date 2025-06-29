import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import urllib

from model.config import Config
from utils.utils import is_first_launch

class WebService:

    def __init__(self, user_data: str):
        self.driver = webdriver.Chrome(options=self.load_options())
        self.user_data = user_data

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
    
    def get_job_tags(self, search_params: Config, pages: int) -> str:
        jobs = []
        for page_index in range(pages):
            html = self.get_html(search_params, self.jobs_chunk * page_index)
            soup = BeautifulSoup(html, 'html.parser')
            jobs += soup.find_all('div', attrs={'data-job-id': True})
        return jobs