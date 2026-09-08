from src.daily_scraper import job_scraper
from src.ai_agents import agentic_summarize,agentic_analyze
from src.smtp import send_email
import logging
logging.getLogger("google_genai.models").setLevel(logging.ERROR)


def main():
    jobs= job_scraper()
    
    print("Number of jobs found:", jobs["id"].count(), flush=True)

    jobs,report= agentic_summarize(jobs)

    print("Number of jobs after work mod filter:", jobs["id"].count())
    
    print("summarization done, now analyzing jobs...", flush=True)

    jobs, job_all,count_id= agentic_analyze(jobs)
    
    print("analysis done, now sending email...", flush=True)

    print("Number of jobs after city filter:", count_id)

    send_email(jobs,job_all,report)
    
    print("email sent, process completed.", flush=True)



main()
