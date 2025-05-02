import sys
import os
import joblib
import numpy as np

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
MODEL_PATH = os.path.join(RESULTS_DIR, 'logreg_model.joblib')
VECTORIZER_PATH = os.path.join(RESULTS_DIR, 'vectorizer.joblib')

# Load model and vectorizer
clf = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

LABELS = {0: 'REAL', 1: 'FAKE'}

def predict(text):
    X = vectorizer.transform([text])
    pred = clf.predict(X)[0]
    if hasattr(clf, 'predict_proba'):
        conf = np.max(clf.predict_proba(X))
    else:
        conf = None
    return pred, conf

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py \"Your news text here\"")
        sys.exit(1)
    text = sys.argv[1]
    label, conf = predict(text)
    label_name = LABELS.get(label, str(label))
    if conf is not None:
        print(f"Prediction: {label_name} (confidence: {conf:.2f})")
    else:
        print(f"Prediction: {label_name}")
