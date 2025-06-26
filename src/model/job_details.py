class JobDetails:
    def __init__(self, location: str, date: str, applications: str):
        self.location = location
        self.date = date
        self.applications = applications

    def __str__(self):
        return f"\tLocation={self.location}\n\tDate={self.date}\n\tApplications={self.applications}"