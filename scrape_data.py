import pandas as pd
import numpy as np
import json
import requests
import argparse

from constants import api_key
from tqdm import tqdm
from formatter import clean_data
from utils import get_payload, get_years, format_frame


def parse_cli() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--id", type=str, help="desired tournamentPastResultsId. Example: 'R2024100'", action="append")
    group.add_argument("-j", "--json", type=str,
                       help="json file containing key value pairs of tournamentPastResultsId: tournament name. Example: 'tournament_keys.json'")

    parser.add_argument("-s", "--save_name", type=str,
                        help="name to save output file as. Example: 'tournament_results'", required=True)

    parser.add_argument("-yr", "--year_range", type=str,
                        help="year range to collect data for. Example: '2010-2020'", required=True)

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = parse_cli()

    # get tournaments
    if args.json:
        tournament_map = json.loads(
            open(args.json, "r").read())

        tournament_keys = list(tournament_map.keys())
    else:
        tournament_keys = args.id

    frames = []
    for tournament_id in tqdm(tournament_keys, desc="tournaments", position=0):

        years = get_years(year_arg=args.year_range,
                          tournament_id=tournament_id)

        for year in tqdm(years, desc=f"years for {tournament_id}", position=1, leave=False):

            page = requests.post("https://orchestrator.pgatour.com/graphql",
                                 json=get_payload(year=int(year), id=tournament_id), headers={"x-api-key": api_key})

            page.raise_for_status()

            raw_data = page.json()["data"]["tournamentPastResults"]["players"]

            frame = pd.DataFrame.from_dict(
                clean_data(raw_data), orient="index")

            frame["tournament_id"] = tournament_id

            if args.json:
                frame["tournament_name"] = frame["tournament_id"].map(
                    tournament_map)
            else:
                frame["tournament_name"] = np.nan

            frame["year"] = year / 10

            frames += [frame]

    df = pd.concat(frames)

    df = format_frame(df)

    df.to_parquet(f"{args.save_name}.pq")
