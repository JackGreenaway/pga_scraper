import pandas as pd
import numpy as np
import requests
import argparse

from numpy.typing import ArrayLike
from constants import api_key


def get_payload(year: int, id: str = "R2023014") -> dict:

    payload = {
        "operationName": "TournamentPastResults",
        "variables": {"tournamentPastResultsId": id, "year": year},
        "query": "query TournamentPastResults($tournamentPastResultsId: ID!, $year: Int) {\n  tournamentPastResults(id: $tournamentPastResultsId, year: $year) {\n    id\n    players {\n      id\n      position\n      player {\n        id\n        firstName\n        lastName\n        shortName\n        displayName\n        abbreviations\n        abbreviationsAccessibilityText\n        amateur\n        country\n        countryFlag\n        lineColor\n      }\n      rounds {\n        score\n        parRelativeScore\n      }\n      additionalData\n      total\n      parRelativeScore\n    }\n    rounds\n    additionalDataHeaders\n    availableSeasons {\n      year\n      displaySeason\n    }\n    winner {\n      id\n      firstName\n      lastName\n      totalStrokes\n      totalScore\n      countryFlag\n      countryName\n      purse\n      points\n    }\n  }\n}",
    }

    return payload


def get_tournament_years(args: argparse.Namespace, tournament_id: str) -> ArrayLike:

    year_arg = args.year_range

    if "-" not in year_arg:
        raise ValueError("character '-' is not in '--year_range' argument")

    year_args = year_arg.split("-")
    min_year, max_year = int(year_args[0]), int(year_args[1])

    years = requests.post(
        "https://orchestrator.pgatour.com/graphql",
        json=get_payload(year=int(0), id=tournament_id),
        headers={"x-api-key": api_key},
    ).json()["data"]["tournamentPastResults"]["availableSeasons"]

    years = np.array([(y["year"], y["year"] / 10) for y in years])
    years = years[np.argsort(years[:, 1])[::-1]]

    target_years = years[
        np.argmax(years[:, 1] <= max_year) : np.argmin(years[:, 1] >= min_year)
    ]

    display_years = target_years[:, 1]
    double_years = display_years[(display_years % 1) != 0].astype(int)

    if len(double_years) > 0:
        target_years[:, 1] = np.where(
            display_years.astype(int) == double_years,
            display_years + 0.1,
            display_years,
        )

    return target_years


def format_frame(df: pd.DataFrame) -> pd.DataFrame:

    df = df.replace("-", 0).replace("E", 0)

    round_columns = df.columns[df.columns.str.contains("round|total", case=True)]
    df[round_columns] = df[round_columns].astype(float)

    df["completed_tournament"] = df[round_columns].notna().all(axis=1)

    return df
