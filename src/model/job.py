from model.job_details import JobDetails

class Job:
    def __init__(self, title, description, business, url, img, job_details: JobDetails):
        self.title = title
        self.business = business
        self.url = url
        self.img = img
        self.description = description
        self.job_details = job_details

    def __str__(self):
        return f"\tTitle={self.title}\n\tDescription={self.description}\n\tEnterprise={self.business}\n\tDetails=\n{self.job_details}\n\turl={self.url}"