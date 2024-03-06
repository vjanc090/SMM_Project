# --------------------------------------------------------------------------------------------------------------------
# This code plots various atmospheric data, calculates integrated spectrums, plots flat versus tilted NSRDB spectrums,
# and plots reference, NSRDB, and CanSIM spectra together.
#
# 2022 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# --------------------------------------------------------------------------------------------------------------------

"""
Import Packages
"""
from matplotlib import pyplot as plt
import numpy as np
import csv
from numpy import loadtxt

"""
Import Reference EQE
"""
reference_eqe = "C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLABSummer2022\\Duet\\EQE\\MRT_RAT_data_Custom_layers_250_um_0_80_deg_AM1.5_enc_280_2500nm.csv"

# Read file headers to get indices required for loadtxt
with open(reference_eqe) as h:
    reader = csv.reader(h)
    r = next(reader)
    rest = [row for row in reader]

# Select headers to read in loadtxt
wl_index = r.index('ï»¿Wavelength (nm)')
eqe_index = r.index('Cell EQE')

# Read columns from EQE file
data_measured_spectra = loadtxt(reference_eqe, skiprows=1, delimiter=",", unpack=True, usecols=(wl_index, eqe_index))

# assign eqe and wavelength data to variables
wl_all = data_measured_spectra[0]
eqe_all = data_measured_spectra[1]

"""
Import Reference Spectrum
"""
# Import reference spectrum and assign wavelength and reference spectra to variables
reference_spectra = "C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLABSummer2022\\SMARTS_data_Air_Mass\\Air_Mass\\AM1.5\\smarts295.ext.txt"
reference_spectrum_data = loadtxt(reference_spectra, skiprows=1, delimiter=" ", unpack=True, usecols=(0,4)) #pull one SMARTS spectrum to get length
reference_spectra_wavelengths = reference_spectrum_data[0]
reference_spectrum = reference_spectrum_data[1]

# Location of NSRDB Spectrum
filepath = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLABSummer2022\Duet\spectransrdb.csv'

# Read file headers to get indices required for loadtxt
with open(filepath) as f:
    reader = csv.reader(f)
    i = next(reader)
    rest = [row for row in reader]

# Select headers to read in loadtxt
wl = i.index('ï»¿Wavelength')
spec_f = i.index('SpectrumF')
spec_t = i.index('SpectrumT')

# Read columns of NSRDB CSV file
data_measured_spectra = loadtxt(filepath, skiprows=1, delimiter=",", unpack=True, usecols=(wl, spec_f, spec_t), max_rows=1962)

# Assign spectrum and wavelength data to variables
wavelength = data_measured_spectra[0]
wl_adj = [x * 1000 for x in wavelength] #micrometers to nanometers
spectrum_f = data_measured_spectra[1] #flat spectrum
spectrum_t = data_measured_spectra[2] #tilted spectrum

"""
Plot Flat and Tilted Spectrums of NSRDB
"""
# Plot the flat and tilted NSRDB spectrums
plt.plot(wl_adj, spectrum_f, "r-", label = "Flat Spectrum")
plt.plot(wl_adj, spectrum_t, "b--", label = "Tilted Spectrum")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Irradiance (W/m2)")
plt.title("Flat and Tilted Spectrum at 1pm June 7, 2017")
plt.legend()
plt.show()

"""
Plot All Spectrums
"""
#Cansim spectra filepath
filepath1 = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLABSummer2022\Duet\spectracansim.csv'

# Read file headers to get indices required for loadtxt
with open(filepath1) as file:
    reader1 = csv.reader(file)
    a = next(reader1)
    rest1 = [row for row in reader1]

# Select headers to read in loadtxt
wavel = a.index('ï»¿Wavelength')
spec_c = a.index('Cansim')

# Read columns of Cansim spectra
data_measured_spectra1 = loadtxt(filepath1, skiprows=1, delimiter=",", unpack=True,
                                usecols=(wavel, spec_c))
# Upack cansim spectra and wavelength data
wavelength1 = data_measured_spectra1[0]
spectrum_c = data_measured_spectra1[1]
spectrum_f_adj = [x /1000 for x in spectrum_f] # Adjust to same scale as CANSIM and Reference

# Plot all 3 spectrums together
plt.plot(reference_spectra_wavelengths, reference_spectrum, "g--", label = "Reference Spectrum")
#plt.plot(wavelength1, spectrum_c,"b-", label = "CanSIM Spectrum")
#plt.plot(wl_adj, spectrum_f_adj, "r--", label = "NSRDB Spectrum")
plt.xlim([300, 1200])
#plt.plot(wl_all,eqe_all, "k-", label = "EQE")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Irradiance (W/m2)")
plt.title("Reference and Cansim Spectrums at 1pm June 7, 2017")
plt.legend()
plt.show()

'''
Plot Atmosphere Details
'''
# File Locations of Atmospheric Data
nsrdb_atmo_file = r"C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLABSummer2022\Duet\nsrdb_sunny_atmo.csv"
cansim_atmo_file = r"C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLABSummer2022\Duet\cansim_sunny_atmo.csv"
cansim_atmofile_spectra = r"C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLABSummer2022\MeasuredSpectra\cansim_spec_atmo_data.csv"

# Read Columns of atmospherica data files
cansim_atmo_spectra = loadtxt(cansim_atmofile_spectra, skiprows= 1, delimiter= ",", unpack = True, usecols = None)
cansim_atmo_data = loadtxt(cansim_atmo_file, skiprows=1, delimiter=",", unpack=True, usecols= None)
nsrdb_atmo_data = loadtxt(nsrdb_atmo_file, skiprows=1, delimiter=",", unpack=True, usecols= None)

# Unpack CanSIM atmospheric Data
cansim_atmo_spec_wl = cansim_atmo_spectra[0]
cansim_atmo_spec_spec = cansim_atmo_spectra[1]
cansim_atmo_wl = cansim_atmo_data[0]
cansim_atmo_rayleigh_scattering = cansim_atmo_data[1]
cansim_atmo_turbidity = cansim_atmo_data[2]
cansim_atmo_aero_scattering_abs = cansim_atmo_data[3]
cansim_atmo_water_vap = cansim_atmo_data[4]
cansim_ozone_abs = cansim_atmo_data[5]
cansim_unmixed_gas_abs = cansim_atmo_data[6]

# Unpack NSRDB atmospheric Data
nsrdb_atmo_wl = nsrdb_atmo_data[0]
nsrdb_atmo_rayleigh_scattering = nsrdb_atmo_data[1]
nsrdb_atmo_turbidity = nsrdb_atmo_data[2]
nsrdb_atmo_aero_scattering_abs = nsrdb_atmo_data[3]
nsrdb_atmo_water_vap = nsrdb_atmo_data[4]
nsrdb_ozone_abs = nsrdb_atmo_data[5]
nsrdb_unmixed_gas_abs = nsrdb_atmo_data[6]

# Plot Atmospheric Data
plt.plot(cansim_atmo_wl, cansim_atmo_rayleigh_scattering, color="darkorchid", label = "CanSIM Rayleigh Scattering")
plt.plot(nsrdb_atmo_wl, nsrdb_atmo_rayleigh_scattering, linestyle = "dashed", color="indigo", label = "NSRDB Rayleigh Scattering")
plt.plot(cansim_atmo_wl, cansim_atmo_turbidity, color="paleturquoise", label = "CanSIM Turbidity")
plt.plot(nsrdb_atmo_wl, nsrdb_atmo_turbidity, linestyle = "dashed", color="darkturquoise", label = "NSRDB Turbidity")
plt.plot(cansim_atmo_wl, cansim_atmo_aero_scattering_abs, color="hotpink", label = "CanSIM Aerosol Sc. and Abs.")
plt.plot(nsrdb_atmo_wl, nsrdb_atmo_aero_scattering_abs, linestyle = "dashed", color="deeppink", label = "NSRDB Aerosol Sc. and Abs.")
plt.plot(cansim_atmo_wl, cansim_ozone_abs, color="lightsteelblue", label = "CanSIM Ozone Absorbtion")
plt.plot(nsrdb_atmo_wl, nsrdb_ozone_abs, linestyle = "dashed", color="steelblue", label = "NSRDB Ozone Absorbtion")
plt.plot(cansim_atmo_wl, cansim_unmixed_gas_abs, color="limegreen", label = "CanSIM Unmixed Gas Absorbtion")
plt.plot(nsrdb_atmo_wl, nsrdb_unmixed_gas_abs, linestyle = "dashed", color="darkgreen", label = "NSRDB Unmixed Gas Absorbtion")
plt.plot(wl_all,eqe_all, "k-", label = "EQE")
plt.xlabel("Wavelength (nm)")
plt.xlim([280,1800])
plt.legend()
plt.show()

# Plot Water Vapour Content
plt.plot(cansim_atmo_wl, cansim_atmo_water_vap, color="r", label = "CanSIM Water Vapour")
plt.plot(nsrdb_atmo_wl, nsrdb_atmo_water_vap, linestyle = "dashed", color="black", label = "NSRDB Water Vapour")
plt.plot(wl_all,eqe_all, "b-", label = "EQE")
plt.xlabel("Wavelength (nm)")
plt.xlim([280,1800])
plt.legend()
plt.show()

'''
Find Value of Integrated Spectrums
'''
# Splicing is done according to bandgap and EQE determined when looking at spectra and wavelength in csv file
cansim_mid_spec_wl = wavelength1[62:901] #360nm - 1200nm
cansim_mid_spec = spectrum_c[62:901] #360nm - 1200nm spectra values
cansim_tot_spec = spectrum_c[0:3700] #complete spectrum
cansim_tot_wl = wavelength1[0:3700] #all wavelengths in complete spectrum
print("The integral is " + str(np.trapz(cansim_mid_spec, cansim_mid_spec_wl)))
print("The integral is " + str(np.trapz(cansim_tot_spec, cansim_tot_wl)))

# Splicing is done according to bandgap and EQE determined when looking at spectra and wavelength in csv file
nsrdb_mid_spec_wl = wl_adj[122:1001] #360nm - 1200nm
nsrdb_mid_spec = spectrum_f[122:1001] #360nm - 1200nm spectra values
nsrdb_tot_spec = spectrum_f[0:1962] #complete spectrum
nsrdb_tot_wl = wavelength1[0:1962] #all wavelengths in complete spectrum
print("The integral is " + str((np.trapz(nsrdb_mid_spec, nsrdb_mid_spec_wl))/1000))
print("The integral is " + str((np.trapz(nsrdb_tot_spec, nsrdb_tot_wl))/1000))

