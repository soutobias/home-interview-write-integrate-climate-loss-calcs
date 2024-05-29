
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
