import requests
import datetime

from .functions import load_config


def info(url):
    reponse = requests.get(url, timeout=10)
    reponse.raise_for_status()
    return reponse.json()


def get_station_status():
    url = load_config()["network"]["gbfs_url"]
    infos = info(url)
    for feed in infos["data"]["en"]["feeds"]:
        if feed["name"] == "station_status":
            return info(feed["url"])
    raise ValueError("Flux 'station_status' introuvable")


def get_station_name():
    url = load_config()["network"]["gbfs_url"]
    infos = info(url)
    for feed in infos["data"]["en"]["feeds"]:
        if feed["name"] == "station_information":
            return info(feed["url"])
    raise ValueError("Flux 'station_information' introuvable")


def handle_alerts(args=None):
    config = load_config()
    if args is None or args.low_bikes is None:
        low_bikes = config["alerts"]["low_bikes"]
    else:
        low_bikes = args.low_bikes
    if args is None or args.low_docks is None:
        low_docks = config["alerts"]["low_docks"]
    else:
        low_docks = args.low_docks

    maintenant = datetime.datetime.now()
    stations = get_station_status()["data"]["stations"]

    hs = []
    en_service = []
    for s in stations:
        if not s["is_installed"] or not s["is_renting"] or not s["is_returning"]:
            hs.append(s["station_id"])
        else:
            en_service.append(s)

    noms = {}
    for s in get_station_name()["data"]["stations"]:
        noms[s["station_id"]] = s["name"]

    hs_name = []
    for station_id in hs:
        hs_name.append(f"{station_id} {noms.get(station_id, 'Inconnue')}")

    low_bike_name = []
    for s in en_service:
        if s["num_bikes_available"] <= low_bikes:
            station_id = s["station_id"]
            low_bike_name.append(
                f"{station_id} {noms.get(station_id, 'Inconnue')} ({s['num_bikes_available']})"
            )

    low_docks_name = []
    for s in en_service:
        if s["num_docks_available"] <= low_docks:
            station_id = s["station_id"]
            places = s["num_docks_available"]
            mot = "places" if places > 1 else "place"
            low_docks_name.append(
                f"{station_id} {noms.get(station_id, 'Inconnue')} ({places} {mot})"
            )

    print(f"{config['network']['name']} - alertes du {maintenant:%d/%m/%Y} à {maintenant:%H:%M}")
    if not hs_name and not low_bike_name and not low_docks_name:
        print("Aucune alerte.")

    if hs_name:
        print(f"Hors service ({len(hs_name)}) {', '.join(hs_name)}")
    if low_bike_name:
        print(f"Vide ou presque ({len(low_bike_name)}) {', '.join(low_bike_name)}")
    if low_docks_name:
        print(f"Pleine ou presque ({len(low_docks_name)}) {', '.join(low_docks_name)}")


if __name__ == "__main__":
    handle_alerts()