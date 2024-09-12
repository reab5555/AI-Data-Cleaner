# Data Cleaning and Preparation Tool
This project focuses on automating the initial steps of data preparation using LLMs to provide smart, context-aware data cleaning. While it can handle the primary cleaning tasks, its mission is to prepare data for more in-depth and complex transformations downstream.

## Features
- **Column Header Normalization**: Auto-corrects and standardizes column headers.
- **Empty Data Removal**: Prunes columns and rows with substantial missing values.
- **Low Count Category Removal**: Cleans categorical columns by eliminating infrequent values.
- **Data Type Enforcement**: Determines and enforces appropriate data types for columns.
- **Typo Detection and Correction**: Spot and fix potential typos in string columns.
- **Outlier Removal**: Identifies and removes outliers from numeric columns.
- **Visualization Reports**: Generates detailed reports to visualize data before and after cleaning.

## Advantages
Using LLMs with prompts over traditional methods like Pandas or Spark offers several benefits:   
1. **Intuitive and Context-Aware**: LLMs understand the context and provide intelligent suggestions.   
2. **Flexible and Adaptive**: Adapts to various data structures and types without hardcoding.   
3. **Reduced Manual Effort**: Automated processes save time and reduce manual interventions.   
4. **Enhanced Error Detection**: Detects and corrects subtle errors and inconsistencies.   
5. **Scalability**: Efficiently handles large datasets by processing data in batches.  

## Steps of Data Cleaning
1. **Normalize Column Headers**: Ensure consistent and valid column names.
2. **Remove Empty Columns**: Drop columns with less than 60% valid data.
3. **Remove Empty Rows**: Drop rows with less than 60% valid data.
4. **Remove Low Count Categories**: Clean categorical columns by removing infrequent values.
5. **Clean Columns**: Process each column in batches and handle non-conforming cells.
6. **Remove Outliers**: Detect and remove outliers from numeric columns.

## Benefits
- **Time-Saving**: Automates repetitive data cleaning tasks.
- **Improved Data Quality**: Ensures data is clean and ready for analysis.
- **Comprehensive Reports**: Visual insights aid better decision-making.
- **Ease of Use**: Simplifies data cleaning, accommodating various user expertise levels.
