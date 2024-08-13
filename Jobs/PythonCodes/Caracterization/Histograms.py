import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import display
import os


path = "/home_cerberus/disk2/haniel.botelho/uploads/Downloads/physionet.org/files/eicu-crd/2.0/"

df_vars = pd.read_csv(path + 'TabelaVars.csv')
tables = df_vars['table'].unique()

start_time = -1440
end_time = 7200
interval = 360

for table in tables:
    df = pd.read_csv(path + table + ".csv")
    df_filtered = df_vars[df_vars['table'] == table]
    totalpatients = df['patientunitstayid'].nunique()

    for index, row in df_filtered.iterrows():
        var_procurada = row['var']
        column_time = row['col_time']
        column_var_name = row['col_var']

        df_filtrado = df[df[column_var_name].str.contains(var_procurada, na=False)].copy()

        df_filtrado = df_filtrado[(df_filtrado[column_time] >= start_time) & (df_filtrado[column_time] <= end_time)]

        bins = list(range(start_time, end_time + interval, interval))

        # Crie o histograma
        plt.figure(figsize=(12, 6))
        counts, bins, _ = plt.hist(df_filtrado[column_time], bins=bins, edgecolor='k')
        for i, freq in enumerate(counts):
            plt.text(bins[i] + (bins[i+1] - bins[i]) / 2, freq + 1, str(int(freq)), fontsize=9, ha='center', va='bottom', rotation=45)
        plt.xlabel('contagem') 
        plt.ylabel('Frequência')
        plt.title(f'Histograma de {var_procurada}')

        # Crie o diretório 'images' se ele não existir
        if not os.path.exists(os.path.join(path, 'images')):
            os.makedirs(os.path.join(path, 'images'))
        
        if not os.path.exists(os.path.join(path, 'images', 'hists')):
            os.makedirs(os.path.join(path, 'images', 'hists'))

        # Salve o gráfico
        file_path = os.path.join(path, 'images', 'hists', f'histograma_{var_procurada}.png')
        plt.savefig(file_path)

        plt.show()
