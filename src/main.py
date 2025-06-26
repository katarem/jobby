from service.job_service import JobService

if __name__ == "__main__":
    user_data_dir = "C:\\Users\\elson\\Desktop\\linkedin"
            
    job_service = JobService(user_data=user_data_dir)
    job_service.get_job_offers("java developer")