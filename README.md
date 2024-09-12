# Data Cleaning and Preparation Tool
This AI-powered tool is designed to streamline the initial stages of data preprocessing, making datasets ready for further, more complex transformations. This tool leverages the power of Large Language Model (LLM) with tailored prompts to provide a more intuitive and efficient cleaning process compared to traditional methods.

## Features
- **Column Header Normalization**: Automatically checks and normalizes column headers to ensure they are valid identifiers.
- **Empty Data Removal**: Removes columns and rows with a significant amount of missing data.
- **Low Count Category Removal**: Cleans categorical columns by removing infrequent values.
- **Data Type Enforcement**: Determines and enforces appropriate data types for each column.
- **Typo Detection and Correction**: Identifies and corrects potential typos in string columns.
- **Outlier Removal**: Detects and removes outliers from numeric columns.
- **Visualization Reports**: Generates comprehensive reports that visualize the state of the data before and after cleaning.

## Steps of Data Cleaning
1. **Normalize Column Headers**: Check and normalize column headers to follow a consistent naming convention.
2. **Remove Empty Columns**: Drop columns with less than 60% valid data.
3. **Remove Empty Rows**: Drop rows with less than 60% valid data.
4. **Remove Low Count Categories**: Remove infrequent categorical values in string columns.
5. **Clean Columns**: Process each column in batches to identify and handle non-conforming cells.
6. **Remove Outliers**: Detect and remove outliers from numeric columns.

## Advantages of Using LLMs with Prompts
### Compared to Pandas or Spark:
1. **Intuitive and Context-Aware**: It can provide context-aware suggestions for data cleaning, understanding the intent behind the data structure and common issues.
2. **Flexible and Adaptive**: It adapt to various data structures and types, providing flexible solutions without hardcoding rules.
3. **Reduced Manual Effort**: Prompts automate several tedious tasks, reducing the need for manual interventions and custom scripts.
4. **Enhanced Error Detection**: It can identify and correct subtle errors, such as typos and inconsistent categories, which traditional methods might overlook.
5. **Scalability**: The tool can handle large datasets efficiently by processing data in batches, making it suitable for big data applications.

## Benefits
- **Time-Saving**: Automates repetitive and time-consuming data cleaning tasks.
- **Improved Data Quality**: Ensures that the data is clean and well-prepared for further analysis or transformation.
- **Comprehensive Reports**: Provides visual insights into the cleaning process and the state of the data, aiding in better decision-making.
- **Ease of Use**: Simplifies the data cleaning process, making it accessible to users with varying levels of expertise in data science.

## Usage
To use this tool, follow these steps:
1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: Install the required dependencies using `pip install -r requirements.txt`.
3. **Run the Cleaning Script**: Execute the `main.py` script to clean your data and generate a report.
