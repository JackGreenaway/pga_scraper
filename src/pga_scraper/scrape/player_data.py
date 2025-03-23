import requests


class PlayerDataScraper:
    def __init__(self, api_key: str, player_id: str, tour_code: str = "R") -> None:
        self.api_key = api_key
        self.player_id = player_id
        self.tour_code = tour_code

    def player_profile(self) -> requests.Response:
        payload = {
            "operationName": "Player",
            "variables": {"playerId": self.player_id},
            "query": "query Player($playerId: ID!) {\n  player(id: $playerId) {\n    bioLink\n    countryFlag\n    country\n    displayName\n    firstName\n    id\n    lastName\n    playerBio {\n      deceased\n      deceasedDate\n      age\n      birthplace {\n        countryCode\n        country\n        city\n        state\n        stateCode\n      }\n      born\n      bornAccessibilityText\n      degree\n      careerEarnings\n      family\n      graduationYear\n      heightImperial\n      heightImperialAccessibilityText\n      heightMeters\n      overview\n      personal\n      playsFrom {\n        city\n        country\n        countryCode\n        state\n        stateCode\n      }\n      pronunciation\n      residence {\n        city\n        country\n        state\n        countryCode\n        stateCode\n      }\n      school\n      social {\n        type\n        url\n      }\n      turnedPro\n      weightImperial\n      weightKilograms\n      websiteURL\n      exemptions {\n        tour\n        description\n        expirationDate\n      }\n    }\n    rank {\n      rank\n      statName\n    }\n    owgr\n  }\n}",
        }

        response = requests.post(
            "https://orchestrator.pgatour.com/graphql",
            json=payload,
            headers={"x-api-key": self.api_key},
        )

        return response

    def player_career(self) -> requests.Response:
        payload = {
            "operationName": "PlayerProfileCareer",
            "variables": {"playerId": self.player_id, "tourCode": self.tour_code},
            "query": "query PlayerProfileCareer($playerId: String!, $tourCode: TourCode) {\n  playerProfileCareer(playerId: $playerId, tourCode: $tourCode) {\n    playerId\n    tourCode\n    events\n    wins\n    winsTitle\n    internationalWins\n    majorWins\n    cutsMade\n    runnerUp\n    second\n    third\n    top10\n    top25\n    years {\n      cutsMade\n      displaySeason\n      events\n      officialMoney\n      second\n      standingsPoints\n      standingsRank\n      third\n      top10\n      top25\n      tourCode\n      wins\n      withdrawn\n      year\n    }\n    officialMoney\n    tourPills {\n      tourCode\n      displayName\n    }\n    achievements {\n      title\n      value\n    }\n    tables {\n      tableName\n      tableDetail\n      rows {\n        rowTitle\n        rowTitleDetail\n        rowContent\n        secondContent\n      }\n    }\n    years {\n      tourCode\n      displaySeason\n      year\n      events\n      wins\n      second\n      third\n      top10\n      top25\n      cutsMade\n      withdrawn\n      officialMoney\n      standingsPoints\n      standingsRank\n    }\n  }\n}",
        }

        response = requests.post(
            "https://orchestrator.pgatour.com/graphql",
            json=payload,
            headers={"x-api-key": self.api_key},
        )

        return response
