# PROGRESS TRACKER

**Last updated:** 29 Sep 2026 (end of Session 3)
**Current step:** Phase 5 COMPLETE. Next is Phase 6 (final README/report, optional dashboard).

## Phase 0: Setup — COMPLETE
## Phase 1: Environment — COMPLETE

## Phase 2: Understand the data (EDA), notebook `01_eda.ipynb` — COMPLETE
- Loaded dataset: 284,807 rows, 31 columns, no missing values
- Class imbalance: 492 frauds = 0.173% (about 1 in 580)
- Fraud mean amount higher (~122 vs 88) but median lower (~9 vs 22)

## Phase 3: Preprocessing, notebook `02_preprocessing.ipynb` — COMPLETE
- Stratified 80/20 split (random_state=42): 394 frauds train, 98 frauds test
- RobustScaler on Time and Amount (fit on train only, transform on test)
- Saved to `data/processed/`

## Phase 4: Models, notebook `03_anomaly_models.ipynb` — COMPLETE
- [x] Isolation Forest: precision 0.34, recall 0.31, PR-AUC 0.001
- [x] Local Outlier Factor: precision ~0.02, recall ~0.02, PR-AUC 0.005 (poor fit — curse of dimensionality on 28D PCA data, confirmed across n_neighbors 5-50)
- [x] Random Forest (class_weight="balanced"): precision 0.961, recall 0.745, F1 0.839, PR-AUC 0.856
  - Top features: V14, V10, V12, V17, V4, V3, V11, V16, V2, V9
- [x] XGBoost (scale_pos_weight=577.29): precision 0.882, recall 0.837, F1 0.859, PR-AUC 0.880 — best model overall
- [ ] Autoencoder — not attempted (optional, can revisit)
- [ ] One-Class SVM — skipped by decision (slow, expected to share LOF's weaknesses)

## Phase 5: Evaluation — COMPLETE
- [x] Precision-Recall curves plotted for all 4 models, combined chart saved
- [x] PR-AUC computed for all 4 models
- [x] Threshold tuning on XGBoost:
  - Manual grid (0.1 to 0.9): precision rises 0.778 → 0.909 as threshold increases, recall stays ~0.84-0.86 then drops slightly
  - Auto-picked threshold for 90% recall target: 0.00055 → recall 0.908, precision only 0.163 (458 false alarms). Steep diminishing returns near max recall
  - **Recommended practical threshold: 0.2** → precision 0.85, recall 0.86, 15 false alarms, 84/98 frauds caught
- [x] Final summary table built (5 rows: Isolation Forest, LOF, Random Forest, XGBoost default, XGBoost threshold=0.2)

### Final Results Table
| Model | Type | Precision | Recall | PR-AUC |
|---|---|---|---|---|
| Isolation Forest | Unsupervised | 0.340 | 0.310 | 0.001 |
| LOF | Unsupervised | 0.020 | 0.020 | 0.005 |
| Random Forest | Supervised | 0.961 | 0.745 | 0.856 |
| XGBoost (default 0.5) | Supervised | 0.882 | 0.837 | 0.880 |
| XGBoost (threshold=0.2) | Supervised | 0.850 | 0.860 | 0.880 |

## Phase 6: Wrap-up — NEXT
- [ ] Write final README.md summarizing the whole project
- [ ] Interpretation write-up: unsupervised vs supervised story, hard-to-distinguish frauds, threshold tradeoff, feature importance
- [ ] Clean up notebooks (add markdown explanations)
- [ ] Optional: Autoencoder as an extra deep learning comparison
- [ ] Optional: Streamlit dashboard for live scoring demo

## Session Log
| Session | Date | What we did | Where we stopped |
|---|---|---|---|
| 1 | 28 Sep 2026 | Overview, setup, environment, EDA, preprocessing | Phase 3 done |
| 2 | 29 Sep 2026 | Isolation Forest, LOF, Random Forest, PR-AUC curves for 3 models | Phase 5 started |
| 3 | 29 Sep 2026 | XGBoost, full 4-model PR-AUC comparison, threshold tuning, final summary table | Phase 5 COMPLETE. Ready to start Phase 6 |

## Mistakes and Corrections (learn from these)
- Wrote fraud percentage as 17%. Correct value is 0.17%.
- Test set IS scaled (via `transform`, using train's fitted scaler), not left unscaled.
- Once mixed up precision vs recall when reporting numbers — always double check which metric is which.
- Minor earlier data inconsistency (support 106 vs 98 across runs) — resolved once cell execution order was consistent.
- When reading the combined PR-AUC chart, initially described XGBoost's curve as "lower" than Random Forest's when it was actually higher for most of the range (which is why its PR-AUC is higher, 0.880 vs 0.856).

## Blockers / Errors


## Next Step
Start Phase 6: draft the project README.md (problem statement, dataset, method, results table, key findings, how to run), and decide whether to add the Autoencoder model or a Streamlit dashboard before finalizing.
# PROGRESS TRACKER

**Last updated:** 30 Sep 2026 (Session 4, in progress)
**Current step:** Deployment prep almost done. Next is `git init` -> GitHub -> Streamlit Cloud.

## Phase 0-3: Setup, Environment, EDA, Preprocessing — COMPLETE
(see decisions.md for details; unchanged from earlier sessions)

## Phase 4: Models — COMPLETE (5 models)
- Isolation Forest: precision 0.34, recall 0.31, PR-AUC 0.001
- LOF: precision ~0.02, recall ~0.02, PR-AUC 0.005 (curse of dimensionality)
- Autoencoder (semi-supervised, trained on normal-only data): PR-AUC 0.543,
  reconstruction error normal=0.185 vs fraud=17.6
- Random Forest: precision 0.961, recall 0.745, F1 0.839, PR-AUC 0.856
- XGBoost: precision 0.882, recall 0.837, F1 0.859, PR-AUC 0.880 — BEST MODEL
  - Top features: V14, V10, V12, V17, V4

## Phase 5: Evaluation — COMPLETE
- All 5 models' PR curves plotted and compared
- Threshold tuning on XGBoost: recommended practical threshold = 0.2
  (precision 0.85, recall 0.86, 15 false alarms)
- Final 6-row summary table built

## Phase 6: Wrap-up — IN PROGRESS

### README — COMPLETE
Full README.md written: problem, dataset, method, results table, key
findings, dashboard section, tech stack, project structure, how to run,
limitations & future work.

### Dashboard (src/app.py) — COMPLETE, reviewed, and fixed
Built first as a simple version, then rebuilt with Gemini's help into a
richer version (Plotly charts, $ business impact metrics, feature
importance, simulated live feed, quick fraud check). Reviewed for honesty
issues and fixed:
- [x] FIX 1: Removed fake "Select Active Model" dropdown (only XGBoost is
      actually loaded) — replaced with a static info label
- [x] FIX 2: Replaced ROC-AUC curve with Precision-Recall curve (matches
      the project's established metric, avoids ROC-AUC's misleading
      optimism on imbalanced data)
- [x] FIX 3: Added clarifying captions to "Business Assumptions" (illustrative
      placeholder $ figures) and "Quick Fraud Check by Amount" (uses an
      average-feature baseline, not a real transaction pattern)
- [x] FIX 4: Live Feed Alerts — replaced np.random.choice() amounts (which
      reshuffled on every slider move) with fixed values, and replaced
      pandas .style.map() coloring with Streamlit's native column_config
      (removes a hidden jinja2 dependency risk on deployment)

### Deployment prep — IN PROGRESS
- [x] Fixed app.py to use `BASE_DIR = Path(__file__).resolve().parent`
      instead of relative "../" paths, so it works regardless of which
      directory it's launched from (important for cloud hosting)
- [x] Created a slim `requirements.txt` (only what app.py imports):
      streamlit, pandas, numpy, joblib, plotly, scikit-learn, xgboost
      (original full pip-freeze requirements.txt, which included
      tensorflow/jupyter/etc, renamed conceptually as "dev" requirements —
      NOT used for deployment)
- [x] Learned local terminal `cd` location matters for `streamlit run app.py`
      (must run from inside `src/`), but this does NOT affect deployment —
      Streamlit Cloud's "Main file path" field (`src/app.py`) handles this
- [x] Checked file sizes: X_test_for_app.csv = 30M, y_test_for_app.csv = 111K,
      xgb_model.pkl = 244K — all safely under GitHub's 100MB limit
- [x] Found and fixed an overly broad first-draft .gitignore attempt
      (`data/`, `*.csv`, `*.pkl` would have blocked files the app NEEDS)
- [x] Corrected .gitignore: excludes .venv/, __pycache__/, .DS_Store,
      data/creditcard.csv (144M raw dataset), and the full train/test CSVs
      (X_train.csv 120M, X_test.csv, y_train.csv, y_test.csv — notebook-only,
      not needed by the app) — but KEEPS X_test_for_app.csv,
      y_test_for_app.csv, and xgb_model.pkl
- [ ] Run `git init`, `git add .`, `git status` (verify creditcard.csv and
      .venv NOT staged, X_test_for_app.csv / xgb_model.pkl ARE staged)
- [ ] `git commit -m "Initial commit: fraud detection project"`
- [ ] Create GitHub repo, `git remote add origin ...`, `git push`
- [ ] Deploy on share.streamlit.io: New app -> select repo -> main file
      path "src/app.py" -> Deploy

## Session Log
| Session | Date | What we did | Where we stopped |
|---|---|---|---|
| 1 | 28 Sep 2026 | Setup, environment, EDA, preprocessing | Phase 3 done |
| 2 | 29 Sep 2026 | Isolation Forest, LOF, Random Forest, PR-AUC | Phase 5 started |
| 3 | 29 Sep 2026 | XGBoost, full comparison, threshold tuning, summary table | Phase 5 complete |
| 3b| 29-30 Sep 2026 | Autoencoder, Streamlit dashboard v1, Gemini dashboard v2 + review + fixes, README | Phase 6 mostly done |
| 4 | 30 Sep 2026 | Deployment prep: path fixes, slim requirements.txt, .gitignore correction, file size checks | About to run git init and push to GitHub |

## Mistakes and Corrections (learn from these)
- Wrote fraud percentage as 17% instead of 0.17%.
- Test set IS scaled (via `transform`, using train's fitted scaler).
- Mixed up precision vs recall once when reporting numbers.
- Misread a PR-AUC chart, thought XGBoost's curve was "lower" than Random
  Forest's when it was actually higher (hence its better PR-AUC).
- Gemini-built dashboard v2 had 3 honesty/technical issues: a non-functional
  model selector, ROC-AUC instead of PR-AUC, and an unlabeled simplification
  in the amount-check feature — all now fixed.
- First .gitignore attempt (`data/`, `*.csv`, `*.pkl`) was too broad and
  would have blocked files the app needs — fixed to name exact large files
  instead of using wildcards.
- Tried `streamlit run app.py` from the project root instead of `src/` —
  confirmed this is a local terminal quirk only, not a deployment risk.

## Blockers / Errors (resolved)
- "File does not exist: app.py" — caused by running the command from the
  wrong folder; fixed by `cd src` first. Confirmed irrelevant to deployment.

## Next Step
Run `git init`, `git add .`, `git status` — verify the staged file list is
correct — then commit, create a GitHub repo, push, and deploy via
share.streamlit.io (main file path: `src/app.py`).