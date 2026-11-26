import requests
import datetime
from .functions import *


def calcul_status():
    maintenant = datetime.datetime.now()
    stations = list(get_stations_status().values())

    nombre = len(stations)
    vide = sum(1 for s in stations if s["num_bikes_available"]==0)
    plein = sum(1 for s in stations if s["num_docks_available"]==0)
    marche = sum(1 for s in stations if s["is_installed"])
    velos = sum(s["num_bikes_available"] for s in stations)
    places = sum(s["num_docks_available"] for s in stations)

    return {"maintenant": maintenant, "stations": stations, "nombre": nombre, "vide": vide,
            "plein":plein, "marche": marche, "velos": velos, "places": places}
   

def handle_status(args : list | None):
    resultat = calcul_status()
    print(f"V'Lille - données du {resultat["maintenant"]:%d/%m/%Y} à {resultat["maintenant"]:%H:%M:%S}\n")
    print(f"Stations en service {resultat["marche"]} / {resultat["nombre"]} hors service {resultat["nombre"]-resultat["marche"]}")
    print(f"         vides {resultat["vide"]} pleines {resultat["plein"]}")
    print(f"Vélos disponibles {resultat["velos"]} places libres {resultat["places"]}")
    print(f"      taux de remplissage {round((resultat["velos"]/resultat["places"])*100)}%")



if __name__ == "__main__":
    handle_status()