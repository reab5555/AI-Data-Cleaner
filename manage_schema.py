import pandas as pd
import numpy as np
import json
from llm_config import generate_llm_response
from llm_prompts import DETERMINE_DTYPE_PROMPT

SAMPLE_SIZE = 200


def determine_column_type(df, column):
    sample = df[column].sample(n=min(SAMPLE_SIZE, len(df)), random_state=42).tolist()
    prompt = DETERMINE_DTYPE_PROMPT.format(sample_values=str(sample))
    response = generate_llm_response(prompt)

    try:
        result = json.loads(response)
        return result['column_type'], result['invalid_indices']
    except (json.JSONDecodeError, KeyError):
        print(f"Error parsing LLM response for column {column}")
        return 'string', []


def enforce_column_type(df, column, column_type, invalid_indices):
    if column_type == 'float':
        df[column] = pd.to_numeric(df[column], errors='coerce')
    elif column_type == 'integer':
        df[column] = pd.to_numeric(df[column], errors='coerce').astype('Int64')
    elif column_type == 'date':
        df[column] = pd.to_datetime(df[column], errors='coerce')

    # Set invalid values to NaN
    df.loc[invalid_indices, column] = np.nan

    return df


def process_dataframe(df):
    print("Determining and enforcing column data types...")

    for column in df.columns:
        print(f"\nProcessing column: {column}")
        column_type, invalid_indices = determine_column_type(df, column)
        print(f"  Detected type: {column_type}")
        print(f"  Number of invalid values: {len(invalid_indices)}")

        df = enforce_column_type(df, column, column_type, invalid_indices)

        valid_percentage = (df[column].count() / len(df)) * 100
        print(f"  Percentage of valid values after type enforcement: {valid_percentage:.2f}%")

    return df
