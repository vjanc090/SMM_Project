# ---------------------------------------------------------------------------------------------------------
# This code calculates airmass from GHI, DHI, and DNI values from a DSF CSV file, and save the airmass
# values to a new CSV file.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ---------------------------------------------------------------------------------------------------------

import os
import glob
from tqdm import tqdm
from pathlib import Path
import pandas as pd
import numpy as np

file_path = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\cansim\all_dsf\varennes_dsf'
files_in_folder_clean = glob.glob(os.path.join(file_path, '*.csv'))
airmass = []
timestamps = []
ghi = []
for filepath in tqdm(files_in_folder_clean):
    df_file = pd.read_csv(filepath)
    ghi_file = df_file["GHI (W/m2)"]
    dhi_file = df_file["DHI (W/m2)"]
    dni_file = df_file["DNI (W/m2)"]
    z_angle_cos = (ghi_file - dhi_file) / dni_file
    am = 1 / z_angle_cos
    airmass.append(am)
    ghi.append(ghi_file)
    timestamps.append(df_file["Timestamp"])

data_frame_scf = pd.DataFrame({"Timestamp": timestamps, "Airmass": airmass})
data_frame_scf.to_csv(os.path.join("C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLAB2023\\Summer\\AM", "CanSIM_AM_varennes2019.csv"))