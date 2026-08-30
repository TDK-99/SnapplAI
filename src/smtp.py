import smtplib
from email.message import EmailMessage
import os
from datetime import date,datetime
from dotenv import load_dotenv


hour= datetime.now().strftime("%H") 

today= date.today()

load_dotenv(".env")



def send_email(jobs_score):

    body=f""" RESULT:
    {jobs_score}

    """

    msg = EmailMessage()
    msg["Subject"] = f"AI Linkedin job - result of {today}--{hour}"
    msg["From"] = os.getenv("GMAIL_USER")
    msg["To"] = os.getenv("GMAIL_USER")
    msg.set_content(body)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_APP_PASSWORD"))
            s.send_message(msg)
    except Exception as e:
        print(f"Email failed: {e}", flush=True)
