from src.daily_scraper import job_scraper
from src.ai_agents import agentic_summarize,agentic_analyze
from src.smtp import send_email

def main():
    jobs= job_scraper()
    
    print("Number of jobs found:", jobs["id"].count())

    jobs= agentic_summarize(jobs)
    
    print("summarization done, now analyzing jobs...", flush=True)

    jobs, job_all= agentic_analyze(jobs)
    
    print("analysis done, now sending email...", flush=True)

    send_email(jobs,job_all)
    
    print("email sent, process completed.", flush=True)



main()
