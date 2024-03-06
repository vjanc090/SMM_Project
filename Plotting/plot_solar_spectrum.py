# ---------------------------------------------------------------------------------------------------------
# This code plots the solar spectra for a given day, at a given time, and EQE on a secondary axis.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ---------------------------------------------------------------------------------------------------------

# Import Packages
import pandas as pd
import matplotlib.pyplot as plt
import os

# install Helvetica fonts; may not be necessary on some computers
font_dir = 'C:\\Users\\vjanc\\AppData\\Local\\Microsoft\\Windows\\Fonts'
import matplotlib.font_manager
for font_file in os.listdir(font_dir):
    if 'Helvetica' in font_file and (font_file.endswith('.ttf') or font_file.endswith('.otf')):
        matplotlib.font_manager.fontManager.addfont(font_dir + '\\' + font_file)

plt.rcParams['font.family'] = 'Helvetica'

mid_font = 12
large_font = 12

# Read the CSV files
df = pd.read_csv(r'C:\Users\vjanc\Downloads\colorado_spectra_cleaned_4\colorado_spectra_cleaned_4\jas2\20220906\2022-09-06_12-00-00_SSIM_Spectrum_SN1057.csv')
spectral_irradiance = df['Spectral irradiance from 280-4000nm (W/m2/nm)']
wavelength = df['Wavelength (nm)']

df_2 = pd.read_csv(r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\SMARTSAM1_5.csv')
spectral_irradiance_2 = df_2['GTI']
wavelength_2 = df_2['Wavelength']

df_3 = pd.read_csv(r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\MRT_RAT_data_Custom_layers_250_um_0_80_deg_AM1.5_enc_280_2500nm.csv')
eqe = df_3['Cell EQE']
wavelength_3 = df_3['Wavelength (nm)']

# Plot the solar spectrum from a csv file using pandas
df_1 = pd.read_csv(r'C:\Users\vjanc\Downloads\colorado_spectra_cleaned_4\colorado_spectra_cleaned_4\jas2\20220909\2022-09-09_12-00-00_SSIM_Spectrum_SN1057.csv')
spectral_irradiance_1 = df_1['Spectral irradiance from 280-4000nm (W/m2/nm)']
wavelength_1 = df_1['Wavelength (nm)']

# Create a figure and the first axis
fig, ax1 = plt.subplots(figsize=(7, 4))

# Plot the solar spectra
ax1.plot(wavelength_2, spectral_irradiance_2, linewidth=1, color='green', label='AM1.5G')
ax1.plot(wavelength, spectral_irradiance, linewidth=1, color='blue', label='Sunny  (09/06/2022 12:00:00)')
ax1.plot(wavelength_1, spectral_irradiance_1, linewidth=1, color='red', label='Cloudy (09/09/2022 12:00:00)')

# Set labels and legend for the first axis
ax1.set_xlabel('Wavelength (nm)', fontsize=large_font, fontweight='bold')
ax1.set_ylabel('Spectral Irradiance (W/m$^2$/nm)', fontsize=large_font, fontweight='bold')
ax1.tick_params(axis='both', which='major', labelsize=mid_font)
legend1 = ax1.legend(fontsize= 10, loc='upper right')

# Create a second y-axis for EQE
ax2 = ax1.twinx()

# Plot EQE on the secondary axis
ax2.plot(wavelength_3, eqe, linewidth=1, color='black', label='EQE')

# Set labels and legend for the second axis
ax2.set_ylabel('EQE', fontsize=large_font, fontweight='bold', color='black')
ax2.tick_params(axis='y', which='major', labelsize=mid_font, colors='black')


# Set x-axis ticks for every 500 nm
ax1.set_xticks(range(0, int(wavelength_2.max()) + 1, 1000))
ax2.set_xticks(range(0, int(wavelength_2.max()) + 1, 1000))


# Show the plot
plt.tight_layout()
plt.show()
