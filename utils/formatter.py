import numpy as np


def clean_data(data: dict) -> dict:

    formatted_dict = {}
    for index, data in enumerate(data):

        player_data = data["player"]
        rounds_data = data["rounds"]

        formatted_dict[index] = {
            "player": player_data["displayName"],
            "final_position": data["position"],
            "country": player_data["country"],
            "amateur": player_data["amateur"],

            "round_1": rounds_data[0]["score"] if len(rounds_data) > 0 else np.nan,
            "round_1_rel": rounds_data[0]["parRelativeScore"] if len(rounds_data) > 0 else np.nan,

            "round_2": rounds_data[1]["score"] if len(rounds_data) > 1 else np.nan,
            "round_2_rel": rounds_data[1]["parRelativeScore"] if len(rounds_data) > 1 else np.nan,

            "round_3": rounds_data[2]["score"] if len(rounds_data) > 2 else np.nan,
            "round_3_rel": rounds_data[2]["parRelativeScore"] if len(rounds_data) > 2 else np.nan,

            "round_4": rounds_data[3]["score"] if len(rounds_data) > 3 else np.nan,
            "round_4_rel": rounds_data[3]["parRelativeScore"] if len(rounds_data) > 3 else np.nan,

            "total": data["total"],
            "total_relative": data["parRelativeScore"]
        }

    return formatted_dict
