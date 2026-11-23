from .functions import load_config
from pathlib import Path

config_file = load_config()
data_path = Path(config_file["data"]["folder"])

