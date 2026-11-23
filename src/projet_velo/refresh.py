from pathlib import Path 
import requests 
import json

config_file = Path.home()/".config"/"velo"/"config.yaml"
data_file = Path.home()/".local"/"share"/"velo"
url  = "https://media.ilevia.fr/opendata/gbfs.json"

def handle_refresh(args):
    try: 
        data = requests.get(url)
        vlille = data_file/"vlille"
        vlille.mkdir(parents=True, exist_ok=True)

        for i in range(4): 
            files = data.json()["data"]["en"]["feeds"][i]
            url_files = files["url"]
            name_files = files["name"]
            data_files = requests.get(url_files).json()
            match name_files: 
                case "vehicle_types": 
                    with open(vlille/"vehicle_types.json", "w") as f:
                        json.dump(data_files, f)
                case "station_information": 
                    with open(vlille/"station_information.json", "w") as f:
                        json.dump(data_files, f)
                        nb_station = len(data_files["data"]["stations"])
                case "system_information": 
                    with open(vlille/"system_information.json", "w") as f:
                        json.dump(data_files, f)

        print("Données mises à jour")
        print(f"Connexion à V’Lille : OK  {nb_station} station")
    except ConnectionError: 
        print("Erreur de connexion avec V'lille")
    