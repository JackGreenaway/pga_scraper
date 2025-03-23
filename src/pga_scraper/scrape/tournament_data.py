import requests
import numpy as np
import yaml


class TournamentDataScraper:
    def __init__(self, api_key: str, tournament_id: str):
        self.api_key = api_key
        self.tournament_id = tournament_id

        self.gql_queries = yaml.safe_load(
            open("src/pga_scraper/scrape/gql_queries.yaml")
        )

    def tournament_avaliable_years_data(self) -> requests.Response:
        payload = {
            "operationName": "TournamentPastResults",
            "variables": {
                "tournamentPastResultsId": self.tournament_id,
                "year": int(0),
            },
            # "query": "query TournamentPastResults($tournamentPastResultsId: ID!, $year: Int) {\n  tournamentPastResults(id: $tournamentPastResultsId, year: $year) {\n    id\n    players {\n      id\n      position\n      player {\n        id\n        firstName\n        lastName\n        shortName\n        displayName\n        abbreviations\n        abbreviationsAccessibilityText\n        amateur\n        country\n        countryFlag\n        lineColor\n      }\n      rounds {\n        score\n        parRelativeScore\n      }\n      additionalData\n      total\n      parRelativeScore\n    }\n    rounds\n    additionalDataHeaders\n    availableSeasons {\n      year\n      displaySeason\n    }\n    winner {\n      id\n      firstName\n      lastName\n      totalStrokes\n      totalScore\n      countryFlag\n      countryName\n      purse\n      points\n    }\n  }\n}",
            "query": self.gql_queries["tournament_data"]["tournament_past_results"],
        }

        response = requests.post(
            "https://orchestrator.pgatour.com/graphql",
            json=payload,
            headers={"x-api-key": self.api_key},
        )

        return response

    def tournament_result_data(self, year: int) -> requests.Response:
        payload = {
            "operationName": "TournamentPastResults",
            "variables": {
                "tournamentPastResultsId": self.tournament_id,
                "year": year,
            },
            # "query": "query TournamentPastResults($tournamentPastResultsId: ID!, $year: Int) {\n  tournamentPastResults(id: $tournamentPastResultsId, year: $year) {\n    id\n    players {\n      id\n      position\n      player {\n        id\n        firstName\n        lastName\n        shortName\n        displayName\n        abbreviations\n        abbreviationsAccessibilityText\n        amateur\n        country\n        countryFlag\n        lineColor\n      }\n      rounds {\n        score\n        parRelativeScore\n      }\n      additionalData\n      total\n      parRelativeScore\n    }\n    rounds\n    additionalDataHeaders\n    availableSeasons {\n      year\n      displaySeason\n    }\n    winner {\n      id\n      firstName\n      lastName\n      totalStrokes\n      totalScore\n      countryFlag\n      countryName\n      purse\n      points\n    }\n  }\n}",
            "query": self.gql_queries["tournament_data"]["tournament_past_results"],
        }

        response = requests.post(
            "https://orchestrator.pgatour.com/graphql",
            json=payload,
            headers={"x-api-key": self.api_key},
        )

        return response

    def formatter(self, data: list[dict]) -> list[dict]:
        n_rounds = 4
        formatted_dict_list = []

        for index, entry in enumerate(data):
            player_data = entry["player"]
            rounds_data = entry.get("rounds", [])

            formatted_dict_list += [
                {
                    "player": player_data.get("displayName", "Unknown"),
                    "final_position": entry.get("position", np.nan),
                    "country": player_data.get("country", "Unknown"),
                    "amateur": player_data.get("amateur", False),
                    **{
                        f"round_{i + 1}": (
                            rounds_data[i]["score"]
                            if i < len(rounds_data)
                            else "None"  # I would rather this be None but Polras can get upset with different types
                        )
                        for i in range(n_rounds)
                    },
                    **{
                        f"round_{i + 1}_rel": (
                            rounds_data[i]["parRelativeScore"]
                            if i < len(rounds_data)
                            else "None"
                        )
                        for i in range(n_rounds)
                    },
                    "total": entry.get("total", np.nan),
                    "total_relative": entry.get("parRelativeScore", np.nan),
                }
            ]

        return formatted_dict_list
