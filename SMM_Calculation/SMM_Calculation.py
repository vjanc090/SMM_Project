# ------------------------------------------------------------------------------------------------------
# This code calculates the spectral correction factor using CanSIM Data.
# Data Cleaning: Before running the program delete all timestamps_file in the DSF csv files with GHI = -1 AND DHI = -1!
# Data Cleaning: No modifications need to be done on the spectral csv files
#
# 2022 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ------------------------------------------------------------------------------------------------------

"""
Import Packages
"""
from numpy import loadtxt
import numpy as np
import csv
from matplotlib import pyplot as plt
import pandas as pd
import glob
import os
from tqdm import tqdm
import pvlib

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

"""
User Inputs
"""
desired_wl_start = 300      # starting wavelength (nm)
desired_wl_stop = 4000      # ending wavelength (nm)

num_dirs_to_skip = 0

"""
File Locations
"""
# File locations of the EQE, SMARTS spectra, CanSIM daily summary files and spectra.
# cansim_spectra_file_location holds folders containing csv spectra files
# cansim_dsf contains all of the daily summary files in csv form
# EQE = r'D:\SMM_files\EQE Data\MRT_RAT_data_Custom_layers_250_um_0_80_deg_AM1.5_enc_280_2500nm.csv'
EQE = r'D:\SMM_files\EQE Data\PERC_EQE.csv'
# EQE = r'D:\SMM_files\EQE Data\TOPCon_EQE.csv'
    # r"C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLAB2023\\Summer\\EQE Data\\MRT_RAT_data_Custom_layers_250_um_0_80_deg_AM1.5_enc_280_2500nm.csv"
reference_spectra = r'D:\SMM_files\SMARTS_data_Air_Mass\Air_Mass\AM1.5\smarts295.ext.txt'
    # r"C:\\Users\\vjanc\OneDrive\\Documents\\UniversityofOttawa\\SUNLAB2023\\Summer\\SMARTS_data_Air_Mass\\Air_Mass\\AM1.5\\smarts295.ext.txt"
cansim_spectra_file_location = r'D:\SMM_files\DSF_Spectra_Cities\Golden\Spectra_cleaned'
    # r"C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLAB2023\\Summer\\cansim\\colorado_spectra_cleaned\\ond2"
cansim_dsf = r'D:\SMM_files\DSF_Spectra_Cities\Golden\DSF_Cleaned'
    # r"C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLAB2023\\Summer\\cansim\\colorado_dsf_cleaned\\ond2"
# output_file_prefix = r'D:\SMM_files\Generated_SMM\Devon\TOPCon\CanSIM_SMM_TOPCon_Devon_'
output_file_prefix = r'D:\SMM_files\Generated_SMM_newAM_20240304\Golden\PERC\CanSIM_SMM_PERC_Golden_'

Colorado = True

#Golden
station_number = 'SN1057'
latitude = 51.3
longitude = -117.0
timezone_string = 'US/Mountain'

# #Devon
# station_number = '3248'
# latitude = 51.3
# longitude = -117.0
# timezone_string = 'US/Mountain'

# #Ottawa
# station_number = '3242'
# latitude = 45.4
# longitude = -75.7
# timezone_string = 'America/Toronto'

#Cambridge Bay
# station_number = '3254'
# latitude = 69.1
# longitude = -105.1
# timezone_string = 'US/Mountain'

"""
Constants
"""
# Define constants for Jsc calculation
h = 6.62607004e-34  # Planck constant, J.s (W.s^2)
c = 2.99792458e8  # speed of light, m/s
q = 1.6021766208e-19  # Elementary charge, C (A.s)

"""
Import Reference EQE
"""
# Read file headers to get indices required for loadtxt
# with open(EQE) as f:
#     reader = csv.reader(f)
#     i = next(reader)
#     rest = [row for row in reader]
#
# # Select headers to read in loadtxt
# wl_index = i.index('ï»¿Wavelength (nm)')
# eqe_index = i.index('Cell EQE')

# Read columns of EQE CSV file
# data_measured_EQE = loadtxt(EQE, skiprows=1, delimiter=",", unpack=True, usecols=(wl_index, eqe_index))
# data_measured_EQE = loadtxt(EQE, skiprows=1, delimiter=",", unpack=True)
data_measured_EQE = pd.read_csv(EQE)
data_measured_EQE = data_measured_EQE.dropna()
# print(data_measured_EQE)

# assign EQE and wavelength data to variables and define start and stop wavelengths
wl_all = (data_measured_EQE['Wavelength (nm)']).values
# print("wl_all: "+str(wl_all))
eqe_all = (data_measured_EQE['Front EQE']/100).values
eqe_all_rear = (data_measured_EQE['Rear EQE']/100).values
wl_stop = desired_wl_stop
wl_start = wl_all[0]

"""
Import Reference Spectra AM1.5G
"""
# Read columns of SMARTS spectrum file
reference_spectrum_data = loadtxt(reference_spectra, skiprows=1, delimiter=" ", unpack=True,
                                  usecols=(0, 8))  # pull one SMARTS spectrum to get length

"""
Perform reference integral with reference spectrum
"""
# Find length of measured spectra list
length = len(data_measured_EQE)

# Interpolate EQE to have values for all SMARTS data points
ref_IAM_integrated = np.zeros([1])
ref_Jsc1 = np.zeros([1])
ref_diff = np.zeros([1])

# Get index of starting EQE wavelength
start_index = np.where(reference_spectrum_data[0] == desired_wl_start)
ref_start_index = start_index[0]
ref_start_index = ref_start_index[0]

# Get index of ending EQE wavelength
stop_index = np.where(reference_spectrum_data[0] == desired_wl_stop)
ref_stop_index = stop_index[0]
ref_stop_index = ref_stop_index[0]

# Get intensity of reference spectra
ref_total_incident_irradiance = np.trapz(reference_spectrum_data[1], reference_spectrum_data[0])
ref_incident_irradiance = np.trapz(reference_spectrum_data[1, ref_start_index:ref_stop_index],
                                   reference_spectrum_data[0, ref_start_index:ref_stop_index])

# Get length of interpolated range of wavelengths and interpolate EQE to have all points for spectrum wavelengths
l = len(reference_spectrum_data[0, ref_start_index:ref_stop_index])
ref_EQE_interp = np.interp(reference_spectrum_data[0, ref_start_index:ref_stop_index],
                           wl_all[ref_start_index:ref_stop_index], eqe_all[
                                                                   ref_start_index:ref_stop_index])  # Interpolate to
# get QE values at all SMARTS wavelengths

ref_EQE_rear_interp = np.interp(reference_spectrum_data[0, ref_start_index:ref_stop_index],
                           wl_all[ref_start_index:ref_stop_index], eqe_all_rear[
                                                                   ref_start_index:ref_stop_index])  # Interpolate to
# get QE values at all SMARTS wavelengths
# Define and perform the reference integral
integral = (q / (h * c) * 1e-9 * 1000 * 0.0001 * ref_EQE_interp * reference_spectrum_data[1,
                            ref_start_index:ref_stop_index] * reference_spectrum_data[0, ref_start_index:ref_stop_index])
ref_Jsc = np.trapz(integral, reference_spectrum_data[0, ref_start_index:ref_stop_index])

integral = (q / (h * c) * 1e-9 * 1000 * 0.0001 * ref_EQE_rear_interp * reference_spectrum_data[1,
                            ref_start_index:ref_stop_index] * reference_spectrum_data[0, ref_start_index:ref_stop_index])
ref_Jsc_rear = np.trapz(integral, reference_spectrum_data[0, ref_start_index:ref_stop_index])
# print("ref_Jsc_rear:")
# print(ref_Jsc_rear)
'''
Import Daily Summary Files (DSF)
'''
# Importing and unpacking of the CanSIM DSF, including timestamps_file and GHI
path = cansim_dsf
csv_files = glob.glob(os.path.join(path, "*.csv"))
# print("DSF file list: "+str(csv_files))
# print("")

# print("timestamps:")
# print(timestamps)
'''
Import Cansim Spectra and Perform Measured Integral
'''
# Imports and assigns spectra to variable, defines and performs the integral to find Jsc
list_of_dirs = [x[0] for x in os.walk(cansim_spectra_file_location)]
print("cansim_spectra_file_location")
print(cansim_spectra_file_location)
print("list_of_dirs")
print(list_of_dirs)
list_of_dirs = list_of_dirs[1:]
print("list_of_dirs")
print(list_of_dirs)

for dir_ix in tqdm(range(num_dirs_to_skip, len(list_of_dirs))):
    # print("test")
    # print(dir_ix)
    timestamps = []
    pressures = []
    measured_ghi = []
    measured_dhi = []
    zenith_angle = []

    jsc = []
    jsc_rear = []
    spectral_ghi = []

    f = csv_files[dir_ix]
    dir = list_of_dirs[dir_ix]

    df = pd.read_csv(f)

    date_str = f.split('\\')[-1][:10]
    # print(date_str)

    # print('Location:', f)
    # print('File Name:', f.split("\\")[-1])
    # print('Content:')
    # print(df_file)
    for ind in df.index:
        if Colorado:
            ts = df['Time stamp'][ind]
        else:
            ts = df['Timestamp'][ind]
            #ts could be a datetime object, cross-referenced with timestamp of spectrum...?
        timestamps.append(ts)
        if Colorado:
            m_ghi = df['Global irradiance (W/m2)'][ind]
        else:
            m_ghi = df['GHI (W/m2)'][ind]
        measured_ghi.append(m_ghi)
        if Colorado:
            m_dhi = np.nan
        else:
            m_dhi = df['DHI (W/m2)'][ind]


        pressure = (df['Ambient pressure (kPa)'][ind]*1000)
        measured_dhi.append(m_dhi)
        el_angle_deg = df['Elevation (deg)'][ind]
        zenith_angle.append(el_angle_deg)
        pressures.append(pressure)

    csv_files_in_dirs = glob.glob(os.path.join(dir, "*{station}*.csv".format(station=station_number)))
    for n in csv_files_in_dirs:
        # print("File:"+str(n))
        #Check if spectrum file has an entry in daily summary files. If not, skip it
        filename = os.path.basename(n)
        timestamp_list = list(filename[:19])
        timestamp_list[10] = ' '
        timestamp_list[13] = ':'
        timestamp_list[16] = ':'
        timestamp_string = "".join(timestamp_list)
        # print("timestamp_string:" + timestamp_string)
        if timestamp_string in timestamps:
            # print("TRUE")
            data_frame = pd.read_csv(n)
            # print(data_frame)
            if Colorado:
                spectral_ghi_list = [x for x in data_frame['Spectral irradiance from 280-4000nm (W/m2/nm)'][10:-1]]
            else:
                spectral_ghi_list = [x for x in data_frame['Spectral GHI 280-4000 nm (W/m2/nm)'][10:-1]]
            integral = (q / (h * c)) * 1e-9 * 1000 * 0.0001 * ref_EQE_interp * reference_spectrum_data[0,
                                                                               ref_start_index:ref_stop_index] * spectral_ghi_list[
                                                                                                                 ref_start_index:ref_stop_index]
            # print(integral)
            integral_jsc = np.trapz(integral, reference_spectrum_data[0, ref_start_index:ref_stop_index])
            # print(jsc)
            jsc.append(integral_jsc)

            integral = (q / (h * c)) * 1e-9 * 1000 * 0.0001 * ref_EQE_rear_interp * reference_spectrum_data[0,
                                                                               ref_start_index:ref_stop_index] * spectral_ghi_list[
                                                                                                                 ref_start_index:ref_stop_index]
            integral_jsc_rear = np.trapz(integral, reference_spectrum_data[0, ref_start_index:ref_stop_index])
            jsc_rear.append(integral_jsc_rear)
            spectral_ghi.append(spectral_ghi_list)
        else:
            print("timestamp_string:" + timestamp_string)
            print("FALSE")

    # Creates NumPy arrays of the spectrum and the Jsc and a list of spectrum wavelengths
    jsc = np.array(jsc)
    jsc_rear = np.array(jsc_rear)
    spectral_ghi = np.array(spectral_ghi)
    # print(spectral_ghi.shape)
    spectrum_wavelengths_all = np.linspace(300, 4000, spectral_ghi.shape[1])
    # print(np.array(spectral_ghi).shape)
    # print(spectrum_wavelengths_all.shape)

    # Creates list of total incident irradiance and incident irradiance
    total_incident_irradiance_list = []
    incident_irradiance_list = []
    for i in range(spectral_ghi.shape[0]):
        total_incident_irradiance_list.append(np.trapz(spectral_ghi[i], spectrum_wavelengths_all))
        incident_irradiance_list.append(np.trapz(spectral_ghi[i][ref_start_index:ref_stop_index],
                                                 spectrum_wavelengths_all[ref_start_index:ref_stop_index]))

    # Creates NumPy arrays of the total incident and incident irradiances
    total_incident_irradiance_list = np.array(total_incident_irradiance_list)
    incident_irradiance_list = np.array(incident_irradiance_list)

    # Defines intensity norm and computes spectral correction factor (SCF)
    intensity_norm_ghi = ref_total_incident_irradiance / total_incident_irradiance_list
    spectral_modifier_ghi = intensity_norm_ghi * (jsc / ref_Jsc)
    spectral_modifier_ghi_rear = intensity_norm_ghi * (jsc_rear / ref_Jsc_rear)

    dhi_fraction = [a/b for a, b in zip(measured_dhi, measured_ghi)]

    #airmass = 1/np.cos(np.radians(zenith_angle))
    '''
    solar_position = pvlib.solarposition.get_solarposition(df['Timestamp'], latitude, longitude)
    df['solar position'] = solar_position['apparent_zenith'].to_numpy()
    df['AM'] = pvlib.atmosphere.get_relative_airmass(df['solar position'], model = 'simple')
    airmass = df['AM'].tolist()
    '''

    """
    print("total_incident_irradiance_list length: "+str(len(total_incident_irradiance_list)))
    print("jsc Length: "+str(len(jsc)))
    print("Timestamp Length:"+str(len(timestamps)))
    print("SMM Length:"+str(len(spectral_modifier_ghi)))
    print("SMM Rear Length:"+str(len(spectral_modifier_ghi_rear)))
    print("GHI Length:"+str(len(measured_ghi)))
    print("DHI Length:"+str(len(measured_dhi)))
    print("DHI Fraction Length:"+str(len(dhi_fraction)))
    print("Air Mass Length:"+str(len(airmass)))
    """

    # Calculate Airmass
    timestamps_corrected, solar_pos, rel_airmass, abs_airmass_w_pressure = calculate_airmass(timestamps, pressures, latitude, longitude, timezone_string)

    # Saves timestamps_file and smm_file to a CSV file
    # data_frame_scf = pd.DataFrame({"Timestamp": timestamps, "SCF": spectral_modifier_ghi, "GHI (W/m2)": measured_ghi, "Airmass": airmass})
    # data_frame_scf = pd.DataFrame({"Timestamp": timestamps, "SCF": spectral_modifier_ghi, "GHI (W/m2)": measured_ghi, "DHI (W/m2)": measured_dhi, "DHI Fraction": dhi_fraction, "Airmass": airmass})
    data_frame_scf = pd.DataFrame({"Timestamp": timestamps_corrected, "SMM": spectral_modifier_ghi,"SMM Rear": spectral_modifier_ghi_rear, "GHI (W/m2)": measured_ghi, "DHI (W/m2)": measured_dhi, "DHI Fraction": dhi_fraction, "AM Gueymard1993 PVLib": rel_airmass, 'AM Pressure Corrected PVLib': abs_airmass_w_pressure, 'Solar Position': solar_pos})

    output_file_ix = output_file_prefix + date_str + '.csv'

    os.makedirs(os.path.split(output_file_ix)[0], exist_ok=True)
    data_frame_scf.to_csv(output_file_ix)
    # data_frame_scf.to_csv(os.path.join("C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLAB2023\\Summer\\Generated_SCF_files", "CanSIM_SMM_Golden2022_8.csv"))