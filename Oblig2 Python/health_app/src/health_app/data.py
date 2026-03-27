import json
import os
from collections import Counter
from health_app.health import Health

DEFAULT_FILE = "health_records.json"


def save_all_records(records: list[Health], filename: str = DEFAULT_FILE):
    """Saves a list of Health objects to a JSON file with indent=2."""
    data_to_save = [
        {
            "name": r.name,
            "weight_kg": r.weight_kg,
            "height_m": r.height_m,
            "calculated_bmi": r.calculate_bmi(),
        }
        for r in records
    ]

    with open(filename, "w") as f:
        json.dump(data_to_save, f, indent=2)


def load_records(filename: str = DEFAULT_FILE) -> list[Health]:
    """Loads records and converts them back into Health objects."""
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return [
                Health(item["name"], item["weight_kg"], item["height_m"])
                for item in data
            ]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_statistics(filename: str = DEFAULT_FILE) -> dict:
    """Returns a dictionary of detailed BMI statistics."""
    records = load_records(filename)

    if not records:
        return {
            "total_records": 0,
            "avg_bmi": 0.0,
            "most_common_category": "None",
            "category_distribution": {},
        }

    bmis = [r.calculate_bmi() for r in records]
    categories = [r.get_category() for r in records]

    # Calculate distribution and most common
    dist = dict(Counter(categories))
    most_common = max(dist, key=dist.get) if dist else "None"

    return {
        "total_records": len(records),
        "avg_bmi": round(sum(bmis) / len(bmis), 2),
        "most_common_category": most_common,
        "category_distribution": dist,
    }
