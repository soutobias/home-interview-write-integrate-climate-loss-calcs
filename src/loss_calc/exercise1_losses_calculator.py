"""This module calculates the total projected losses for a set of buildings based
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
import argparse
import time

import numpy as np
import pandas as pd

# Load and parse the JSON data file
def load_data(filepath):
    """Load and parse the JSON data file

    Args:
        filepath (str): Path to the JSON file

    Raises:
        ValueError: Error loading JSON file
        TypeError: Error on data type

    Returns:
        pd.DataFrame: Parsed data
    """

    try:
        df = pd.read_json(filepath, lines=filepath.endswith(".jsonl"))
    except ValueError as e:
        print(f"Error loading JSON file: {e}")
        return None
    except FileNotFoundError as e:
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
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise TypeError(f"Column '{col}' must contain numeric values")

        for col in ["construction_cost", "floor_area"]:
            if (df[col] < 0).any():
                raise ValueError(f"Column '{col}' cannot contain negative values")

    except ValueError as e:
        print(f"Error parsing data: {e}")
        return None
    except TypeError as e:
        print(f"Error parsing data: {e}")
        return None

    df.set_index("buildingId", inplace=True)
    return df


# Calculate total projected loss with additional complexity and errors
def calculate_projected_losses(
    building_data: pd.DataFrame,
    years: int = 1,
    discount_rate: float = 0.05,
    maintenance_rate: float = 50,
) -> float:
    """Calculate the total projected losses

    Args:
        building_data (pd.DataFrame): building data
        years (int, optional): Number of years to perform the calculation. Defaults to 1.
        discount_rate (float, optional): Discount rate. Defaults to 0.05.
        maintenance_rate (float, optional): Maintenance rate. Defaults to 50.

    Returns:
        float: Total projected losses
    """

    # Calculate future cost
    future_cost = (
        building_data["construction_cost"]
        * (1 + building_data["inflation_rate"]) ** years
    )

    # Calculate risk-adjusted loss
    risk_adjusted_loss = future_cost * building_data["hazard_probability"]

    # Calculate present value of the risk-adjusted loss
    present_value_loss = risk_adjusted_loss / (1 + discount_rate)

    # Calculate maintenance and total maintenance cost
    maintenance_cost = building_data["floor_area"] * maintenance_rate
    total_maintenance_cost = maintenance_cost / (1 + discount_rate)

    # Total loss calculation
    total_loss = present_value_loss.sum() + total_maintenance_cost.sum()

    return total_loss


# Calculate total projected loss with additional complexity and errors
def calculate_complex_projected_losses(
    building_data: pd.DataFrame, years: int = 1, discount_rate: float = 0.05
) -> float:
    """Calculate the total projected losses with additional complexity and errors.

    Args:
        building_data (list): building data
        years (int, optional): Number of years to perform the calculation. Defaults to 1.
        discount_rate (float, optional): Discount rate. Defaults to 0.05.

    Returns:
        float: Total projected losses with additional complexity and errors
    """
    building_data["potential_finantial_losses"] = (
        building_data["construction_cost"]
        * np.exp(building_data["inflation_rate"] * building_data["floor_area"] / 1000)
        * building_data["hazard_probability"]
        / (1 + discount_rate) ** years
    )
    potential_finantial_losses = building_data.potential_finantial_losses.to_dict()
    potential_finantial_losses["total"] = building_data.potential_finantial_losses.sum()
    return potential_finantial_losses


# Main execution function
def main():
    """Main function for the losses calculator."""
    parser = argparse.ArgumentParser(description="Calculate projected losses.")
    parser.add_argument("data_file", help="Path to the JSON data file")
    parser.add_argument(
        "--years",
        type=int,
        default=1,
        help="Number of years for projection (default: 1)",
    )
    parser.add_argument(
        "--discount_rate",
        type=float,
        default=0.05,
        help="Discount rate (default: 0.05)",
    )
    parser.add_argument(
        "--maintenance_rate",
        type=float,
        default=50,
        help="Maintenance rate (default: 50)",
    )
    args = parser.parse_args()

    start_time = time.time()

    data = load_data(args.data_file)

    total_projected_loss = calculate_projected_losses(
        data, args.years, args.discount_rate, args.maintenance_rate
    )
    complex_total_projected_loss = calculate_complex_projected_losses(
        data, args.years, args.discount_rate
    )

    print(f"Total Projected Loss: ${total_projected_loss:.2f}")
    print(f"Total Complex Projected Loss: ${complex_total_projected_loss['total']:.2f}")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")


if __name__ == "__main__":
    main()
