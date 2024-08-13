import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar o arquivo .csv
data = pd.read_csv('dffinal.csv')

# Pré-processar os dados
# Codificar a variável alvo
label_encoder = LabelEncoder()
data['diagnostico'] = label_encoder.fit_transform(data['diagnostico'])

# Separar as características (X) e a variável alvo (y)
X = data.drop('diagnostico', axis=1)
y = data['diagnostico']

# Substituir valores infinitos ou extremamente grandes por NaN
X.replace([np.inf, -np.inf], np.nan, inplace=True)

# Tratar valores ausentes (substituir por média da coluna)
X.fillna(X.mean(), inplace=True)

# Dividir os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizar/normalizar os dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Treinar um modelo de aprendizado de máquina (Ex: MLP)
mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=300, random_state=42)
mlp.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
y_pred = mlp.predict(X_test)

# Avaliar o modelo
print("Acurácia:", accuracy_score(y_test, y_pred))
print("Relatório de Classificação:\n", classification_report(y_test, y_pred))

# Calcular a matriz de confusão
conf_matrix = confusion_matrix(y_test, y_pred)

# Plotar a matriz de confusão
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Matriz de Confusão')

# Salvar a matriz de confusão como imagem
plt.savefig('matriz_de_confusao.png')

# Exibir a matriz de confusão
plt.show()

# Salvar o modelo treinado (opcional)
# import joblib
# joblib.dump(mlp, 'modelo_treinado.pkl')
