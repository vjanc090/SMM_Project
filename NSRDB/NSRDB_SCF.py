# ----------------------------------------------------------------------------------
# This code calculates the spectral correction factor using NSRDB Data.
# Data Cleaning: !!Before running the program delete all timetamps where GHI is 0!!
#
# 2022 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ----------------------------------------------------------------------------------

"""
Import Packages
"""
from numpy import loadtxt
import numpy as np
import csv
from matplotlib import pyplot as plt
import pandas as pd
import os

"""
Inputs
"""
# Defines the start and end wavelengths (nm) for smm_file calculation
desired_wl_start = 300
desired_wl_stop = 4000

# Creates list of wavelengths
spectrum_wavelengths = np.arange(300, 4010, 10)

# Defines what the local time is. (Found in top row of NSRDB CSV file)
localtime = -5

"""
File Locations
"""
#File locations of the EQE file, reference spectrum, and NSRDB measured spectrum
reference_eqe_data = "C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLABSummer2022\\Duet\\EQE\\MRT_RAT_data_Custom_layers_250_um_0_80_deg_AM1.5_enc_280_2500nm.csv"
reference_spectra_data = "C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLABSummer2022\\SMARTS_data_Air_Mass\\Air_Mass\\AM1.5\\smarts295.ext.txt"
measured_spectra_data = "C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLABSummer2022\\MeasuredSpectra\\may24_cloudy.csv"

"""
Constants
"""
h = 6.62607004e-34  # Plank constant, J.s (W.s^2)
c = 2.99792458e8  # speed of light, m/s
q = 1.6021766208e-19  # Elementary charge, C (A.s)
constant = q / (h * c)  # constant to multiply results, in A/W.m

"""
Useful Functions
"""
# Removes micrometers from wavelength list to convert from string to int type. Removes nan values from wavelength list.
def um_text_to_nm_number(um_text):
    try:
        return np.round(1000 * float(um_text[:-3]))
    except:
        return np.nan

"""
Import Reference EQE
"""
# Read file headers to get indices required for loadtxt
with open(reference_eqe_data) as f:
    reader = csv.reader(f)
    i = next(reader)
    rest = [row for row in reader]

# Select headers to read in loadtxt
wl_index = i.index('ï»¿Wavelength (nm)')
eqe_index = i.index('Cell EQE')

# Read columns of EQE file to get data
ref_eqe_data = loadtxt(reference_eqe_data, skiprows=1, delimiter=",", unpack=True, usecols=(wl_index, eqe_index))

# assign EQE and wavelength data to variables and define start and stop wavelengths
wl_all = ref_eqe_data[0]
eqe_all = ref_eqe_data[1]
wl_stop = desired_wl_stop
wl_start = wl_all[0]

"""
Import SMARTS Reference Spectra AM1.5G
"""
# Read columns of SMARTS spectrum file
reference_spectrum_data = loadtxt(reference_spectra_data, skiprows=1, delimiter=" ", unpack=True, usecols=(0, 4))

"""
Perform reference integral with reference spectrum
"""
# Find length of EQE list
length = len(ref_eqe_data)

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

# Get length of interpolated range of wavelengths
l = len(reference_spectrum_data[0, ref_start_index:ref_stop_index])

# Interpolate the EQE to have points for all spectrum wavelengths
ref_EQE_interp = np.interp(reference_spectrum_data[0, ref_start_index:ref_stop_index],wl_all[ref_start_index:ref_stop_index], eqe_all[ref_start_index:ref_stop_index])  # Interpolate to get QE values at all SMARTS wavelengths

# Define and perform the reference integral
integral = (q / (h * c) * 1e-9 * 1000 * 0.0001 * ref_EQE_interp * reference_spectrum_data[1, ref_start_index:ref_stop_index] * reference_spectrum_data[0, ref_start_index:ref_stop_index])  # not sure why 0.1/0.01 required...?
ref_Jsc = np.trapz(integral, reference_spectrum_data[0, ref_start_index:ref_stop_index])

"""
Import Measured Spectra
"""
# Load NSRDB hour and GHI data
ref_eqe_data = loadtxt(measured_spectra_data, skiprows=3, delimiter=",", unpack=True)
hour = ref_eqe_data[3] + localtime
ghi = ref_eqe_data[14]


# The spectrum has NaN's in it where the non-wavelength values are, the function um_text_to_nm_number is used as the
# converter for loadtxt. The converter converts the data from "xxx um"" to int(xxx).
data_measured_spectra_wl = loadtxt(measured_spectra_data, skiprows=2, max_rows=1, delimiter=",",converters=um_text_to_nm_number)

# pick out the specific indices of the wavelengths we want
wl_indices = [np.where(data_measured_spectra_wl == wl)[0][0] for wl in spectrum_wavelengths]

# Create 2d list of wavelengths and corresponding spectrum.
spectral_list = ref_eqe_data[wl_indices, :]

# create tiled wavelengths with respect to spectrum
wl_tiled = np.tile(spectrum_wavelengths, (spectral_list.shape[1], 1)).transpose()
EQE_interp = np.interp(spectrum_wavelengths, wl_all, eqe_all)           # Interpolate to get QE values at all SMARTS wavelengths
EQE_tiled = np.tile(EQE_interp, (spectral_list.shape[1], 1)).transpose()        # Create tiled EQE with repect to spectrum

# calculate the integral of the Jsc
Jsc = constant * 1e-12 * 0.1 * np.trapz(spectral_list * EQE_tiled * wl_tiled, spectrum_wavelengths, axis=0)  # Not sure why 0.1 needed??

# normalize the irradiance and calculate the smm_file
intensity_norm_ghi = ref_total_incident_irradiance / ghi
spectral_modifier = intensity_norm_ghi * (Jsc / ref_Jsc)

# Export hour, smm_file, wavelength, and spectrum to a csv File
df = pd.DataFrame({"Hour": hour, "scf_ghi": spectral_modifier, "Wavelength": spectral_list[0], "Spectrum:": spectral_list[1]})
df.to_csv(os.path.join("C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLABSummer2022\\Duet",
                       "spectral_correction_factor_calc.csv"))

'''
Plot EQE and SR
'''
# Use EQE and Wavelength to create list of spectral modifier without constant
spectral_r = [a * b for a, b in zip(wl_all, eqe_all)]

# Multiply spectral modifier by constants to get actual SR
s_r = [x * (q / (1000000000 * c * h)) for x in spectral_r]

# Plot EQE and SR
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
plt.plot(wl_all, eqe_all, "k-")
ax1.set_ylabel("External Quantum Efficiency", fontsize=15, fontweight="bold")
ax1.set_xlabel("Wavelength (nm)", fontsize=15, fontweight="bold")
ax2.set_ylabel("Spectral Responsivity (A/W)", fontsize=15, fontweight="bold")
ax1.set_ylim([0, 1])
ax2.set_ylim([0, 1])
ax1.set_xlim([300, 1200])
ax1.tick_params(axis='both', which='major', labelsize=13)
ax2.tick_params(axis='both', which='major', labelsize=13)
plt.legend(["EQE", " SR"], fontsize=13)
plt.show()

"""
Plot SCF
"""
# Create list of organized hours
hour_index_list = []
scf_hour_list = []

# This determines what hours you are plotting and makes a list of those hours. Adjust the range if an error is given.
# Make sure you are using the correct hour range. **The NSRDB gives Greenwich time data**.
for i in range(5, 20):
    if i == 20:
        h = localtime
    else:
        h = i
    hour_index_list.append(np.where(hour == h))
    scf_hour = [spectral_modifier[j] for j in hour_index_list[-1]]
    scf_hour_list.append(scf_hour)

# Plots the smm_file hour list.
for i in range(len(scf_hour_list)):
    plt.plot(i + 5, scf_hour_list[i], 'o')

# Define the X-Values and Y-Values
xvals = np.arange(5, len(scf_hour_list) + 5)
yvals = scf_hour_list

# Define  X-tick and corresponding labels
xticks = [6, 8, 10, 12, 14, 16, 18, 20]
xticklabels = ["6:00", "8:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]

# Plot SCF
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.axhline(y=1, linewidth=1, color="k", linestyle="dotted")
ax2.fill_between(xvals, ghi, 0, color="orange", alpha=0.3)
ax2.plot(xvals, ghi, '-', color="orange", linewidth=0.05, label="GHI")
ax1.plot(xvals, yvals, 'k--', label="SCF")
plt.xticks(xticks, xticklabels)
ax1.patch.set_alpha(0)
ax1.set_zorder(1)
ax2.set_zorder(0)
ax1.set_xlabel("Time of Day", fontsize=15, fontweight="bold")
ax1.set_ylabel("Spectral Correction Factor", fontsize=15, fontweight="bold")
ax2.set_ylabel("GHI $(W/m^2)$", fontsize=15, fontweight="bold")
ax2.set_ylim([0, 1000])
ax1.set_ylim([0.9, 1.19])
ax1.tick_params(axis='both', which='major', labelsize=15)
ax2.tick_params(axis='both', which='major', labelsize=15)
ax1.set_title("June 7, 2017 - Sunny - NSRDB", fontsize=15, fontweight="bold")
handles, labels = [(a + b) for a, b in zip(ax1.get_legend_handles_labels(), ax2.get_legend_handles_labels())]
fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.75, 0.75, 0.1, 0.1))
plt.show()