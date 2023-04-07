import pandas as pd
import json
import os
from datetime import datetime
from shutil import rmtree
from pathlib import Path

fullfilename_csv = os.path.join('.','data_org','CD','export_subjects_fmri_corr_rep_measures_03.csv')
fullfilename_json = os.path.join('.','data_org','CD','export_fmri_corr_rep_measures.json')
df = pd.read_csv(fullfilename_csv, sep = '|', encoding='utf8', engine='python')
print(df.head())
with open(fullfilename_json) as f:
    data = json.load(f)


print(f"type(data)={type(data)}")
for key in data:
    print(f"{key}")

for key in data:
    print(f"{key} : {data[key]}")





def perform_preprocessing2(outdir, df_BD=None, datafilename=None,
                           postfix="tmp", datarootpath=None):

    def get_methodname(data):
        return data["type"]

    def check_and_create_data_dir(method, postfix, datarootpath):
        rootdir = Path(datarootpath) if datarootpath is not None else Path(".")
        datadir = rootdir / method / postfix

        if datadir.exists():
            rmtree(str(datadir))
        os.makedirs(str(datadir), exist_ok=True)
        return str(datadir)

    def check_data_structure(data, df_BD, method):
        # check for consistency and eliminate empty trials and frequencies
        # TODO: Implement this function
        return data

    def extract_data_array(data, df_BD, method):
        # TODO: Implement this function
        return None

    def create_new_data_structure(data, df_BD, mdat, method):
        # TODO: Implement this function
        return None

    def save_data_structure(outdir, D):
        # TODO: Implement this function
        pass

    start_time = datetime.now()
    print("Start perform_preprocessing")

    if datafilename is None:
        datafilename = "./app/tests/testthat/data/MEG/export_conn_coh.json"
    with open(datafilename, "r") as f:
        data = json.load(f)

    if data is None:
        datafilename = "./app/tests/testthat/data/MEG/export_conn_coh.json"
        with open(datafilename, "r") as f:
            data = json.load(f)

    if df_BD is None:
        df_BD = pd.read_csv("./app/tests/testthat/data/MEG/bd.csv",
                             header=True, sep=";", check_names=False)

    method = get_methodname(data)
    outdir = check_and_create_data_dir(method, postfix, datarootpath)

    # check for consistency and eliminate empty trials and frequencies
    data = check_data_structure(data, df_BD, method)

    prepro_data = data
    prepro_df_BD = df_BD

    mdat = extract_data_array(data, df_BD, method)
    D = create_new_data_structure(data, df_BD, mdat, method)
    save_data_structure(outdir, D)

    preprocessing_time = datetime.now() - start_time
     
    return D