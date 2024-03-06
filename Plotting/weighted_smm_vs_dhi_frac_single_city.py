# ------------------------------------------------------------------------------------------------------
# This code plots the SMM (SCF) versus a weighted GHI for a single city.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
# ------------------------------------------------------------------------------------------------------

# Import packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load SMM CSV file
file_path = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\cansim_full_year_smm_all_cities\filtered_smm\lat_5CanSIM_SMM_Devon2019_cleaned.csv'
df = pd.read_csv(file_path)
ghi = df["GHI (W/m2)"]
dhi = df["DHI (W/m2)"]
scf = df["SCF"]
dhi_fraction = df["DHI Fraction"]
timestamps = df["Timestamp"]
airmass = df["Airmass"]

# Calculate weighted GHI
ghi_mult_scf = np.multiply(ghi, scf)
ghi_sum = np.sum(ghi)
weighted_ghi = [val/ghi_sum for val in ghi_mult_scf]
ghi_weighted_scf = (weighted_ghi*scf)
print(ghi_weighted_scf)

# Calculate the Fraction_Weighted_Avg#
plt.rcParams.update({'font.size': 16})
bin_edges = [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1]
df['DHI_fraction_bins'] = pd.cut(df['DHI Fraction'], bins=bin_edges)
df['Fraction_Weighted_Avg'] = df['GHI (W/m2)'] * df['SCF']
df['Fraction_Weighted_Avg_AM'] = df['GHI (W/m2)'] * df['Airmass']

# Group by 'DHI_fraction_bins' and calculate the sum of 'GHI (W/m2)' and 'Fraction_Weighted_Avg'
df_summed = df.groupby('DHI_fraction_bins')['GHI (W/m2)', 'Fraction_Weighted_Avg'].sum()
df_summed_am = df.groupby('DHI_fraction_bins')['GHI (W/m2)', 'Fraction_Weighted_Avg_AM'].sum()

# Calculate the Weighted_Average for each bin
df_summed['Weighted_Average'] = df_summed['Fraction_Weighted_Avg'] / df_summed['GHI (W/m2)']
df_summed_am['Weighted_Average_AM'] = df_summed_am['Fraction_Weighted_Avg_AM'] / df_summed_am['GHI (W/m2)']

# Group by 'DHI_fraction_bins' and calculate the mean of 'Weighted_Average'
binned_data = df_summed.groupby('DHI_fraction_bins')['Weighted_Average'].mean().reset_index()
binned_data_am = df_summed_am.groupby('DHI_fraction_bins')['Weighted_Average_AM'].mean().reset_index()

# Plotting
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
bars_list = plt.bar(binned_data['DHI_fraction_bins'].astype(str), df_summed['Weighted_Average'])

# Plot the second set of bars for counts
bin_counts_file = df.groupby('DHI_fraction_bins').size()
for i, bar in enumerate(bars_list):
    count = bin_counts_file[i]
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), count, ha='center', va='bottom', fontsize=12)

# Plot details
plt.axhline(y=1.00, color='black', linestyle='dashed')
plt.xlabel('DHI Fraction Bins')
plt.ylabel('Weighted Average')
plt.title('SMM Weighted Average vs. DHI Fraction Year for Cambridge Bay (08/2019-11/2019)')
plt.ylim(0.99, 1.09)
plt.tight_layout()  # Ensures all elements fit within the plot area
plt.show()