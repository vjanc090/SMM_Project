# ---------------------------------------------------------------------------------------------------------
# This code cleans csv files by dropping rows with -1 values in the Global Irradiance column, and for
# airmass values less than 20.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ---------------------------------------------------------------------------------------------------------

import pandas as pd
import os
from pathlib import Path
import glob

file_path_1 = r'D:\SMM_files\DSF_Spectra_Cities\CB_2019\DSF'  # file path for dsf
files_in_folder_clean = glob.glob(os.path.join(file_path_1, '*.csv'))
for filepath in files_in_folder_clean: #create iteratable & iterate on it.
    file = Path(filepath)
    df_file = pd.read_csv(file)
    df = df_file[df_file["GHI (W/m2)"] != -1]
    df = df_file[df_file["DHI (W/m2)"] != -1]
    #df_file = df_file[(df_file["Airmass"] >= 1) & (df_file["Airmass"] <= 20)]
    new_file_name = file.parent.joinpath(f"{file.stem}_cleaned.csv")
    os.remove(file)
    df_file.to_csv(new_file_name, index=None, encoding='utf-8')
