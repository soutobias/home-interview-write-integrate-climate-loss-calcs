
""" Work in progress
"""
import argparse
import time
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# schema = T.StructType(
#     [
#         T.StructField("buildingId", T.IntegerType(), True),
#         T.StructField("construction_cost", T.FloatType(), True),
#         T.StructField("inflation_rate", T.FloatType(), True),
#         T.StructField("hazard_probability", T.FloatType(), True),
#         T.StructField("floor_area", T.FloatType(), True),
#     ]
# )


def load_data(filepath):
    spark = SparkSession.builder.getOrCreate()
    df = spark.read.json(filepath)
    # df = spark.read.schema(schema).option("mode", "PERMISSIVE").json(filepath)

    return df


def calculate_projected_losses(
    building_data, years=1, discount_rate=0.05, maintenance_rate=50
):
    """Calculate the total projected losses using Spark DataFrame operations"""

    future_cost = building_data["construction_cost"] * (
        (1 + building_data["inflation_rate"]) ** years
    )
    risk_adjusted_loss = future_cost * building_data["hazard_probability"]
    present_value_loss = risk_adjusted_loss / (1 + discount_rate)
    maintenance_cost = building_data["floor_area"] * maintenance_rate
    total_maintenance_cost = maintenance_cost / (1 + discount_rate)

    total_loss_column = present_value_loss + total_maintenance_cost

    total_loss = building_data.agg(
        F.sum(total_loss_column).alias("total_loss")
    ).first()["total_loss"]

    return total_loss


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
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")


if __name__ == "__main__":
    main()
