from pydantic import BaseModel
from pydantic import Field

from typing import Optional, Literal

class JobSummary(BaseModel):
    city: str  = Field(description="the city")
    location: str  = Field(description="the country")
    role: str = Field(description="Job title")
    seniority: str = Field(description="Seniority level: intern|junior|mid|senior|lead|manager|director")
    modality: str = Field(description="Work modality: remote|hybrid|on-site")
    experience_years_min: Optional[int] = Field(description="Minimum years of experience required, null if not specified")
    required_skills: list[str] = Field(description="Explicitly required tools, languages and platforms")
    nice_to_have_skills: list[str] = Field(description="Preferred or bonus skills")
    required_education: Optional[str] = Field(description="Required degree or certification, null if not specified")
    languages: list[str] = Field(description="Required spoken languages with proficiency level")



class JobScore(BaseModel):
    analysis: str = Field(description="Concise reasoning covering key match/mismatch criteria")
    score: int = Field(ge=1, le=10, description="Fit score from 1 to 10 based on the analysis")
    location: str = Field(description="Country of the job")
    city: str = Field(description="City of the job")
    a_summirize: str = Field(max_length=100, description="Alternate summary of the analysis, max 100 chars")
    company: str = Field(description="The company name")
    role: str = Field(description="Exact job title")
    work_mode: Literal["remote", "hybrid", "onsite", "unknown"] = Field(description="Work mode extracted from the description")
    apply_link: str = Field(description="Original LinkedIn URL, copied exactly without modification")
    
    
