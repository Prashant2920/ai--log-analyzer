from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyModel:
    def __init__(self):
        self.model = IsolationForest(contamination=0.2, random_state=42)

    def train(self, data):
        self.model.fit(data)

    def predict(self, data_point):
        pred = self.model.predict([data_point])
        return pred[0]  # -1 = anomaly, 1 = normal