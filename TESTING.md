# MARVIN Testing

The repo contains several independent Python tools. Run their tests per suite from the suite root; do not run one root-level pytest command across every `tests/` directory. Several suites intentionally use a top-level `tests` package name, which can collide during collection.

## Python Version

The root project supports Python `>=3.12,<3.15`. The root `pyproject.toml` declares this so `uv` does not infer an unintended Python range from an empty project.

## Commands

From the repo root:

```bash
uvx ruff check .
```

Harden skill:

```bash
cd skills/harden
uv run pytest tests
```

Slack integration:

```bash
cd integrations/slack
uv run pytest tests
```

Resume editor:

```bash
cd skills/resume-editor
uv run --isolated --with pytest --with python-docx pytest tests
```

Update resume:

```bash
cd skills/update-resume
uv run --isolated --with pytest --with python-docx --with PyPDF2 pytest tests
```

TWC PDF tooling:

```bash
cd content/jobs/TWC
uv run --isolated --with pytest --with PyPDF2 --with python-dotenv pytest tests
```

## Notes

- `skills/resume-editor/tests/test_build_integration.py` and `test_regression.py` skip tests when local `~/Resume` fixtures are unavailable.
- Resume and cover-letter output filenames come from the resume header name, for example `Matthew_Druhl_resume.docx` and `Matthew_Druhl_cover_letter.docx`. Company-specific organization belongs in the output directory path.
