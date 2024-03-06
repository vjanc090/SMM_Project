import pandas as pd
import numpy as np
import os

# Load the CSV file into a DataFrame
df = pd.read_csv(r"C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\AM_pvlib\CanSIM_AM_Ottawa2019.csv")

timestamps = df['Timestamp'].tolist()
ghi = df['GHI'].tolist()
airmass = df['Airmass'].tolist()

# Calculate the weighted average of Airmass based on GHI for each timestamp
ghi_weighted_am = np.round(df["Airmass"] * df["GHI"] / df["GHI"].sum(), 2)

# Create a DataFrame with the calculated values
data_frame_scf = pd.DataFrame({"Timestamp": timestamps, "Airmass": airmass, "GHI": ghi, "GHI_weighted_AM": ghi_weighted_am})

# Save the new DataFrame to a CSV file
output_file_path = os.path.join("C:\\Users\\vjanc\\OneDrive\\Documents\\UniversityofOttawa\\SUNLAB2023\\Summer\\AM_pvlib", "CanSIM_AM_Ottawa2019_weighted.csv")
data_frame_scf.to_csv(output_file_path, index=False)
print(f"Results saved to {output_file_path}")
