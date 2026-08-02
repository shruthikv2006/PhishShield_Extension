# ✅ Import required libraries
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
import os
import libsql_client
from datetime import datetime
from url_feature_extractor import URLFeatureExtractor

# ✅ Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load the scaler and XGBoost model
scaler = joblib.load("scaler.pkl")
booster = xgb.Booster()
booster.load_model("xgb_model.json")

FEATURE_COLUMNS = [
    "URLLength", "DomainLength", "TLDLength", "NoOfImage", "NoOfJS", "NoOfCSS",
    "NoOfSelfRef", "NoOfExternalRef", "IsHTTPS", "HasObfuscation", "HasTitle",
    "HasDescription", "HasSubmitButton", "HasSocialNet", "HasFavicon",
    "HasCopyrightInfo", "popUpWindow", "Iframe", "Abnormal_URL",
    "LetterToDigitRatio", "Redirect_0", "Redirect_1"
]

# ✅ Turso DB connection setup
TURSO_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

def get_db_client():
    http_url = TURSO_URL.replace("libsql://", "https://")
    return libsql_client.create_client_sync(url=http_url, auth_token=TURSO_TOKEN)

def init_db():
    client = get_db_client()
    client.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            result TEXT,
            score REAL,
            timestamp TEXT
        )
    """)
    client.close()

def save_scan(url, result, score):
    try:
        client = get_db_client()
        client.execute(
            "INSERT INTO scan_history (url, result, score, timestamp) VALUES (?, ?, ?, ?)",
            [url, result, score, datetime.utcnow().isoformat()]
        )
        client.close()
    except Exception as e:
        print("DB save error:", e)

init_db()

class URLFeatures(BaseModel):
    URLLength: int
    DomainLength: int
    TLDLength: int
    NoOfImage: int
    NoOfJS: int
    NoOfCSS: int
    NoOfSelfRef: int
    NoOfExternalRef: int
    IsHTTPS: int
    HasObfuscation: int
    HasTitle: int
    HasDescription: int
    HasSubmitButton: int
    HasSocialNet: int
    HasFavicon: int
    HasCopyrightInfo: int
    popUpWindow: int
    Iframe: int
    Abnormal_URL: int
    LetterToDigitRatio: float
    Redirect_0: int
    Redirect_1: int

class URLInput(BaseModel):
    url: str

@app.post("/predict")
def predict(features: URLFeatures):
    try:
        input_df = pd.DataFrame([features.dict()], columns=FEATURE_COLUMNS)
        scaled_input = scaler.transform(input_df)
        dmatrix = xgb.DMatrix(scaled_input, feature_names=FEATURE_COLUMNS)
        pred = booster.predict(dmatrix)
        label = int(round(pred[0]))
        result = "Legitimate" if label == 1 else "Phishing"

        save_scan("N/A (manual features)", result, float(pred[0]))

        return {"prediction": label, "result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/predict_url")
def predict_from_url(input_data: URLInput):
    try:
        extractor = URLFeatureExtractor(input_data.url)
        features = extractor.extract_model_features()

        if "error" in features:
            return {"error": features["error"]}

        input_df = pd.DataFrame([features], columns=FEATURE_COLUMNS)
        scaled_input = scaler.transform(input_df)
        dmatrix = xgb.DMatrix(scaled_input, feature_names=FEATURE_COLUMNS)
        pred = booster.predict(dmatrix)
        label = int(round(pred[0]))
        result = "Legitimate" if label == 1 else "Phishing"

        save_scan(input_data.url, result, float(pred[0]))

        return {"features": features, "prediction": label, "result": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/history")
def get_history(limit: int = 20):
    try:
        client = get_db_client()
        rs = client.execute(
            "SELECT url, result, score, timestamp FROM scan_history ORDER BY id DESC LIMIT ?",
            [limit]
        )
        client.close()
        history = [
            {"url": row[0], "result": row[1], "score": row[2], "timestamp": row[3]}
            for row in rs.rows
        ]
        return {"history": history}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def read_root():
    return {"message": "PhishShield API is running 🚀"}
