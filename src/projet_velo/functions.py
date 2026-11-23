import yaml
import sys
from pathlib import Path

def load_config():
    try:
        with open(Path.home()/".config"/"velo"/"config.yaml") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        sys.exit("File not found")