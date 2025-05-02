from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import os
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for local extension development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
MODEL_PATH = os.path.join(RESULTS_DIR, 'logreg_model.joblib')
VECTORIZER_PATH = os.path.join(RESULTS_DIR, 'vectorizer.joblib')

clf = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)
LABELS = {0: 'REAL', 1: 'FAKE'}

class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(req: PredictRequest):
    X = vectorizer.transform([req.text])
    pred = clf.predict(X)[0]
    if hasattr(clf, 'predict_proba'):
        conf = float(np.max(clf.predict_proba(X)))
    else:
        conf = None
    return {
        "label": LABELS.get(pred, str(pred)),
        "confidence": conf
    }

@app.get("/")
def root():
    return {"message": "Fake News Detection API is running."}
