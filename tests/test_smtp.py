import pytest
import pandas as pd
from unittest.mock import patch

from src.smtp import send_email


@patch("smtplib.SMTP_SSL")
def test_send_email(mock_smtp, monkeypatch):
    # fake env vars so os.getenv doesn't return None
    monkeypatch.setenv("SMTP_USER", "fake@gmail.com")
    monkeypatch.setenv("SMTP_PASSWORD", "fake_password")
    monkeypatch.setenv("SMTP_HOST", "smtp.gmail.com")
    monkeypatch.setenv("SMTP_PORT", "465")
    monkeypatch.setenv("search_term", "Data Engineer")

    # fake inputs for send_email
    fake_body = "Here are your job matches for today."

    fake_job_all = pd.DataFrame([
        {"role": "Data Engineer", "city": "Rome", "modality": "remote"},
        {"role": "Data Analyst", "city": "Milan", "modality": "hybrid"}
    ])

    fake_report = b"Summary: 2 jobs found, 1 remote match."

    # mock_smtp = fake class, .return_value = fake instance (the server)
    mock_server = mock_smtp.return_value.__enter__.return_value

    send_email(fake_body, fake_job_all, fake_report)

    mock_smtp.assert_called_once_with("smtp.gmail.com", 465)
    mock_server.login.assert_called_once_with("fake@gmail.com", "fake_password")
    mock_server.send_message.assert_called_once()