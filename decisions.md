# DECISIONS LOG

Every important choice goes here with the reason, so we never re-argue it later.

| # | Date | Decision | Reason |
|---|---|---|---|
| D1 | 28 Sep 2026 | Project topic: Credit Card Fraud Detection Using Anomaly Detection Techniques | B.Tech project |
| D2 | 28 Sep 2026 | Dataset: Kaggle Credit Card Fraud Detection (ULB) | Standard, well-documented, free |
| D3 | 28 Sep 2026 | Editor: VS Code | Student's choice |
| D4 | 28 Sep 2026 | Computer: Mac (use `python3` / `pip3`) | Student's machine |
| D5 | 28 Sep 2026 | Maintain `progress.md`, `decisions.md`, `learning-notes.md`, `PROJECT_CONTEXT.md` and upload them each session | To resume work without losing context |
| D6 | 28 Sep 2026 | Use a virtual environment `.venv` inside the project | Keeps project libraries separate and clean |
| D7 | 28 Sep 2026 | Scale only `Time` and `Amount` with RobustScaler | V1 to V28 are already scaled (PCA output). RobustScaler is not thrown off by big Amount outliers |
| D8 | 28 Sep 2026 | Split data 80/20, stratified, random_state=42 | Keeps fraud ratio equal in train and test, and makes results repeatable |
| D9 | 28 Sep 2026 | Fit the scaler on train only, then apply to test | Prevents data leakage |
| D10 | 28 Sep 2026 | Save processed data in `data/processed/` | Later notebooks can load it without repeating preprocessing |
| D11 | 28 Sep 2026 | Do not use accuracy as the main metric. Use Precision, Recall, F1 and PR-AUC | Fraud is only 0.17%, so accuracy is misleading |
| D12 | 29 Sep 2026 | Isolation Forest with contamination=0.0017, n_estimators=100 | Match the real fraud rate; use many trees for stable voting |
| D13 | 29 Sep 2026 | Tested LOF with n_neighbors 5, 10, 20, 35, 50 | To rule out bad hyperparameter choice before concluding it underperforms |
| D14 | 29 Sep 2026 | Skip One-Class SVM | Slow on 56,000+ rows and expected to share LOF's high-dimension weakness |
| D15 | 29 Sep 2026 | Random Forest with class_weight="balanced" as the supervised baseline | Forces the model to pay attention to the rare fraud class instead of ignoring it |
| D16 | 29 Sep 2026 | Use PR-AUC (average_precision_score) as the main comparison metric across models, not ROC-AUC | ROC-AUC looks deceptively high on 0.17% imbalance; PR-AUC focuses on the rare positive class |

## Open Questions (to decide later)
- Random split was used for now. Should we also try a time-based split as an extra experiment?
- Still deciding whether to attempt an Autoencoder (deep learning) model
- Which deep learning library if we do: TensorFlow/Keras or PyTorch?
- Build a dashboard (Streamlit) at the end?
- Which threshold to pick for Random Forest based on a business goal (e.g. recall >= 0.9)? To be decided in next session's Step 39.

| D17 | 29 Sep 2026 | Add XGBoost as a second supervised model, using scale_pos_weight instead of class_weight | XGBoost doesn't support class_weight="balanced" like Random Forest; scale_pos_weight is its equivalent imbalance fix |
| D18 | 29 Sep 2026 | Selected XGBoost as the best overall model (PR-AUC 0.880 vs Random Forest's 0.856) | Highest PR-AUC among all 4 models tested |
| D19 | 29 Sep 2026 | Recommended practical threshold = 0.2 for XGBoost (precision 0.85, recall 0.86) instead of default 0.5 or the extreme 90%-recall threshold | Default 0.5 was arbitrary; the 90%-recall threshold (0.00055) caused 458 false alarms for only 5 extra frauds caught — poor tradeoff. 0.2 balances both reasonably |

| D20 | 29-30 Sep 2026 | Add Autoencoder (Keras/TensorFlow) as a semi-supervised model, trained only on normal transactions, scored by reconstruction error | Rounds out the model comparison with a deep-learning, label-light approach for contrast against fully supervised and fully unsupervised models |
| D21 | 30 Sep 2026 | Build a Streamlit dashboard (src/app.py) as the project's interactive deliverable, with a threshold slider, PR curve, feature importance, and a "try your own transaction" simulator | Turns the notebook results into something non-technical reviewers can click through live |
| D22 | 30 Sep 2026 | Rejected a fake "Select Active Model" dropdown, ROC-AUC display, and an unlabeled amount-only fraud checker (all from a Gemini-generated dashboard draft) | These misrepresented what the app actually does or contradicted the project's own established metric choices (PR-AUC over ROC-AUC) |
| D23 | 30 Sep 2026 | Anchor all file paths in app.py with `Path(__file__).resolve().parent` instead of relative "../" paths | Makes the app work regardless of which directory it's launched from — required for reliable cloud deployment |
| D24 | 30 Sep 2026 | Use a separate, slim requirements.txt for deployment (streamlit, pandas, numpy, joblib, plotly, scikit-learn, xgboost only) instead of the full local pip-freeze | Full environment includes TensorFlow, Jupyter, etc. — too heavy for Streamlit Cloud's free-tier build limits and unnecessary since app.py doesn't import them |
| D25 | 30 Sep 2026 | .gitignore excludes raw creditcard.csv and the full train/test notebook CSVs, but explicitly keeps X_test_for_app.csv, y_test_for_app.csv, and xgb_model.pkl | Those three files are exactly what the deployed dashboard needs to run; broad wildcard rules (*.csv, *.pkl) were rejected because they would have excluded these too |
| D26 | 30 Sep 2026 | Deploy via Streamlit Community Cloud (free), main file path set to src/app.py | Free, simple, integrates directly with GitHub |