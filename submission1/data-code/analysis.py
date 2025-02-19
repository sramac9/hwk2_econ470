

# Install and import the required packages
#required_packages = ["pandas", "numpy", "tidyverse"]

#for package in required_packages:
    #install_and_import(package)

# Importing the libraries
import pandas as pd
import numpy as np



file_path = "/Users/sammyram/Documents/Github/Homework2_econ470/submission1/data/output/HCRIS_1996.csv"
df0 = pd.read_csv(file_path, encoding='ISO-8859-1', on_bad_lines='skip', low_memory=True)  # or 'latin1', 'utf-16', etc.


#question 1
dup_hcris = df0.groupby(('provider_number', 'year')).size().reset_index(name='report_count')
dup_hcris = dup_hcris[dup_hcris['report_count'] > 1]

count = dup_hcris.groupby('provider_number')['year'].nunique()


