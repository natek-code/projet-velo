import requests
import datetime
from .functions import load_config

config = load_config()
url = config["network"]["gbfs_url"]


def info(url):
    info = requests.get(url)
    return info.json()


def get_station_status():
    infos = info(url)
    for feed in infos["data"]["en"]["feeds"]:
        if feed["name"] == "station_status":
            return info(feed["url"])
    raise ValueError("Flux 'station_status' introuvable")


def handle_status(args : list | None):
    maintenant = datetime.datetime.now()
    stations = get_station_status()["data"]["stations"]

    nombre = len(stations)
    vide = sum(1 for s in stations if s["num_bikes_available"]==0)
    plein = sum(1 for s in stations if s["num_docks_available"]==0)
    marche = sum(1 for s in stations if s["is_installed"])
    velos = sum(s["num_bikes_available"] for s in stations)
    places = sum(s["num_docks_available"] for s in stations)

    print(f"V'Lille - données du {maintenant:%d/%m/%Y} à {maintenant:%H:%M:%S}\n")
    print(f"Stations en service {marche} / {nombre} hors service {nombre-marche}")
    print(f"         vides {vide} pleines {plein}")
    print(f"Vélos disponibles {velos} places libres {places}")
    print(f"      taux de remplissage {round((velos/places)*100)}%")


if __name__ == "__main__":
    handle_status()