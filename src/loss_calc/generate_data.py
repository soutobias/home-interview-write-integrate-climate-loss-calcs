"""Generate building data as json or jsonl"""

import json
import numpy as np

# Generate building data
def generate_json(num_records, output_filename="generated_data.json"):
    """Generate building data as json

    Args:
        num_records (int): Number of records to generate
        output_filename (str, optional): Output filename. Defaults to "generated_data.json".
    """
    data = []
    for building_id in range(1, num_records + 1):
        record = {
            "buildingId": building_id,
            "floor_area": np.random.randint(500, 5001),
            "construction_cost": np.random.randint(500, 5001),
            "hazard_probability": round(np.random.randint(1, 21) / 100, 2),
            "inflation_rate": round(np.random.randint(1, 6) / 100, 2),
        }
        data.append(record)
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Generate building data
def generate_jsonl(num_records, output_filename="generated_data.jsonl"):
    """Generate building data as jsonl

    Args:
        num_records (int): Number of records to generate
        output_filename (str, optional): Output filename. Defaults to "generated_data.jsonl".
    """
    with open(output_filename, "w", encoding="utf-8") as f:
        for building_id in range(1, num_records + 1):
            record = {
                "buildingId": building_id,
                "floor_area": np.random.randint(500, 5001),
                "construction_cost": np.random.randint(500, 5001),
                "hazard_probability": round(np.random.randint(1, 21) / 100, 2),
                "inflation_rate": round(np.random.randint(1, 6) / 100, 2),
            }
            f.write(json.dumps(record) + "\n")
