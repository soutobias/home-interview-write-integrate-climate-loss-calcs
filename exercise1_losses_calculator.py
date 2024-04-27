import json
import math

# Load and parse the JSON data file
def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Calculate total projected loss with additional complexity and errors
def calculate_projected_losses(building_data):
    total_loss = 0
    for building in building_data:
        floor_area = building['floor_area']
        construction_cost = building['construction_cost']
        hazard_probability = building['hazard_probability']
        inflation_rate = building['inflation_rate']

        # Calculate future cost
        future_cost = construction_cost * (1 + inflation_rate)  

        # Calculate risk-adjusted loss
        risk_adjusted_loss = future_cost * (1 - hazard_probability) 

        # Calculate present value of the risk-adjusted loss
        discount_rate = 0.05  # Assuming a 5% discount rate
        present_value_loss = risk_adjusted_loss / (1 + discount_rate)

        # Calculate maintenance and total maintenance cost
        maintenance_cost = floor_area * 50  # assuming a flat rate per square meter
        total_maintenance_cost = maintenance_cost / (1 + discount_rate)  

        # Total loss calculation
        total_loss += present_value_loss + total_maintenance_cost

    return total_loss

# Main execution function
def main():
    data = load_data('data.json')
    total_projected_loss = calculate_projected_losses(data)
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")

if __name__ == '__main__':
    main()