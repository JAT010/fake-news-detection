# LEARNING NOTES (your personal glossary)

Simple explanations of every new word we meet. We add to this each session.

## Session 1

### Basics
| Word | Simple meaning |
|---|---|
| **Anomaly detection** | A security guard who learns what "normal" looks like and raises an alert when something looks strange |
| **Fraud** | A transaction the real cardholder did not make |
| **Class imbalance** | Almost all transactions are normal, only about 0.17% are fraud |
| **Dataset / CSV file** | A big table of data saved as plain text |
| **Python / VS Code / Terminal** | The language, the editor, and the command window we use |
| **Virtual environment (.venv)** | A private toolbox of libraries just for this project |
| **Library** | Code someone else already wrote that we can reuse |
| **Notebook / cell** | A file where code is written in small blocks and run with Shift + Enter |

### Data words
| Word | Simple meaning |
|---|---|
| **pandas / DataFrame (df)** | Excel controlled by code |
| **EDA** | Exploratory Data Analysis: a health check of the data |
| **Mean vs Median** | Mean = average (can be skewed by outliers); Median = middle value (more robust) |
| **Histogram** | A graph that counts values falling into buckets |
| **Outlier** | A value far from the others |

### Preprocessing words
| Word | Simple meaning |
|---|---|
| **X and y** | X = features (questions), y = labels (answer key) |
| **Train / Test set** | 80% to learn from (study material), 20% hidden to check (exam) |
| **Stratify** | Split so both sets keep the same fraud proportion |
| **Scaling / RobustScaler** | Bringing columns to similar size, robust to outliers via the median |
| **fit vs transform vs fit_transform** | fit = learn numbers; transform = apply learned numbers; fit_transform = both (train only) |
| **Data leakage** | Test-set info sneaking into training, makes results falsely good |
| **random_state=42** | Fixed shuffle so results are repeatable |

## Session 2

### Models
| Word | Simple meaning |
|---|---|
| **Isolation Forest** | Randomly splits data again and again; abnormal points get isolated faster than normal ones. Unsupervised (never sees fraud labels) |
| **Local Outlier Factor (LOF)** | Flags points sitting in unusually low-density ("sparse") neighborhoods compared to their neighbors. Unsupervised |
| **Curse of dimensionality** | In high-dimensional data (like our 28 V-columns), "distance between points" stops being meaningful, which is why LOF struggled here |
| **Random Forest** | Many decision trees vote together on yes/no questions; supervised, meaning it learns directly from the fraud labels (y_train) |
| **class_weight="balanced"** | Makes the model treat each rare fraud example as much more important during training, so it doesn't just ignore fraud |
| **Supervised vs Unsupervised** | Supervised = model sees the answer key (labels) while learning. Unsupervised = model never sees labels, only guesses from patterns |

### Evaluation words
| Word | Simple meaning |
|---|---|
| **Confusion matrix** | 2x2 table of True Negative, False Positive, False Negative, True Positive |
| **Precision** | Of everything flagged as fraud, what fraction really was fraud |
| **Recall** | Of all actual frauds, what fraction did we catch |
| **F1-score** | A single number balancing precision and recall |
| **predict_proba** | Gives a confidence score (0 to 1) instead of a hard yes/no |
| **Precision-Recall curve** | Plots precision vs recall across every possible decision threshold |
| **PR-AUC (average_precision_score)** | Summarizes the whole PR curve into one number; higher is better. Preferred over ROC-AUC on imbalanced data because ROC-AUC can look deceptively high |
| **Threshold** | The cutoff probability above which we call something "fraud" (default is usually 0.5, but it can be tuned) |

## Key Lessons
1. Never trust accuracy on imbalanced data.
2. Average can mislead; check the median too.
3. Split first, then scale. Scaler learns from train only, but IS applied to test too (via transform).
4. Unsupervised models (Isolation Forest, LOF) guess patterns without labels; supervised models (Random Forest) learn directly from labels and generally perform far better when labels are available.
5. LOF struggles badly on high-dimensional PCA data (curse of dimensionality) — confirmed by testing across 5 different n_neighbors values, not just one guess.
6. PR-AUC is the fairer metric for comparing models on rare-event problems like fraud.

## Mac Terminal Cheat Sheet
| Command | What it does |
|---|---|
| `python3 --version` | Checks if Python is installed |
| `pwd` | Shows which folder you are in |
| `ls` | Lists files in the current folder |
| `cd folder-name` | Goes into a folder |
| `cd ..` | Goes back one folder |
| `source .venv/bin/activate` | Switches on your project toolbox |
| `pip install name` | Installs a library |
| `pip freeze > requirements.txt` | Saves the list of installed libraries |

## Questions I Want to Revisit
(add your doubts here)

## Session 3

### XGBoost and boosting
| Word | Simple meaning |
|---|---|
| **XGBoost (Extreme Gradient Boosting)** | Builds trees one after another, where each new tree focuses on correcting the mistakes (residuals) of all previous trees combined |
| **Boosting vs Bagging** | Boosting (XGBoost) = trees built sequentially, each fixing prior errors. Bagging (Random Forest) = trees built independently in parallel, then averaged/voted |
| **scale_pos_weight** | XGBoost's version of class_weight; a single number (here ~577) telling the model to treat each fraud example as that many times more important |
| **eval_metric="logloss"** | The internal scoring rule XGBoost minimizes while building each tree |

### Threshold tuning
| Word | Simple meaning |
|---|---|
| **Threshold** | The probability cutoff above which a prediction is called "fraud" (default is usually 0.5) |
| **Threshold tuning** | Deliberately choosing a non-default cutoff to match a business goal (e.g. "catch at least 90% of fraud") |
| **Diminishing returns (in this context)** | Pushing recall higher and higher eventually requires a hugely lower threshold for only small recall gains, causing false alarms to explode |

## Key Lessons (continued)
7. Boosting (XGBoost) often beats bagging (Random Forest) on tabular imbalanced data by explicitly targeting past mistakes.
8. There is no single "correct" threshold — it's a business decision balancing false alarms vs missed fraud, and different thresholds should be reported side by side.
9. The hardest-to-catch frauds look statistically similar to normal transactions; squeezing them out costs a disproportionate number of false alarms. That's a data limitation, not a model flaw.
# LEARNING NOTES (your personal glossary)

Simple explanations of every new word we meet. We add to this each session.

## Session 1

### Basics
| Word | Simple meaning |
|---|---|
| **Anomaly detection** | A security guard who learns what "normal" looks like and raises an alert when something looks strange |
| **Fraud** | A transaction the real cardholder did not make |
| **Class imbalance** | Almost all transactions are normal, only about 0.17% are fraud |
| **Dataset / CSV file** | A big table of data saved as plain text |
| **Python / VS Code / Terminal** | The language, the editor, and the command window we use |
| **Virtual environment (.venv)** | A private toolbox of libraries just for this project |
| **Library** | Code someone else already wrote that we can reuse |
| **Notebook / cell** | A file where code is written in small blocks and run with Shift + Enter |

### Data words
| Word | Simple meaning |
|---|---|
| **pandas / DataFrame (df)** | Excel controlled by code |
| **EDA** | Exploratory Data Analysis: a health check of the data |
| **Mean vs Median** | Mean = average (can be skewed by outliers); Median = middle value (more robust) |
| **Histogram** | A graph that counts values falling into buckets |
| **Outlier** | A value far from the others |

### Preprocessing words
| Word | Simple meaning |
|---|---|
| **X and y** | X = features (questions), y = labels (answer key) |
| **Train / Test set** | 80% to learn from (study material), 20% hidden to check (exam) |
| **Stratify** | Split so both sets keep the same fraud proportion |
| **Scaling / RobustScaler** | Bringing columns to similar size, robust to outliers via the median |
| **fit vs transform vs fit_transform** | fit = learn numbers; transform = apply learned numbers; fit_transform = both (train only) |
| **Data leakage** | Test-set info sneaking into training, makes results falsely good |
| **random_state=42** | Fixed shuffle so results are repeatable |

## Session 2

### Models
| Word | Simple meaning |
|---|---|
| **Isolation Forest** | Randomly splits data again and again; abnormal points get isolated faster than normal ones. Unsupervised (never sees fraud labels) |
| **Local Outlier Factor (LOF)** | Flags points sitting in unusually low-density ("sparse") neighborhoods compared to their neighbors. Unsupervised |
| **Curse of dimensionality** | In high-dimensional data (like our 28 V-columns), "distance between points" stops being meaningful, which is why LOF struggled here |
| **Random Forest** | Many decision trees vote together on yes/no questions; supervised, meaning it learns directly from the fraud labels (y_train) |
| **class_weight="balanced"** | Makes the model treat each rare fraud example as much more important during training, so it doesn't just ignore fraud |
| **Supervised vs Unsupervised** | Supervised = model sees the answer key (labels) while learning. Unsupervised = model never sees labels, only guesses from patterns |

### Evaluation words
| Word | Simple meaning |
|---|---|
| **Confusion matrix** | 2x2 table of True Negative, False Positive, False Negative, True Positive |
| **Precision** | Of everything flagged as fraud, what fraction really was fraud |
| **Recall** | Of all actual frauds, what fraction did we catch |
| **F1-score** | A single number balancing precision and recall |
| **predict_proba** | Gives a confidence score (0 to 1) instead of a hard yes/no |
| **Precision-Recall curve** | Plots precision vs recall across every possible decision threshold |
| **PR-AUC (average_precision_score)** | Summarizes the whole PR curve into one number; higher is better. Preferred over ROC-AUC on imbalanced data because ROC-AUC can look deceptively high |
| **Threshold** | The cutoff probability above which we call something "fraud" (default is usually 0.5, but it can be tuned) |

## Key Lessons
1. Never trust accuracy on imbalanced data.
2. Average can mislead; check the median too.
3. Split first, then scale. Scaler learns from train only, but IS applied to test too (via transform).
4. Unsupervised models (Isolation Forest, LOF) guess patterns without labels; supervised models (Random Forest) learn directly from labels and generally perform far better when labels are available.
5. LOF struggles badly on high-dimensional PCA data (curse of dimensionality) — confirmed by testing across 5 different n_neighbors values, not just one guess.
6. PR-AUC is the fairer metric for comparing models on rare-event problems like fraud.

## Mac Terminal Cheat Sheet
| Command | What it does |
|---|---|
| `python3 --version` | Checks if Python is installed |
| `pwd` | Shows which folder you are in |
| `ls` | Lists files in the current folder |
| `cd folder-name` | Goes into a folder |
| `cd ..` | Goes back one folder |
| `source .venv/bin/activate` | Switches on your project toolbox |
| `pip install name` | Installs a library |
| `pip freeze > requirements.txt` | Saves the list of installed libraries |

## Questions I Want to Revisit
(add your doubts here)

## Session 3

### XGBoost and boosting
| Word | Simple meaning |
|---|---|
| **XGBoost (Extreme Gradient Boosting)** | Builds trees one after another, where each new tree focuses on correcting the mistakes (residuals) of all previous trees combined |
| **Boosting vs Bagging** | Boosting (XGBoost) = trees built sequentially, each fixing prior errors. Bagging (Random Forest) = trees built independently in parallel, then averaged/voted |
| **scale_pos_weight** | XGBoost's version of class_weight; a single number (here ~577) telling the model to treat each fraud example as that many times more important |
| **eval_metric="logloss"** | The internal scoring rule XGBoost minimizes while building each tree |

### Threshold tuning
| Word | Simple meaning |
|---|---|
| **Threshold** | The probability cutoff above which a prediction is called "fraud" (default is usually 0.5) |
| **Threshold tuning** | Deliberately choosing a non-default cutoff to match a business goal (e.g. "catch at least 90% of fraud") |
| **Diminishing returns (in this context)** | Pushing recall higher and higher eventually requires a hugely lower threshold for only small recall gains, causing false alarms to explode |

## Key Lessons (continued)
7. Boosting (XGBoost) often beats bagging (Random Forest) on tabular imbalanced data by explicitly targeting past mistakes.
8. There is no single "correct" threshold — it's a business decision balancing false alarms vs missed fraud, and different thresholds should be reported side by side.
9. The hardest-to-catch frauds look statistically similar to normal transactions; squeezing them out costs a disproportionate number of false alarms. That's a data limitation, not a model flaw.

## Session 4 — Deployment

### Autoencoder & dashboard words
| Word | Simple meaning |
|---|---|
| **Autoencoder** | A neural network trained to rebuild its own input; trained only on normal data so it gets good at rebuilding normal patterns and bad at rebuilding fraud |
| **Reconstruction error** | How different a rebuilt transaction is from the original — used as the fraud score (higher error = more abnormal) |
| **Bottleneck layer** | The narrowest middle layer of an autoencoder, forces the network to compress data into fewer numbers |
| **Streamlit** | A Python library that turns a plain script into a clickable web app (sliders, buttons, charts) with no HTML/JS needed |
| **st.session_state** | Streamlit's memory box — remembers a value (like a loaded transaction) across reruns, so it doesn't reset every time you move a slider |
| **st.cache_resource** | Tells Streamlit to load something (like a model) once and reuse it, instead of reloading on every interaction |

### Deployment words
| Word | Simple meaning |
|---|---|
| **Deployment** | Putting your app on a public server so anyone with a link can use it, not just you on your own computer |
| **requirements.txt** | A list of exactly which library versions your project needs, so someone else's computer (or a server) can install the same setup |
| **Git** | A tool that tracks changes to your code over time and lets you "save checkpoints" (commits) |
| **GitHub** | A website that stores your Git-tracked code online, and that deployment services (like Streamlit Cloud) read from |
| **.gitignore** | A file listing what Git should NOT track/upload (large files, secrets, junk files) |
| **git init / add / commit / push** | init = start tracking this folder; add = stage files for saving; commit = save a checkpoint with a message; push = upload it to GitHub |
| **Path(__file__).resolve().parent** | Python code that finds the folder a script physically lives in, no matter where it's run from — used to make file loading location-independent |
| **Working directory** | The folder your terminal is currently "standing in" — matters for relative commands like `streamlit run app.py`, but is separate from how the script itself locates its own files |

## Key Lessons (continued)
10. A model that's technically working can still be dishonest in presentation (e.g. a dropdown that doesn't do anything) — always check that what the UI implies is actually true.
11. Stay consistent with your own methodology — since PR-AUC was chosen over ROC-AUC for good reasons, a dashboard shouldn't quietly reintroduce ROC-AUC.
12. Deployment needs a MINIMAL requirements.txt, not your full local environment — extra unused libraries (like TensorFlow, only needed for the Autoencoder notebook) can break or slow down a cloud build.
13. .gitignore rules should be as specific as possible (exact filenames) rather than broad wildcards (*.csv), to avoid accidentally excluding files the app actually needs.
14. Local terminal folder location (cd) affects local commands but has nothing to do with how a deployed app finds its own files — those are two separate concerns.