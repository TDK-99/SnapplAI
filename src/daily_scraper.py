from jobspy import scrape_jobs
from dotenv import load_dotenv
import pandas as pd
import os

def job_scraper():
    load_dotenv("your_cv_config/file_config.env", override=True)
    jobs = []
    for loc in os.getenv("location").split(","):
        jobs_df = scrape_jobs(
            site_name= os.getenv("site_name"),
            search_term= os.getenv("search_term"),
            location= loc.strip(),
            results_wanted= int(os.getenv("results_wanted")),
            hours_old= int(os.getenv("hours_old")),
            linkedin_fetch_description= os.getenv("linkedin_fetch_description") == "True",
            proxies= os.getenv("proxies").split(",") if os.getenv("proxies") else None,
        )
        jobs.append(jobs_df)

    jobs = pd.concat(jobs, ignore_index=True)

    if os.getenv("country_no"):
        # jobspy only gives a combined "City, Region, Country" string, no clean
        # country field, so exclusion is a case-insensitive substring match.
        for country in os.getenv("country_no").split(","):
            jobs = jobs[~jobs["location"].str.contains(country.strip(), case=False, na=False)]

    return jobs