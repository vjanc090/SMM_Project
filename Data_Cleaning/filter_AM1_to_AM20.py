import pandas as pd

# Load the CSV file into a DataFrame
df_file = pd.read_csv(r"C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\AM_Calc\Ottawa_Airmass_Data.csv")

# Apply the filter to keep values between 1 and 20 in the "Airmass" column
df_filtered = df_file[(df_file["Airmass"] >= 1) & (df_file["Airmass"] <= 20)]

# Save the filtered DataFrame to a new CSV file
df_filtered.to_csv(r"C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\AM_Calc\cleaned\Ottawa_am_cleaned.csv", index=False)
