import requests
from bs4 import BeautifulSoup
import json
import argparse


def parse_cli() -> argparse.Namespace:

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--url",
        type=str,
        help="pga schedule webpage",
        default="https://www.pgatour.com/schedule",
    )

    args = parser.parse_args()

    return args


def clean_keys(key: str) -> str:

    replace_dict = {".": "", "_": "", "-": "_"}

    for target_kw, replace_kw in replace_dict.items():
        key = key.replace(target_kw, replace_kw)

    return key


def scrape_tournament_keys(url: str = "https://www.pgatour.com/schedule") -> dict:

    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")

    tournaments_href = [
        a["href"]
        for a in soup.find_all("a", class_="chakra-link css-1jfg7sy")
        if "/tournaments/" in a["href"]
    ]

    tournamnet_keys = {
        keys[4]: clean_keys(keys[3])
        for keys in [t.split("/") for t in tournaments_href]
    }

    return tournamnet_keys


def write_json(tournament_keys: dict) -> None:

    with open("tournament_keys.json", "w") as json_file:
        json.dump(tournament_keys, json_file, indent=4)


if __name__ == "__main__":

    args = parse_cli()

    print("collecting tournaments")
    t_keys = scrape_tournament_keys(url=args.url)

    print("writing tournament file")
    write_json(tournament_keys=t_keys)

    print(f"success - {len(list(t_keys.keys()))} tournaments collected")
