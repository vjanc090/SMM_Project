# ---------------------------------------------------------------------------------------------------------
# This code plots the Airmass Weighted Average vs. DHI Fraction for SMM CSV files located in one folder.
# The cities are plotted in order of organization, make sure to change the city name.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ---------------------------------------------------------------------------------------------------------

# Import packages
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the font size for the plot
plt.rcParams.update({'font.size': 16})

# Folder path containing the CSV files
folder_path = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files'

# List all CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Name list corresponding to each CSV file
name = ['Golden','Egbert', 'Ottawa', 'Varennes', 'Charlottetown', 'Devon', 'Cambridge Bay']


all_weighted_averages_am = []
all_bin_counts = []
# Calculate weighted averages for all cities
for file in csv_files:
    file_path = os.path.join(folder_path, file)
    print(f"Processing file: {file_path}")

    # Load CSV
    df = pd.read_csv(file_path)
    ghi = df["GHI (W/m2)"]
    scf = df["SCF"]
    airmass = df["Airmass"]

    # Calculate weighted GHI
    ghi_mult_scf = np.multiply(ghi, scf)
    ghi_sum = np.sum(ghi)
    weighted_ghi = [val / ghi_sum for val in ghi_mult_scf]
    ghi_weighted_scf = (weighted_ghi * scf)

    # Binned Plot
    bin_edges = [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1]
    df['DHI_fraction_bins'] = pd.cut(df['DHI Fraction'], bins=bin_edges)

    # Calculate the Fraction_Weighted_Avg
    df['Fraction_Weighted_Avg'] = df['GHI (W/m2)'] * df['SCF']
    df['Fraction_Weighted_Avg_AM'] = df['GHI (W/m2)'] * df['Airmass']

    # Group by 'DHI_fraction_bins' and calculate the sum of 'GHI (W/m2)' and 'Fraction_Weighted_Avg'
    df_summed = df.groupby('DHI_fraction_bins')['GHI (W/m2)', 'Fraction_Weighted_Avg'].sum()
    df_summed_am = df.groupby('DHI_fraction_bins')['GHI (W/m2)', 'Fraction_Weighted_Avg_AM'].sum()

    # Calculate the Weighted_Average for each bin
    df_summed['Weighted_Average'] = df_summed['Fraction_Weighted_Avg'] / df_summed['GHI (W/m2)']
    df_summed_am['Weighted_Average_AM'] = df_summed_am['Fraction_Weighted_Avg_AM'] / df_summed_am['GHI (W/m2)']

    # Append the data to the lists
    all_weighted_averages_am.append(df_summed_am['Weighted_Average_AM'])
    all_bin_counts.append(df.groupby('DHI_fraction_bins').size())

# Plotting
fig, ax = plt.subplots()
width = 0.15
x = np.arange(len(df_summed.index))  # Use df_summed.index instead of df_summed_am['DHI_fraction_bins']
for i, city in enumerate(name):
    bars_am = all_weighted_averages_am[i]
    bars_list_am = ax.bar(x + i * width, bars_am, width=width, alpha=0.7)

    # Plot the second set of bars for counts
    bin_counts_file = all_bin_counts[i]
    for j, bar in enumerate(bars_list_am):
        count = bin_counts_file[j]
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), count, ha='center', va='bottom', fontsize=12)

# Plot details
ax.set_xlabel('DHI Fraction Bins')
ax.set_ylabel('AM Weighted Average')
ax.legend(name)
ax.set_xticks(x + width * (len(name) - 1) / 2)
ax.set_xticklabels(df_summed.index.astype(str))  # Use df_summed.index instead of df_summed_am['DHI_fraction_bins']
plt.tight_layout()  # Ensures all elements fit within the plot area
plt.show()
