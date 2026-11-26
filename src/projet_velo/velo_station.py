import json
from pathlib import Path
import re
from .functions import *

def handle_station_list(args):
    stations = sorted(get_stations_info().values(), key = lambda i : int(i["station_id"]))
    for s in stations:
        print(f"{s['station_id']:<6} {s['name']}")
    return 0


def handle_station_search(args):
    stations = sorted(get_stations_info().values(), key = lambda i : int(i["station_id"]))    
    try:
        pattern = re.compile(args.texte, re.IGNORECASE)
    except re.error:
        print("Regex invalide")
        return 1

    results = [s for s in stations if pattern.search(s["name"])]

    if not results:
        print("Aucune station trouvée.")
        return 0

    for s in results:
        print(f"{s['station_id']:<6} {s['name']}")
    return 0