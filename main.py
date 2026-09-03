from jobspy import scrape_jobs
from dotenv import load_dotenv
import os
import pandas as pd
from google import genai
from google.genai import types
import json
import time
import smtplib
from email.message import EmailMessage
import os
from datetime import date,datetime
from pypdf import PdfReader
import time
import logging
logging.getLogger("google_genai.models").setLevel(logging.ERROR)


import sys
sys.path.append("..")

from src.daily_scraper import job_scraper
from src.ai_agents import agentic_summarize,agentic_analyze
from src.smtp import send_email

def main():
    jobs= job_scraper()
    
    print("Number of jobs found:", jobs["id"].count(), flush=True)

    print(jobs["location"].unique(), flush=True)

    jobs= agentic_summarize(jobs)

    print("Number of jobs found after filter:", jobs["id"].count())
    
    print("summarization done, now analyzing jobs...", flush=True)

    jobs, job_all= agentic_analyze(jobs)
    
    print("analysis done, now sending email...", flush=True)

    send_email(jobs,job_all)
    
    print("email sent, process completed.", flush=True)



main()
