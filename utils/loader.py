import os
def load_items(path=os.path.join(os.getcwd(), 'utils', 'recycle_items.txt')):
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines