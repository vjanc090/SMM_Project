import pandas as pd
import os
import numpy as np
import pytz
import pvlib
from tqdm import tqdm
import traceback

folder_path = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\CWEEDS_Data\CWEEDS_2020_NB\CWEEDS_2020_NB'
folder_path_new = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\CWEEDS_Avg_AM_All_Years'
province_abv = 'NB'
date_format = '%Y%m%d%H'

# Get the list of CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Initialize lists to store data
all_station_list = []
all_ghi_list = []
all_dhi_list = []
all_latitude_list = []
all_longitude_list = []
all_station_name_list = []
all_province_list = []
all_dni_list = []
all_solar_position_list = []
all_AM_list = []

# Check if there are any CSV files
for file in tqdm(csv_files, desc="Processing files", unit="file"):
    try:
        file_path = os.path.join(folder_path, file)

        # Read the first row of the CSV file to extract station information
        df_info = pd.read_csv(file_path, nrows=1)
        station_name = df_info.iloc[0, 1]
        province = df_info.iloc[0, 2]
        latitude = df_info.iloc[0, 5]
        longitude = df_info.iloc[0, 6]
        utc_offset = df_info.iloc[0, 7]

        # Read the CSV file skipping the header and use the second row
        df = pd.read_csv(file_path, header=2, usecols=['ECCC station identifier', 'Year Month Day Hour (YYYYMMDDHH)',
                                                       'Global horizontal irradiance / kJ/m2',
                                                       'Diffuse horizontal irradiance / kJ/m2',
                                                       ], index_col=False)

        # Convert specific columns to numeric
        df['Global horizontal irradiance / kJ/m2'] = pd.to_numeric(df['Global horizontal irradiance / kJ/m2'], errors='coerce')
        df['Diffuse horizontal irradiance / kJ/m2'] = pd.to_numeric(df['Diffuse horizontal irradiance / kJ/m2'], errors='coerce')

        # Remove rows where GHI is 0
        df = df[df['Global horizontal irradiance / kJ/m2'] != 0]

        # Handle date parsing with errors='coerce'
        df['Year Month Day Hour (YYYYMMDDHH)'] = pd.to_datetime(df['Year Month Day Hour (YYYYMMDDHH)'], format=date_format, errors='coerce')
        df['Year Month Day Hour (YYYYMMDDHH)'] = df['Year Month Day Hour (YYYYMMDDHH)'].dt.tz_localize(pytz.FixedOffset(int(utc_offset) * 60))

        # Convert KJ/m2 to W/m2
        df['Global horizontal irradiance / kJ/m2'] = df['Global horizontal irradiance / kJ/m2'] / 3.6
        df['Diffuse horizontal irradiance / kJ/m2'] = df['Diffuse horizontal irradiance / kJ/m2'] / 3.6

        # Calculate Solar Position and AM
        solar_position = pvlib.solarposition.get_solarposition(df['Year Month Day Hour (YYYYMMDDHH)'], latitude, longitude)
        df['Solar Position'] = solar_position['apparent_zenith'].to_numpy()
        df['AM'] = pvlib.atmosphere.get_relative_airmass(df['Solar Position'], model='simple')

        df = df.dropna(subset=['AM'])

        num_elements = len(df['ECCC station identifier'].tolist())
        new_stations = df['ECCC station identifier'].tolist()
        new_ghi = df['Global horizontal irradiance / kJ/m2'].tolist()
        new_dhi = df['Diffuse horizontal irradiance / kJ/m2'].tolist()
        new_am = df['AM'].tolist()

        # Append the lists for the current file to the overall lists
        all_station_list.extend(new_stations)
        all_ghi_list.extend(new_ghi)
        all_dhi_list.extend(new_dhi)
        all_AM_list.extend(new_am)

        all_latitude_list.extend([latitude] * num_elements)
        all_longitude_list.extend([longitude] * num_elements)
        all_station_name_list.extend([station_name] * num_elements)
        all_province_list.extend([province] * num_elements)

    except Exception as e:
        print(f"An error occurred while processing file '{file}': {e}")
        print(traceback.format_exc())

# Create a DataFrame for the filtered data for all years
final_df_all_years = pd.DataFrame({
    'Station': all_station_list,
    'Global Horizontal Irradiance': all_ghi_list,
    'Diffuse Horizontal Irradiance': all_dhi_list,
    'Latitude': all_latitude_list,
    'Longitude': all_longitude_list,
    'Station Name': all_station_name_list,
    'Province': all_province_list,
    'AM': all_AM_list
})

# Convert GHI to numeric
final_df_all_years['Global Horizontal Irradiance'] = pd.to_numeric(final_df_all_years['Global Horizontal Irradiance'], errors='coerce')

# Calculate GHI-weighted average air mass
weighted_am_avg_all_years = final_df_all_years.groupby(['Station', 'Station Name', 'Province', 'Latitude', 'Longitude']) \
    .apply(lambda x: np.average(x['AM'], weights=x['Global Horizontal Irradiance'])) \
    .reset_index(name='Weighted AM')

# Merge the GHI-weighted average air mass back to the original DataFrame
final_df_all_years = pd.merge(final_df_all_years, weighted_am_avg_all_years, on=['Station', 'Station Name', 'Province', 'Latitude', 'Longitude'])

# Create a DataFrame for the average for each station
avg_dhi_percent_df_all_years = final_df_all_years.groupby(['Station', 'Station Name', 'Province', 'Latitude', 'Longitude']).mean().reset_index()

# Save the DataFrame to a CSV file in location new_file
new_file_all_years = os.path.join(folder_path_new, f'CWEEDS_All_Years_{province_abv}_GHI_Weighted_AM.csv')
avg_dhi_percent_df_all_years.to_csv(new_file_all_years, index=False)
