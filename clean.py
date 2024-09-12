import pandas as pd
import numpy as np
import json
import time
from tqdm import tqdm
from llm_config import generate_llm_response
from llm_prompts import (
    CHECK_HEADERS_PROMPT,
    NORMALIZE_HEADERS_PROMPT,
    CHECK_COLUMN_CONTENT_PROMPT,
    CHECK_TYPOS_PROMPT,
    TRANSFORM_STRING_PROMPT,
    CHECK_LOW_COUNT_VALUES_PROMPT
)

BATCH_SIZE = 50
EMPTY_THRESHOLD = 0.5


def print_dataframe_info(df, step=""):
    num_columns = df.shape[1]
    num_rows = df.shape[0]
    num_cells = num_columns * num_rows
    print(f"{step}Dataframe info:")
    print(f"  Number of columns: {num_columns}")
    print(f"  Number of rows: {num_rows}")
    print(f"  Total number of cells: {num_cells}")


def check_and_normalize_column_headers(df):
    print("Checking and normalizing column headers...")

    check_prompt = CHECK_HEADERS_PROMPT.format(columns=df.columns.tolist())
    check_response = generate_llm_response(check_prompt)
    try:
        invalid_columns = json.loads(check_response)
        if invalid_columns:
            print(f"Columns with invalid names (indices): {invalid_columns}")
            for idx in invalid_columns:
                new_name = f"column_{idx}"
                print(f"Renaming column at index {idx} to '{new_name}'")
                df.rename(columns={df.columns[idx]: new_name}, inplace=True)
        else:
            print("All column headers are valid or no invalid headers detected.")
    except json.JSONDecodeError:
        print("Error parsing LLM response for column headers check.")

    normalize_prompt = NORMALIZE_HEADERS_PROMPT.format(columns=df.columns.tolist())
    normalize_response = generate_llm_response(normalize_prompt)
    try:
        normalized_names = json.loads(normalize_response)
        if normalized_names:
            df.rename(columns=normalized_names, inplace=True)
            print("Column names have been normalized.")
        else:
            print("No column names were normalized. Proceeding with current names.")
    except json.JSONDecodeError:
        print("Error parsing LLM response for column name normalization.")

    # Fallback normalization
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    print("Applied fallback normalization to ensure valid column names.")

    return df


def process_column_batch(column_data, column_name):
    sample = column_data.sample(n=min(BATCH_SIZE, len(column_data)), random_state=42).tolist()
    prompt = CHECK_COLUMN_CONTENT_PROMPT.format(column_name=column_name, sample_values=str(sample))
    response = generate_llm_response(prompt)
    try:
        result = json.loads(response)
        if not all(key in result for key in ['data_type', 'empty_indices', 'invalid_indices']):
            raise ValueError("Missing required keys in LLM response")
        return result
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing LLM response for column {column_name}: {str(e)}")
        print(f"LLM Response: {response}")
        return {'data_type': 'string', 'empty_indices': [], 'invalid_indices': []}


def check_typos(column_data, column_name):
    sample = column_data.sample(n=min(BATCH_SIZE, len(column_data)), random_state=42).tolist()
    prompt = CHECK_TYPOS_PROMPT.format(column_name=column_name, sample_values=str(sample))
    response = generate_llm_response(prompt)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        print(f"Error parsing LLM response for typo check in column {column_name}")
        return {"typos": {}}


def transform_string_column(column_data, column_name):
    unique_values = column_data.unique().tolist()
    prompt = TRANSFORM_STRING_PROMPT.format(column_name=column_name, unique_values=unique_values)
    response = generate_llm_response(prompt)
    try:
        result = json.loads(response)
        return result
    except json.JSONDecodeError:
        print(f"Error parsing LLM response for string transformation in column {column_name}")
        return {}


def check_low_count_values(column_data, column_name):
    value_counts = column_data.value_counts().to_dict()
    prompt = CHECK_LOW_COUNT_VALUES_PROMPT.format(column_name=column_name, value_counts=value_counts)
    response = generate_llm_response(prompt)
    try:
        result = json.loads(response)
        return result
    except json.JSONDecodeError:
        print(f"Error parsing LLM response for low count values in column {column_name}")
        return []


def remove_empty_columns(df, threshold=EMPTY_THRESHOLD):
    print(f"Removing columns with less than {threshold * 100}% valid data...")
    valid_threshold = int(df.shape[0] * threshold)
    df = df.dropna(axis=1, thresh=valid_threshold)
    return df


def remove_empty_rows(df, threshold=EMPTY_THRESHOLD):
    print(f"Removing rows with less than {threshold * 100}% valid data...")
    valid_threshold = int(df.shape[1] * threshold)
    df = df.dropna(axis=0, thresh=valid_threshold)
    return df


def remove_low_count_categories(df):
    print("Removing strings with count below 2...")
    for col in df.select_dtypes(include=['object']).columns:
        value_counts = df[col].value_counts()
        to_remove = value_counts[value_counts < 2].index
        df[col] = df[col].replace(to_remove, np.nan)
    return df


def clean_column(df, column_name):
    print(f"Cleaning column: {column_name}")
    column_data = df[column_name]
    total_rows = len(column_data)
    empty_indices = []
    invalid_indices = []
    data_type = "string"
    nonconforming_cells = 0

    for i in range(0, total_rows, BATCH_SIZE):
        batch = column_data.iloc[i:i + BATCH_SIZE]
        result = process_column_batch(batch, column_name)

        valid_empty_indices = [idx for idx in result["empty_indices"] if idx + i < total_rows]
        valid_invalid_indices = [idx for idx in result["invalid_indices"] if idx + i < total_rows]

        empty_indices.extend([idx + i for idx in valid_empty_indices])
        invalid_indices.extend([idx + i for idx in valid_invalid_indices])

        if i == 0:  # Use the data type from the first batch
            data_type = result["data_type"]

    print(f"  Data type determined: {data_type}")
    print(f"  Empty cells: {len(empty_indices)}")
    print(f"  Invalid cells: {len(invalid_indices)}")

    # Convert column to determined data type
    if data_type == "float":
        df.loc[:, column_name] = pd.to_numeric(df[column_name], errors='coerce')
    elif data_type == "integer":
        df.loc[:, column_name] = pd.to_numeric(df[column_name], errors='coerce').astype('Int64')
    elif data_type == "date":
        df[column_name] = pd.to_datetime(df[column_name], errors='coerce')
    elif data_type == "string" or data_type == "object":
        # Transform string values
        transform_result = transform_string_column(column_data, column_name)
        df[column_name] = df[column_name].map(transform_result).fillna(df[column_name])

        # Handle "nan" strings
        df[column_name] = df[column_name].replace({"nan": np.nan, "NaN": np.nan, "NAN": np.nan})

        # Check for low count values
        low_count_values = check_low_count_values(df[column_name], column_name)
        df.loc[df[column_name].isin(low_count_values), column_name] = np.nan

        # Check for typos
        typo_result = check_typos(df[column_name], column_name)
        if typo_result["typos"]:
            print(f"  Potential typos found: {typo_result['typos']}")

    # Set empty and invalid cells to NaN
    df.loc[empty_indices + invalid_indices, column_name] = np.nan
    nonconforming_cells = len(empty_indices) + len(invalid_indices)

    return df, nonconforming_cells


def remove_outliers(df):
    print("Removing rows with outliers from numeric/integer/float columns...")
    rows_to_remove = set()
    for column in df.select_dtypes(include=[np.number]).columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier_rows = df[(df[column] < lower_bound) | (df[column] > upper_bound)].index
        rows_to_remove.update(outlier_rows)

    initial_rows = len(df)
    df = df.drop(index=list(rows_to_remove))
    removed_rows = initial_rows - len(df)
    print(f"Removed {removed_rows} rows containing outliers.")
    return df, removed_rows


def calculate_nonconforming_cells(df):
    nonconforming_cells = {}
    for column in df.columns:
        # Count NaN values
        nan_count = df[column].isna().sum()

        # For numeric columns, count infinite values
        if np.issubdtype(df[column].dtype, np.number):
            inf_count = np.isinf(df[column]).sum()
        else:
            inf_count = 0

        # For object columns, count empty strings
        if df[column].dtype == 'object':
            empty_string_count = (df[column] == '').sum()
        else:
            empty_string_count = 0

        nonconforming_cells[column] = nan_count + inf_count + empty_string_count

    return nonconforming_cells


def clean_data(df):
    start_time = time.time()
    process_times = {}
    removed_rows = 0
    removed_columns = 0

    print("Starting data validation and cleaning...")
    print_dataframe_info(df, "Initial - ")

    # Calculate nonconforming cells before cleaning
    nonconforming_cells_before = calculate_nonconforming_cells(df)

    steps = ['Normalize headers', 'Remove empty columns', 'Remove empty rows', 'Remove low count strings', 'Clean columns', 'Remove outliers']
    total_steps = len(steps) + len(df.columns)  # Add column count for individual column cleaning

    # Step 1: Normalize column headers
    step_start_time = time.time()
    df = check_and_normalize_column_headers(df)
    process_times['Normalize headers'] = time.time() - step_start_time
    yield 1 / total_steps, "Normalized headers"

    # Step 2: Remove empty columns (less than 60% valid data)
    step_start_time = time.time()
    df = remove_empty_columns(df)
    process_times['Remove empty columns'] = time.time() - step_start_time
    yield 2 / total_steps, "Removed empty columns"

    # Step 3: Remove empty rows (less than 60% valid data)
    step_start_time = time.time()
    df = remove_empty_rows(df)
    process_times['Remove empty rows'] = time.time() - step_start_time
    yield 3 / total_steps, "Removed empty rows"

    # Step 4: Remove low count categories
    step_start_time = time.time()
    df = remove_low_count_categories(df)
    process_times['Remove low count strings'] = time.time() - step_start_time
    yield 4 / total_steps, "Removed low count strings"

    # Step 5: Clean columns (in batches)
    column_cleaning_times = {}
    for i, column in enumerate(df.columns):
        column_start_time = time.time()
        df, nonconforming = clean_column(df, column)
        column_cleaning_times[f"Clean column: {column}"] = time.time() - column_start_time
        yield (5 + i) / total_steps, f"Cleaning column: {column}"
    process_times.update(column_cleaning_times)

    # Step 6: Remove outliers from numeric columns
    step_start_time = time.time()
    df, outlier_rows_removed = remove_outliers(df)
    removed_rows += outlier_rows_removed
    process_times['Remove outliers'] = time.time() - step_start_time
    yield 1.0, (df, nonconforming_cells_before, process_times, removed_columns, removed_rows)

    print("Cleaning process completed.")
    print_dataframe_info(df, "Final - ")
