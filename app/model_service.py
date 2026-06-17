from pathlib import Path
from typing import Dict, Any, List

import joblib
import numpy as np


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR / "models" / "model.joblib"


class ModelService:
    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = model_path
        self.artifact: Dict[str, Any] = {}
        self.model = None
        self.class_names: List[str] = []
        self.n_features: int = 0

    def load_model(self):
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found: {self.model_path}. "
                f"Please run: python train/train.py"
            )

        self.artifact = joblib.load(self.model_path)
        self.model = self.artifact["model"]
        self.class_names = self.artifact["class_names"]
        self.n_features = self.artifact["n_features"]

    def predict(self, features: List[float]) -> Dict[str, Any]:
        if self.model is None:
            raise RuntimeError("Model is not loaded.")

        if len(features) != self.n_features:
            raise ValueError(
                f"Expected {self.n_features} features, got {len(features)}."
            )

        x = np.array(features, dtype=float).reshape(1, -1)

        pred = self.model.predict(x)[0]
        label = int(pred)
        class_name = self.class_names[label]

        probability = None
        if hasattr(self.model, "predict_proba"):
            probability = self.model.predict_proba(x)[0].tolist()

        return {
            "label": label,
            "class_name": class_name,
            "probability": probability,
        }
    
    def batch_predict(self, samples: List[List[float]]) -> List[Dict[str, Any]]:
        results = []
        for features in samples:
            results.append(self.predict(features))
        return results
