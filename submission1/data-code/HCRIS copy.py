

# Ensure required libraries are installed
import subprocess
import sys

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        __import__(package)

# Install and import the required packages
required_packages = ["pandas", "numpy"]

for package in required_packages:
    install_and_import(package)

# Importing the libraries
import pandas as pd
import numpy as np
import zipfile


# selecting variables via locations

        # Create a list of lists containing the data
import pandas as pd
import warnings
warnings.simplefilter('ignore')

# Define the list of variables and locations
hcris_vars = pd.DataFrame([
    ('beds', 'S300001', '01200', '0100', 'numeric'),
    ('tot_charges', 'G300000', '00100', '0100', 'numeric'),
    ('tot_discounts', 'G300000', '00200', '0100', 'numeric'),
    ('tot_operating_exp', 'G300000', '00400', '0100', 'numeric'),
    ('ip_charges', 'G200000', '00100', '0100', 'numeric'),
    ('icu_charges', 'G200000', '01500', '0100', 'numeric'),
    ('ancillary_charges', 'G200000', '01700', '0100', 'numeric'),
    ('tot_discharges', 'S300001', '00100', '1500', 'numeric'),
    ('mcare_discharges', 'S300001', '00100', '1300', 'numeric'),
    ('mcaid_discharges', 'S300001', '00100', '1400', 'numeric'),
    ('tot_mcare_payment', 'E00A18A', '01600', '0100', 'numeric'),
    ('secondary_mcare_payment', 'E00A18A', '01700', '0100', 'numeric'),
    ('street', 'S200000', '00100', '0100', 'alpha'),
    ('city', 'S200000', '00101', '0100', 'alpha'),
    ('state', 'S200000', '00101', '0200', 'alpha'),
    ('zip', 'S200000', '00101', '0300', 'alpha'),
    ('county', 'S200000', '00101', '0400', 'alpha')
], columns=['variable', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'source'])

#colnames(hcris.vars)=c("variable","WKSHT_CD","LINE_NUM","CLMN_NUM","source")

#reading in data from zip files

zip_path08 = "submission1/Data/input/HCRIS_data/HospitalFY2008.zip"
zip_path09 = "submission1/Data/input/HCRIS_data/HospitalFY2009.zip"

alpha08 = "HospitalFY2008/hosp_2008_ALPHA.CSV"
numeric08 = "HospitalFY2008/hosp_2008_NMRC.CSV"
alpha09 = "HospitalFY2009/hosp_2009_ALPHA.CSV"
numeric09 = "HospitalFY2009/hosp_2009_NMRC.CSV"

rpt08 = "HospitalFY2008/hosp_2008_RPT.CSV"
rpt09 = "HospitalFY2009/hosp_2009_RPT.CSV"




#creating dataframes:
#98
    # Open the ZIP file
with zipfile.ZipFile(zip_path08, 'r') as z:
    # Choose a specific file inside the ZIP
    # Read the CSV file directly into a DataFrame
    with z.open(alpha08) as file01:
        df2008a = pd.read_csv(file01, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(numeric08) as file1:
        df2008n = pd.read_csv(file1, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(rpt08) as file001:
        df2008r = pd.read_csv(file001, names=['RPT_REC_NUM','PRVDR_CTRL_TYPE_CD','PRVDR_NUM','NPI',
                                    'RPT_STUS_CD','FY_BGN_DT','FY_END_DT','PROC_DT',
                                    'INITL_RPT_SW','LAST_RPT_SW','TRNSMTL_NUM','FI_NUM',
                                    'ADR_VNDR_CD','FI_CREAT_DT','UTIL_CD','NPR_DT',
                                    'SPEC_IND','FI_RCPT_DT'], dtype=str)
#99  
with zipfile.ZipFile(zip_path09, 'r') as z:  
    with z.open(alpha09) as file02:
        df2009a = pd.read_csv(file02, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(numeric09) as file2:
        df2009n = pd.read_csv(file2, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(rpt09) as file002:
        df2009r = pd.read_csv(file002, names=['RPT_REC_NUM','PRVDR_CTRL_TYPE_CD','PRVDR_NUM','NPI',
                                    'RPT_STUS_CD','FY_BGN_DT','FY_END_DT','PROC_DT',
                                    'INITL_RPT_SW','LAST_RPT_SW','TRNSMTL_NUM','FI_NUM',
                                    'ADR_VNDR_CD','FI_CREAT_DT','UTIL_CD','NPR_DT',
                                    'SPEC_IND','FI_RCPT_DT'], dtype=str)

#build dataset
#McCarthy Code

final_hcris_v1996 = None

for year in range(2008, 2010):

    data_r = globals()[f"df{year}r"]
    data_n = globals()[f"df{year}n"]
    data_a = globals()[f"df{year}a"]
    final_reports = data_r[['RPT_REC_NUM', 'PRVDR_NUM', 'NPI', 'FY_BGN_DT', 'FY_END_DT', 'PROC_DT',
                                  'FI_CREAT_DT', 'RPT_STUS_CD']]
    final_reports.columns = ['report', 'provider_number', 'npi', 'fy_start', 'fy_end', 'date_processed',
                             'date_created', 'status']
    final_reports['year'] = year
    print("processing year")
    for _, row in hcris_vars.iterrows():
        hcris_data = data_n if row['source'] == 'numeric' else data_a
        val = hcris_data[(hcris_data['WKSHT_CD'] == row['WKSHT_CD']) &
                         (hcris_data['LINE_NUM'] == row['LINE_NUM']) &
                         (hcris_data['CLMN_NUM'] == row['CLMN_NUM'])][['RPT_REC_NUM', 'ITM_VAL_NUM']]
        val.columns = ['report', row['variable']]
        #val.to_csv('val', index=False)
        #if row['source'] == 'n':
            #final_reports[row['variable']] = final_reports[row['variable']].astype(float)
        final_reports = final_reports.merge(val, on='report', how='left')
    
    if final_hcris_v1996 is None:
        final_hcris_v1996 = final_reports
    else:
        final_hcris_v1996 = pd.concat([final_hcris_v1996, final_reports], ignore_index=True)

# Save final dataset
final_hcris_v1996.to_csv('submission1/data/output/HCRIS_v1996.csv', index=False)

