# ----------------------------------------------------------------------------------------------------------
# Description: This script adds DHI values to the Golden SMM file, according to timestamp. The DHI values
# are taken from the golden_dhi_datetime.csv file.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
# ----------------------------------------------------------------------------------------------------------

# Import Packages
import pandas as pd
import glob
import os


# Define Function to merge two CSV files
def merge_dhi_values(df_timestamps, df_dhi, output_file):

    # Convert timestamp columns to datetime objects
    df_timestamps["Timestamp"] = pd.to_datetime(df_timestamps["Timestamp"])
    df_timestamps.drop(columns=['DHI (W/m2)', 'DHI Fraction', 'Airmass'], inplace=True)

    # Merge the DataFrames based on matching timestamps
    merged_df = pd.merge(df_timestamps, df_dhi, on="Timestamp", how="inner")

    # Rename the DHI column to something more descriptive, like "DHI Value"
    merged_df.rename(columns={"Airmass": "Airmass Values"}, inplace=True)

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_file, index=False)

if __name__ == "__main__":

    input_folder = r'D:\SMM_files\Generated_SMM\Golden\TOPCon'
    output_folder = r'D:\SMM_files\Generated_SMM\Golden_corrected\TOPCon'
    csv_files = glob.glob(os.path.join(input_folder, "*.csv"))
    input_DHI_file = r'D:\SMM_files\Golden_DHI\DHI_Golden_2022.csv'

    DHI_data = pd.read_csv(input_DHI_file)
    DHI_data["Timestamp"] = pd.to_datetime(DHI_data["DATE (MM/DD/YYYY)"]+' '+DHI_data["MST"])
    DHI_data['DHI Fraction'] = DHI_data['Diffuse Horizontal [W/m^2]']/DHI_data['Global Horizontal [W/m^2]']
    DHI_data.drop(columns=['DATE (MM/DD/YYYY)', 'MST', 'Global Horizontal [W/m^2]','Direct Normal [W/m^2]'], inplace=True)
    DHI_data.rename(columns={"Diffuse Horizontal [W/m^2]": "DHI (W/m2)"}, inplace=True)

    print(DHI_data)
    for file in csv_files:
        input_SMM_data = pd.read_csv(file)

        input_filename = os.path.splitext(os.path.basename(file))[0]
        output_filename = input_filename + '_clean.csv'
        output_file = os.path.join(output_folder, output_filename)

        ## need to apportion DHI_values_file by day here? timestamp-matching

        merge_dhi_values(input_SMM_data, DHI_data, output_file)
