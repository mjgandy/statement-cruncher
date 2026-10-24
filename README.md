# Statement Cruncher

Statement Cruncher is a small Python utility that converts a Starling bank statement CSV into a the correct format for use with Crunch accounting software.

I wrote this specifically to make my own life easier when running a business that requires monthly reconciliation of bank statements. Instead of manually reformatting sometimes very lengthy CSV statements, this program does it for me, saving a lot of time!

In future I might consider expanding this to accept bank statements in various other formats, but for now this works for what I need.

It expects input rows with the following columns:

- `Date`
- `Counter Party`
- `Amount (GBP)`
- `Balance (GBP)`

It writes a new CSV with the structure:

- `Date`
- `Reference`
- `Paid In (GBP)`
- `Paid Out (GBP)`
- `Balance (GBP)`

## What it does

- Prompts you to select a CSV file from your machine
- Validates that the file exists and is a `.csv`
- Reads each transaction row
- Splits credit and debit values into separate columns
- Saves a processed file next to the original with a `_crunch.csv` suffix

## Requirements

- Python 3.13+
- `uv` (recommended for dependency management)

## Installation

```bash
uv sync
```

## Usage

Run the CLI:

```bash
uv run statement-cruncher
```

You can also run the module directly from the project root:

```bash
python -m src.statement_cruncher.main
```

The tool will prompt you for a CSV file path. Enter `q` at any time to quit.

## Docker

A Docker image is included for running the app in a containerized environment.

Build and run with:

```bash
docker compose up --build
```

The compose setup mounts a `statements` directory, which makes it convenient to keep statement files in a local folder while running the app.

## Project structure

```text
.
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── README.md
├── src/
│   └── statement_cruncher/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
└── uv.lock
```
