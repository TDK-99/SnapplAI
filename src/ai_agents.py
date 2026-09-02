import pandas as pd
from schedule import jobs
from pypdf import PdfReader
from dotenv import load_dotenv
import os
import json
from google import genai
from google.genai import types
import time

from src.pydantic import JobSummary, JobScore

load_dotenv(".env")
load_dotenv("your_cv_config/file_config.env")
client = genai.Client(api_key=os.getenv("LLM_GEMINI"))


def agentic_summarize(jobs): # summirize the description and create an output of dettail of the job descriprion
    


    system_prompt= """ 
    Extract structured data from a job posting. Return ONLY valid JSON, no markdown, no text.
    If not in the posting, use null. Do not invent. Keep original language for title and responsibilities. Ignore benefits, perks, company values.
    Few note:
    for the role dont invent take fromt {row["title"]} and for location always write in english so if you find Roma put Rome"""
    
    load_dotenv(".env")


    for index, row in jobs.iterrows():
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"{row["location"]},{row["title"]}, {row["description"]}",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0,
                response_mime_type="application/json", 
                response_schema=JobSummary # forza output JSON
            )
        )
        jobs.at[index, "summary"] = response.text
        time.sleep(7)  # wait 7 seconds between requests to avoid rate limiting

    jobs["summary_parsed"] = jobs["summary"].apply(json.loads)

    df_expanded = pd.json_normalize(jobs["summary_parsed"])

    jobs = pd.concat([jobs, df_expanded], axis=1)


    if os.getenv("work_from_home") == "True":
        jobs = jobs[jobs["modality"].isin(["remote","hybrid"])]
    else:
        jobs

    if os.getenv("remote_only") == "True":
        jobs = jobs[jobs["modality"].isin(["remote"])]
    else:
        jobs

    city =os.getenv("city").split(",")

    if os.getenv("work_from_home") is None:
        jobs
    else:
        jobs= jobs[jobs["city"].isin(city)]


    jobs = jobs.drop(columns=[
    'site', 'job_url_direct', 'date_posted', 'job_type', 'salary_source',
    'interval', 'min_amount', 'max_amount', 'currency', 'emails',
    'listing_type', 'company_logo', 'company_addresses',
    'company_num_employees', 'company_revenue', 'company_description',
    'skills', 'experience_range', 'company_rating', 'company_reviews_count',
    'vacancy_count', 'work_from_home_type','summary','summary_parsed','company_url_direct'
    ])
        
    return jobs



def agentic_analyze(jobs): # agentic ai that compare your cv with the output of summarize for define an analisys for give a score
    reader = PdfReader(os.getenv("dir_cv"))
    cv = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            cv += text
    system_prompt = f"""
    
    You are a job-fit evaluator. You will receive a candidate CV and a job description summary. Your task is to assess how well the candidate fits the role.

                ## Candidate CV
                {cv}

                ## Evaluation criteria (use ALL of these in your analysis)
                1. **Skills overlap** — how many required/preferred skills does the CV cover?
                2. **Seniority alignment** — does the candidate's experience level match what the role asks for?
                3. **Domain relevance** — is the candidate's industry/domain experience relevant?
                4. **Title alignment** — how close is the candidate's current/past titles to this role?
                5. **Location/remote fit** — can the candidate realistically work this role?

                ## Scoring rubric
                - 1-3: Poor fit — major gaps in required skills or seniority mismatch, Overqualified (e.g. 2+ yrs for stage/internship)? Max 3.
                - 4-5: Partial fit — some relevant skills but significant gaps remain
                - 6-7: Good fit — most key skills covered, minor gaps only
                - 8-9: Strong fit — skills, seniority, and domain all align well
                - 10: Near-perfect fit — candidate matches almost every requirement

                ## Output rules
                - "analysis": concise reasoning covering key match/mismatch criteria.
                - "score": integer 1-10, based on your analysis above
                - "location": country of the job
                - "city": city of the job 
                - "a_summirize": alternate summary of the analysis max 100 chars.
                - "company": extract from the job description
                - "role": exact job title from the description
                - "work_mode": one of "remote", "hybrid", "onsite", "unknown" — extract from description
                - "apply_link": the original LinkedIn URL (https://www.linkedin.com/jobs/view/...), copy it exactly, never modify it

                Respond ONLY with valid JSON, no markdown, no extra text:
                {{"analysis": "...", "score": "...","a_summirize": "..."  , "company": "...", "role": "...", "work_mode": "...", "apply_link": "..."}}"""
    response_list= []
    for index, row in jobs.iterrows():
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"""{row["role"]},{row["company"]}, {row["seniority"]}, {row["modality"]}, {row["experience_years_min"]}, 
                        {row["required_skills"]}, {row["nice_to_have_skills"]}, {row["required_education"]}, {row["languages"]},{row["job_url"]}""",
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0,
                response_mime_type="application/json",
                response_schema=JobScore  # forza output JSON
            )
        )
        response_list.append(response.text)
        time.sleep(7)  # wait 7 seconds between requests to avoid rate limiting

    #normilize output as dataframe

    parsed = [json.loads(x) for x in response_list]

    jobs_score = pd.json_normalize(parsed)

    # filter df with env score
    
    job_all= jobs_score

    jobs_score = jobs_score[jobs_score["score"]>=int(os.getenv("score_config"))]

    # df to dict

    jobs_score = jobs_score[["score","company","role","work_mode","a_summirize","apply_link"]]

    jobs_score = jobs_score.to_dict(orient="records")

    #clean the dict output

    jobs_score = json.dumps(jobs_score, indent=1)
    jobs_score = jobs_score.replace("'", "").replace("[", "").replace("]", "").replace("{", "").replace("},", "       ").replace('"', '').replace(',', '')

    
    return jobs_score, job_all



        