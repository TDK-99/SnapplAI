from src.daily_scraper import job_scraper
from src.ai_agents import agentic_summarize,agentic_analyze
from src.smtp import send_email

def main():
    jobs= job_scraper()

    jobs= agentic_summarize(jobs)

    jobs= agentic_analyze(jobs)

    send_email(jobs)



main()
