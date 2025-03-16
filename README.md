# PGA Tournament Data Scraper

This project scrapes data related to PGA tournaments from the PGA website API, collects tournament metadata and results, and exports the collected data to Parquet files for further analysis.

---
## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager for dependency management

### Install Dependencies with UV

1. Install UV:
   ```bash
   pip install uv
   ```

2. Sync `.venv`:
    ```bash
    uv sync
    ```

---

## Environment Variables

To authenticate API requests, you'll need to set your API key in an `.env` file.
1. Create a `.env` file in the root directory of the project.
2. Add the following line to the `.env` file:
    ```bash
    API_KEY=your_api_key_here
    ```
    Replace `your_api_key_here` with your actual API key.

*You can find an api key on the PGA website within a headers request.*

---

## Code Structure

1. Main Scraping Logic:
    - The main script main.py orchestrates the collection of data, calling scraping functions from the scrape_data.py module located in src/pga_scraper/.

2. Scraping:
    - Data scraping is split into different modules:
        - **id_data.py**: Scrapes IDs relating to tournaments and players.
        - **player_data.py**: Scrapes player data from the PGA directory.
        - **tournament_data.py**: Scrapes tournament results data.

3. Data Formatting:
    - The utils/frame_formatters.py file contains logic for cleaning and formatting the scraped data before exporting it.

```
+---data
+---src
    +---pga_scraper
        +---scrape
        +---utils
```

---

## Running the script

```bash
uv run main.py
```

---

## Output
After the script finishes, you should see the following Parquet files in the data/ folder:

- `pga_tournament_results_data_2020_2025.pq`: tournament results data.
- `pga_tournament_metadata_data_2020_2025.pq`: metadata about the tournaments.

---

## Todo

1. Implement command line option processing
    - Years
    - Export file names
    - Specific tournaments and players
2. Implement the rest of player profile processing
3. Parallelisation of scraping logic