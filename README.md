# Fake News Detector Extension – Project Overview

This project is a complete Fake News Detection system featuring:
- A browser extension (Chrome/Edge compatible)
- A machine learning API backend (FastAPI)
- Model training scripts and dataset management

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [How It Works](#how-it-works)
3. [Browser Extension](#browser-extension)
4. [API Backend](#api-backend)
5. [Dataset Url](#dataset-url)
6. [Model Training](#model-training)
7. [Setup & Installation](#setup--installation)
8. [Development Notes](#development-notes)

---

## Project Structure
```
fakenews/
├── extension/         # Chrome/Edge extension source code
│   ├── background.js
│   ├── content.js
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   └── popup.css
├── model/             # Backend and ML code
│   ├── api_server.py
│   ├── requirements.txt
│   ├── train.py
│   ├── predict.py
│   ├── results/       # Trained model and vectorizer
│   │   ├── logreg_model.joblib
│   │   └── vectorizer.joblib
│   └── ...
├── check_gpu.py       # Utility to check GPU availability
├── news_dataset.csv   # News dataset for training
└── README.md          # API documentation
```

---

## How It Works
- The browser extension extracts article text from web pages and sends it to the local FastAPI backend.
- The backend predicts whether the article is REAL or FAKE using a trained ML model.
- Results are shown in the extension popup and as a badge on the browser toolbar.

---

## Browser Extension
- **manifest.json**: Declares extension permissions and scripts.
- **content.js**: Extracts article text from web pages.
- **background.js**: Handles communication with the backend API and manages extension state.
- **popup.html / popup.js / popup.css**: User interface for displaying results and collecting feedback.

### Permissions
- ActiveTab, Scripting, Storage, and access to all URLs for analysis.

### Usage
- When you visit a news article, the extension automatically analyzes the content and displays the result in the popup.
- Feedback can be submitted via the popup.

---

## API Backend
- Built with **FastAPI** (see `model/api_server.py`).
- Loads a trained scikit-learn model and TF-IDF vectorizer.
- Endpoints:
  - `POST /predict` – Classifies input text as REAL or FAKE
  - `GET /` – Health/status check
- CORS enabled for local development.

---

## Model Training

- Link to download Dataset is https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset?resource=download

---

## Model Training
- Training script: `model/train.py`
- Uses logistic regression and TF-IDF vectorization.
- Dataset: `news_dataset.csv` (or combine `Fake.csv` and `True.csv` if present).
- Outputs: `results/logreg_model.joblib` and `results/vectorizer.joblib`

---

## Setup & Installation
### 1. Install Python Dependencies
```bash
pip install -r model/requirements.txt
```

### 2. Train or Use Existing Model
- To retrain: `python model/train.py`
- Or use the provided model files in `model/results/`

### 3. Run the API Server
```bash
cd model
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### 4. Load the Extension in Chrome/Edge
- Go to `chrome://extensions` (or Edge equivalent)
- Enable Developer Mode
- Click **Load unpacked** and select the `extension/` folder

### 5. Usage
- Visit any news article and click the extension icon to see the prediction.
- The badge will display "R" (Real), "F" (Fake), or "?" (Unknown).

---

## Development Notes
- The extension expects the API server to run at `http://127.0.0.1:8000`.
- For production, deploy the backend and update the extension API URL accordingly.
- The ML model is a baseline (logistic regression + TF-IDF); you can upgrade it for better accuracy.
- Feedback mechanism is stubbed; you can extend it to store or send user feedback.

---

## Credits
- Built using FastAPI, scikit-learn, and standard web technologies.
- BERT reference in extension (for future/optional upgrades).

---

For more details, see specific READMEs in `model/` or the API documentation.
