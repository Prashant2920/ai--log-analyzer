import pandas as pd
from sklearn.ensemble import IsolationForest

# Load logs WITH column names manually
df = pd.read_csv("logs.csv", header=None)
df.columns = ["timestamp", "endpoint", "response_time", "status"]

# Select important features
features = df[["response_time", "status"]]

# Create model
model = IsolationForest(contamination=0.1, random_state=42)

# Train model
model.fit(features)

# Predict anomalies
df["anomaly"] = model.predict(features)

# Convert output: -1 → anomaly
df["anomaly"] = df["anomaly"].apply(lambda x: 1 if x == -1 else 0)

# Show anomalies
anomalies = df[df["anomaly"] == 1]

print("\n🚨 Anomalies Detected:\n")
print(anomalies)