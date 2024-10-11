import pandas as pd
from .field_list import Field_List
import re

def calculate_fields(df):
    # Conversion factors
    km_to_miles = 0.621371
    miles_to_km = 1.60934

    try:

        # Convert fields to numeric, coercing errors to NaN
        df['Yearly_Mileage_Km'] = pd.to_numeric(df['Yearly_Mileage_Km'], errors='coerce')
        df['Yearly_Mileage_Miles'] = pd.to_numeric(df['Yearly_Mileage_Miles'], errors='coerce')
        df['Contract_Duration_Months'] = pd.to_numeric(df['Contract_Duration_Months'], errors='coerce')
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

        # Perform calculations
        if 'Yearly_Mileage_Km' in df.columns and df['Yearly_Mileage_Km'].notnull().any():
            df['Yearly_Mileage_Miles'] = df['Yearly_Mileage_Km'] * km_to_miles

        if 'Yearly_Mileage_Miles' in df.columns and df['Yearly_Mileage_Miles'].notnull().any():
            df['Yearly_Mileage_Km'] = df['Yearly_Mileage_Miles'] * miles_to_km

        if 'Contract_Duration_Months' in df.columns and df['Contract_Duration_Months'].notnull().any():
            if 'Yearly_Mileage_Miles' in df.columns and df['Yearly_Mileage_Miles'].notnull().any():
                df['Total_Contract_Mileage_Miles'] = df['Yearly_Mileage_Miles'] * (df['Contract_Duration_Months'] / 12)
            if 'Yearly_Mileage_Km' in df.columns and df['Yearly_Mileage_Km'].notnull().any():
                df['Total_Contract_Mileage_Km'] = df['Yearly_Mileage_Km'] * (df['Contract_Duration_Months'] / 12)
        return df
    except: 
        return df


# Function to convert values to integer
def safe_convert_to_int(value):
    """Convert value to integer if possible; return None if not."""
    if value is None or value == 'Not Available':
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


# Define the dateFormator function
def dateFormator(date):
    if date is None or date == 'Not Available':
        return None
 
    try:
        pattern = r'\d{2}.\d{2}.\d{4}'
        match = re.search(pattern, date)
        if match:
            date = date.replace('.','-').replace('/','-').replace(' ','-').replace('|','-')
            date = '-'.join(date.split('-')[::-1])
            return date
        else:
            date = date.replace('.','-').replace('/','-').replace(' ','-').replace('|','-')
            return date
    except:
        return date
        
def transform_data(df):
    # Initialize a new DataFrame with expected fields as columns and fill it with 'Not Available'
    fields = Field_List()
    expected_fields = fields.expected_fields
    new_df = pd.DataFrame(columns=expected_fields)

    # Fill the new DataFrame with all the data Fields (153)
    for col in df.columns:
        if col in expected_fields:
            new_df[col] = df[col]

    # Filling empty values with Not Available
    new_df.fillna('Not Available', inplace=True)

    # Convert fields to integer
    for col in new_df.columns:
      if col in fields.date_fields:
          new_df[col] = new_df[col].apply(dateFormator)
          # Convert formatted dates to datetime objects
          new_df[col] = pd.to_datetime(new_df[col], errors='coerce')

    # # Calculating fields
    new_df = calculate_fields(new_df)

    return new_df