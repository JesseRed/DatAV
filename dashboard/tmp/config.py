
import pandas as pd
import os, chardet


p = os.path.join(os.getcwd(),'..','..','data_dashboard','CD_20230407')
datafile = os.path.join(p,'df_main_spm_results.csv')
datafile = os.path.join(p,'beer_googles.csv')

with open(datafile, 'rb') as f:
    result = chardet.detect(f.read())
df = pd.read_csv(datafile, delimiter = '|', encoding=result['encoding'], engine='python')
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