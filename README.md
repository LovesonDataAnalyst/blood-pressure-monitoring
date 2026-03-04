# blood-pressure-monitoring
Real-time blood pressure monitoring system using Kafka, Elasticsearch, Kibana and Machine Learning.
 Système de Surveillance de la Pression Artérielle en Temps Réel
Kafka • Machine Learning • Elasticsearch • Kibana
 Présentation du Projet

Ce projet implémente un système de surveillance en temps réel des risques cardiovasculaires basé sur des flux de données de pression artérielle.

Il simule des constantes vitales patients, les traite via un modèle de machine learning pour détecter les anomalies, calcule un score de risque médical, puis visualise les résultats dans un dashboard Kibana en temps réel.

L’objectif est de démontrer :

Une architecture de streaming temps réel

L’intégration d’un modèle ML dans une pipeline événementielle

L’indexation optimisée dans Elasticsearch

La conception d’un dashboard métier orienté santé

Une structuration de projet proche d’un environnement production

 Architecture
Producer (Observations FHIR)
        ↓
Kafka Topic (blood-pressure)
        ↓
Consumer ML (Anomalie + Score de Risque)
        ↓
Index Elasticsearch (blood-pressure-ml)
        ↓
Dashboard Kibana (Monitoring temps réel)
⚙️ Stack Technique
Couche	Technologie
Streaming	Apache Kafka
Coordination	Zookeeper
Traitement	Python
Machine Learning	Scikit-learn
Stockage	Elasticsearch 8.12
Visualisation	Kibana
Conteneurisation	Docker Compos

📊 Fonctionnalités
🔹 Simulation Temps Réel

Observations conformes au format FHIR

Suivi longitudinal de patients

Génération continue via Kafka

🔹 Machine Learning

Modèle de détection d’anomalies entraîné

Classification binaire (normal / anomalie)

Calcul d’un score de risque médical (0–100)

Classification : LOW / MEDIUM / HIGH / CRITICAL

🔹 Indexation Elasticsearch

Chaque observation est indexée avec :

{
  "patient_id": "patient_5",
  "systolic": 164,
  "diastolic": 106,
  "prediction": 1,
  "risk_score": 60.91,
  "risk_level": "HIGH",
  "timestamp": "2026-03-03T16:40:00"
}
🔹 KPIs du Dashboard

Nombre total d’observations

Taux d’anomalies

Cas à haut risque

Évolution de la pression artérielle

Score de risque moyen

Distribution des niveaux de risque

Registre des patients les plus vulnérables

📁 Structure du Projet
blood-pressure-monitoring/
│
├── App/
│   ├── Producer/
│   │   └── producer_data_generator.py
│   ├── Consumer/
│   │   └── consumer_ml.py
│   └── Config/
│       └── thresholds.json
│
├── ML/
│   ├── train_model.py
│   ├── bp_anomaly_model.pkl
│
├── Data/
│   └── blood_pressure_dataset.csv
│
├── docker/
│   └── docker-compose.yml
│
├── kibana/
│   └── dashboard.ndjson
│
├── requirements.txt
├── README.md
└── .gitignore

🚀 Lancer le Projet
1️⃣ Démarrer l’infrastructure
docker compose up -d

Cela démarre :

Elasticsearch

Kibana

Zookeeper

Kafka

2️⃣ Lancer le Consumer ML
python App/Consumer/consumer_ml.py

Ce script :

Charge le modèle ML

Écoute le topic Kafka

Calcule anomalie + score de risque

Indexe les données dans Elasticsearch

3️⃣ Lancer le Producer
python App/Producer/producer_data_generator.py

Ce script :

Génère des observations FHIR

Les envoie vers Kafka toutes les 2 secondes

📈 Accès au Dashboard

Ouvrir :

http://localhost:5601

Index utilisé :

blood-pressure-ml
📦 Importer le Dashboard Kibana

Le fichier d’export est disponible dans :

kibana/dashboard.ndjson

Pour l’importer :

Aller dans Stack Management

Cliquer sur Saved Objects

Cliquer sur Import

Sélectionner dashboard.ndjson

🧠 Logique du Score de Risque

Formule :

sys_score = max(0, systolic - 90) * 0.7
dia_score = max(0, diastolic - 60) * 0.3
score = min(sys_score + dia_score, 100)

Classification :

Score	Niveau
< 40	LOW
40–64	MEDIUM
65–84	HIGH
≥ 85	CRITICAL
📊 Aperçu du Dashboard

<img width="959" height="414" alt="image" src="https://github.com/user-attachments/assets/f3a9800c-1753-4778-830d-642b57f176d2" />


docs/dashboard.png

Markdown :

![Dashboard](docs/dashboard.png)
🔎 Intérêt du Projet

Ce projet illustre :

Une architecture orientée événements

L’inférence ML en temps réel

Une pipeline Data Engineering complète

Une modélisation métier dans le domaine médical

Une infrastructure conteneurisée prête à être déployée

Il reflète des architectures utilisées dans :

Systèmes hospitaliers

Surveillance à distance des patients

Startups HealthTech

IoT médical

📌 Améliorations Futures

Système d’alerting (email / webhook)

Enrichissement des profils patients

API REST

Authentification et gestion des rôles

Réentraînement automatique du modèle

Pipeline CI/CD

👤 Auteur

Love-son Sauveur, Nithilan Sivaanpu, Billal Biad 

Big Data Engineering, Analyse & Bisiness Intelligence
