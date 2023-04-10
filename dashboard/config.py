
import pandas as pd
import os, chardet


current_file = __file__  # get the path of the current file
current_folder = os.path.dirname(current_file)  # get the directory name of the current file
#data_folder = os.path.join(os.getcwd(),'..','data_dashboard','CD_20230407')
validation_data_folder = os.path.join(current_folder,'assets','validation_datasets')
general_data_folder = os.path.join(current_folder,'..','data_dashboard','CD_20230407')
datafile_christiane = os.path.join(general_data_folder,'df_main_spm_results.csv')
datafile_beer_googles = os.path.join(validation_data_folder,'beer_googles.csv')
#datafile = os.path.join(p,'beer_googles.csv')


with open(datafile_christiane, 'rb') as f:
    result = chardet.detect(f.read())
df = pd.read_csv(datafile_christiane, delimiter = '|', encoding=result['encoding'], engine='python')
df_org = df.copy()
colors = {'background-color': '#171339',
          'background-panel': '#282a52',
          'font1': '#e0e1e6',
          'bar1': '#50d1fe',
          'bar2': '#e1c758',
          'bar3': '#be5ae4',
          'bar4': '#d64646',
          'bar5': '#6ab04c',
          'mygreen': '#4ad056',
          'warning': '#f0606d',
          'positive': '#4ad056',
          'negative': '#b65165',
          'mild_warning': '#f8e9e9'
          }