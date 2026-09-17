# Workflow preferences

- Pull requests always target the `dev` branch (never the repo's default branch, never `main`/`master`), unless the user explicitly says otherwise.
- Commit messages are always in English.
- Commit messages always start with a conventional keyword followed by a short description, e.g. `feat: short description`, `fix: short description`. Choose the keyword (`feat`, `fix`, `docs`, `chore`, `ci`, `refactor`, `test`, etc.) based on the nature of the change.
- The user wants to write, test, and commit most of the code themselves. Aim for roughly a 70/30 split (user/Claude). Act as an assistant, not the primary developer: point out bugs, explain root causes, propose approaches, review code, answer questions. Only write/edit/commit code directly when explicitly asked to, or for small mechanical changes (config, workflow files, trivial fixes).
