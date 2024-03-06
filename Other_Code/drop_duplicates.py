# ---------------------------------------------------------------------------------------------------------
# This code drops timestamps that have seconds values.
#
# 2023 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# ---------------------------------------------------------------------------------------------------------

import pandas as pd
import os
from pathlib import Path

filepath = r'C:\Users\vjanc\OneDrive\Documents\UniversityofOttawa\SUNLAB2023\Summer\Generated_SCF_files\20220101.csv'
df = pd.read_csv(filepath)
df_new = df[(df["Secs"] != 20) & (df["Secs"] != 40)]
file = Path(filepath)
new_file_name = file.parent.joinpath(f"{file.stem}_cleaned.csv")
df_new.to_csv(new_file_name, index=None, encoding='utf-8')