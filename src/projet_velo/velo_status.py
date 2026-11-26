import requests
import datetime
from .functions import *


def handle_status(args : list | None):
    maintenant = datetime.datetime.now()
    stations = list(get_stations_status().values())

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