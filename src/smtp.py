import smtplib
from email.message import EmailMessage
import os
from datetime import date,datetime
from dotenv import load_dotenv
import pandas as pd
from io import BytesIO
from datetime import datetime


hour= datetime.now().strftime("%H") 

today= date.today()

load_dotenv(".env")




def send_email(jobs,job_all):

    body=f""" RESULT:
    {jobs}

    """

    msg = EmailMessage()
    msg["Subject"] = f"AI Linkedin job - result of {today}--{hour}"
    msg["From"] = os.getenv("GMAIL_USER")
    msg["To"] = os.getenv("GMAIL_USER")
    msg.set_content(body)
    
    buffer_excel = BytesIO()

    with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
        job_all.to_excel(writer, index=False, sheet_name="all jobs")
    
    jobs_log = buffer_excel.getvalue()
    
    msg.add_attachment(
        jobs_log,
        maintype="application",
        subtype="xlsx",
        filename="all_jobs.xlsx"
    )
    
    

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD"))
            s.send_message(msg)
    except Exception as e:
        print(f"Email failed: {e}", flush=True)

