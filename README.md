# Senior Full Stack Engineer Assessment

## Overview
The assessment for Section 2 involves correcting, enhancing, and developing Python scripts to calculate projected financial losses for buildings based on provided data about climate hazards. You are expected to complete Exercises 1, 2, and 3 at home. Exercise 4 is a live interview task.

## Technical Setup and Interview Process

### Pre-Interview Setup
1. **Slack Channel Invitation**: You will receive an invitation via email to join our interview Slack channel, sent to the email address provided to your Climate X recruiter. Please follow the link in this email to join the channel. This channel will serve as the primary mode of communication throughout the assignment process and will be used to distribute materials for the live interview assessment.
2. **Submission Instructions**: After completing Section 1 and Section 2 (Exercises 1-3), please submit your work in the Slack channel. You can provide either links to your work or directly upload the submissions in the requested format. Ensure that this is done prior to your interview date. Your interviewers will confirm receipt of your submissions.

### Live Interview Setup
3. **Interview Day Provision**: On the day of your interview, a laptop and a private room will be made available to you. All necessary libraries and packages required for the task will be pre-installed on the laptop. You will have 30 minutes to complete Exercise 4 during the live interview. After completion, you will present your working code to the interviewers.

## Exercise 1: Correcting and Enhancing the Loss Calculation Script

### Task Description
You are provided with a Python script and a JSON file (`data.json`) containing data for five buildings. This script is designed to calculate total projected financial losses, taking into account factors such as inflation over time, the probability of hazard occurrence, and the process of discounting future losses to their present value.

### Requirements
- **Future Cost Calculation**: Adjust each building's construction cost by applying an exponential growth rate to reflect inflation over time.
- **Risk-Adjusted Loss Calculation**: Modify the future construction cost with the likelihood of experiencing a hazard by multiplying it by the hazard probability.
- **Discounting to Present Value**: Apply a discounting process to calculate the present value of the estimated future losses using a standard discount rate.
- **Total Projected Loss Calculation**: Sum the present values of the estimated losses from all buildings to determine the total financial impact.

### Data Structure
Each entry in the `data.json` file includes:
- `buildingId`: Identifier for the building
- `floor_area`: Floor area in square meters
- `construction_cost`: Construction cost per square meter
- `hazard_probability`: Likelihood of experiencing a climate-related hazard
- `inflation_rate`: Annual inflation rate applicable to the construction cost

### Instructions
- Review and correct any errors in the provided Python script.
- Ensure the script accurately implements the calculations as described.
- Output the total projected financial loss after running the script.

## Exercise 2: Implementing a Complex Mathematical Loss Formula

### Task Description
Implement a complex mathematical formula in Python to calculate potential financial losses using detailed attributes of the same five buildings.

### Complex Loss Calculation Formula
$$
LE = \left( \text{Construction Cost} \times e^{(\text{Inflation Rate} \times \text{Floor Area} / 1000)} \times \text{Hazard Probability} \right) / \left(1 + \text{Standard Discount Rate}\right)^{\text{Number of Years}}
$$

### Expected Output
The script should output the individual and total estimated losses for all properties.

### Instructions
- Decompose and implement the specified complex loss estimation formula using data from `data.json`.
- Ensure the output is accurate and reflective of the calculated losses.

## Exercise 3: Scaling the Loss Calculation Model

### Task Description
Provide a written explanation of how you would scale the Python script to efficiently handle a dataset of 1,000,000 buildings.

### Requirements
- **Scalability Analysis**: Evaluate the current script's performance with a larger dataset.
- **Optimization Strategies**: Suggest improvements for script efficiency and scalability.
- **Resource Management**: Discuss how to effectively manage memory and processing power for large datasets.
- **Example Code**: Optionally, include Python code snippets that showcase your scalability solutions.

### Expected Submission
- **Written Explanation**: Detail your strategy for scaling the script, including recommended technologies or methods and their effectiveness.
- **Code Snippets**: Optionally, provide code examples to support your explanations.

## Exercise 4: Live Interview Frontend Development

### Task Description
Develop a small frontend application during the live interview that interfaces with the backend to upload `data.json`, calculate losses, and display the results.

### Requirements
- **User Interface**: Implement functionalities for file uploading, processing through a 'Calculate Losses' button, and result display.
- **Functionality**: Ensure the application handles data upload, interacts with the backend, and displays the losses accurately.

### Instructions
- Use the provided boilerplate code to set up the basic functionalities.
- Focus on creating a user-friendly and effective interface.
- Be prepared to discuss your implementation and design choices during the interview.

## Submission Guidelines
- Complete Exercises 1, 2, and 3 at home and submit them before the interview.
- Exercise 4 will be conducted live. Familiarize yourself with the necessary technologies and prepare for live coding.
- Document any assumptions or important decisions in your approach.
