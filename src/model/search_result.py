from dataclasses import dataclass
from model.job import Job

@dataclass
class SearchResult:
    job: Job
    matching_keywords: list[str]