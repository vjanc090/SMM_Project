# ---------------------------------------------------------------------------------------------------------
# This code plots the airmass vs the spectral mismatch factor for a year. It also plots the
# statistical spead of the spectral mismatch factor for each airmass bin, using the 25th, and 75th
# percentile. This is for one city!
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ---------------------------------------------------------------------------------------------------------

# Import Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

large_font = 30
mid_font = 26

# Function for weighted quantiles
def weighted_quantile(values, quantiles, sample_weight=None,
                      values_sorted=False, old_style=False):
    """ Very close to numpy.percentile, but supports weights.
    NOTE: quantiles should be in [0, 1]!
    :param values: numpy.array with data
    :param quantiles: array-like with many quantiles needed
    :param sample_weight: array-like of the same length as `array`
    :param values_sorted: bool, if True, then will avoid sorting of
        initial array
    :param old_style: if True, will correct output to be consistent
        with numpy.percentile.
    :return: numpy.array with computed quantiles.
    """
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
        # To be convenient with numpy.percentile
        weighted_quantiles -= weighted_quantiles[0]
        weighted_quantiles /= weighted_quantiles[-1]
    else:
        weighted_quantiles /= np.sum(sample_weight)
    return np.interp(quantiles, weighted_quantiles, values)

# Define filepaths and read in data
file_path = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\DTU_extended_SMM.csv'
df = pd.read_csv(file_path)

# Calculate SMM versus Airmass binned average
bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
df['Airmass_bins'] = pd.cut(df['Airmass'], bins=bins)
df['Fraction_Weighted_Avg'] = df['GHI (W/m2)'] * df['SCF']
df_summed = df.groupby('Airmass_bins')['GHI (W/m2)', 'Fraction_Weighted_Avg'].sum().reset_index()
df_summed['Weighted_Average'] = df_summed['Fraction_Weighted_Avg'] / df_summed['GHI (W/m2)']
binned_data = df_summed.groupby('Airmass_bins')['Weighted_Average'].mean().reset_index()
df['SMM_bins'] = pd.cut(df['SCF'], bins=bins)

df_summed_1 = df.groupby('Airmass_bins')['SCF'].sum()
df_summed_smm = df.groupby('Airmass_bins')['SMM_bins'].size()

# Convert Series to DataFrames for the division operation
df_summed_smm = df_summed_smm.reset_index(name='Count')
df_summed_1 = df_summed_1.reset_index(name='Sum')

# Calculate the weighted average and store it in a new DataFrame
weighted_avg_df = pd.DataFrame({
    'Airmass_bins': df_summed_1['Airmass_bins'].astype(str),  # Convert the bins to strings
    'Weighted_Average': df_summed_1['Sum'] / df_summed_smm['Count']
})

# Create the boxplot using the quantiles function
boxes = []
for i in range(len(bins)-1):
    bin_value = bins[i]
    bin_value_2 = bins[i+1]
    df_bin = df.loc[(df['Airmass'] >= bin_value) & (df['Airmass'] < bin_value_2)]

    if not df_bin.empty:
        quantiles = weighted_quantile(df_bin['SCF'], [0, 0.25, 0.5, 0.75, 1], sample_weight=df_bin['GHI (W/m2)'])
    else:
        quantiles = [0, 0, 0, 0, 0]

    case = {
        'label' :str(i),
        'whislo': quantiles[0],    # Bottom whisker position
        'q1'    : quantiles[1],    # First quartile (25th percentile)
        'med'   : quantiles[2],    # Median         (50th percentile)
        'q3'    : quantiles[3],    # Third quartile (75th percentile)
        'whishi': quantiles[4],    # Top whisker position
        'fliers': []        # Outliers
    }
    boxes.append(case)

boxes_1 = []
for i in range(len(bins)-1):
    bin_value = bins[i]
    bin_value_2 = bins[i+1]
    df_bin = df.loc[(df['Airmass'] >= bin_value) & (df['Airmass'] < bin_value_2)]

    if not df_bin.empty:
        quantiles = weighted_quantile(df_bin['SCF'], [0, 0.25, 0.5, 0.75, 1], sample_weight=df_bin['GHI (W/m2)'])
    else:
        quantiles = [0, 0, 0, 0, 0]

    case = {
        'label' :str(i),
        'whislo': quantiles[0],    # Bottom whisker position
        'q1'    : quantiles[1],    # First quartile (25th percentile)
        'med'   : quantiles[2],    # Median         (50th percentile)
        'q3'    : quantiles[3],    # Third quartile (75th percentile)
        'whishi': quantiles[4],    # Top whisker position
        'fliers': []        # Outliers
    }
    boxes_1.append(case)

# Create a single figure with one axis
fig, ax = plt.subplots(figsize=(10, 5))

# Custom tick labels for the x-axis
bins_ticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
bins_for_xticks = [f"[{bins_ticks[i]},{bins_ticks[i+1]}]" for i in range(len(bins_ticks) - 1)]

# Set the width of the boxes (make them skinnier)
box_width = 0.3

# Plot the first box plot for GHI (SMM) at position 0
bp1 = ax.bxp(boxes, positions=np.arange(len(boxes)) - box_width/2, showfliers=False, medianprops=dict(color='blue', linewidth=1.5), widths=box_width)

# Plot the second box plot for SMM at position 0.5 (shifted 0.5 units to the right)
#bp2 = ax.bxp(boxes_1, positions=np.arange(len(boxes_1)) + box_width/2, showfliers=False, medianprops=dict(linewidth=1.5), widths=box_width)

positions = np.arange(len(binned_data['Airmass_bins']))
bar_width = 0.3

# Set the point plot (scatter plot) properties for Weighted Average SMM
ax.scatter(positions - bar_width/2, binned_data['Weighted_Average'], color='blue', label='GHI Weighted Average SMM', marker='o', s=50, zorder = 1)

# Plot details
# set boxplot fill color to blue
for whisker in bp1['whiskers']:
    whisker.set(color='black', linewidth=2, linestyle='-')


for cap in bp1['caps']:
    cap.set(color='black', linewidth=2)

for box in bp1['boxes']:
    box.set(color='black', linewidth=2)

for median in bp1['medians']:
    median.set(color='blue', linewidth=2)

ax.set_xlabel('Airmass Bins', fontsize=large_font, fontweight='bold')
ax.set_ylabel('GHI Weighted SMM', fontsize=large_font, fontweight='bold')
ax.set_xticks(np.arange(len(bins_for_xticks)))
ax.set_xticklabels(bins_for_xticks, fontsize=mid_font)
plt.yticks(fontsize=mid_font)
legend_entries = [mlines.Line2D([], [], color='blue', label='Median'),
                  #mlines.Line2D([], [], color='orange', label='Median SMM'),
                  mlines.Line2D([], [], color='blue', label='GHI Weighted Average SMM', marker='o', markersize=8, linestyle=''),
                  #mlines.Line2D([], [], color='orange', label='Average SMM', marker='o', markersize=8, linestyle= '')
                  ]

positions = np.arange(len(binned_data['Airmass_bins']))
bar_width = 0.3

# Set the point plot (scatter plot) properties for Weighted Average SMM
ax.scatter(positions - bar_width/2, binned_data['Weighted_Average'], color='blue', label='GHI Weighted Average SMM', marker='o', s=50, zorder = 1)

# Set the point plot (scatter plot) properties for Average SMM
#ax.scatter(positions + bar_width/2, weighted_avg_df['Weighted_Average'], color='orange', alpha=0.75, label='Average SMM', marker='o', s=50)
plt.axhline(y=1.00, color='grey', linestyle='dashed')
ax.legend(handles=legend_entries, loc='lower right', handlelength=2.5, fontsize=mid_font)
plt.subplots_adjust(bottom=0.2)
plt.ylim(0.91,1.045)
plt.show()

# Second plot for the average SMM vs airmass
fig, ax = plt.subplots()

# Plot the weighted averages using plt.bar() with an offset for the second set of bars
bar_width = 0.6

ax.bar(np.arange(len(binned_data['Airmass_bins'])), binned_data['Weighted_Average'], color='blue', edgecolor = 'black',width=bar_width, zorder=0.5)
#ax.bar(weighted_avg_df['Airmass_bins'], weighted_avg_df['Weighted_Average'], align='center', color='blue', alpha=0.25, label='Average SMM')

# Adjust the x-axis tick labels to match the Airmass bins
plt.xticks(np.arange(len(binned_data['Airmass_bins'])), binned_data['Airmass_bins'].astype(str))
plt.xlabel('Airmass', fontsize=large_font, fontweight='bold')
plt.ylabel('GHI Weighted SMM', fontsize=large_font, fontweight='bold')
plt.axhline(y=1.00, color='black', linestyle='dashed')
plt.yticks(fontsize=mid_font)
plt.xticks(fontsize=mid_font)
plt.ylim(0.928, 1.21)
plt.show()

