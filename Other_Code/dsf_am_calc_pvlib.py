import os
import glob
from pathlib import Path
import pandas as pd
import pvlib
import pytz

file_path = r'C:\Users\vjanc\Downloads\colorado_dsf_cleaned\colorado_dsf_cleaned'
output_directory = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\AM_pvlib'
utc_offset = -7
latitude = 39.8
longitude = -105.2
date_format = '%Y-%m-%d %H:%M:%S'

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize lists to store data
timestamps = []
ghi = []
airmass = []

# Process each CSV file in the specified folder
for filepath in glob.glob(os.path.join(file_path, '*.csv')):
    try:
        # Read the CSV file
        df = pd.read_csv(filepath)

        # Parse and localize timestamps
        df['Time stamp'] = pd.to_datetime(df['Time stamp'], format=date_format, errors='coerce')
        df['Time stamp'] = df['Time stamp'].dt.tz_localize(pytz.FixedOffset(int(utc_offset) * 60))

        # Calculate solar position
        solar_position = pvlib.solarposition.get_solarposition(df['Time stamp'], latitude, longitude)
        df['Solar Position'] = solar_position['apparent_zenith'].to_numpy()

        # Calculate airmass and drop rows with NaN values
        df['AM'] = pvlib.atmosphere.get_relative_airmass(df['Solar Position'], model='simple')

        # Append data to lists
        timestamps.extend(df['Time stamp'].tolist())
        ghi.extend(df['Global irradiance (W/m2)'].tolist())
        airmass.extend(df['AM'].tolist())

    except Exception as e:
        print(f"Error processing file {filepath}: {e}")

# Create a DataFrame from the collected data
data_frame_scf = pd.DataFrame({"Time stamp": timestamps, "GHI": ghi, "Airmass": airmass})

print(data_frame_scf)

# Save the DataFrame to a CSV file
output_file_path = os.path.join(output_directory, "CanSIM_AM_colorado2019.csv")
data_frame_scf.to_csv(output_file_path, index=False)
print(f"Results saved to {output_file_path}")
