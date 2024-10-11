import pandas as pd
from .field_list import Field_List
import re

# Initialize a Field_List object
expected_fields = Field_List().expected_fields
int_fields = Field_List().int_fields
date_fields = Field_List().date_fields

def clean_text(text):
    """
    Function to clean text by removing non-ASCII characters, extra spaces, newlines, and other unwanted characters.
    """
    if isinstance(text, str):

        text = re.sub(r'[^\x00-\x7F]+', '', text)
        text = re.sub(r'_', ' ', text)
        text = re.sub(r',$', '', text)
        text = text.replace('*', ' ')
        text = text.replace('-', ' ')
        text = text.replace('-', '')
        text = text.replace('|', ' ')
        text = text.replace('//', ' ')
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        text = text.replace('\n', ' ')
    return text

def clean_currency(value):
    """
    Cleans currency values by removing symbols and formatting, converting to float.

    Parameters:
        value (str): The currency value as a string.

    Returns:
        float: The numeric value or NaN if conversion fails.
    """
    # If value is empty or 'Not Available', return NaN
    if pd.isnull(value) or value == 'Not Available':
        return 'Not Available'
    value = str(value).strip()

    # Remove all non-numeric characters except for decimal separators and negative signs
    value = re.sub(r'[^\d.,-]', '', value)

    pattern = r'\.\d*,'
    match = re.search(pattern, value)
    if match:
      value = value.replace('.','').replace(',','.')
      return value
    return value.replace(',', '')

def clean_data(df):
    # Include your existing code for cleaning data
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(clean_text)

    fields = Field_List()
    for col in fields.cost_related_fields:
        if col in df.columns:
            df[col] = df[col].apply(clean_currency)

    # Remove rows where all columns are empty
    df = df.dropna(how='all')
    df = df.fillna(value='Not Available')
    df = df.drop_duplicates()

    # Reset index after cleaning
    df = df.reset_index(drop=True)

    return df
