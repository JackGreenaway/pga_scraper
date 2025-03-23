import warnings
import polars as pl

from tqdm import tqdm

from src.pga_scraper.scrape.tournament_data import TournamentDataScraper


def scrape_tournament_data_loop(
    tournaments_dict: dict, min_year: int, api_key
) -> pl.DataFrame:
    tournament_df = pl.DataFrame()

    tournament_pb = tqdm(tournaments_dict.items(), position=0)

    for tournament, tournament_id in tournament_pb:
        tournament_pb.set_description(f"{tournament}")

        scraper = TournamentDataScraper(api_key=api_key, tournament_id=tournament_id)

        avaliable_years = scraper.tournament_avaliable_years_data().json()["data"][
            "tournamentPastResults"
        ]["availableSeasons"]

        target_years = [i for i in avaliable_years if int(i["year"] / 10) >= min_year]

        year_pb = tqdm(target_years, position=1, leave=False)

        for tournament_year in year_pb:
            year_pb.set_description(f"year: {tournament_year['year'] / 10:.0f}")

            tournament_data_raw = scraper.tournament_result_data(
                year=tournament_year["year"]
            )

            tournament_data = scraper.formatter(
                tournament_data_raw.json()["data"]["tournamentPastResults"]["players"]
            )

            temp_tournament_df = pl.DataFrame(tournament_data).with_columns(
                pl.lit(tournament).alias("tournament_name"),
                pl.lit(
                    tournament_data_raw.json()["data"]["tournamentPastResults"]["id"]
                ).alias("tournament_id"),
                pl.lit(tournament_year["displaySeason"]).alias("tournament_year"),
            )

            try:
                tournament_df = pl.concat([tournament_df, temp_tournament_df])
            except Exception as e:
                warnings.warn(
                    f"tried to concat to {tournament_year['year']} but failed | {e}",
                    UserWarning,
                )
    return tournament_df
