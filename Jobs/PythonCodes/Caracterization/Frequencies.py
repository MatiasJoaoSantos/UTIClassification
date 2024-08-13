import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import display
import os

faixas_tempo = [-5000, -1440, 0, 720, 1440, 2880, 4320, 5760, 7200]  # Exemplos de intervalos de tempo em horas
time_labels = ['<-24h', '-24-0h', '0-12h', '12-24h', '24-48h', '48-72h', '72-96h', '>96h']  # Rótulos para cada intervalo

path = "/home_cerberus/disk2/haniel.botelho/uploads/Downloads/physionet.org/files/eicu-crd/2.0/"

df_vars = pd.read_csv(path + "TabelaVars.csv")

tables = df_vars['table'].unique()

for table in tables:
    df = pd.read_csv(path + table + ".csv")
    df_filtered = df_vars[df_vars['table'] == table]

    totalpatients = df['patientunitstayid'].nunique()

    for index, row in df_filtered.iterrows():
        var_procurada = row['var']
        column_time = row['col_time']
        column_var_name = row['col_var']

        df_filtrado = df[df[column_var_name].str.contains(var_procurada)].copy()

        counting = df_filtrado['patientunitstayid'].value_counts()

        cincMostFreq = counting.value_counts().sort_values(ascending=False).head(5)

        # Plotar o histograma
        plt.figure(figsize=(12, 6))
        bars = cincMostFreq.plot(kind='bar', color='skyblue')
        plt.title(var_procurada)
        plt.xlabel('vezes coletadas')
        plt.ylabel('numero de pacientes')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Adicionar anotações sobre as barras
        for i, val in enumerate(cincMostFreq.values):
            plt.text(i, val + 0.05 * val, f'{val}', ha='center', va='bottom')

        maiorfreq = cincMostFreq.iloc[0]

        plt.text(3.6, maiorfreq - 0*(maiorfreq/20), f"a: {df_vars.at[index, 'totalpatients']}", fontsize=12, color='black')
        plt.text(3.6, maiorfreq - 1*(maiorfreq/20), f"b: {df_vars.at[index, 'totalexampatients']}", fontsize=12, color='black')
        plt.text(3.6, maiorfreq - 2*(maiorfreq/20), f"c: {df_vars.at[index, '%exampatients']}", fontsize=12, color='black')
        plt.text(3.6, maiorfreq - 3*(maiorfreq/20), f"d: {df_vars.at[index, 'modal_colect']}", fontsize=12, color='black')
        plt.text(3.6, maiorfreq - 4*(maiorfreq/20), f"e: {df_vars.at[index, 'percent_modal']}", fontsize=12, color='black')
        plt.text(3.6, maiorfreq - 5*(maiorfreq/20), f"f: {df_vars.at[index, 'mean_time']}", fontsize=12, color='black')

        # Crie o diretório 'images' se ele não existir
        if not os.path.exists(os.path.join(path, 'images')):
            os.makedirs(os.path.join(path, 'images'))
        
        if not os.path.exists(os.path.join(path, 'images', 'freqs')):
            os.makedirs(os.path.join(path, 'images', 'freqs'))

        # Salve o gráfico
        file_path = os.path.join(path, 'images', 'freqs', f'freq_{var_procurada}.png')
        plt.savefig(file_path)
    
        plt.show()

df_vars.to_csv("TabelaVars.csv", index=False)
