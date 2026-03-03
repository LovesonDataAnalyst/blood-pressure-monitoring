import pandas as pd
import random

data = []

for _ in range(5000):
    systolic = random.randint(70, 180)
    diastolic = random.randint(40, 120)

    # règles médicales
    if systolic > 140 or systolic < 90 or diastolic > 90 or diastolic < 60:
        label = 1  # anomalie
    else:
        label = 0  # normal

    data.append({
        "systolic": systolic,
        "diastolic": diastolic,
        "label": label
    })

df = pd.DataFrame(data)
df.to_csv("blood_pressure_dataset.csv", index=False)

print("Dataset généré : blood_pressure_dataset.csv")
