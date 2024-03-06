import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# install Helvetica fonts; may not be necessary on some computers
font_dir = 'C:\\Users\\vjanc\\AppData\\Local\\Microsoft\\Windows\\Fonts'
import matplotlib.font_manager
for font_file in os.listdir(font_dir):
    if 'Helvetica' in font_file and (font_file.endswith('.ttf') or font_file.endswith('.otf')):
        matplotlib.font_manager.fontManager.addfont(font_dir + '\\' + font_file)

plt.rcParams['font.family'] = 'Helvetica'

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


# Define the folder path containing the CSV files
folder_path = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files'

# List of CSV files in the folder
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Initialize lists to store weighted SMM values and labels
all_weighted_smm_values = []
all_labels = []

# Loop through each CSV file
for csv_file in csv_files:
    # Load the CSV file into a DataFrame
    data = pd.read_csv(os.path.join(folder_path, csv_file))

    # Extract relevant columns
    smm_values = data['SCF']
    ghi_values = data['GHI (W/m2)']  # Assuming you have a column named 'GHI'

    # Calculate the weights based on GHI
    weights = ghi_values

    # Calculate weighted SMM values using the weighted_quantile function
    quantiles = [0.25, 0.5, 0.75]
    weighted_smm_quantiles = weighted_quantile(smm_values, quantiles, sample_weight=weights)
    all_weighted_smm_values.append(weighted_smm_quantiles)

    # Create a label for the plot
    file_name = os.path.splitext(csv_file)[0]
    all_labels.append(file_name)
# Make figure size
plt.figure(figsize=(7, 4))

labels = ['Golden', 'Egbert', 'Ottawa', 'Varennes', 'Char. town', 'Devon', 'Cam. Bay']
# Create a box plot with all weighted SMM values
# Define a rainbow colormap
colors = ['#FF0000','#FF8E00','#ffbf00','#008E00','#00C0C0','#400098','#bb66bb']

boxprops = dict(linewidth=1, color='black')
flierprops = dict(marker='o', markersize=8, markerfacecolor='gray', alpha=0.5)

# Calculate the positions evenly distributed along the x-axis
total_width = len(labels)  # Total number of boxes
positions = np.arange(total_width)

# Create the box plot with rainbow colors and adjusted positions
box_plot = plt.boxplot(all_weighted_smm_values, labels=labels, patch_artist=True,
                       boxprops=boxprops, flierprops=flierprops, widths=0.7, positions=positions,
                       medianprops={'solid_capstyle': 'butt'})

# Lighter version of colors for the boxplot fill
light_colors = [
    '#FFECEC',
    '#FFF5E6',
    '#FFFFEC',
    '#ECFFEC',
    '#ECFFFF',
    '#F5ECFF',
    '#F2F2F2'
]

# Apply rainbow colors to the boxes
for box, color in zip(box_plot['boxes'], light_colors):
    box.set(facecolor=color)

for whisker in box_plot['whiskers']:
    whisker.set(color='black', linewidth=1, linestyle='-')

for cap in box_plot['caps']:
    cap.set(color='black', linewidth=1)

# Apply rainbow colors to the median lines
for median, color in zip(box_plot['medians'], colors):
    median.set(color=color)
    median.set(linewidth=0)

    frac_width = 0.99
    x,y = median.get_data()
    xn = (x - (x.sum() / 2.)) * frac_width + (x.sum() / 2.)
    plt.plot(xn, y, color=color, linewidth=2, solid_capstyle="butt", zorder=4)


plt.ylabel('GHI Weighted SMM', fontsize=12, fontweight='bold')
plt.xlabel('Location', fontsize=12, fontweight='bold')
plt.axhline(y=1.0, color='black', linestyle='dashed', linewidth=1)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.ylim(0.97, 1.06)
plt.tight_layout()
plt.show()