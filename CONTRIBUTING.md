# Contributing to SnapplAI

Thanks for your interest in contributing! This document explains how the project works and how to get involved.

## Start with a conversation

Before writing any code, open a thread in [Discussions](https://github.com/TDK-99/SnapplAI/discussions) or an [Issue](https://github.com/TDK-99/SnapplAI/issues). Describe what you want to change and why. This avoids duplicated effort and makes sure your contribution fits the project direction.

The flow is: **Discussion/Issue → align on approach → fork → PR**.

## Setting up the project

1. Fork the repo and clone your fork
2. Create a virtual environment with Python 3.12 (the project is pinned to 3.12)
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `example_env.txt` to `.env` and fill in your API keys (Gemini, SMTP credentials)
5. Place your CV in `your_cv_config/` following the existing format

## Branch workflow

- `main` is the production branch, protected. Only the maintainer merges into it.
- `dev` is the working branch. All PRs from contributors target `dev`.
- Create your feature branch from `dev`:

```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
```

## Making a pull request

1. Keep your PR focused on a single change. One feature or fix per PR.
2. Make sure existing tests pass before submitting:

```bash
pytest -v
```

3. If you add new functionality, add tests for it.
4. Write a clear PR description: what changed, why, and how to test it.
5. Target the `dev` branch, not `main`.
6. Make small, frequent commits. Each commit should represent one logical change. Avoid large commits that bundle multiple unrelated changes together.

## Code conventions

- All code is written in **English**: variable names, function names, comments, tests, docstrings.
- Follow the existing code style in the repo. Keep it consistent.
- Use type hints where possible.
- Keep functions small and focused.

## What you can work on

Check the [Issues](https://github.com/TDK-99/SnapplAI/issues) for open tasks, or propose something new in [Discussions](https://github.com/TDK-99/SnapplAI/discussions). Some areas where contributions are welcome:

- Improving the scoring/matching logic
- Adding support for more job platforms
- Better test coverage
- Documentation improvements

## License

By contributing, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).
