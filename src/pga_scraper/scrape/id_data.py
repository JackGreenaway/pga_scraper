import requests
import re
from datetime import datetime


class IdScraper:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def scrape_tournament_schedule(
        self, year: int = datetime.now().year
    ) -> requests.Response:
        payload = {
            "operationName": "Schedule",
            "query": "query Schedule($tourCode: String!, $year: String, $filter: TournamentCategory) {\n  schedule(tourCode: $tourCode, year: $year, filter: $filter) {\n    completed {\n      month\n      year\n      monthSort\n      ...ScheduleTournament\n    }\n    filters {\n      type\n      name\n    }\n    seasonYear\n    tour\n    upcoming {\n      month\n      year\n      monthSort\n      ...ScheduleTournament\n    }\n  }\n}\n\nfragment ScheduleTournament on ScheduleMonth {\n  tournaments {\n    tournamentName\n    id\n    beautyImage\n    champion\n    champions {\n      displayName\n      playerId\n    }\n    championEarnings\n    championId\n    city\n    country\n    countryCode\n    courseName\n    date\n    dateAccessibilityText\n    purse\n    sortDate\n    startDate\n    state\n    stateCode\n    status {\n      roundDisplay\n      roundStatus\n      roundStatusColor\n      roundStatusDisplay\n    }\n    tournamentStatus\n    ticketsURL\n    tourStandingHeading\n    tourStandingValue\n    tournamentLogo\n    display\n    sequenceNumber\n    tournamentCategoryInfo {\n      type\n      logoLight\n      logoDark\n      label\n    }\n    tournamentSiteURL\n    tournamentStatus\n    useTournamentSiteURL\n  }\n}",
            "variables": {"tourCode": "R", "year": str(year)},
        }

        response = requests.post(
            "https://orchestrator.pgatour.com/graphql",
            json=payload,
            headers={"x-api-key": self.api_key},
        )

        return response

    def scrape_player_directory(self) -> requests.Response:
        payload = {
            "operationName": "PlayerDirectory",
            "variables": {"tourCode": "R"},
            "query": "query PlayerDirectory($tourCode: TourCode!, $active: Boolean) {\n  playerDirectory(tourCode: $tourCode, active: $active) {\n    tourCode\n    players {\n      id\n      isActive\n      firstName\n      lastName\n      shortName\n      displayName\n      alphaSort\n      country\n      countryFlag\n      headshot\n      playerBio {\n        id\n        age\n        education\n        turnedPro\n      }\n    }\n  }\n}",
        }

        response = requests.post(
            "https://orchestrator.pgatour.com/graphql",
            json=payload,
            headers={"x-api-key": self.api_key},
        )

        return response

    def __clean_tournament_ids(self, tournament_ids: dict) -> dict:
        cleaned_tournament_data = []

        for kt in ["completed", "upcoming"]:
            if kt in tournament_ids.keys():
                for tournament_month in tournament_ids[kt]:
                    for tournament in tournament_month["tournaments"]:
                        cleaned_tournament_data += [
                            {
                                "tournament_name": tournament["tournamentName"],
                                "id": tournament["id"],
                                "champion_earnings": "".join(
                                    re.findall("\d+", tournament["championEarnings"])
                                ),
                                "purse": "".join(
                                    re.findall("\d+", tournament["purse"])
                                ),
                                "currency": "".join(
                                    re.findall("[$€£¥₹]", tournament["purse"])
                                ),
                                "city": tournament["city"],
                                "country_code": tournament["countryCode"],
                                "start_date": datetime.fromtimestamp(
                                    tournament["startDate"] / 1000
                                ),
                                "tour_standing_value": tournament["tourStandingValue"],
                                "course_name": tournament["courseName"],
                            }
                        ]

        return cleaned_tournament_data

    def scrape_unique_tournaments_in_range(
        self,
        min_year,
        max_year,
    ) -> dict:
        self.tournament_metadata = []
        for year in list(range(min_year, max_year + 1))[::-1]:
            metadata = self.__clean_tournament_ids(
                tournament_ids=self.scrape_tournament_schedule(year=year).json()[
                    "data"
                ]["schedule"]
            )

            self.tournament_metadata += metadata

        return self.tournament_metadata

    @property
    def unique_tournaments(self) -> dict:
        unique_tournaments = {}

        for tournament in self.tournament_metadata:
            # for key, value in pga_season.items():

            if (
                re.sub("\(\d{4}\)", "", tournament["tournament_name"]).strip()
                not in unique_tournaments
            ):
                unique_tournaments[tournament["tournament_name"]] = tournament["id"]

        return unique_tournaments
