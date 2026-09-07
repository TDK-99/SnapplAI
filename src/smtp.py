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

    # SMTP config is provider-agnostic: host/port/credentials come from env.
    # Defaults keep Gmail working out of the box, and the GMAIL_* vars are still
    # honored as a fallback so existing setups don't break.
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER") or os.getenv("GMAIL_USER")
    smtp_password = os.getenv("SMTP_PASSWORD") or os.getenv("GMAIL_APP_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = f"AI Linkedin job - result of {today}--{hour}"
    msg["From"] = smtp_user
    msg["To"] = smtp_user
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
        # Port 465 uses implicit SSL (Gmail); other ports (e.g. 587 for
        # Outlook/Office365) use STARTTLS over a plain connection.
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port) as s:
                s.login(smtp_user, smtp_password)
                s.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port) as s:
                s.starttls()
                s.login(smtp_user, smtp_password)
                s.send_message(msg)
    except Exception as e:
        print(f"Email failed: {e}", flush=True)

