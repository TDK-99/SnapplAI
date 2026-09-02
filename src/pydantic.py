from pydantic import BaseModel
from pydantic import Field

from typing import Optional

class JobSummary(BaseModel):
    city: str  = Field(description="the city")
    role: str = Field(description="Job title")
    seniority: str = Field(description="Seniority level: intern|junior|mid|senior|lead|manager|director")
    modality: str = Field(description="Work modality: remote|hybrid|on-site")
    experience_years_min: Optional[int] = Field(description="Minimum years of experience required, null if not specified")
    required_skills: list[str] = Field(description="Explicitly required tools, languages and platforms")
    nice_to_have_skills: list[str] = Field(description="Preferred or bonus skills")
    required_education: Optional[str] = Field(description="Required degree or certification, null if not specified")
    languages: list[str] = Field(description="Required spoken languages with proficiency level")



class JobScore(BaseModel):
    analysis: str
    score: int
    a_summirize: str
    company: str
    role: str
    work_mode: str
    apply_link: str
    
    
