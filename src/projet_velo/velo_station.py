import json
from pathlib import Path
import re
from .functions import load_config


def get_stations():
    config = load_config()
    path = Path(config["data"]["folder"]) / "vlille" / "station_information.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)["data"]["stations"]


def handle_station_list(args):
    for s in get_stations():
        print(f"{s['station_id']:<6} {s['name']}")
    return 0


def handle_station_search(args):
    try:
        pattern = re.compile(args.texte, re.IGNORECASE)
    except re.error:
        print("Regex invalide")
        return 1

    for s in get_stations():
        if pattern.search(s["name"]):
            print(f"{s['station_id']:<6} {s['name']}")
    return 0