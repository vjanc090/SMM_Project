import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import griddata

# Folder containing CSV files with DHI data, latitudes, and longitudes
folder_path = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\CWEEDS_DHI_Percent_All_Years'

# Read DHI data from CSV files
dfs = []
for file_path in glob.glob(os.path.join(folder_path, '*.csv')):
    df = pd.read_csv(file_path)
    dfs.append(df)

# Concatenate the DataFrames
data = pd.concat(dfs, ignore_index=True)

# Map extent
extent = [-130, -55, 36.5, 75]
central_lon = np.mean(extent[:2])
central_lat = np.mean(extent[2:])

# Create the map
plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.AlbersEqualArea(central_lon, central_lat))
ax.set_extent(extent)

# Map features
resol = '50m'
land = cfeature.NaturalEarthFeature('physical', 'land', scale=resol, edgecolor='k', facecolor=cfeature.COLORS['land'])
ocean = cfeature.NaturalEarthFeature('physical', 'ocean', scale=resol, edgecolor='b', alpha=0.25, facecolor=cfeature.COLORS['water'])

ax.add_feature(land, facecolor='white', zorder=4)
ax.add_feature(ocean, linewidth=0.2)

# Country and province borders
country_bodr = cfeature.NaturalEarthFeature(category='cultural', name='admin_0_boundary_lines_land', scale=resol,
                                            facecolor='none', edgecolor='k')
provinc_bodr = cfeature.NaturalEarthFeature(category='cultural', name='admin_1_states_provinces_lines', scale=resol,
                                             facecolor='none', edgecolor='k')

ax.add_feature(country_bodr, linestyle='-', linewidth=0.8, edgecolor="k", zorder=10)  # USA/Canada
ax.add_feature(provinc_bodr, linestyle='-', linewidth=0.6, edgecolor="k", zorder=10)

# Create a regular grid for interpolation
grid_x, grid_y = np.meshgrid(np.linspace(data['Longitude'].min(), data['Longitude'].max(), 1000),np.linspace(data['Latitude'].min(), data['Latitude'].max(), 1000))

# Interpolate DHI values onto the regular grid
grid_z = griddata((data['Longitude'], data['Latitude']), data['DHI%'], (grid_x, grid_y), method='linear')

# Create a continuous heatmap using pcolormesh
mesh = ax.pcolormesh(grid_x, grid_y, grid_z, cmap='viridis',transform=ccrs.PlateCarree(), shading='auto', zorder=7, alpha=0.5)

# Add colorbar
cbar = plt.colorbar(mesh, orientation='vertical', fraction=0.025, pad=0.05)
cbar.set_label('DHI %')

# Show the plot
plt.show()
