from dataclasses import dataclass
from job.model.job import Job

@dataclass
class SearchResult:
    job: Job
    matching_keywords: list[str]