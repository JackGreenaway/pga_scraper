## PGA Historical Rounds Scraper

---

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python 3.6](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/release/python-30/)

---
### Overview

This is a repo that enables easy scraping of data from the PGA website for analysis.

It leverages the backend GraphQL requests that the website sends to collect information on rounds.

---
### Setup
This repo uses the [uv](https://github.com/astral-sh/uv) package manager becuase everything else is just a faff.

To run the `script_data.py` file first install `uv` with `pip install uv` and then run `uv sync` to set up the environment.

---
### Example Usage
```
usage: scrape_data.py [-h] (--id ID | -j JSON) -s SAVE_NAME -yr YEAR_RANGE

options:
  -h, --help            show this help message and exit
  --id ID               desired tournamentPastResultsId. Example: 'R2024100'
  -j, --json JSON       json file containing key value pairs of tournamentPastResultsId: tournament name. Example:
                        'tournament_keys.json'
  -s, --save_name SAVE_NAME
                        name to save output file as. Example: 'tournament_results'
  -yr, --year_range YEAR_RANGE
                        year range to collect data for. Example: '2010-2020'
```

Using a `.json` file to define the torunaments to collect  

```
uv run .\scrape_data.py --json tournament_keys.json -s major_comp_results -yr 1990-2024
``` 

Manually defining tournaments to collect

```
uv run .\scrape_data.py --id R2024100 --id R2023014 --id R2024026 --id R2024011 -s major_comp_results -yr 1990-2024
```
