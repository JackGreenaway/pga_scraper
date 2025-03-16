import polars as pl
import os
import warnings

from tqdm import tqdm
from dotenv import load_dotenv

from src.pga_scraper.scrape.id_data import IdScraper
from src.pga_scraper.scrape.tournament_data import TournamentDataScraper
from src.pga_scraper.utils.frame_formatters import (
    format_tournament_results_frame,
    format_tournament_metadata_frame,
)


def main():
    """
    Main function to scrape and collect PGA tournament data (metadata and results) between specified years,
    then export the results to parquet files.
    """

    # Load environment variables from a .env file
    load_dotenv()

    # Fetch the API key from environment variables
    API_KEY = os.getenv("API_KEY")

    # Define the year range for the data collection
    min_year = 2010
    max_year = 2024

    # Initialize the IdScraper with the provided API key
    id_scraper = IdScraper(api_key=API_KEY)

    print(f"Collecting tournament data between {min_year} - {max_year}")

    # Scrape metadata for tournaments within the given year range
    tournament_metadata = id_scraper.scrape_unique_tournaments_in_range(
        min_year=min_year, max_year=max_year
    )

    print(f"{len(tournament_metadata):,} tournaments found")

    # Retrieve the unique tournaments
    unique_tournaments = id_scraper.unique_tournaments

    # Initialize an empty DataFrame to hold tournament results
    tournament_df = pl.DataFrame()

    print("Collecting tournament results data")

    # Create a progress bar for tournaments
    tournament_pb = tqdm(unique_tournaments.items(), position=0)

    # Loop through each tournament and its corresponding ID
    for tournament, tournament_id in tournament_pb:
        tournament_pb.set_description(f"{tournament}")

        # Initialize the TournamentDataScraper with the tournament ID and API key
        scraper = TournamentDataScraper(api_key=API_KEY, tournament_id=tournament_id)

        # Fetch available years of results for the current tournament
        available_years = scraper.tournament_avaliable_years_data().json()["data"][
            "tournamentPastResults"
        ]["availableSeasons"]

        # Filter available years based on the minimum year
        target_years = [i for i in available_years if int(i["year"] / 10) >= min_year]

        # Create a progress bar for years
        year_pb = tqdm(target_years, position=1, leave=False)

        # Loop through each target year for the tournament
        for tournament_year in year_pb:
            year_pb.set_description(f"Year: {tournament_year['year'] / 10:.0f}")

            # Fetch the raw tournament result data for the given year
            tournament_data_raw = scraper.tournament_result_data(
                year=tournament_year["year"]
            )

            # Format the raw tournament data
            tournament_data = scraper.formatter(
                tournament_data_raw.json()["data"]["tournamentPastResults"]["players"]
            )

            # Create a temporary DataFrame with the tournament results and metadata
            temp_tournament_df = pl.DataFrame(tournament_data).with_columns(
                pl.lit(tournament).alias("tournament_name"),
                pl.lit(
                    tournament_data_raw.json()["data"]["tournamentPastResults"]["id"]
                ).alias("tournament_id"),
                pl.lit(tournament_year["displaySeason"]).alias("tournament_year"),
            )

            # Attempt to concatenate the current data to the main DataFrame
            try:
                tournament_df = pl.concat([tournament_df, temp_tournament_df])
            except Exception as e:
                warnings.warn(
                    f"Failed to concatenate data for year {tournament_year['year']} due to error: {e}",
                    UserWarning,
                )

    print("Exporting data")

    # Format and export the tournament results data to a parquet file
    tournament_df = format_tournament_results_frame(df=tournament_df)
    tournament_df.write_parquet("data/pga_tournament_results_data_2020_2025.pq")

    # Format and export the tournament metadata to a parquet file
    tournament_metadata = format_tournament_metadata_frame(
        pl.DataFrame(tournament_metadata)
    )
    tournament_metadata.write_parquet("data/pga_tournament_metadata_data_2020_2025.pq")

    # Print the shape (number of samples) of the exported data
    print(f"Tournament result data: {tournament_df.shape} samples")
    print(f"Tournament metadata: {tournament_metadata.shape} samples")


if __name__ == "__main__":
    main()
