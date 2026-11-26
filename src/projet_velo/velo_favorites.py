from .functions import *
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

def write_favs(favs):
    try:
        with open(fav_file, "w", encoding="utf-8") as f:
            json.dump({"favorites" : favs}, f)
    except FileNotFoundError:
        pass

def handle_favorites(args):
    favs = get_favs()
    if len(favs) == 0:
        print("Liste des favoris vide, vous pouvez en ajouter via velo favorites add 'id_station'")
        return
    print(f"{"ID":<{3}} {"Station":<{25}} {"Velos":<{5}} {"Places":<{5}}")
    stations_infos = get_stations_info()
    stations_status = get_stations_status()
    for ele in favs:
        info = get_info(ele, stations_infos)
        status = get_status(ele, stations_status)
        print(f"{info["station_id"]:<{3}} {info["name"]:<{25}} {status["num_bikes_available"]:<{5}} {status["num_docks_available"]:<{5}}")
        

def handle_favorites_add(args):
    favs = get_favs()
    stations = get_stations_info()
    if args.station_id not in list(stations.keys()):
        print("L'id de la station n'existe pas !")
    if len(favs) >= MAX_FAVORITES :
        print("Liste des favoris pleine, vous pouvez en retirer via velo favorites remove 'id_station'")
    if args.station_id not in favs:
        favs.append(args.station_id)
    write_favs(favs)

def handle_favorites_remove(args):
    favs = get_favs()
    if args.station_id in favs:
        favs.pop(favs.index(args.station_id))
    else:
        print("L'id de cette station n'est pas dans la liste de vos favoris")
    write_favs(favs)