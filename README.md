# Credit Card Fraud Detection Using Anomaly Detection Techniques
**Live Demo:** 

https://frauddetection1-goedxft4tnviaure33ogvo.streamlit.app


## Problem
Credit card fraud is rare (0.17% of transactions in this dataset) but costly.
This project compares unsupervised, semi-supervised, and supervised approaches
to detecting fraud, and shows how to properly evaluate and tune a model on
extremely imbalanced data — then ships the result as an interactive dashboard.

## Dataset
- Source: Kaggle Credit Card Fraud Detection (ULB)
- 284,807 transactions, 492 frauds (0.173%)
- Features: Time, V1–V28 (PCA-anonymized), Amount, Class (0=normal, 1=fraud)

## Method
1. **EDA**: explored class imbalance, amount distributions (fraud has lower
   median but higher mean amount than normal transactions)
2. **Preprocessing**: stratified 80/20 train/test split, RobustScaler on
   Time and Amount (fit on train only, to avoid data leakage)
3. **Models trained**:
   - Isolation Forest (unsupervised)
   - Local Outlier Factor (unsupervised)
   - Autoencoder (semi-supervised — trained on normal transactions only,
     scored by reconstruction error)
   - Random Forest (supervised, class_weight="balanced")
   - XGBoost (supervised, scale_pos_weight=577.29)
4. **Evaluation**: Precision, Recall, F1, and PR-AUC — not accuracy or
   ROC-AUC, both of which are misleading on this imbalanced data
5. **Threshold tuning** on the best model (XGBoost) to explore the
   precision/recall tradeoff and pick a business-justified operating point
6. **Interactive dashboard** (Streamlit) to explore the tradeoff live and
   test individual transactions

## Results

| Model | Type | Precision | Recall | PR-AUC |
|---|---|---|---|---|
| Isolation Forest | Unsupervised | 0.340 | 0.310 | 0.001 |
| LOF | Unsupervised | 0.020 | 0.020 | 0.005 |
| Autoencoder | Semi-supervised | — | — | 0.543 |
| Random Forest | Supervised | 0.961 | 0.745 | 0.856 |
| XGBoost (default 0.5) | Supervised | 0.882 | 0.837 | 0.880 |
| **XGBoost (threshold=0.2)** | **Supervised** | **0.850** | **0.860** | **0.880** |

**Best model: XGBoost**, with a recommended operating threshold of 0.2,
balancing recall (86%) against a manageable false-alarm rate.

## Key Findings
- Unsupervised models struggled badly. LOF in particular failed due to the
  curse of dimensionality in the 28-dimensional PCA feature space (confirmed
  by testing n_neighbors from 5 to 50, all with recall under 6%).
- The Autoencoder, trained only on normal transactions, separated fraud from
  normal clearly by reconstruction error (mean error 17.6 vs 0.185) but its
  PR-AUC (0.543) still trailed the fully supervised models — labels help.
- Supervised models performed far better, showing the value of labeled data
  when it's available.
- XGBoost slightly outperformed Random Forest overall (PR-AUC 0.880 vs 0.856)
  by trading a little precision for meaningfully higher recall.
- Pushing recall from ~86% to ~91% required lowering the decision threshold
  almost 200x, and caused false alarms to jump from 15 to 458 — steep
  diminishing returns. The last few frauds are the hardest to distinguish
  from normal behavior with these features alone.
- Top predictive features: V14, V10, V12, V17, V4.

## Dashboard
An interactive Streamlit dashboard (`src/app.py`) lets you:
- Drag the decision threshold and watch precision/recall/F1 and the
  confusion matrix update live
- View the Precision-Recall curve and top feature importances
- Load a random real transaction, tweak its top features, and see the
  model's live prediction
- Run a simplified "amount-only" risk check against an average transaction
  profile

Run it with:
cd src
streamlit run app.py


## Tech Stack
Python, pandas, NumPy, scikit-learn, XGBoost, Plotly, Streamlit

This project uses a lean runtime setup for the deployed dashboard. The optional
notebook experiments may also use TensorFlow/Keras for the Autoencoder, but the
live app itself only needs the packages in `requirements.txt`.

## Project Structure

fraud-detection/
├── data/
│ ├── creditcard.csv
│ └── processed/
├── notebooks/
│ ├── 01_eda.ipynb
│ ├── 02_preprocessing.ipynb
│ └── 03_anomaly_models.ipynb
├── src/
│ ├── app.py
│ └── xgb_model.pkl
├── README.md
└── requirements.txt


## How to Run
1. Clone/download this repo
2. Create a virtual environment: `python3 -m venv .venv && source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Download `creditcard.csv` from Kaggle (ULB Credit Card Fraud Detection)
   and place it in `data/`
5. Run the notebooks in order (01 → 02 → 03) to reproduce the models
6. Launch the dashboard from the project root or inside `src/`:
   - `cd src && streamlit run app.py`
   - or `streamlit run src/app.py` from the repository root

## Limitations & Future Work
- Anonymized features (V1–V28) limit interpretability
- No time-based split tested (data may have concept drift over time)
- Dashboard currently serves one production model (XGBoost); a true
  multi-model comparison view is a natural next step
- Model trained on a static dataset; a production system would need
  retraining strategies as fraud patterns evolve