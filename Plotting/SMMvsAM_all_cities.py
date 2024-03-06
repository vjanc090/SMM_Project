# ---------------------------------------------------------------------------------------------------------
# This code plots the airmass vs the spectral mismatch factor for a given day. It also plots the
# statistical spread of the spectral mismatch factor for each airmass bin, using the 25th, and 75th
# percentile. This is for multiple cities!
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ---------------------------------------------------------------------------------------------------------

# Import Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Install Helvetica fonts; may not be necessary on some computers
font_dir = 'C:\\Users\\vjanc\\AppData\\Local\\Microsoft\\Windows\\Fonts'
import matplotlib.font_manager
for font_file in os.listdir(font_dir):
    if 'Helvetica' in font_file and (font_file.endswith('.ttf') or font_file.endswith('.otf')):
        matplotlib.font_manager.fontManager.addfont(os.path.join(font_dir, font_file))

plt.rcParams['font.family'] = 'Helvetica'


# Colors used for plotting
colors = ['#FF0000','#FF8E00','#FFFF00','#008E00','#00C0C0','#400098','#bb66bb']
# Lighter version of colors for the boxplot fill
light_colors = colors  # Adding alpha for lighter color
mid_font = 12
large_font = 12
legend_font = 12

# Function for weighted quantiles
def weighted_quantile(values, quantiles, sample_weight=None,
                      values_sorted=False, old_style=False):
    values = np.array(values)
    quantiles = np.array(quantiles)
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    sample_weight = np.array(sample_weight)
    assert np.all(quantiles >= 0) and np.all(quantiles <= 1), \
        'quantiles should be in [0, 1]'

    if not values_sorted:
        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]

    weighted_quantiles = np.cumsum(sample_weight) - 0.5 * sample_weight
    if old_style:
        weighted_quantiles -= weighted_quantiles[0]
        weighted_quantiles /= weighted_quantiles[-1]
    else:
        weighted_quantiles /= np.sum(sample_weight)

    return np.interp(quantiles, weighted_quantiles, values)

# Define filepaths and read in data
file_paths = [
    r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\CanSIM_SMM_Golden2022_cleaned.csv',
    r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\lat_1CanSIM_SMM_Egbert2019_cleaned_am_cutoff.csv',
    r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\lat_2CanSIM_SMM_Ottawa2019_cleaned_am_cutoff.csv',
    r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\lat_3CanSIM_SMM_Varennes2019_cleaned_am_cutoff.csv',
    r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\lat_4CanSIM_SMM_Charlottetown2019_cleaned_am_cutoff.csv',
    r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\lat_5CanSIM_SMM_Devon2019_cleaned_am_cutoff.csv',
    r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\lat_6CanSIM_SMM_CambridgeBay2019A_N_cleaned_am_cutoff.csv'
]

dfs = []
binned_data = []

for file_path in file_paths:
    df = pd.read_csv(file_path)

    # Calculate SMM versus Airmass binned average
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    df['Airmass_bins'] = pd.cut(df['Airmass'], bins=bins)
    df['Fraction_Weighted_Avg'] = df['GHI (W/m2)'] * df['SCF']
    df_summed = df.groupby('Airmass_bins')['GHI (W/m2)', 'Fraction_Weighted_Avg'].sum().reset_index()
    df_summed['Weighted_Average'] = df_summed['Fraction_Weighted_Avg'] / df_summed['GHI (W/m2)']
    binned_data_1 = df_summed.groupby('Airmass_bins')['Weighted_Average'].mean().reset_index()

    # Create a new column with the SMM bins
    df['SMM_bins'] = pd.cut(df['SCF'], bins=bins)
    binned_data.append(binned_data_1)
    dfs.append(df)

# Define boxplot details
fig, ax = plt.subplots(figsize=(7, 5))
bins_ticks = bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
bins_for_xticks = [f"[{bins_ticks[i]},{bins_ticks[i+1]}]" for i in range(len(bins_ticks) - 1)]
box_width = 0.125

# Plot the boxplots
for i, df in enumerate(dfs):
    boxes = []
    for j in range(len(bins_ticks) - 1):
        bin_value = bins_ticks[j]
        bin_value_2 = bins_ticks[j+1]
        df_bin = df.loc[(df['Airmass'] >= bin_value) & (df['Airmass'] < bin_value_2)]

        if not df_bin.empty:
            quantiles = weighted_quantile(df_bin['SCF'], [0, 0.25, 0.5, 0.75, 1], sample_weight=df_bin['GHI (W/m2)'])
        else:
            quantiles = [0, 0, 0, 0, 0]

        case = {
            'label' :str(i),
            'whislo': quantiles[0],
            'q1'    : quantiles[1],
            'med'   : quantiles[2],
            'q3'    : quantiles[3],
            'whishi': quantiles[4],
            'fliers': []
        }
        boxes.append(case)

    bp = ax.bxp(boxes, positions=np.arange(len(boxes)) - box_width/2 + (i * box_width), patch_artist=True,
                showfliers=False, medianprops=dict(linewidth=1.5, color = colors[i]), widths=box_width, boxprops=dict(edgecolor='black', facecolor=light_colors[i]))

# Plot the scatter points
positions = np.arange(len(binned_data[0]['Airmass_bins']))
bar_width = 0.35
GHI_smm_cities = ['Golden                    39.8° N', 'Egbert                     44.2° N', 'Ottawa                    45.4° N', 'Varennes                 45.6° N', 'Charlottetown         46.2° N', 'Devon                     53.4° N', 'Cambridge Bay*      69.1° N']
for i, df in enumerate(dfs):
    df_summed = df.groupby('Airmass_bins')['GHI (W/m2)', 'Fraction_Weighted_Avg'].sum().reset_index()
    df_summed['Weighted_Average'] = df_summed['Fraction_Weighted_Avg'] / df_summed['GHI (W/m2)']
    weighted_avg_df = pd.DataFrame({
        'Airmass_bins': df_summed['Airmass_bins'].astype(str),
        'Weighted_Average': df_summed['Weighted_Average']
    })
    # Repositioning scatter plot points to the middle of box plots
    center_position = np.arange(len(bins_ticks) - 1) + (i * box_width - 0.065)

    ax.scatter(center_position, weighted_avg_df['Weighted_Average'],
               color=colors[i], alpha=0.75, label=GHI_smm_cities[i], marker='o', s=40)

# Plot details
plt.yticks(fontsize=mid_font)
plt.axhline(y=1.00, color='grey', linestyle='dashed')
ax.set_xlabel('Airmass', fontsize=large_font, fontweight='bold')
ax.set_ylabel('GHI Weighted SMM / Average SMM', fontsize=large_font, fontweight='bold')
ax.set_xticks(np.arange(len(bins_ticks) - 1) + (box_width * (len(dfs) - 1)) / 2)
ax.set_xticklabels(bins_for_xticks, fontsize=mid_font)
plt.legend(loc='lower right', handlelength=2.5, fontsize=legend_font)
plt.ylim(0.55, 1.27)
plt.tight_layout()
plt.show()

# Plot the weighted average Airmass against SMM
fig, ax = plt.subplots(figsize=(7, 4.25))

# Plot the weighted averages using plt.bar() with an offset for the second set of bars
bar_width = 0.12
city_labels = ['Golden                    39.8° N', 'Egbert                     44.2° N', 'Ottawa                    45.4° N', 'Varennes                45.6° N', 'Charlottetown         46.2° N', 'Devon                     53.4° N', 'Cambridge Bay*     69.1° N']
for i, city_df in enumerate(binned_data):
    ax.bar(np.arange(len(city_df['Airmass_bins'])) + i * bar_width, city_df['Weighted_Average'], color=colors[i], width=bar_width, zorder=0.5, label=city_labels[i])

# Adjust the x-axis tick labels to match the Airmass bins with (,] format
tick_positions = np.arange(len(binned_data[0]['Airmass_bins'])) + (bar_width * (len(binned_data) - 1)) / 2
ax.set_xticks(tick_positions)
ax.set_xticklabels([f"({bins_for_xticks[i][1:]}" for i in range(len(bins_for_xticks))], fontsize=mid_font)

# Plot details
plt.xlabel('Airmass', fontsize=large_font, fontweight='bold')
plt.ylabel('GHI Weighted SMM', fontsize=large_font, fontweight='bold')
plt.axhline(y=1.00, color='black', linestyle='dashed')
plt.yticks(fontsize=mid_font)
plt.xticks(fontsize=mid_font)
plt.legend(loc='upper left', fontsize=legend_font)
plt.ylim(0.99, 1.1)
plt.tight_layout()
plt.show()
