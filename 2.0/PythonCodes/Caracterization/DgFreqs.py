import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import display
import os


path = "/home_cerberus/disk2/haniel.botelho/uploads/Downloads/physionet.org/files/eicu-crd/2.0/"

df_diagnosis = pd.read_csv(path + "diagnosis.csv")
column_time = 'diagnosisoffset'

counting = df_diagnosis['patientunitstayid'].value_counts()
cincMostFreq = counting.value_counts().sort_values(ascending=False).head(5)

df_time = df_diagnosis.sort_values(by=['patientunitstayid', column_time])
df_time['previous'] = df_time.groupby('patientunitstayid')[column_time].shift(1)
df_time['timedif'] = df_time[column_time] - df_time['previous']

valid_dif = df_time['timedif'].dropna()
timemean = valid_dif.mean()

plt.figure(figsize=(12, 6))
cincMostFreq.plot(kind='bar', color='skyblue')
plt.title("diagnósticos")
plt.xlabel('vezes coletadas')
plt.ylabel('numero de pacientes')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for i, val in enumerate(cincMostFreq.values):
    plt.text(i, val + 0.05 * val, f'{val}', ha='center', va='bottom')

maiorfreq = cincMostFreq.iloc[0]

plt.text(3.6, maiorfreq, f"mean_time: {round(timemean, 2)}", fontsize=12, color='black')


file_path = os.path.join(path, 'images', 'freq_diagnosis.png')
plt.savefig(file_path)
