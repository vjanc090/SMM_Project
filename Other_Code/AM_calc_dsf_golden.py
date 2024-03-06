import glob
from pathlib import Path
import pandas as pd
import numpy as np

file_path = Path(r'C:/Users/vjanc/Downloads/DSF_ottawa')
files_in_folder_clean = glob.glob(str(file_path / '*.csv'))

airmass = []
timestamps = []
ghi = []

for filepath in files_in_folder_clean:
    df_file = pd.read_csv(filepath)
    elevation_angle_file = df_file["Elevation (deg)"]
    zenith_angle = 90 - elevation_angle_file
    airmass_value = 1 / np.cos(np.radians(zenith_angle))
    airmass.extend(airmass_value)
    timestamps.extend(df_file["Timestamp"])
    ghi.extend(df_file["GHI (W/m2)"])

data_frame_scf = pd.DataFrame({
    "Timestamp": pd.to_datetime(timestamps),
    "Airmass": airmass,
    "GHI": ghi
})

output_path = Path("C:/Users/vjanc/OneDrive/Documents/UniversityofOttawa/SUNLAB2023/Summer/AM_Calc") / "Ottawa_Airmass_Data.csv"
data_frame_scf.to_csv(output_path, index=False)
