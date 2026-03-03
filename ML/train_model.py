import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Générer dataset réaliste
np.random.seed(42)

n = 5000

systolic = np.random.randint(90, 180, n)
diastolic = np.random.randint(60, 120, n)

pulse_pressure = systolic - diastolic

def classify(sys, dia):
    if sys > 140 or dia > 90:
        return 2  # hypertension
    elif sys < 100 or dia < 60:
        return 0  # hypotension
    else:
        return 1  # normal

labels = [classify(s, d) for s, d in zip(systolic, diastolic)]

df = pd.DataFrame({
    "systolic": systolic,
    "diastolic": diastolic,
    "pulse_pressure": pulse_pressure,
    "label": labels
})

X = df[["systolic", "diastolic", "pulse_pressure"]]
y = df["label"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

joblib.dump(model, "bp_model.pkl")

print("Modèle ML entraîné et sauvegardé")