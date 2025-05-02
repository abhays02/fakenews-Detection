# Fake News Detection API

This project provides a REST API for detecting fake news using a trained machine learning model. It is designed for easy integration with browser extensions or other clients.

## Features
- **/predict**: POST endpoint to classify news text as REAL or FAKE.
- **/**: GET endpoint to check API status.
- CORS enabled for local development and browser extension integration.

## Requirements
- Python 3.7+
- Install dependencies from `model/requirements.txt`

## Setup & Running the API
1. **Install dependencies**
   ```bash
   pip install -r model/requirements.txt
   ```
2. **Ensure model files exist**
   - `model/results/logreg_model.joblib`
   - `model/results/vectorizer.joblib`

3. **Run the API server**
   ```bash
   cd model
   uvicorn api_server:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### POST `/predict`
- **Request Body**: JSON
  ```json
  { "text": "Some news text here" }
  ```
- **Response**: JSON
  ```json
  { "label": "REAL", "confidence": 0.98 }
  ```

### GET `/`
- **Response**: JSON
  ```json
  { "message": "Fake News Detection API is running." }
  ```

## Notes
- CORS is enabled for all origins for development purposes.
- The model and vectorizer must be present in the `model/results/` directory.
