from pathlib import Path
import yaml 
import requests 
import os

def handle_init(args):
    config_file = Path.home()/".config"/"velo"/"config.yaml"
    data_file = Path.home()/".local"/"share"/"velo"
    url  = "https://media.ilevia.fr/opendata/gbfs.json"
    
    if not os.path.isfile(config_file) or args.force:
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