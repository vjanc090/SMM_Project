# --------------------------------------------------------------------------------------------------------------------
# This code loops through the cansim spectra file and cansim daily summary file to find the missing timestamps.
#
# 2022 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# --------------------------------------------------------------------------------------------------------------------

"""
Import Packages
"""
import os
from datetime import timedelta
import datetime
import glob
import csv

"""
File Locations
"""
day = 1
month = 6
year = 2022
cansim_spectra_file_location = "C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLAB2023\\Summer\\spectra_cansim_june_2022\\20220606"
cansim_dsf = "C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLAB2023\\Summer\\dsf_cansim_june_2022\\2022-06-06_Station_3242_Data.csv"

list_of_missing_timestamps = []
list_of_dirs = [x[1] for x in os.walk(cansim_spectra_file_location)][0]
for dir in list_of_dirs:
    full_dir = os.path.join(cansim_spectra_file_location, dir)
    file_list = glob.glob(os.path.join(full_dir, "*.csv"))

    spectra_time_list = []
    for n in range(len(file_list)):
        file = file_list[n]
        time_ext = file[138:143]
        hour = int(time_ext[0:2])
        minute = int(time_ext[3:5])
        the_time = datetime.datetime(year,month,day, hour, minute)
        spectra_time_list.append(the_time)
    spectra_time_list_str = [x.strftime("%H:%M") for x in spectra_time_list]
    spectra_start_time = spectra_time_list[0]
    spectra_end_time = spectra_time_list[-1]
    time_array = [(spectra_start_time + timedelta(hours = i / 60)).strftime("%H:%M") for i in range(int((spectra_end_time - spectra_start_time).total_seconds() / 60.0))]
    missing_spectral_timestamps = sorted(set(spectra_time_list_str) ^ set(time_array))
    list_of_missing_timestamps.append(missing_spectral_timestamps)
print(list_of_missing_timestamps)


file_list_dsf = glob.glob(os.path.join(cansim_dsf, "*.csv"))

assert (len(file_list_dsf) == len(list_of_missing_timestamps))

for j in range(len(file_list_dsf)):
    missing_times = [datetime.datetime.strptime(list_of_dirs[j] + " " + timestamp, "%Y%m%d %H:%M") for timestamp in list_of_missing_timestamps[j]]
    with open(file_list_dsf[j], 'r') as inp, open(file_list_dsf[j] + ".fixed", 'w', newline='') as out:
        writer = csv.writer(out)
        for row in csv.reader(inp):
            if row[0] == "Timestamp":
                writer.writerow(row)
                continue
            row_time = datetime.datetime.strptime(row[0][0:16], "%Y-%m-%d %H:%M")
            if row_time not in missing_times:
                writer.writerow(row)
            else:
                print(row)
    os.rename(file_list_dsf[j], file_list_dsf[j] + ".fixed")
