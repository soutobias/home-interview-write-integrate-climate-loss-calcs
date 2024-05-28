""" This module contains the test cases for the losses calculator functions.
"""
import os
import unittest
import json
import pandas as pd

from loss_calc.exercise1_losses_calculator import (
    load_data,
    calculate_projected_losses,
    calculate_complex_projected_losses,
)


class TestLossesCalculator(unittest.TestCase):
    """Test cases for the losses calculator functions.
    """
    def setUp(self):
        self.sample_data = [
            {
                "buildingId": 1,
                "floor_area": 2000,
                "construction_cost": 1200,
                "hazard_probability": 0.1,
                "inflation_rate": 0.03,
            },
            {
                "buildingId": 2,
                "floor_area": 1500,
                "construction_cost": 1300,
                "hazard_probability": 0.2,
                "inflation_rate": 0.04,
            },
            {
                "buildingId": 3,
                "floor_area": 1800,
                "construction_cost": 1400,
                "hazard_probability": 0.15,
                "inflation_rate": 0.02,
            },
            {
                "buildingId": 4,
                "floor_area": 1600,
                "construction_cost": 1500,
                "hazard_probability": 0.05,
                "inflation_rate": 0.05,
            },
            {
                "buildingId": 5,
                "floor_area": 2200,
                "construction_cost": 1100,
                "hazard_probability": 0.12,
                "inflation_rate": 0.03,
            },
        ]
        with open("sample_data.json", "w", encoding="utf-8") as f:
            json.dump(self.sample_data, f)

    def tearDown(self):
        os.remove("sample_data.json")

    # Test load_data
    def test_load_data_valid(self):
        """Test loading data from a valid JSON file.
        """
        df = load_data("sample_data.json")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 5)
        self.assertTrue(
            set(df.columns)
            == set(
                [
                    "construction_cost",
                    "inflation_rate",
                    "hazard_probability",
                    "floor_area",
                ]
            )
        )

    def test_load_data_invalid_file(self):
        """Test loading data from a nonexistent file.
        """
        df = load_data("nonexistent_file.json")
        self.assertIsNone(df)

    def test_calculate_projected_losses(self):
        """Test calculating projected losses.
        """
        df = load_data("sample_data.json")
        result = calculate_projected_losses(df)
        self.assertAlmostEqual(result, 434117.05714285705, places=2)

        result = calculate_projected_losses(df, years=5)
        self.assertNotAlmostEqual(result, 434117.05714285705, places=2)

        result = calculate_projected_losses(
            df, discount_rate=0.10
        )
        self.assertNotAlmostEqual(result, 434117.05714285705, places=2)

        result = calculate_projected_losses(
            df, maintenance_rate=100
        )
        self.assertNotAlmostEqual(result, 434117.05714285705, places=2)

    def test_calculate_complex_projected_losses(self):
        """Test calculating complex projected losses.
        """
        df = load_data("sample_data.json")
        result = calculate_complex_projected_losses(df)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 6)
        self.assertAlmostEqual(
            result["total"], 803.2838782779653, places=2
        )

if __name__ == "__main__":
    unittest.main()
