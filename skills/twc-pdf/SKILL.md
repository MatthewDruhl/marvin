# TWC PDF Generation Skill

Generate official Texas Workforce Commission Work Search Activity Log PDFs from CSV files.

## Usage

Run this whenever TWC CSV files have been updated (new job search activities logged).

## How to Run

```bash
cd content/jobs/TWC
for file in work-search-week-*.csv; do
    python3 fill_twc_pdf.py "$file" 2>/dev/null
done
```

## Details

- **Input:** `content/jobs/TWC/work-search-week-*.csv` files
- **Output:** Filled PDF forms alongside the CSV files
- **Script:** `content/jobs/TWC/fill_twc_pdf.py` (uses PyPDF2)
- **Supports:** Multi-page weeks (generates part1, part2, etc. for weeks with >3 activities)
- **Naming:** CSV files use full ISO dates: `work-search-week-YYYY-MM-DD.csv` (the Sunday the week starts), matching `twc_week_filename()` in `scripts/marvin_start.py`. Legacy files from early 2026 use a 2-digit year (`work-search-week-26-MM-DD.csv`); the glob matches both.

## When to Run

- At `/end` session (automatic)
- At `/update` checkpoint (only if TWC files changed)
- Manually when new job search activities are logged
