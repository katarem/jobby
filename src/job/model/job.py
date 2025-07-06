from dataclasses import dataclass
from job.model.job_details import JobDetails

@dataclass
class Job:
    title: str
    description: str
    business: str
    url: str
    img: str
    job_details: JobDetails