import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

print("1. Leyendo tu archivo asl_landmarks_final.csv...")
df = pd.read_csv("asl_landmarks_final.csv")

# Separamos correctamente: 'label' es la respuesta, el resto son los números
y = df['label'].values 
X = df.drop(columns=['label']).values

print(f"2. Entrenando modelo con {len(X)} muestras...")
modelo = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
modelo.fit(X, y)

# Guardamos tu cerebro local
with open("modelo_señas.pkl", 'wb') as f:
    pickle.dump(modelo, f)

print("[✓] ¡ÉXITO TOTAL! Tu modelo 'modelo_señas.pkl' ha sido creado.")