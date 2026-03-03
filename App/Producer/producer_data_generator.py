from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime, timezone

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Patients fixes (suivi longitudinal)
patients = {
    f"patient_{i}": {
        "systolic": random.randint(110, 140),
        "diastolic": random.randint(70, 90)
    }
    for i in range(1, 11)
}

def update_pressure(patient):
    patient["systolic"] += random.randint(-3, 3)
    patient["diastolic"] += random.randint(-2, 2)

    patient["systolic"] = max(80, min(180, patient["systolic"]))
    patient["diastolic"] = max(50, min(120, patient["diastolic"]))

def build_fhir_observation(patient_id, systolic, diastolic):
    return {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "85354-9",
                    "display": "Blood pressure panel"
                }
            ]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "effectiveDateTime": datetime.now(timezone.utc).isoformat(),
        "component": [
            {
                "code": { "text": "Systolic blood pressure" },
                "valueQuantity": { "value": systolic, "unit": "mmHg" }
            },
            {
                "code": { "text": "Diastolic blood pressure" },
                "valueQuantity": { "value": diastolic, "unit": "mmHg" }
            }
        ]
    }

if __name__ == "__main__":
    while True:
        patient_id = random.choice(list(patients.keys()))
        patient = patients[patient_id]

        update_pressure(patient)

        observation = build_fhir_observation(
            patient_id,
            patient["systolic"],
            patient["diastolic"]
        )

        producer.send("blood-pressure", value=observation)
        print("Sent FHIR Observation for", patient_id)

        time.sleep(2)
