import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from IPython.display import display
import os


path = "/home_cerberus/disk2/haniel.botelho/uploads/Downloads/physionet.org/files/eicu-crd/2.0/"
nome_imagem = 'alguma_coisa'

df_infusion = pd.read_csv(path + 'infusionDrug.csv').copy()
df_med = pd.read_csv(path + 'medication.csv').copy()

df_infusion = df_infusion['drugname'].unique()
df_med = df_med['drugname'].unique()

print(df_infusion)
print(df_med)