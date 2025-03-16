import numpy as np


def historical_tournament_data_formatter(data: list[dict]) -> dict:

    n_rounds = 4

    formatted_dict = {}

    for index, entry in enumerate(data):

        player_data = entry["player"]
        rounds_data = entry.get("rounds", [])

        formatted_dict[index] = {
            "player": player_data.get("displayName", "Unknown"),
            "final_position": entry.get("position", np.nan),
            "country": player_data.get("country", "Unknown"),
            "amateur": player_data.get("amateur", False),
            **{
                f"round_{i+1}": (
                    rounds_data[i]["score"] if i < len(rounds_data) else np.nan
                )
                for i in range(n_rounds)
            },
            **{
                f"round_{i+1}_rel": (
                    rounds_data[i]["parRelativeScore"]
                    if i < len(rounds_data)
                    else np.nan
                )
                for i in range(n_rounds)
            },
            "total": entry.get("total", np.nan),
            "total_relative": entry.get("parRelativeScore", np.nan),
        }

    return formatted_dict
