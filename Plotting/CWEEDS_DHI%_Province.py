import pandas as pd
import os
from tqdm import tqdm  # Import tqdm for progress bars
import pvlib

folder_path = r'C:\Users\vjanc\Downloads\CWEEDS_2020_QC\CWEEDS_2020_QC'
folder_path_new = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\CWEEDS_DHI_Percent'
province_abv = 'QC'

# Get the list of CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Initialize lists to store data
all_station_list = []
all_ts_list = []
all_ghi_list = []
all_dhi_list = []
all_latitude_list = []
all_longitude_list = []
all_station_name_list = []
all_province_list = []
all_dhi_percent_list = []
all_airmass_list = []

# Check if there are any CSV files
for file in tqdm(csv_files, desc="Processing files", unit="file"):
    file_path = os.path.join(folder_path, file)

    # Read the first row of the CSV file to extract station information
    df_info = pd.read_csv(file_path, nrows=1)
    station_name = df_info.iloc[0, 1]
    province = df_info.iloc[0, 2]
    latitude = df_info.iloc[0, 5]
    longitude = df_info.iloc[0, 6]

    # Read the CSV file skipping the header and use the second row
    df = pd.read_csv(file_path, header=2, usecols=['ECCC station identifier', 'Year Month Day Hour (YYYYMMDDHH)',
                                                   'Global horizontal irradiance / kJ/m2', 'Diffuse horizontal irradiance / kJ/m2'],
                     index_col=False)

    # Convert specific columns to numeric
    df['Global horizontal irradiance / kJ/m2'] = pd.to_numeric(df['Global horizontal irradiance / kJ/m2'], errors='coerce')
    df['Diffuse horizontal irradiance / kJ/m2'] = pd.to_numeric(df['Diffuse horizontal irradiance / kJ/m2'], errors='coerce')

    # Filter out rows with NaN values
    df = df.dropna(subset=['Global horizontal irradiance / kJ/m2', 'Diffuse horizontal irradiance / kJ/m2'])

    # Remove rows where GHI is 0
    df = df[df['Global horizontal irradiance / kJ/m2'] != 0]

    # Filter data for the year 2013
    df_2013 = df[df['Year Month Day Hour (YYYYMMDDHH)'].astype(str).str.startswith('2013')].copy()
    df_2013['Year Month Day Hour (YYYYMMDDHH)'] = pd.to_datetime(df_2013['Year Month Day Hour (YYYYMMDDHH)'], format='%Y%m%d%H')

    # Calculate average DHI%
    df_2013['DHI%'] = df_2013['Diffuse horizontal irradiance / kJ/m2'] / df_2013['Global horizontal irradiance / kJ/m2'] * 100

    # Convert KJ/m2 to W/m2
    df_2013['Global horizontal irradiance / kJ/m2'] = df_2013['Global horizontal irradiance / kJ/m2'] / 3.6
    df_2013['Diffuse horizontal irradiance / kJ/m2'] = df_2013['Diffuse horizontal irradiance / kJ/m2'] / 3.6

    num_elements = len(df_2013['ECCC station identifier'].tolist())
    new_stations = df_2013['ECCC station identifier'].tolist()
    new_ts = df_2013['Year Month Day Hour (YYYYMMDDHH)'].tolist()
    new_ghi = df_2013['Global horizontal irradiance / kJ/m2'].tolist()
    new_dhi = df_2013['Diffuse horizontal irradiance / kJ/m2'].tolist()
    new_dhi_percent = df_2013['DHI%'].tolist()

    # Append the lists for the current file to the overall lists
    all_station_list.extend(new_stations)
    all_ts_list.extend(new_ts)
    all_ghi_list.extend(new_ghi)
    all_dhi_list.extend(new_dhi)
    all_dhi_percent_list.extend(new_dhi_percent)

    all_latitude_list.extend([latitude] * num_elements)
    all_longitude_list.extend([longitude] * num_elements)
    all_station_name_list.extend([station_name] * num_elements)
    all_province_list.extend([province] * num_elements)

# Create a DataFrame for the filtered data for the year 2013
final_df_2013 = pd.DataFrame({
    'Station': all_station_list,
    'Timestamp': all_ts_list,
    'Global Horizontal Irradiance': all_ghi_list,
    'Diffuse Horizontal Irradiance': all_dhi_list,
    'Latitude': all_latitude_list,
    'Longitude': all_longitude_list,
    'Station Name': all_station_name_list,
    'Province': all_province_list,
    'DHI%': all_dhi_percent_list
})

# Print the resulting DataFrame
#print(final_df_2013.head(100).to_string())

# Create a DataFrame for the average DHI% for each station
avg_dhi_percent_df = final_df_2013.groupby(['Station', 'Station Name', 'Province', 'Latitude', 'Longitude']).mean().reset_index()

# Save the DataFrame to a CSV file in location new_file
new_file = os.path.join(folder_path_new, f'CWEEDS_2013_{province_abv}_DHI_percent.csv')
avg_dhi_percent_df.to_csv(new_file, index=False)



