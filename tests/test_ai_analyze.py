import pytest
import pandas as pd
import json
from unittest.mock import patch, MagicMock
from pypdf import PdfReader



@pytest.fixture
def fake_jobs():
    return pd.DataFrame([
        {
            "id": "123",
            "job_url": "https://www.linkedin.com/jobs/view/123456789",
            "title": "Data Engineer",
            "company": "Acme Corp",
            "location": "",
            "is_remote": True,
            "job_level": "",
            "job_function": "",
            "description": "We are looking for a data engineer...",
            "company_industry": "",
            "company_url": "",
            "city": "Rome",
            "role": "",
            "seniority": "",
            "modality": "",
            "experience_years_min": "",
            "required_skills": "",
            "nice_to_have_skills": "",
            "required_education": "",
            "languages": ""
        }
    ])


@pytest.fixture
def fake_api_response():
    return {
        "analysis": "Strong match: requires Python and SQL, mid-level data engineering role.",
        "score": 8,
        "location": "Italy",
        "city": "Roma",
        "a_summirize": "Mid-level Data Engineer role, remote, Python and SQL required",
        "company": "Acme Corp",
        "role": "Data Engineer",
        "work_mode": "remote",
        "apply_link": "https://www.linkedin.com/jobs/view/123456789"
    }

from unittest.mock import patch, MagicMock
from os import environ

@patch.dict(environ, {
    "dir_cv": "fake.pdf",
    "score_config": "5",
    "city": "Roma",
})


@patch("src.ai_agents.PdfReader")
@patch("src.ai_agents.time.sleep")
@patch("src.ai_agents.generate_content_resilient")
def test_agentic_analyze_processes_columns(
    mock_generate,
    mock_sleep,
    mock_pdf_reader,
    fake_jobs,
    fake_api_response
):
    mock_pdf_reader.return_value.pages = [MagicMock(extract_text=lambda: "Fake CV content")]

    mock_response = MagicMock()
    mock_response.text = json.dumps(fake_api_response)
    mock_generate.return_value = mock_response

    from src.ai_agents import agentic_analyze
    _, result, _, = agentic_analyze(fake_jobs)

    assert mock_generate.call_count == 1

    call_kwargs = mock_generate.call_args.kwargs
    contents_sent = call_kwargs["contents"]

    assert "Data Engineer" in contents_sent
    assert "Acme Corp" in contents_sent
    assert "Rome" in contents_sent
    assert "https://www.linkedin.com/jobs/view/123456789" in contents_sent

    assert "analysis" in result.columns
    assert "score" in result.columns
    assert "city" in result.columns
    assert "role" in result.columns
    assert "work_mode" in result.columns
    assert "apply_link" in result.columns
    assert "a_summirize" in result.columns

    mock_sleep.assert_called_once_with(7)