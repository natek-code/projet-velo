from .functions import load_config
from pathlib import Path
import os, json

MAX_FAVORITES = 10

config_file = load_config()
data_path = Path(config_file["data"]["folder"])/"vlille"
fav_file = data_path/"favorites.json"
stations_file = data_path/"station_information.json"

def get_favs():
    favorites = {}
    try:
        with open(fav_file, "r", encoding="utf-8") as f:
            favorites = json.load(f)
            return favorites["favorites"]
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return []

def get_list_stations():
    stations_id = []
    try:
        with open(stations_file, "r", encoding="utf-8") as f:
            stations = json.load(f)["data"]["stations"]
            for ele in stations:
                stations_id.append(ele["station_id"])
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return stations_id

def write_favs(favs):
    try:
        with open(fav_file, "w", encoding="utf-8") as f:
            json.dump({"favorites" : favs}, f)
    except FileNotFoundError:
        pass

favs = get_favs()

def handle_favorites(args):
    if len(favs) == 0:
        print("Liste des favoris vide, vous pouvez en ajouter via velo favorites add 'id_station'")
    for ele in favs:
        print(ele)

def handle_favorites_add(args):
    stations_id = get_list_stations()
    if args.station_id not in stations_id:
        print("L'id de la station n'existe pas !")
    if len(favs) >= MAX_FAVORITES :
        print("Liste des favoris pleine, vous pouvez en retirer via velo favorites remove 'id_station'")
    if args.station_id not in favs:
        favs.append(args.station_id)
    write_favs(favs)

def handle_favorites_remove(args):
    if args.station_id in favs:
        favs.pop(favs.index(args.station_id))
    else:
        print("L'id de cette station n'est pas dans la liste de vos favoris")
    write_favs(favs)