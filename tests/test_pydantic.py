# tests/test_pydantic.py

from pydantic import ValidationError
import pytest
from src.pydantic import JobSummary, JobScore

# --- Test  JobSummary ---

def test_jobsummary_valid():
    job=JobSummary(
            city= "Milan",
            role="Data",
            seniority= "mid",
            modality= "remote",
            experience_years_min= 1,
            required_skills= ["claude","code"],
            nice_to_have_skills= ["claude","code"],
            required_education= "",
            languages= ["english","italian"]
            )
    assert isinstance(job.languages, list)
    assert isinstance(job.required_skills, list)
    assert isinstance(job.nice_to_have_skills, list)

def test_jobsummary_skills_not_list():
     with pytest.raises(ValidationError):
            JobSummary(
                city= "Milan",
                role="Data",
                seniority= "mid",
                modality= "remote",
                experience_years_min= 1,
                required_skills= "",
                nice_to_have_skills= ["claude","code"],
                required_education= "",
                languages= ["english","italian"]
                )



# --- Test  JobScore ---
def test_jobscore_valid():
    job = JobScore(
        analysis="Buon match fti",
        score=7,              
        location="Italy",
        city="Rome",
        a_summirize="Good fit",
        company="Acme",
        role="Data Engineer",
        work_mode="remote",
        apply_link="https://linkedin.com/jobs/123")
    assert job.score == 7
    assert job.work_mode == "remote"


def test_score_too_high():
    with pytest.raises(ValidationError):
        JobScore(
            analysis="Buon match fti",
            score=15,              # ← 15 outof range (max 10)
            location="Italy",
            city="Rome",
            a_summirize="Good fit",
            company="Acme",
            role="Data Engineer",
            work_mode="remote",
            apply_link="https://linkedin.com/jobs/123"
        )

def test_score_work_mode_wrong():
    with pytest.raises(ValidationError):
        JobScore(
            analysis="Buon match fti",
            score=10,              
            location="Italy",
            city="Rome",
            a_summirize="Good fit",
            company="Acme",
            role="Data Engineer",
            work_mode="remoto", # wrong value must be "remote", "hybrid", "onsite", "unknown"
            apply_link="https://linkedin.com/jobs/123"
        )
    