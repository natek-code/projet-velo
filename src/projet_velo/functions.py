import yaml, sys, requests, json
from pathlib import Path

def load_config():
    try:
        with open(Path.home()/".config"/"velo"/"config.yaml") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        sys.exit("File not found")

config = load_config()
status_url = config["network"]["gbfs_url"]
stations_file = Path(config["data"]["folder"])/"vlille"/"station_information.json"

def get_stations_status():
    infos = requests.get(status_url).json()
    for feed in infos["data"]["en"]["feeds"]:
        if feed["name"] == "station_status":
            stations = requests.get(feed["url"]).json()["data"]["stations"]
            return {str(st["station_id"]) : st for st in stations}
    raise ValueError("Flux 'station_status' introuvable")

def get_stations_info():
    stations = {}
    try:
        with open(stations_file, "r", encoding="utf-8") as f:
            stations = json.load(f)["data"]["stations"]
            return {str(st["station_id"]) : st for st in stations}
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return stations

def get_info(id, d):
    return d[str(id)]

def get_status(id, d):
    return d[str(id)]