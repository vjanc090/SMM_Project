# ---------------------------------------------------------------------------------------------------------
# This code plots the SMARTS solar spectrum from a csv file.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ---------------------------------------------------------------------------------------------------------

# Import packages
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv(r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\SMARTS_data_Air_Mass\Air_Mass\AM1.5\SMARTSAM1_5.csv')
spectral_irradiance = df['GHI']
extraterrestrial_spectrum = df['Extraterrest. Spectrum']
wavelength = df['Wavelength']

# Read other csv file
df_1 = pd.read_csv(r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\SMARTS_data_Air_Mass\Air_Mass\AM7.0\SMARTSAM7.csv')
spectral_iradiance_1 = df_1['GHI']
wavelength_1 = df_1['Wavelength']

# Plot the spectrum
plt.plot(wavelength, extraterrestrial_spectrum, linewidth = 1, color = 'black', label = 'AM0')
plt.plot(wavelength, spectral_irradiance, linewidth = 1, color = 'red', label = 'AM1.5')
plt.plot(wavelength_1, spectral_iradiance_1, linewidth = 1, color = 'blue', label = 'AM7.0')
plt.xlabel('Wavelength (nm)', fontsize = 26, fontweight = 'bold')
plt.ylabel('Spectral irradiance (W/m$^2$/nm)',fontsize = 26, fontweight = 'bold')
plt.xticks(fontsize = 26)
plt.yticks(fontsize = 26)
plt.legend(fontsize = 26)
plt.xlim(280,4000)
plt.show()


