# ------------------------------------------------------------------------------------------------------
# This code drops missing timestamps in both the dsf and spectra files and saves the files.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
# ------------------------------------------------------------------------------------------------------
# Import Packages
import glob
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import shutil
import numpy as np

# Read CSV files
file_path = Path(r'D:\SMM_files\DSF_Spectra_Cities\Devon_2019\DSF')  # file path for dsf
file_path_spectra = Path(r'D:\SMM_files\DSF_Spectra_Cities\Devon_2019\Spectra')  # file path for spectra
filepath_dsf_c = Path(r'D:\SMM_files\DSF_Spectra_Cities\Devon_2019\DSF_cleaned')
filepath_spectra_c = Path(r'D:\SMM_files\DSF_Spectra_Cities\Devon_2019\Spectra_cleaned')
filepath_dsf_c.mkdir(parents=True, exist_ok=True)
filepath_spectra_c.mkdir(parents=True, exist_ok=True)
Golden = False
# Create a list of all CSV files in the folder
all_files = glob.glob(os.path.join(file_path, "*.csv"))  # define file type
iteration = 0

# Loop through each CSV file
for filepath in tqdm(all_files):
    # print(filepath)
    filename_only = os.path.basename(filepath)
    foldername = (filename_only.split('_', 1)[0]).replace('-', '')

    # Read the CSV file and extract the timestamps
    df = pd.read_csv(filepath)
    if Golden:
        timestamps = df['Time stamp'].tolist()
    else:
        timestamps = df['Timestamp'].tolist()


    file_timestamp_pairs = []
    files_in_folder = glob.glob(os.path.join(file_path_spectra, foldername, '*.csv'))
    for filepath_in_folder in files_in_folder:
        filename_in_folder_only = os.path.basename(filepath_in_folder)
        [file_date, file_time] = filename_in_folder_only.split('_', 2)[0:2]
        file_in_folder_timestamp = file_date + ' ' + file_time.replace('-', ':')

        file_timestamp_pairs.append([file_in_folder_timestamp, filepath_in_folder])

    # Remove timestamps that are not in the spectra folder
    csv_timestamps_to_remove = []
    for timestamp in timestamps:
        if timestamp not in [item[0] for item in file_timestamp_pairs]:
            csv_timestamps_to_remove.append(timestamp)

    # Remove rows with timestamps that are not in the spectra folder
    csv_rows_to_remove = []
    for timestamp_to_remove in csv_timestamps_to_remove:
        ix = timestamps.index(timestamp_to_remove)
        csv_rows_to_remove.append(ix)

    # Copy files to new folder
    folder_files_to_copy = []
    for pair in file_timestamp_pairs:
        pair_timestamp = pair[0]
        if pair_timestamp in timestamps:
            folder_files_to_copy.append(pair[1])

    for file_to_copy in folder_files_to_copy:
        file_to_copy_base = os.path.basename(file_to_copy)
        file_to_copy_folder = file_to_copy.split(os.sep)[-2]
        os.makedirs(os.path.join(filepath_spectra_c, file_to_copy_folder), exist_ok=True)
        shutil.copyfile(file_to_copy, os.path.join(filepath_spectra_c, file_to_copy_folder, file_to_copy_base))

    df = df.drop(csv_rows_to_remove)
    df.to_csv(os.path.join(filepath_dsf_c,filename_only), index=None, encoding='utf-8')
    # print("saved")
