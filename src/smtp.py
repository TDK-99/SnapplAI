import smtplib
from email.message import EmailMessage
import os
import html
from datetime import date,datetime
from dotenv import load_dotenv
import pandas as pd
from io import BytesIO
from datetime import datetime


hour= datetime.now().strftime("%H") 

today= date.today()

load_dotenv(".env", override=True)
load_dotenv("your_cv_config/file_config.env", override=True)




def _job_plain_block(job):
    return (
        f"{job['role']} - {job['company']} (score {job['score']}/10)\n"
        f"{job['city']}, {job['location']} - {job['work_mode']}\n"
        f"{job['a_summirize']}\n"
        f"Apply: {job['apply_link']}\n"
    )


def _job_html_card(job):
    return f"""\
    <div style="border:1px solid #e1e4e8; border-radius:8px; padding:12px; margin-bottom:10px;">
      <div style="font-weight:bold; font-size:15px;">{html.escape(str(job['role']))} &mdash; {html.escape(str(job['company']))}</div>
      <div style="color:#777; font-size:13px; margin:4px 0;">{html.escape(str(job['city']))}, {html.escape(str(job['location']))} &middot; {html.escape(str(job['work_mode']))} &middot; score {job['score']}/10</div>
      <div style="font-size:14px; margin-bottom:6px;">{html.escape(str(job['a_summirize']))}</div>
      <a href="{job['apply_link']}" style="font-size:13px;">Apply &rarr;</a>
    </div>
"""


def send_email(jobs,job_all,report):

    if isinstance(jobs, str):
        body = f" RESULT:\n    {jobs}\n\n    "
        jobs_html = f"<p>{html.escape(jobs)}</p>"
    else:
        body = "RESULT:\n\n" + "\n".join(_job_plain_block(job) for job in jobs)
        jobs_html = "".join(_job_html_card(job) for job in jobs)

    # Minimal HTML alternative: same result as one card per job, readable on
    # mobile, with apply links clickable. Clients without HTML support fall
    # back to the plain-text `body` above.
    html_body = f"""\
<html>
  <body style="font-family: Arial, Helvetica, sans-serif; color:#222;">
    <p style="color:#777; margin-top:0;">{os.getenv("search_term")} &middot; {today}</p>
    {jobs_html}
  </body>
</html>
"""

    # SMTP config is provider-agnostic: host/port/credentials come from env.
    # Defaults keep Gmail working out of the box, and the GMAIL_* vars are still
    # honored as a fallback so existing setups don't break.
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER") or os.getenv("GMAIL_USER")
    smtp_password = os.getenv("SMTP_PASSWORD") or os.getenv("GMAIL_APP_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = f"SnapplAI - AI Linkedin job result of {os.getenv("search_term")} {today}--{hour}"
    msg["From"] = smtp_user
    msg["To"] = smtp_user
    msg.set_content(body)
    msg.add_alternative(html_body, subtype="html")

    buffer_excel = BytesIO()

    with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
        job_all.to_excel(writer, index=False, sheet_name="all jobs")
    
    jobs_log = buffer_excel.getvalue()
    
    msg.add_attachment(
        jobs_log,
        maintype="application",
        subtype="xlsx",
        filename=f"jobs_filter_{today}.xlsx"
    )

    msg.add_attachment(
        report,
        maintype="application",
        subtype="txt",
        filename=f"analytics_{os.getenv("search_term")}_{today}.txt"
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

