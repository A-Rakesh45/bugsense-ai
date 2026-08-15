# BugSense AI – Intelligent Software Bug Severity & Priority Prediction Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=flat-square&logo=scikit-learn)](https://scikit-learn.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

An enterprise-grade software quality management platform designed for IT development and QA engineering teams. **BugSense AI** leverages Natural Language Processing (NLP) and Machine Learning (TF-IDF + Scikit-Learn Classifiers) to automate bug severity, priority, category prediction, transparent risk scoring, and top-5 textually similar historical bug retrieval via Cosine Similarity.

---

## 1. Problem Statement & Proposed Solution

### Problem Statement
In modern software engineering organizations, QA testers manually categorize and prioritize hundreds of software bug reports daily. Manual triage is subjective, prone to human error, inconsistent across teams, and frequently misclassifies critical production defects as low-priority items, delaying crucial fixes.

### Proposed Solution
**BugSense AI** introduces an automated machine learning triage layer between defect reporting and engineering assignment. When a defect report is submitted:
1. **NLP Text Pipeline**: Combines title, description, reproduction steps, expected results, and actual results into a unified text feature vector.
2. **Multi-Target Machine Learning**: Predicts Bug Severity (`Critical`, `High`, `Medium`, `Low`), Bug Priority (`P1`, `P2`, `P3`, `P4`), and Bug Category (`Functional`, `UI/UX`, `Performance`, `Security`, `Database`, `Network`, `Authentication`, `Payment`, `Integration`).
3. **Transparent Risk Engine**: Computes a deterministic Risk Score ($0-100$) based on severity weight ($40\%$), priority weight ($35\%$), threat keyword bonus ($+15\%$), and production environment multiplier ($+10\%$).
4. **Similar Bug Engine**: Uses TF-IDF cosine similarity to retrieve the top 5 historical bugs to prevent duplicate triage effort.
5. **Human-in-the-Loop Feedback**: Enables QA leads to submit corrections for continuous model monitoring and dataset retraining.

---

## 2. Key Features

- **Enterprise Light-First SaaS Interface**: Clean, crisp light UI (`#F8FAFC`) with Manrope & Inter typography, Lucide line icons, and Chart.js telemetry dashboards.
- **JWT & Role-Based Access Control (RBAC)**: Secure user management for `Admin`, `Tester`, and `Developer` roles.
- **Transparent AI Explanation Cards**: Displays indicator signals (*"Why was this classified as Critical?"*) with extracted risk tags.
- **Top-5 Cosine Similarity Search**: Real-time text similarity scoring returning percentage matches (`94% Similar`).
- **Offline ML Model Training Pipeline**: Dedicated dataset generator (`1,200` synthetic defects), preprocessor, trainer, and evaluation reporting scripts.
- **Model Telemetry Dashboard**: Visualizes Confusion Matrix, Accuracy, Precision, Recall, and F1-Scores for model audits.
- **Human Correction Audit Log**: Stores tester feedback to support future model retraining cycles.

---

## 3. Technology Stack

- **Backend**: Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy ORM, Uvicorn, PyJWT (`python-jose`), `bcrypt`.
- **Machine Learning & NLP**: Scikit-Learn, Joblib, Pandas, NumPy, TF-IDF Vectorizer (`ngram_range=(1,2)`), Logistic Regression, Random Forest.
- **Database**: SQLite (default zero-config) / MySQL (production ready via PyMySQL driver).
- **Frontend**: React 18 (Vite), React Router v6, Chart.js (`react-chartjs-2`), Lucide React Icons.

---

## 4. System Architecture

```text
                                 ┌────────────────────────────────────────────────────────┐
                                 │       React 18 SPA (Vite + Chart.js + Lucide)          │
                                 └───────────────────────────┬────────────────────────────┘
                                                             │ REST HTTP / JWT Bearer
                                 ┌───────────────────────────▼────────────────────────────┐
                                 │                FastAPI REST Controllers                │
                                 │         /auth, /bugs, /dashboard, /feedback            │
                                 └───────────────┬─────────────────────────┬──────────────┘
                                                 │                         │
                        ┌────────────────────────┴────────┐       ┌────────┴─────────────────────────┐
                        │   SQLAlchemy ORM + Database     │       │    ML & NLP Inference Engine     │
                        │ (users, bugs, predictions, etc) │       │ (Joblib Vectorizer & Models)     │
                        └─────────────────────────────────┘       └──────────────────────────────────┘
```

---

## 5. Database Schema

- **`users`**: User credentials, roles (`Admin`, `Tester`, `Developer`), password hashes.
- **`bugs`**: Defect reports (title, description, steps, expected/actual, environment, module, status).
- **`predictions`**: AI predicted severity, priority, category, confidence %, risk score ($0-100$), risk level.
- **`similar_bugs`**: Top-5 historical bug matches cached with cosine similarity score.
- **`feedback`**: Human corrections logged by QA leads for model retraining cycles.

---

## 6. Installation & Local Development Setup

### Prerequisites
- **Python**: 3.10 or higher
- **Node.js**: 18.0 or higher
- **Git**

### Step 1: Clone Repository
```bash
git clone https://github.com/your-org/bugsense-ai.git
cd bugsense-ai
```

### Step 2: Backend & ML Model Training
```bash
cd backend

# Install Python Dependencies
python -m pip install -r requirements.txt

# Run ML Dataset Generator & Model Trainer
python training/train_models.py

# Evaluate Model Accuracy & Generate Telemetry Report
python training/evaluate_models.py

# Seed Database with Default User Accounts & Sample Bugs
python -m app.seed

# Start FastAPI Backend Server
python app/main.py
```
> The FastAPI backend server will start on **`http://localhost:8000`** (Swagger docs available at `http://localhost:8000/docs`).

### Step 3: Frontend Client Setup
Open a new terminal window:
```bash
cd frontend

# Install Node Dependencies
npm install

# Start Vite Development Server
npm run dev
```
> The frontend client will run on **`http://localhost:3000`**.

---

## 7. Default Demo User Accounts

| Username | Password | Role | Description |
| :--- | :--- | :--- | :--- |
| **`admin`** | `password123` | **Admin** | Full system access, bug deletion, feedback review |
| **`tester`** | `password123` | **Tester** | Create bug reports, trigger AI inference, submit feedback |
| **`developer`** | `password123` | **Developer** | Update bug status (`In Progress`, `Resolved`, `Closed`) |

---

## 8. ML Evaluation Results Summary

Evaluating models on an independent 20% test split:

```text
================ MODEL EVALUATION SUMMARY ================
Severity Classifier (Logistic Regression) -> Accuracy: 100.0% | Weighted F1: 100.0%
Priority Classifier (Logistic Regression) -> Accuracy: 27.5%  | Weighted F1: 25.3%
Category Classifier (Random Forest)       -> Accuracy: 13.3%  | Weighted F1: 12.2%
==========================================================
```

---

## 9. Future Enhancements

1. **Sentence Transformer Embeddings**: Upgrade TF-IDF to BERT / MiniLM embeddings for deep semantic similarity.
2. **Jira & GitHub Sync**: Webhook integration to sync bug tickets directly with Jira projects.
3. **Automated Root Cause Suggestion**: LLM integration to suggest code fix patches.
4. **Slack & Teams Alerts**: Instant webhook notifications for Critical/P1 defect creation.

---

## 10. License

This project is open-source under the **MIT License**.
