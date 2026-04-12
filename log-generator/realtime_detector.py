import pandas as pd
import time
from sklearn.ensemble import IsolationForest

print("🚀 Starting Real-Time Anomaly Detection...\n")

# Initial load
df = pd.read_csv("logs.csv", header=None)
df.columns = ["timestamp", "endpoint", "response_time", "status"]

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(df[["response_time", "status"]])

seen_rows = len(df)

while True:
    df = pd.read_csv("logs.csv", header=None)
    df.columns = ["timestamp", "endpoint", "response_time", "status"]

    new_data = df.iloc[seen_rows:]

    if not new_data.empty:
        predictions = model.predict(new_data[["response_time", "status"]])

        for i, row in new_data.iterrows():
            if predictions[i - seen_rows] == -1:
                print(f"🚨 Anomaly Detected: {row.values}")

        seen_rows = len(df)

    time.sleep(2)