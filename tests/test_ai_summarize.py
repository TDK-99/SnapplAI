import pytest
import pandas as pd
import json
from unittest.mock import patch, MagicMock


@pytest.fixture
def fake_jobs():
    return pd.DataFrame([
        {
            "location": "Roma",
            "title": "Data Engineer",
            "description": "We are looking for a data engineer...",
            "site": "",
            "job_url_direct": "",
            "date_posted": "",
            "job_type": "",
            "salary_source": "",
            "interval": "",
            "min_amount": "",
            "max_amount": "",
            "currency": "",
            "emails": "",
            "listing_type": "",
            "company_logo": "",
            "company_addresses": "",
            "company_num_employees": "",
            "company_revenue": "",
            "company_description": "",
            "skills": "",
            "experience_range": "",
            "company_rating": "",
            "company_reviews_count": "",
            "vacancy_count": "",
            "work_from_home_type": "",
            "company_url_direct": ""
        }
    ])


@pytest.fixture
def fake_api_response():
    return {
        "role": "Data Engineer",
        "location": "Rome",
        "modality": "remote",
        "responsibilities": ["Build ETL pipelines"],
        "requirements": ["Python", "SQL"],
        "seniority": "mid"
    }


@patch("src.ai_agents.time.sleep")
@patch("src.ai_agents.generate_content_resilient")
def test_agentic_summarize_processes_columns(
    mock_generate,
    mock_sleep,
    fake_jobs,
    fake_api_response
):
    mock_response = MagicMock()
    mock_response.text = json.dumps(fake_api_response)
    mock_generate.return_value = mock_response

    from src.ai_agents import agentic_summarize
    result = agentic_summarize(fake_jobs)

    assert mock_generate.call_count == 1

    call_kwargs = mock_generate.call_args.kwargs
    contents_sent = call_kwargs["contents"]

    assert "Roma" in contents_sent
    assert "Data Engineer" in contents_sent
    assert "We are looking for" in contents_sent

    assert "role" in result.columns
    assert "modality" in result.columns

    mock_sleep.assert_called_once_with(7)