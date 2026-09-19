# CLAUDE.md

## Project

SnapplAI is a daily job-alert pipeline: it scrapes LinkedIn postings via
jobspy, uses Gemini agents to summarize and score each job against a
candidate's CV, then emails the filtered matches. Runs as a GitHub Action,
entry point `main.py`.

## Project structure

- `main.py`            — pipeline entry point (scrape → summarize → analyze → email)
- `src/daily_scraper.py` — jobspy scraping (`job_scraper`)
- `src/ai_agents.py`    — Gemini agents: `agentic_summarize`, `agentic_analyze`
- `src/llm.py`          — resilient Gemini call wrapper (retry + model fallback)
- `src/pydantic.py`     — `JobSummary` / `JobScore` schemas used to force LLM JSON output
- `src/smtp.py`         — builds and sends the report email
- `tests/`              — pytest suite (one file per module)

## Common commands

- Install deps: `pip install -r requirements.txt`
- Run: `python main.py`
- Run tests: `pip install pytest && pytest` (pytest isn't in requirements.txt;
  CI installs it separately)

## Environment

Config comes from two places:
- `.github/workflows/snapplai.yml` `env:` block — search settings (`location`,
  `city`, `search_term`, `results_wanted`, `hours_old`, `work_from_home`,
  `remote_only`, `dir_cv`, `score_config`).
- Secrets (GitHub Actions secrets, or local `.env` / `your_cv_config/file_config.env`):
  `LLM_GEMINI`, `GMAIL_USER`, `GMAIL_APP_PASSWORD` (or the generic
  `SMTP_HOST`/`SMTP_PORT`/`SMTP_USER`/`SMTP_PASSWORD` overrides in `src/smtp.py`).

## Git workflow

1. Pull requests always target the `dev` branch (never the repo's default
   branch, never `main`/`master`), unless explicitly told otherwise.
2. Use a single persistent branch called `claude` (branched from `dev`) as the
   standing development branch. Don't create a new branch per fix/feature.
   Only `main`, `dev`, and `claude` should exist as branches in this repo.
3. Rebase `claude` onto `dev` before opening or updating a PR.
4. Work and commit locally first, accumulating changes. Only open/push a PR
   once there's meaningful work ready, not one PR per single commit.
5. Commit messages are always in English.
6. Commit messages use conventional format: `feat: short description`,
   `fix: short description` (`feat`, `fix`, `docs`, `chore`, `ci`,
   `refactor`, `test`, ...), chosen by the nature of the change.
7. Never include the Claude session link (claude.ai/code/session_...) in
   commit messages or PR descriptions. The "Co-Authored-By" line and
   "Generated with Claude Code" badge are fine to keep, just not the URL.

## Code style

- All code is written in English: variable names, function names, comments,
  docstrings, test names.

## Verification

After implementing, run the test suite to verify before considering the task
done. If a test fails, fix it and re-run. Don't mark work as complete based on
"it looks right" alone.

## Compaction

When compacting, always preserve the full list of modified files, any failing
test output, and the current task goal.

## Things to avoid

- Don't assume a collection (list, DataFrame, query result) has items: guard
  the empty case explicitly instead of letting a missing key or undefined
  variable crash the run.
- Never let an LLM guess data the code already has: always pass real values to
  prompts instead of letting the model invent them.
