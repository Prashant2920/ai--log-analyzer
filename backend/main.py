from fastapi import FastAPI, Response
from pydantic import BaseModel
import numpy as np
import time

from sklearn.ensemble import IsolationForest
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI()

# ------------------ Prometheus Metrics ------------------
REQUEST_COUNT = Counter("request_count_total", "Total API Requests")
ANOMALY_COUNT = Counter("anomaly_count_total", "Total Anomalies Detected")
REQUEST_TIME = Histogram(
    "request_processing_seconds",
    "Time spent processing request"
)

# ------------------ ML Model ------------------
class AnomalyModel:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)

    def train(self, data):
        self.model.fit(data)

    def predict(self, features):
        return self.model.predict([features])[0]  # -1 anomaly, 1 normal


model = AnomalyModel()

# Dummy training data (normal behavior baseline)
train_data = np.array([
    [100, 200],
    [120, 200],
    [150, 200],
    [200, 200],
    [250, 200]
])

model.train(train_data)


# ------------------ Request Schema ------------------
class Log(BaseModel):
    response_time: int
    status: int
    endpoint: str = "/unknown"


# ------------------ Feature Engineering ------------------
def transform(log: Log):
    """
    Convert log into ML features
    """
    return [
        log.response_time,
        log.status
    ]


# ------------------ Predict Endpoint ------------------
@app.post("/predict")
def predict(log: Log):
    start_time = time.time()

    REQUEST_COUNT.inc()

    features = transform(log)
    prediction = model.predict(features)

    is_anomaly = prediction == -1

    if is_anomaly:
        ANOMALY_COUNT.inc()

    response = {
        "anomaly": bool(is_anomaly),
        "endpoint": log.endpoint
    }

    # record latency
    REQUEST_TIME.observe(time.time() - start_time)

    return response


# ------------------ Metrics Endpoint ------------------
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


# ------------------ Health Check (optional but useful) ------------------
@app.get("/health")
def health():
    return {"status": "ok"}