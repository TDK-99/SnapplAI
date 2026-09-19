import pandas as pd
import pytest
from unittest.mock import patch


@pytest.fixture
def fake_job_df():
    return pd.DataFrame([{"id": "1", "title": "Data Analyst", "location": "Rome"}])


@patch("src.daily_scraper.load_dotenv")  # don't let the real committed file_config.env override monkeypatch
@patch("src.daily_scraper.scrape_jobs")
def test_multiple_locations_are_scraped_and_concatenated(mock_scrape_jobs, mock_load_dotenv, fake_job_df, monkeypatch):
    # Comma-separated locations with stray whitespace that job_scraper must strip,
    # plus the numeric/boolean env var conversions it has to do before calling jobspy.
    monkeypatch.setenv("location", "Italy, Spain")
    monkeypatch.setenv("site_name", "linkedin")
    monkeypatch.setenv("search_term", "Data Analyst")
    monkeypatch.setenv("results_wanted", "10")
    monkeypatch.setenv("hours_old", "24")
    monkeypatch.setenv("linkedin_fetch_description", "True")
    monkeypatch.delenv("proxies", raising=False)

    mock_scrape_jobs.return_value = fake_job_df

    from src.daily_scraper import job_scraper
    result = job_scraper()

    assert mock_scrape_jobs.call_count == 2
    called_locations = [call.kwargs["location"] for call in mock_scrape_jobs.call_args_list]
    assert called_locations == ["Italy", "Spain"]
    assert mock_scrape_jobs.call_args.kwargs["results_wanted"] == 10  # str -> int
    assert mock_scrape_jobs.call_args.kwargs["linkedin_fetch_description"] is True  # str -> bool

    # One row per location, concatenated with a fresh 0..N index (ignore_index=True).
    assert len(result) == 2
    assert list(result.index) == [0, 1]