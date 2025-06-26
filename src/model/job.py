from model.job_details import JobDetails

class Job:
    def __init__(self, title, description, business, location, url, img, job_details: JobDetails):
        self.title = title
        self.business = business
        self.location = location
        self.url = url
        self.img = img
        self.description = description
        self.job_details = job_details

    def __str__(self):
        return f"\tTitulo={self.title}\n\tDescripción={self.description}\n\tUbicación={self.location}\n\tEmpresa={self.business}\n\tDetalles\n{self.job_details}\n\turl={self.url}"