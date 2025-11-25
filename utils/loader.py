import os
import json
import pandas as pd

def load_items_obsolete(path=os.path.join(os.getcwd(), 'utils', 'recycle_items.txt')):
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines

def load_items():
    base_dir = os.path.dirname(__file__)
    path = os.path.join(base_dir, "data.json")
    if not os.path.exists(path):
        return []

    df = pd.read_json(path)
    df = pd.json_normalize(df['ArcRaiderItems'])
    return df

if __name__ == "__main__":
    df = load_items()
    print(df)