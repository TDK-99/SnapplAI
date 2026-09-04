from src.daily_scraper import job_scraper
from src.ai_agents import agentic_summarize,agentic_analyze
from src.smtp import send_email
import logging
logging.getLogger("google_genai.models").setLevel(logging.ERROR)


def main():
    jobs= job_scraper()
    
    print("Number of jobs found:", jobs["id"].count(), flush=True)

    jobs= agentic_summarize(jobs)

    print("Number of jobs found after filter:", jobs["id"].count())
    
    print("summarization done, now analyzing jobs...", flush=True)

    jobs, job_all= agentic_analyze(jobs)
    
    print("analysis done, now sending email...", flush=True)

    send_email(jobs,job_all)
    
    print("email sent, process completed.", flush=True)



main()
