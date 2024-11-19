import pandas as pd


def get_payload(year: int, id: str = "R2023014") -> dict:
    payload = {
        "operationName": "TournamentPastResults",
        "variables": {
            "tournamentPastResultsId": id,
            "year": year
        },
        "query": "query TournamentPastResults($tournamentPastResultsId: ID!, $year: Int) {\n  tournamentPastResults(id: $tournamentPastResultsId, year: $year) {\n    id\n    players {\n      id\n      position\n      player {\n        id\n        firstName\n        lastName\n        shortName\n        displayName\n        abbreviations\n        abbreviationsAccessibilityText\n        amateur\n        country\n        countryFlag\n        lineColor\n      }\n      rounds {\n        score\n        parRelativeScore\n      }\n      additionalData\n      total\n      parRelativeScore\n    }\n    rounds\n    additionalDataHeaders\n    availableSeasons {\n      year\n      displaySeason\n    }\n    winner {\n      id\n      firstName\n      lastName\n      totalStrokes\n      totalScore\n      countryFlag\n      countryName\n      purse\n      points\n    }\n  }\n}"
    }

    return payload


def get_years(year_arg: str, tournament_id: str) -> list[float]:

    if "-" not in year_arg:
        raise ValueError("character '-' is not in '--year_range' argument")

    year_args = year_arg.split("-")
    min_year, max_year = int(year_args[0]), int(year_args[1])

    years = list(range(min_year * 10, (max_year + 1) * 10, 10))

    if tournament_id == "R2023014" and 20210 in years:
        # for the 2021 masters year there was two tournaments
        years.remove(20210)
        years += [20210, 20211]

    return years


def format_frame(df: pd.DataFrame) -> pd.DataFrame:

    df = df.replace("-", 0).replace("E", 0)
    
    round_columns = df.columns[df.columns.str.contains("round|total", case=True)]
    df[round_columns] = df[round_columns].astype(float)
    
    df["completed_tournament"] = df[round_columns].notna().all(axis=1)

    return df
