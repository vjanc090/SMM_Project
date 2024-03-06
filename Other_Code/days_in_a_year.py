# ---------------------------------------------------------------------------------------------------------
# This code prints the number of days in a year based on timestamp values from a DSF CSV.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ---------------------------------------------------------------------------------------------------------


import pandas as pd
from datetime import datetime

# Step 1: Read the CSV file into a pandas DataFrame
df = pd.read_csv(r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\cansim_full_year_smm_all_cities\filtered_smm\AM_cutoff_20\lat_6CanSIM_SMM_CambridgeBay2019A_N_cleaned_am_cutoff.csv')

# Step 2: Convert the timestamp column to a pandas datetime data type
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Step 3: Extract the year and day-of-year from the datetime column
df['year'] = df['Timestamp'].dt.year
df['day_of_year'] = df['Timestamp'].dt.dayofyear

# Step 4: Count the number of unique days within the year
unique_days = df.drop_duplicates(subset=['year', 'day_of_year'])
number_of_days_in_year = unique_days.groupby('year').size()

print(number_of_days_in_year)