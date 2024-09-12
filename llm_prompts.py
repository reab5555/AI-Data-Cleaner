CHECK_HEADERS_PROMPT = """
Analyze the following DataFrame columns and identify any columns without names or with invalid names. 
Return only a JSON list of column indices (0-based) that need attention, without any explanation.
Columns: {columns}
"""

NORMALIZE_HEADERS_PROMPT = """
Analyze the following DataFrame column names and normalize them according to these rules:
1. Convert to lowercase
2. Replace empty strings or spaces with underscores
3. Remove any invalid characters (keep only letters, numbers, and underscores)

Return only a JSON object where keys are the original column names and values are the normalized names, without any explanation.
Column names: {columns}
"""

CHECK_COLUMN_CONTENT_PROMPT = """
Analyze the following sample of values from the column '{column_name}' and determine:
1. The most appropriate data type (float, integer, string, or date)
2. Indices of empty or blank values
3. Indices of values that don't conform to the determined data type

Sample values:
{sample_values}

Return only a JSON object with the following structure, without any explanation:
{{
    "data_type": "detected_type",
    "empty_indices": [list of indices of empty or blank values],
    "invalid_indices": [list of indices of values that don't conform to the detected type]
}}
"""

CHECK_TYPOS_PROMPT = """
Analyze the following sample of values from the column '{column_name}' and identify any potential typos or misspellings.
For each identified typo, suggest a correction.

Sample values:
{sample_values}

Return only a JSON object with the following structure, without any explanation:
{{
    "typos": {{
        "original_value1": "corrected_value1",
        "original_value2": "corrected_value2",
        ...
    }}
}}

If no typos are found, return an empty object for "typos".
"""

ENCODE_STRING_PROMPT = """
Analyze the following unique values from the column '{column_name}' and create an encoding scheme.
Assign a unique integer to each unique string value, starting from 0.

Unique values:
{unique_values}

Return only a JSON object with the following structure, without any explanation:
{{
    "string_value1": 0,
    "string_value2": 1,
    "string_value3": 2,
    ...
}}

Ensure that each unique string value is assigned a unique integer.
"""

DETERMINE_DTYPE_PROMPT = """
Analyze the following sample values from a column and determine the most appropriate data type.
Possible types are: float, integer, string, or date.
If more than 80% of the values conform to a specific type, choose that type.
Otherwise, default to string.

Sample values:
{sample_values}

Return only a JSON object with the following structure, without any explanation:
{{
    "column_type": "detected_type",
    "invalid_indices": [list of indices that do not conform to the detected type]
}}
"""

TRANSFORM_STRING_PROMPT = """
Transform the following unique string values from the column '{column_name}' to lowercase.
If a value is a variation of "nan" (case-insensitive), map it to "nan".

Unique values:
{unique_values}

Return only a JSON object with the following structure, without any explanation:
{{
    "original_value1": "transformed_value1",
    "original_value2": "transformed_value2",
    ...
}}
"""

CHECK_LOW_COUNT_VALUES_PROMPT = """
Analyze the following value counts from the column '{column_name}' and identify values with a count lower than 2.

Value counts:
{value_counts}

Return only a JSON list of values that have a count lower than 2, without any explanation.
"""


CHECK_SCHEMA_CONFORMITY_PROMPT = """
Analyze the following sample of values from the column '{column_name}' and check if they conform to the determined data type '{data_type}'.

Sample values:
{sample_values}

Return only a JSON object with the following structure, without any explanation:
{{
    "conforming_indices": [list of indices of values that conform to the data type],
    "nonconforming_indices": [list of indices of values that do not conform to the data type]
}}
"""