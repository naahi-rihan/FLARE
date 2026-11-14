import json
from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "investigations.json"

def load_investigations(path=DATA_PATH):
    with open(path, "r", encoding="utf-8") as f:
        records = json.load(f)
    return pd.DataFrame(records)
