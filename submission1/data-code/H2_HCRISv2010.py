########################################################################################
## Author:        Sammy Ramacher
## Date Created:  2/18/2025
## Date Edited:   2/18/2025
## Notes:         Python file to read in HCRIS data (2010 version of forms)
########################################################################################

import pandas as pd
import zipfile
import warnings
warnings.simplefilter('ignore')

# Define variables and locations
hcris_vars = pd.DataFrame([
    ('beds', 'S300001', '01400', '00200', 'numeric'),
    ('tot_charges', 'G300000', '00100', '00100', 'numeric'),
    ('tot_discounts', 'G300000', '00200', '00100', 'numeric'),
    ('tot_operating_exp', 'G300000', '00400', '00100', 'numeric'),
    ('ip_charges', 'G200000', '00100', '00100', 'numeric'),
    ('icu_charges', 'G200000', '01600', '00100', 'numeric'),
    ('ancillary_charges', 'G200000', '01800', '00100', 'numeric'),
    ('tot_discharges', 'S300001', '00100', '01500', 'numeric'),
    ('mcare_discharges', 'S300001', '00100', '01300', 'numeric'),
    ('mcaid_discharges', 'S300001', '00100', '01400', 'numeric'),
    ('tot_mcare_payment', 'E00A18A', '05900', '00100', 'numeric'),
    ('secondary_mcare_payment', 'E00A18A', '06000', '00100', 'numeric'),
    ('street', 'S200001', '00100', '00100', 'alpha'),
    ('city', 'S200001', '00200', '00100', 'alpha'),
    ('state', 'S200001', '00200', '00200', 'alpha'),
    ('zip', 'S200001', '00200', '00300', 'alpha'),
    ('county', 'S200001', '00200', '00400', 'alpha'),
    ('hvbp_payment', 'E00A18A', '07093', '00100', 'numeric'),
    ('hrrp_payment', 'E00A18A', '07094', '00100', 'numeric')
], columns=['variable', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'source'])

#file paths
zip_path10 = "submission1/Data/input/HCRIS_data/HospitalFY2010.zip"
zip_path11 = "submission1/Data/input/HCRIS_data/HospitalFY2011.zip"
zip_path12 = "submission1/Data/input/HCRIS_data/HospitalFY2012.zip"
zip_path13 = "submission1/Data/input/HCRIS_data/HospitalFY2013.zip"
zip_path14 = "submission1/Data/input/HCRIS_data/HospitalFY2014.zip"
zip_path15 = "submission1/Data/input/HCRIS_data/HospitalFY2015.zip"

alpha10 = "HospitalFY2010/hosp10_2010_ALPHA.CSV"
numeric10 = "HospitalFY2010/hosp10_2010_NMRC.CSV"
alpha11 = "HospitalFY2011/hosp10_2011_ALPHA.CSV"
numeric11 = "HospitalFY2011/hosp10_2011_NMRC.CSV"
alpha12 = "HospitalFY2012/hosp10_2012_ALPHA.CSV"
numeric12 = "HospitalFY2012/hosp10_2012_NMRC.CSV"
alpha13 = "HospitalFY2013/hosp10_2013_ALPHA.CSV"
numeric13 = "HospitalFY2013/hosp10_2013_NMRC.CSV"
alpha14 = "HospitalFY2014/hosp10_2014_ALPHA.CSV"
numeric14 = "HospitalFY2014/hosp10_2014_NMRC.CSV"
alpha15 = "HospitalFY2015/hosp10_2015_ALPHA.CSV"
numeric15 = "HospitalFY2015/hosp10_2015_NMRC.CSV"

rpt10 = "HospitalFY2010/hosp10_2010_RPT.CSV"
rpt11 = "HospitalFY2011/hosp10_2011_RPT.CSV"
rpt12 = "HospitalFY2012/hosp10_2012_RPT.CSV"
rpt13 = "HospitalFY2013/hosp10_2013_RPT.CSV"
rpt14 = "HospitalFY2014/hosp10_2014_RPT.CSV"
rpt15 = "HospitalFY2015/hosp10_2015_RPT.CSV"

#with zipfile.ZipFile(zip_path11, 'r') as zip_ref:
    #file_names = zip_ref.namelist()  # Get a list of file names
    #print(file_names)

#pull files from zip
#00
with zipfile.ZipFile(zip_path10, 'r') as z:
    with z.open(alpha10) as file03:
        df2010a = pd.read_csv(file03, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(numeric10) as file3:
        df2010n = pd.read_csv(file3, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(rpt10) as file003:
        df2010r = pd.read_csv(file003, names=['RPT_REC_NUM','PRVDR_CTRL_TYPE_CD','PRVDR_NUM','NPI',
                                    'RPT_STUS_CD','FY_BGN_DT','FY_END_DT','PROC_DT',
                                    'INITL_RPT_SW','LAST_RPT_SW','TRNSMTL_NUM','FI_NUM',
                                    'ADR_VNDR_CD','FI_CREAT_DT','UTIL_CD','NPR_DT',
                                    'SPEC_IND','FI_RCPT_DT'], dtype=str)
#01
with zipfile.ZipFile(zip_path11, 'r') as z:
    with z.open(alpha11) as file04:
        df2011a = pd.read_csv(file04, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(numeric11) as file4:
        df2011n = pd.read_csv(file4, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(rpt11) as file004:
        df2011r = pd.read_csv(file004, names=['RPT_REC_NUM','PRVDR_CTRL_TYPE_CD','PRVDR_NUM','NPI',
                                    'RPT_STUS_CD','FY_BGN_DT','FY_END_DT','PROC_DT',
                                    'INITL_RPT_SW','LAST_RPT_SW','TRNSMTL_NUM','FI_NUM',
                                    'ADR_VNDR_CD','FI_CREAT_DT','UTIL_CD','NPR_DT',
                                    'SPEC_IND','FI_RCPT_DT'], dtype=str)
#02
with zipfile.ZipFile(zip_path12, 'r') as z:
    with z.open(alpha12) as file05:
       df2012a = pd.read_csv(file05, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(numeric12) as file5:
       df2012n = pd.read_csv(file5, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(rpt12) as file005:
        df2012r = pd.read_csv(file005, names=['RPT_REC_NUM','PRVDR_CTRL_TYPE_CD','PRVDR_NUM','NPI',
                                    'RPT_STUS_CD','FY_BGN_DT','FY_END_DT','PROC_DT',
                                    'INITL_RPT_SW','LAST_RPT_SW','TRNSMTL_NUM','FI_NUM',
                                    'ADR_VNDR_CD','FI_CREAT_DT','UTIL_CD','NPR_DT',
                                    'SPEC_IND','FI_RCPT_DT'], dtype=str)
#03
with zipfile.ZipFile(zip_path13, 'r') as z:
    with z.open(alpha13) as file06:
       df2013a = pd.read_csv(file06, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(numeric13) as file6:
       df2013n = pd.read_csv(file6, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(rpt13) as file006:
       df2013r = pd.read_csv(file006, names=['RPT_REC_NUM','PRVDR_CTRL_TYPE_CD','PRVDR_NUM','NPI',
                                    'RPT_STUS_CD','FY_BGN_DT','FY_END_DT','PROC_DT',
                                    'INITL_RPT_SW','LAST_RPT_SW','TRNSMTL_NUM','FI_NUM',
                                    'ADR_VNDR_CD','FI_CREAT_DT','UTIL_CD','NPR_DT',
                                    'SPEC_IND','FI_RCPT_DT'], dtype=str)
#04
with zipfile.ZipFile(zip_path14, 'r') as z:
    with z.open(alpha14) as file07:
       df2014a = pd.read_csv(file07, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(numeric14) as file7:
       df2014n = pd.read_csv(file7, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(rpt14) as file007:
        df2014r = pd.read_csv(file007, names=['RPT_REC_NUM','PRVDR_CTRL_TYPE_CD','PRVDR_NUM','NPI',
                                    'RPT_STUS_CD','FY_BGN_DT','FY_END_DT','PROC_DT',
                                    'INITL_RPT_SW','LAST_RPT_SW','TRNSMTL_NUM','FI_NUM',
                                    'ADR_VNDR_CD','FI_CREAT_DT','UTIL_CD','NPR_DT',
                                    'SPEC_IND','FI_RCPT_DT'], dtype=str)
#05
with zipfile.ZipFile(zip_path15, 'r') as z:
    with z.open(alpha15) as file08:
       df2015a = pd.read_csv(file08, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(numeric15) as file8:
       df2015n = pd.read_csv(file8, names=['RPT_REC_NUM', 'WKSHT_CD', 'LINE_NUM', 'CLMN_NUM', 'ITM_VAL_NUM'], dtype=str)
    with z.open(rpt15) as file008:
        df2015r = pd.read_csv(file008, names=['RPT_REC_NUM','PRVDR_CTRL_TYPE_CD','PRVDR_NUM','NPI',
                                    'RPT_STUS_CD','FY_BGN_DT','FY_END_DT','PROC_DT',
                                    'INITL_RPT_SW','LAST_RPT_SW','TRNSMTL_NUM','FI_NUM',
                                    'ADR_VNDR_CD','FI_CREAT_DT','UTIL_CD','NPR_DT',
                                    'SPEC_IND','FI_RCPT_DT'], dtype=str)

#build dataset
 
final_hcris_v2010 = None

for year in range(2010, 2016):

    data_r = globals()[f"df{year}r"]
    data_n = globals()[f"df{year}n"]
    data_a = globals()[f"df{year}a"]
    final_reports = data_r[['RPT_REC_NUM', 'PRVDR_NUM', 'NPI', 'FY_BGN_DT', 'FY_END_DT', 'PROC_DT',
                                  'FI_CREAT_DT', 'RPT_STUS_CD']]
    final_reports.columns = ['report', 'provider_number', 'npi', 'fy_start', 'fy_end', 'date_processed',
                             'date_created', 'status']
    final_reports['year'] = year
    print('processing year')
    for _, row in hcris_vars.iterrows():
        hcris_data = data_n if row['source'] == 'numeric' else data_a
        val = hcris_data[(hcris_data['WKSHT_CD'] == row['WKSHT_CD']) &
                         (hcris_data['LINE_NUM'] == row['LINE_NUM']) &
                         (hcris_data['CLMN_NUM'] == row['CLMN_NUM'])][['RPT_REC_NUM', 'ITM_VAL_NUM']]
        val.columns = ['report', row['variable']]
        #if row['source'] == 'numeric':
            #final_reports[row['variable']] = final_reports[row['variable']].astype(float)
        final_reports = final_reports.merge(val, on='report', how='left')

    if final_hcris_v2010 is None:
        final_hcris_v2010 = final_reports
    else:
        final_hcris_v2010 = pd.concat([final_hcris_v2010, final_reports], ignore_index=True)
     

final_hcris_v2010.to_csv("submission1/data/output/HCRIS_v2010.csv", index=False)
