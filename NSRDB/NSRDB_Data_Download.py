# --------------------------------------------------------------------------------------------------------------------
# This code pulls data from the NSRDB website and sends and email to you with the generated data
# Important: You must create your own API Key before usage. For information on code usage visit
# https://developer.nrel.gov/docs/solar/nsrdb/dynamic_spectral_data_download/
#
# 2022 Victoria Jancowski, Ottawa, Canada
# Email: vjanc090@uottawa.ca
#
# --------------------------------------------------------------------------------------------------------------------

import requests
# Declare url string
url = 'https://developer.nrel.gov/api/nsrdb_api/solar/spectral_ondemand_download.json?api_key=taOQcF0XluBuyF2tlQ3Ai6MBRWoaZmxM596xd4VG&wkt=POINT(-76%2045.0)&names=2017&full_name=Victoria%20Jancowski&email=vjanc090@uottawa.ca&affiliation=UOTTAWA&mailing_list=false&reason=test&equipment=fixed_tilt&tilt=0&angle=0'
f = requests.get(url)
print(f.text)