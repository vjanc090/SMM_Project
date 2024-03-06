import pandas as pd
import os
import pvlib
from tqdm import tqdm

def calculate_airmass(timestamp_list, pressure_list, lat, long, timezone_str):
    # Parse timestamps and localize to UTC
    if type(timestamp_list) in (list, tuple):
        timestamp_list = pd.Series(timestamp_list)
    datetime = pd.to_datetime(timestamp_list, errors='coerce')
    output_timestamps = datetime.dt.tz_localize(timezone_str)

    # Calculate Solar Position
    solar_position = pvlib.solarposition.get_solarposition(output_timestamps, lat, long)
    apparent_zenith = solar_position['apparent_zenith'].to_numpy()

    # Calculate AM Corrected
    relative_am = pvlib.atmosphere.get_relative_airmass(apparent_zenith, model='gueymard1993')
    absolute_am_pressure_corr = pvlib.atmosphere.get_absolute_airmass(relative_am, pressure_list)

    return output_timestamps, apparent_zenith, relative_am, absolute_am_pressure_corr

folder_path = r'D:\SMM_files\Generated_SMM\Golden_corrected\TOPCon'
new_folder_path = r'D:\SMM_files\Generated_SMM_PvLib_AM\Golden_corrected\TOPCon'
date_format = '%Y-%m-%d %H:%M'
latitude = 51.3  # Convert latitude to float
longitude = -117.0  # Convert longitude to float (- for west)
timezone_string = 'US/Mountain'

# Get a list of all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Create tqdm progress bar
progress_bar = tqdm(total=len(csv_files), desc='Processing files')

for file_name in csv_files:
    try:
        # Read the CSV file into a DataFrame
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)

        df['Timestamp'], df['Solar Position'], df['AM PVLib'], df['AM Pressure Corrected'] = calculate_airmass(df['Timestamp'], None, latitude, longitude, timezone_string)

        # Save the modified DataFrame back to a new CSV file
        modified_file_path = os.path.join(new_folder_path, 'modified_' + file_name)
        df.to_csv(modified_file_path, index=False)

        # Update tqdm progress bar
        progress_bar.update(1)

    except Exception as e:
        print(f"Error processing file '{file_name}': {e}")

# Close tqdm progress bar
progress_bar.close()
