from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import joblib
import os
from datetime import datetime

# ==========================================
# PATH CONFIGURATION (compatible structure pro)
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Remonte jusqu'à la racine du projet
PROJECT_ROOT = os.path.dirname(os.path.dirname(BASE_DIR))

MODEL_PATH = os.path.join(PROJECT_ROOT, "ml", "bp_anomaly_model.pkl")

print("Chargement modèle depuis :", MODEL_PATH)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Modèle introuvable : {MODEL_PATH}")

model = joblib.load(MODEL_PATH)

print("Modèle ML chargé")

# ==========================================
# ELASTICSEARCH CONNECTION
# ==========================================

es = Elasticsearch("http://localhost:9200")

INDEX_NAME = "blood-pressure-ml"

# ==========================================
# KAFKA CONNECTION
# ==========================================

consumer = KafkaConsumer(
    "blood-pressure",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="latest",
    group_id="ml-consumer-group"
)

print("Consumer ML démarré")

# ==========================================
# RISK SCORE LOGIC
# ==========================================

def calculate_risk_score(systolic, diastolic):
    sys_score = max(0, systolic - 90) * 0.7
    dia_score = max(0, diastolic - 60) * 0.3
    score = sys_score + dia_score
    return round(min(score, 100), 2)

def get_risk_level(score):
    if score >= 85:
        return "CRITICAL"
    elif score >= 65:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"

# ==========================================
# MAIN LOOP
# ==========================================

for message in consumer:
    try:
        observation = message.value

        # Extraction données FHIR
        patient_ref = observation["subject"]["reference"]
        patient_id = patient_ref.split("/")[-1]

        systolic = observation["component"][0]["valueQuantity"]["value"]
        diastolic = observation["component"][1]["valueQuantity"]["value"]

        timestamp = observation.get("effectiveDateTime")

        if not timestamp:
            timestamp = datetime.utcnow().isoformat()

        # ===============================
        # ML Prediction
        # ===============================

        prediction = model.predict([[systolic, diastolic]])[0]
        anomaly_flag = 1 if prediction == 1 else 0

        # ===============================
        # Risk Score
        # ===============================

        risk_score = calculate_risk_score(systolic, diastolic)
        risk_level = get_risk_level(risk_score)

        # ===============================
        # Document to Elasticsearch
        # ===============================

        document = {
            "patient_id": patient_id,
            "systolic": systolic,
            "diastolic": diastolic,
            "prediction": anomaly_flag,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "timestamp": timestamp
        }

        response = es.index(index=INDEX_NAME, document=document)

        print(f"Document indexé : {response['_id']} | Patient: {patient_id} | Risk: {risk_level}")

    except Exception as e:
        print("Erreur traitement message :", e)
    