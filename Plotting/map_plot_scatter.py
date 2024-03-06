import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

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
lakes = cfeature.NaturalEarthFeature('physical', 'lakes', scale=resol, edgecolor='b', alpha=0.25, facecolor=cfeature.COLORS['water'])
rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', scale=resol, edgecolor='none', facecolor='none')

ax.add_feature(land, facecolor='white', zorder=4)
ax.add_feature(ocean, linewidth=0.2)
ax.add_feature(lakes, zorder=5)
ax.add_feature(rivers, linewidth=0.5, zorder=6)

# Country and province borders
country_bodr = cfeature.NaturalEarthFeature(category='cultural', name='admin_0_boundary_lines_land', scale=resol,
                                            facecolor='none', edgecolor='k')
provinc_bodr = cfeature.NaturalEarthFeature(category='cultural', name='admin_1_states_provinces_lines', scale=resol,
                                             facecolor='none', edgecolor='k')

ax.add_feature(country_bodr, linestyle='-', linewidth=0.8, edgecolor="k", zorder=10)  # USA/Canada
ax.add_feature(provinc_bodr, linestyle='-', linewidth=0.6, edgecolor="k", zorder=10)

# Scatter plot of DHI values
sc = ax.scatter(
    data['Longitude'], data['Latitude'],c=data['DHI%'], cmap='viridis', s=50, transform=ccrs.PlateCarree(), zorder=7
)

# Add colorbar
cbar = plt.colorbar(sc, orientation='vertical', fraction=0.025, pad=0.05)
cbar.set_label('DHI %')

# Show the plot
plt.show()
