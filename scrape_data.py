import pandas as pd
import numpy as np
import json
import requests
import argparse
import logging

from constants import api_key
from tqdm import tqdm
from formatter import clean_data
from utils import (
    get_payload,
    format_frame,
    get_tournament_years,
)


def main(args: argparse.Namespace) -> None:

    # get tournaments
    if args.json:
        tournament_map = json.loads(open(args.json, "r").read())

        tournament_keys = tournament_map
    else:
        tournament_keys = {id_: "unkown" for id_ in args.id}

    frames = []

    progress_bar_tournament = tqdm(
        tournament_keys.items(), desc="tournaments", position=0
    )

    for tournament_id, tournament_name in progress_bar_tournament:

        progress_bar_tournament.set_description(f"tournament: {tournament_name}")

        logging.info(f"collecting data for {tournament_name}")

        years = get_tournament_years(args=args, tournament_id=tournament_id)

        progress_bar_year = tqdm(
            years,
            position=1,
            leave=False,
        )

        for year_id, display_year in progress_bar_year:

            progress_bar_year.set_description(f"year: {display_year}")

            page = requests.post(
                "https://orchestrator.pgatour.com/graphql",
                json=get_payload(year=int(year_id), id=tournament_id),
                headers={"x-api-key": api_key},
            )

            page.raise_for_status()

            raw_data = page.json()["data"]["tournamentPastResults"]["players"]

            if len(raw_data) < 0:
                logging.error(
                    f"data likely incorrect/imcomplete/missing for {tournament_name}, {year_id}, {display_year}, {tournament_id}"
                )

            frame = pd.DataFrame.from_dict(clean_data(raw_data), orient="index")

            frame["tournament_id"] = tournament_id

            if args.json:
                frame["tournament_name"] = frame["tournament_id"].map(tournament_map)
            else:
                frame["tournament_name"] = np.nan

            frame["year"] = display_year

            frames += [frame]

    df = pd.concat(frames)

    df = format_frame(df)

    df.to_parquet(f"{args.save_name}.pq")


def parse_cli() -> argparse.Namespace:

    parser = argparse.ArgumentParser()

    tournament_ids = parser.add_mutually_exclusive_group(required=True)

    tournament_ids.add_argument(
        "--id",
        type=str,
        help="desired tournamentPastResultsId. Example: 'R2024100'",
        action="append",
    )

    tournament_ids.add_argument(
        "-j",
        "--json",
        type=str,
        help="json file containing key value pairs of tournamentPastResultsId: tournament name. Example: 'tournament_keys.json'",
    )

    parser.add_argument(
        "-s",
        "--save_name",
        type=str,
        help="name to save output file as. Example: 'tournament_results'",
        required=True,
    )

    parser.add_argument(
        "-yr",
        "--year_range",
        type=str,
        help="year range to collect data for. Example: '2010-2020'",
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse_cli()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="scraping_debug.log",
    )

    main(args=args)
