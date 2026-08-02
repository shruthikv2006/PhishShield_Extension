# Phishing Detection Chrome Extension using Machine Learning
This project is a browser-based phishing detection system implemented as a Chrome Extension that leverages machine learning models to identify and block phishing websites in real-time. It is part of a research initiative focused on enhancing web security through intelligent URL and content-based analysis.

**🚀 Features**

  🔍 Real-time detection of phishing URLs while browsing

  🧠 Backend powered by an optimized XGBoost machine learning model, retrained on fresh live data (PhishTank + Tranco) with 99.37% test accuracy

  📦 Lightweight frontend Chrome extension with clean UI

  📈 Extracts over 20 handcrafted features from the webpage and URL

  ⚡ FastAPI-based backend server for model inference

  🔗 REST API integration between extension and ML model

  🗄️ Cloud SQL database (Turso) for persistent scan history

**📂 Project Structure**
  📁 Frontend/ – Chrome extension frontend (HTML + JS)
  📁 backend/ – Python backend with FastAPI and XGBoost model

app.py: API endpoints (predict, predict_url, history)

url_feature_extractor.py: Feature engineering logic

scaler.pkl / xgb_model.json: Trained ML model + scaler

**🛠️ Technologies Used**
  Machine Learning: XGBoost, Scikit-learn

  Web: JavaScript, HTML, Chrome APIs

  Backend: Python, FastAPI

  Database: Turso (SQL/SQLite-based) — stores scan history (URL, result, confidence score, timestamp)

  Tools: Pandas, NumPy, Joblib

**🧪 How It Works**
  The user visits a website.

  The extension captures the URL and webpage data.

  Extracted features are sent to the FastAPI backend.

  The trained ML model predicts whether the URL is phishing or safe.

  The result is displayed to the user in real-time and saved to the database.

**🎓 Project Context**
This extension is the implementation part of a research project on phishing detection using machine learning. The goal is to build a practical, scalable solution for securing users against phishing attacks during regular browsing.

---

## 🌐 Live Deployment (This Fork)

- **Live Backend API:** https://phishshield-extension-y8f0.onrender.com
- **Status:** Live ✅ (kept awake via automated health-check pings to avoid free-tier cold starts)

### Additions & Improvements in This Fork
- Deployed the backend live to Render (Free Tier) as a working production API
- Fixed a `scikit-learn` version mismatch between the trained scaler and runtime environment for reliable, consistent predictions
- Set up automated keep-alive pinging to eliminate cold-start delays
- Debugged and validated the full end-to-end pipeline (feature extraction → scaling → prediction)
- Connected and tested the Chrome Extension against the live backend on real browsing sessions
- Retrained the ML model on fresh, live phishing URLs (PhishTank) and legitimate top-ranked domains (Tranco), achieving 99.37% test accuracy
- Integrated a cloud SQL database (Turso) to persist scan history

### 👩‍💻 Maintained By
**Shruthi Kaituri Vaidyam**

---

📜 **License**
This project is open-source and available under the MIT License. Original base project by [BKG10](https://github.com/BKG10/PhishShield_Extension).

**If you want to use this:** just download it as a zip, unzip it on your computer, enable Developer Mode in Chrome under Extensions, click "Load unpacked," and select the `Frontend` folder. Pin it and you're ready to go!
