# ------------------------------------------------------------------------------------------------------
# This code plots the SMM (SCF) versus a weighted GHI for all cities.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
# ------------------------------------------------------------------------------------------------------

# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# Load SMM CSV file and data
filepath_SMM = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files'

# Install Helvetica fonts; may not be necessary on some computers
font_dir = 'C:\\Users\\vjanc\\AppData\\Local\\Microsoft\\Windows\\Fonts'
import matplotlib.font_manager
for font_file in os.listdir(font_dir):
    if 'Helvetica' in font_file and (font_file.endswith('.ttf') or font_file.endswith('.otf')):
        matplotlib.font_manager.fontManager.addfont(os.path.join(font_dir, font_file))

plt.rcParams['font.family'] = 'Helvetica'

binned_data_list = []
filename_list = []
bin_counts_list = []
airmass_list = []
files_in_SMM_folder = glob.glob(os.path.join(filepath_SMM, '*.csv'))
for filepath in (files_in_SMM_folder):
    df_file = pd.read_csv(filepath)
    ghi_file = df_file["GHI (W/m2)"]
    dhi_file = df_file["DHI (W/m2)"]
    smm_file = df_file["SCF"]       #SMM = SCF
    dhi_fraction_file = df_file["DHI Fraction"]
    timestamps_file = df_file["Timestamp"]
    airmass_file = df_file["Airmass"]

    # Calculate weighted GHI
    ghi_mult_scf_file = np.multiply(ghi_file, smm_file)
    ghi_sum_file = np.sum(ghi_file)
    weighted_ghi_file = [val / ghi_sum_file for val in ghi_mult_scf_file]
    ghi_weighted_scf_file = (weighted_ghi_file * smm_file)

    bin_edges = [0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1]
    df_file['DHI_fraction_bins'] = pd.cut(df_file['DHI Fraction'], bins=bin_edges)
    df_file['Fraction_Weighted_Avg'] = (df_file['GHI (W/m2)'] * df_file['SCF'])
    df_summed = df_file.groupby('DHI_fraction_bins')['GHI (W/m2)', 'Fraction_Weighted_Avg'].transform('sum')
    df_summed['DHI_fraction_bins'] = df_file['DHI_fraction_bins']
    df_summed['Weighted_Average'] = df_summed['Fraction_Weighted_Avg']/df_summed['GHI (W/m2)']
    binned_data = df_summed.groupby('DHI_fraction_bins')['Weighted_Average'].mean()

    df_file['DHI_fraction_bins'] = pd.cut(df_file['DHI Fraction'], bins=bin_edges)
    df_file['Fraction_Weighted_Avg_AM'] = (df_file['GHI (W/m2)'] * df_file['Airmass'])
    df_summed_am = df_file.groupby('DHI_fraction_bins')['GHI (W/m2)', 'Fraction_Weighted_Avg_AM'].transform('sum')
    df_summed_am['DHI_fraction_bins'] = df_file['DHI_fraction_bins']
    df_summed_am['Weighted_Average_AM'] = df_summed_am['Fraction_Weighted_Avg_AM'] / df_summed_am['GHI (W/m2)']
    binned_data_AM = df_summed_am.groupby('DHI_fraction_bins')['Weighted_Average_AM'].mean()

    # Calculate the count of elements in each bin for Ottawa and Cambridge Bay
    bin_counts_file = df_file.groupby('DHI_fraction_bins').size()

    airmass_list.append(airmass_file)
    filename_list.append(filepath)
    binned_data_list.append(binned_data)
    bin_counts_list.append(bin_counts_file)

# Plotting
# Determine the width of each bar
bar_width = 0.11

# Calculate the x-axis positions for Ottawa bars
ottawa_bins = np.arange(len(binned_data))
ottawa_x = ottawa_bins +0.5 * bar_width

mid_font = 12
large_font = 12
# Plot the bars
plt.rcParams.update({'font.size': mid_font})
fig, ax = plt.subplots(figsize=(7, 5))

colors = ['#FF0000','#FF8E00','#FFFF00','#008E00','#00C0C0','#400098','#bb66bb']
num_colors = len(binned_data_list)

for i in range(len(binned_data_list)):
    #colors = ['#ffffcc', '#c7e9b4', '#7fcdbb', '#41b6c4', '#2c7fb8', '#253494']
    #colors = ['#fb9155', '#ff7a05', '#e61c05', '#9f120f', '#5e0305', '#010648']
    #colors =  ['#ff87b5', '#c592ff', '#9fe5ff', '#b3db79', '#fbffa3', '#ffc97e', '#e27e66']
    #colors = ['#ff3694','#fdce5e', '#e8933c', '#7c4e9e', '#2FCCCC', '#8e8fc1', '#8bc697']
    names = ['Golden                    39.8° N','Egbert                     44.2° N', 'Ottawa                    45.4° N', 'Varennes                45.6° N', 'Charlottetown         46.2° N', 'Devon                     53.4° N', 'Cambridge Bay*     69.1° N']
    bars_list = ax.bar(ottawa_x + i * bar_width, binned_data_list[i], width=bar_width, label=names[i], color=colors[i])

    #for bar, count in zip(bars_list, bin_counts_list[i]):
        #ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), count, ha='center', va='bottom', fontsize=4.9)

# Set the x-axis tick labels
ax.set_xticks(ottawa_x + (len(binned_data_list) / 2) * bar_width)
ax.set_xticklabels(binned_data.index.astype(str))
ax.set_xticklabels(binned_data.index.astype(str), rotation=45, ha='right')

# Set the x-axis label, y-axis label, and plot title
ax.set_xlabel('DHI Fraction', fontsize = large_font, fontweight = 'bold')
ax.set_ylabel('GHI Weighted Average SMM', fontsize = large_font, fontweight='bold')
ax.axhline(y=1.00, color='black', linestyle='dashed')

# Add a legend and display the plot
ax.legend(loc='upper left', fontsize = mid_font)
plt.ylim(0.97, 1.1)
plt.tight_layout()
plt.show()
