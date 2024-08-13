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
    df_time = df_filtrado[['patientunitstayid', column_time]].copy()

    numPatientSpec = df_filtrado['patientunitstayid'].nunique()

    counting = df_filtrado['patientunitstayid'].value_counts()

    cincMostFreq = counting.value_counts().sort_values(ascending=False).head(5)
    sum = cincMostFreq.sum()
    percentModal = round(((sum/numPatientSpec) * 100), 2)

    df_time = df_time.sort_values(by=['patientunitstayid', column_time])
    df_time['previous'] = df_time.groupby('patientunitstayid')[column_time].shift(1)
    df_time['timedif'] = df_time[row['col_time']] - df_time['previous']

    valid_dif = df_time['timedif'].dropna()
    timemean = valid_dif.mean()

    maiorfreq = cincMostFreq.iloc[0]

    df_vars.at[index, 'totalpatients'] = round(totalpatients, 2)
    df_vars.at[index, 'totalexampatients'] = round(numPatientSpec, 2)
    df_vars.at[index, '%exampatients'] = round(((numPatientSpec/totalpatients)*100), 2)
    df_vars.at[index, 'modal_colect'] = round(sum, 2)
    df_vars.at[index, 'percent_modal'] = round(percentModal, 2)
    df_vars.at[index, 'mean_time'] = round(timemean, 2)

    df_filtrado['faixas'] = pd.cut(df_filtrado[column_time], bins=faixas_tempo, labels=time_labels, right=False)

    contagem_faixas = df_filtrado['faixas'].value_counts().sort_index()
    cores = plt.cm.viridis(np.linspace(0, 1, len(contagem_faixas)))

    plt.figure(figsize=(10, 6))
    plt.bar(contagem_faixas.index, contagem_faixas.values, color= cores)

    for i, valor in enumerate(contagem_faixas):
        plt.text(i, valor + 0.1, str(valor), ha='center', va='bottom')

    plt.xticks(rotation=45, ha='right')

    plt.xlabel('Tempo')
    plt.ylabel('Número de Pacientes')
    plt.title(f'Distribuição de Pacientes por Faixas para {var_procurada}')

    # Crie o diretório 'images' se ele não existir
    if not os.path.exists(os.path.join(path, 'images')):
        os.makedirs(os.path.join(path, 'images'))
        
    if not os.path.exists(os.path.join(path, 'images', 'stats')):
        os.makedirs(os.path.join(path, 'images', 'stats'))


    # Salve o gráfico
    file_path = os.path.join(path, 'images', 'stats', f'dist_{var_procurada}.png')
    plt.savefig(file_path)
    
    plt.show()

df_vars.to_csv("TabelaVars.csv", index=False)

