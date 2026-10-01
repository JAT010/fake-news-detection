# PROJECT CONTEXT (upload this file first in every new chat)

## Instructions for Claude (read this first)
- The student is a B.Tech 3rd year student with NO prior coding experience.
- Act as a patient mentor. Explain like the student is in class 10: simple words, real-life analogies, one small step at a time.
- The student uses a **Mac** and **VS Code**. Use `python3` and `pip3` in terminal commands.
- Never skip steps. After each step, give a checkpoint and wait for confirmation.
- At the end of every session, regenerate `progress.md`, `decisions.md` and `learning-notes.md` with updates so the student can download and replace the old ones.

## Project
- **Title:** Credit Card Fraud Detection Using Anomaly Detection Techniques
- **Dataset:** Kaggle Credit Card Fraud Detection (ULB), file `creditcard.csv`
  - about 284,807 transactions, 492 frauds (about 0.17%)
  - columns: Time, V1 to V28 (anonymized), Amount, Class (0 = normal, 1 = fraud)
- **Goal:** detect fraud using anomaly detection, compare several methods, evaluate properly on imbalanced data

## Project Folder Structure
```
fraud-detection/
├── data/           <- creditcard.csv goes here
├── notebooks/      <- step-by-step experiments
├── src/            <- clean reusable code (later)
├── README.md
├── PROJECT_CONTEXT.md
├── progress.md
├── decisions.md
└── learning-notes.md
```

## Current Status
See `progress.md` for exactly where we stopped.
