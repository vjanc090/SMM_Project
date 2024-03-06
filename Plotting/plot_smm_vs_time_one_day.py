# ---------------------------------------------------------------------------------------------------------
# This code plots the SMM vs time for the Cansim SMM data, as well as the SMM. Pick an index (row value)
# for the start and end of the data you want to plot in the csv file you are pulling from.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ---------------------------------------------------------------------------------------------------------

# Import packages
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
mid_font = 10
mid_large_font = 10
large_font = 10

# install Helvetica fonts; may not be necessary on some computers
font_dir = 'C:\\Users\\vjanc\\AppData\\Local\\Microsoft\\Windows\\Fonts'
import matplotlib.font_manager
for font_file in os.listdir(font_dir):
    if 'Helvetica' in font_file and (font_file.endswith('.ttf') or font_file.endswith('.otf')):
        matplotlib.font_manager.fontManager.addfont(font_dir + '\\' + font_file)
plt.rcParams['font.family'] = 'Helvetica'

# Set the start and end indices for the data these indicies are the rows in the csv file. Pick a timestamp
# from the csv file and find the row number it is in. That is the index.
start = 2000
end = 6000

date_name = 'CB, Nunavut, 08/04/2019'

# Define file path and read data
#file = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\lat_6CanSIM_SMM_CambridgeBay2019A_N_cleaned_am_cutoff.csv'
#file = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\lat_2CanSIM_SMM_Ottawa2019_cleaned_am_cutoff.csv'
file = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\lat_6CanSIM_SMM_CambridgeBay2019A_N_cleaned_am_cutoff.csv'
df = pd.read_csv(file)

time = df['Timestamp']
smm = df['SCF']
ghi = df['GHI (W/m2)']

time_1 = time[start:end]
smm_1 = smm[start:end]
ghi_1 = ghi[start:end]

time_1 = pd.to_datetime(time_1)

# Plot the SMM and GHI vs Time
fig, ax1 = plt.subplots(figsize=(3.5, 3))
ax1.plot(time_1, smm_1, color='black', linewidth=1.5, linestyle='-', label='SMM', alpha=1, zorder=101)
ax1.set_xlabel('Time', fontsize=mid_large_font, fontweight='bold')
ax1.set_ylabel('SMM', color='black', fontweight='bold', fontsize=mid_large_font)
ax1.tick_params(axis='y', labelcolor='black', colors='black', labelsize=mid_font)
ax2 = ax1.twinx()
ax2.fill_between(time_1, ghi_1, color='tab:orange', alpha=0.2, label='GHI', zorder=2)
ax2.set_ylabel(r'$\mathbf{GHI\ (W/m^2)}$', color='tab:orange', fontweight='bold', fontsize=mid_large_font)
ax2.tick_params(axis='y', labelcolor='tab:orange', colors='black', labelsize=mid_font)

# Set the locator and formatter for the x-axis to show only every 3 hours
hours_locator = mdates.HourLocator(interval=3)
hours_formatter = mdates.DateFormatter('%H:%M')
ax1.xaxis.set_major_locator(hours_locator)
ax1.xaxis.set_major_formatter(hours_formatter)
ax1.xaxis.set_tick_params(labelsize=mid_font)

# Combine the legends for both lines
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=8)

ax1.annotate(date_name, xy=(0.99, 0.95), xycoords='axes fraction', fontsize=5.8, horizontalalignment='right', verticalalignment='bottom', fontweight='bold')

# Plot details
ax1.axhline(y=1.00, color='grey', linestyle='dashed', zorder=100)
ax1.xaxis.label.set_color('black')
ax1.yaxis.label.set_color('black')
ax2.yaxis.label.set_color('black',)
ax1.tick_params(axis='y', colors='black', labelsize=mid_font)
ax2.tick_params(axis='y', colors='black', labelsize=mid_font)
plt.gca().spines['bottom'].set_color('black')
plt.gca().spines['left'].set_color('black')
plt.gca().spines['right'].set_color('black')
plt.gca().spines['top'].set_color('black')
ax1.title.set_color('black')
plt.xticks(fontsize=mid_font)
ax1.set_ylim([0.96, 1.16])
ax2.set_ylim([0, 1000])
plt.tight_layout()
plt.show()
