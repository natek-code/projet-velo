import requests
import datetime

url = "https://media.ilevia.fr/opendata/gbfs.json"


def info(url):
    info = requests.get(url)
    return info.json()


def get_station_status():
    infos = info(url)
    for feed in infos["data"]["en"]["feeds"]:
        if feed["name"] == "station_status":
            return info(feed["url"])
    raise ValueError("Flux 'station_status' introuvable")


def get_station_name():
    infos = info(url)
    for feed in infos["data"]["en"]["feeds"]:
        if feed["name"] == "station_information":
            return info(feed["url"])
    raise ValueError("Flux 'station_information' introuvable")


def handle_status(args=None):
    maintenant = datetime.datetime.now()
    stations = get_station_status()["data"]["stations"]

    hs = []
    for s in stations:
        if not s["is_renting"]:
            hs.append(s["station_id"])

    noms = {}
    for s in get_station_name()["data"]["stations"]:
        noms[s["station_id"]] = s["name"]

    hs_name = []
    for station_id in hs:
        hs_name.append(f"{station_id} {noms.get(station_id, 'Inconnue')}")

    print(f"V'Lille - alertes du {maintenant:%d/%m/%Y} à {maintenant:%H:%M}")
    print(f"Hors service ({len(hs)}) {', '.join(hs_name)}")


if __name__ == "__main__":
    handle_status()