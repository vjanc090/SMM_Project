import pandas as pd
import os
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

        # Read the CSV file skipping the header and use the second row
        df = pd.read_csv(file_path, header=2, usecols=['ECCC station identifier', 'Year Month Day Hour (YYYYMMDDHH)',
                                                       'Global horizontal irradiance / kJ/m2',
                                                       'Diffuse horizontal irradiance / kJ/m2',
                                                       'Direct normal irradiance / kJ/m2'],index_col=False)

        # Convert specific columns to numeric
        df['Global horizontal irradiance / kJ/m2'] = pd.to_numeric(df['Global horizontal irradiance / kJ/m2'], errors='coerce')
        df['Diffuse horizontal irradiance / kJ/m2'] = pd.to_numeric(df['Diffuse horizontal irradiance / kJ/m2'], errors='coerce')
        df['Direct normal irradiance / kJ/m2'] = pd.to_numeric(df['Direct normal irradiance / kJ/m2'], errors='coerce')

        # Filter out rows with NaN values
        df = df.dropna(subset=['Global horizontal irradiance / kJ/m2', 'Diffuse horizontal irradiance / kJ/m2', 'Direct normal irradiance / kJ/m2'])

        # Remove rows where GHI is 0
        df = df[df['Global horizontal irradiance / kJ/m2'] != 0]

        # Handle date parsing with errors='coerce'
        df['Year Month Day Hour (YYYYMMDDHH)'] = pd.to_datetime(df['Year Month Day Hour (YYYYMMDDHH)'], format=date_format, errors='coerce')

        # Convert KJ/m2 to W/m2
        df['Global horizontal irradiance / kJ/m2'] = df['Global horizontal irradiance / kJ/m2'] / 3.6
        df['Diffuse horizontal irradiance / kJ/m2'] = df['Diffuse horizontal irradiance / kJ/m2'] / 3.6
        df['Direct normal irradiance / kJ/m2'] = df['Direct normal irradiance / kJ/m2'] / 3.6

        num_elements = len(df['ECCC station identifier'].tolist())
        new_stations = df['ECCC station identifier'].tolist()
        new_ghi = df['Global horizontal irradiance / kJ/m2'].tolist()
        new_dhi = df['Diffuse horizontal irradiance / kJ/m2'].tolist()
        new_direct = df['Direct normal irradiance / kJ/m2'].tolist()

        # Append the lists for the current file to the overall lists
        all_station_list.extend(new_stations)
        all_ghi_list.extend(new_ghi)
        all_dhi_list.extend(new_dhi)
        all_dni_list.extend(new_direct)

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
    'DNI': all_dni_list,
    'Latitude': all_latitude_list,
    'Longitude': all_longitude_list,
    'Station Name': all_station_name_list,
    'Province': all_province_list,
})

# Create a DataFrame for the average for each station
avg_dhi_percent_df_all_years = final_df_all_years.groupby(['Station', 'Station Name', 'Province', 'Latitude', 'Longitude']).mean().reset_index()

# Save the DataFrame to a CSV file in location new_file
new_file_all_years = os.path.join(folder_path_new, f'CWEEDS_All_Years_{province_abv}.csv')
avg_dhi_percent_df_all_years.to_csv(new_file_all_years, index=False)
