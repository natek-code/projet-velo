from pathlib import Path
import yaml 
import requests 
import os, json

def handle_init(args):
    config_file = Path.home()/".config"/"velo"/"config.yaml"
    data_file = Path.home()/".local"/"share"/"velo"
    url  = "https://media.ilevia.fr/opendata/gbfs.json"
    
    if not ( os.path.isfile(config_file) and os.path.isdir(data_file) ) or args.force:
        config_file.parent.mkdir(parents=True, exist_ok=True)
        data_file.mkdir(parents=True, exist_ok=True)

        config_dict = {
            "network": {"name":"V'Lille", "gbfs_url": "https://media.ilevia.fr/opendata/gbfs.json"}, 
            "data": {"folder": Path.home()/".local"/"share"/"velo"}, 
            "refresh": {"max_age_days": 7 }, # au - del à : avertissement
            "collect":{"interval_seconds": 120}, # minimum 60
            "alerts": { 
                "low_bikes":2,  # 2 vélos ou moins : presque vide
                "low_docks":2  # 2 places ou moins : presque pleine
                }, 
            "dashboard":{
                "refresh_seconds": 60 # minimum 60
                } , 
            "logging":{
                "level": "INFO"
            }

        }
        
        with open(config_file, "w") as f:
            yaml.dump(config_dict, f)
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

            print(f"Configuration créée : {str(Path.home())}/.config/velo/config.yaml")
            print(f"Dossier de données créé : {str(Path.home())}/.local/share/velo/")
            print(f"Connexion à V’Lille : OK  {nb_station} station")
        except ConnectionError: 
            print("Erreur de connexion avec V'lille")
            print(f"Configuration créée : {str(Path.home())}/.config/velo/config.yaml")
            print(f"Dossier de données créé : {str(Path.home())}/.local/share/velo/")
            
    else: 
        print("Config déja existante")
    
           

            

            
            
