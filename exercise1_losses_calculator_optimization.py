""" This module calculates the total projected losses for a set of buildings based
on their construction cost, inflation rate, hazard probability, and floor area.
The total projected losses are calculated as the sum of the present value of the
risk-adjusted loss and the present value of the maintenance cost for each building.

The module provides two functions:
- load_data(filepath): Load and parse the JSON data file containing building data.
- calculate_projected_losses(building_data, years, discount_rate, maintenance_rate):
    Calculate the total projected losses for a set of buildings.
- calculate_complex_projected_losses(building_data, years, discount_rate):
    Calculate the total projected losses with additional complexity and errors.
"""

import numpy as np
import pandas as pd
import dask.dataframe as dd
import json

# Generate building data
def generate_building_data(num_records, output_filename="generated_data.json"):
    """Generate building data

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
    with open(output_filename, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def load_data(filepath):
    """Load and parse the JSON data file

    Args:
        filepath (str): Path to the JSON file

    Raises:
        ValueError: Error loading JSON file
        TypeError: Error on data type

    Returns:
        dd.DataFrame: Parsed data
    """

    try:
        df = pd.read_json(filepath)
        ddf = dd.from_pandas(df, chunksize=1_000_000)
        # ddf = dd.from_pandas(df, npartitions=4)
        # ddf = dd.read_json(filepath, orient="records", lines=False, blocksize=None)
        # ddf = ddf.repartition(npartitions=8)
        # ddf = dd.read_json(filepath,
        #                    blocksize=None,
        #                    orient="records",
        #                    lines=False)
    except ValueError as e:
        print(f"Error loading JSON file: {e}")
        return None

    try:
        required_columns = [
            "construction_cost",
            "inflation_rate",
            "hazard_probability",
            "floor_area",
        ]
        for col in required_columns:
            if col not in ddf.columns:
                raise ValueError(f"Missing required column: {col}")
            # if not pd.api.types.is_numeric_dtype(ddf[col]):
            #     raise TypeError(f"Column '{col}' must contain numeric values")

    except ValueError as e:
        print(f"Error parsing data: {e}")
        return None
    except TypeError as e:
        print(f"Error parsing data: {e}")
        return None

    ddf = ddf.set_index("buildingId")
    return ddf

# Calculate total projected loss with additional complexity and errors
def calculate_projected_losses(
    building_data: dd.DataFrame,
    years: int = 1,
    discount_rate: float = 0.05,
    maintenance_rate: float = 50,
) -> float:
    """Calculate the total projected losses

    Args:
        building_data (dd.DataFrame): building data
        years (int, optional): Number of years to perform the calculation. Defaults to 1.
        discount_rate (float, optional): Discount rate. Defaults to 0.05.
        maintenance_rate (float, optional): Maintenance rate. Defaults to 50.

    Returns:
        float: Total projected losses
    """

    future_cost = building_data["construction_cost"] * (
        (1 + building_data["inflation_rate"]) ** years
    )
    risk_adjusted_loss = future_cost * building_data["hazard_probability"]
    present_value_loss = risk_adjusted_loss / (1 + discount_rate)
    maintenance_cost = building_data["floor_area"] * maintenance_rate
    total_maintenance_cost = maintenance_cost / (1 + discount_rate)

    total_loss = (present_value_loss + total_maintenance_cost).sum().compute()
    return total_loss

# Calculate total projected loss with additional complexity and errors
def calculate_complex_projected_losses(
    building_data: dd.DataFrame, years: int = 1, discount_rate: float = 0.05
) -> float:
    """Calculate the total projected losses with additional complexity and errors.

    Args:
        building_data (list): building data
        years (int, optional): Number of years to perform the calculation. Defaults to 1.
        discount_rate (float, optional): Discount rate. Defaults to 0.05.

    Returns:
        float: Total projected losses with additional complexity and errors
    """
    potential_finantial_losses = (
        building_data["construction_cost"]
        * np.exp(building_data["inflation_rate"] * building_data["floor_area"] / 1000)
        * building_data["hazard_probability"]
        / (1 + discount_rate) ** years
    )

    # Compute the total loss and convert the result to a dictionary
    total_loss = potential_finantial_losses.sum().compute()
    potential_finantial_losses = potential_finantial_losses.compute().to_dict()
    potential_finantial_losses["total"] = total_loss

    # total_loss_series = dd.from_pandas(
    #     pd.Series({'total': building_data['potential_finantial_losses'].sum()}), npartitions=1
    # )
    # result_series = dd.concat([building_data['potential_finantial_losses'], total_loss_series])

    return potential_finantial_losses

# Main execution function
def main():
    """Main function to execute the program."""
    data = load_data("data.json")
    years = 1
    total_projected_loss = calculate_projected_losses(data, years)
    complex_total_projected_loss = calculate_complex_projected_losses(data, years)
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")
    print(f"Complex Total Projected Loss: ${complex_total_projected_loss:.2f}")


if __name__ == "__main__":
    main()
