import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import display
import os


path = "/home_cerberus/disk2/haniel.botelho/uploads/Downloads/physionet.org/files/eicu-crd/2.0/"

df_patient = pd.read_csv(path + 'patient.csv')

bins = range(-1440, 10800, 360)

# Definir o intervalo de tempo (360 minutos)
intervalo = 1440

# Criar uma lista de tempos a partir de T=0 até o tempo máximo de alta no DataFrame
tempos = list(range(1440 * 0, 1440 * 28, intervalo))

# Contar o número de pacientes ainda internados em cada intervalo de tempo
contagem_pacientes = [df_patient[df_patient['hospitaldischargeoffset'] > t].shape[0] for t in tempos]

# Plotar o gráfico de linhas
plt.figure(figsize=(20, 6))
plt.plot(tempos, contagem_pacientes, marker='o')

# Adicionar números acima dos pontos
for i, txt in enumerate(contagem_pacientes):
    plt.annotate(txt, (tempos[i], contagem_pacientes[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Adicionar títulos e rótulos
plt.title('Número de Pacientes Ainda Internados ao Longo do Tempo')
plt.xlabel('Tempo (minutos)')
plt.ylabel('Número de Pacientes')
plt.grid(True)

file_path = os.path.join(path, 'images', 'discharge.png')
plt.savefig(file_path)