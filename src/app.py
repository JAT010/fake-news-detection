import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    precision_recall_curve,
    average_precision_score
)


# =========================================================
# CONFIG
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "xgb_model.pkl"
X_TEST_PATH = BASE_DIR.parent / "data" / "processed" / "X_test_for_app.csv"
Y_TEST_PATH = BASE_DIR.parent / "data" / "processed" / "y_test_for_app.csv"

required_paths = [MODEL_PATH, X_TEST_PATH, Y_TEST_PATH]
missing_paths = [str(path) for path in required_paths if not path.exists()]

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

if missing_paths:
    st.error(
        "Missing required runtime files. Make sure the model and processed test data are present before running the app.\n\n"
        + "\n".join(f"- {path}" for path in missing_paths)
    )
    st.stop()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #080b12;
    color: #ffffff;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #0d111a;
    border-right: 1px solid #202633;
}

section[data-testid="stSidebar"] * {
    color: #ffffff;
}

/* Main title */

.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 4px;
}

.subtitle {
    color: #8d96a8;
    font-size: 14px;
    margin-bottom: 28px;
}

/* Status */

.status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0, 230, 118, 0.08);
    border: 1px solid rgba(0, 230, 118, 0.25);
    padding: 7px 12px;
    border-radius: 20px;
    color: #00e676;
    font-size: 12px;
    font-weight: 600;
}

/* KPI */

.kpi {
    background: #10151f;
    border: 1px solid #202735;
    border-radius: 14px;
    padding: 20px;
    min-height: 125px;
}

.kpi-label {
    color: #8d96a8;
    font-size: 12px;
    margin-bottom: 12px;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: white;
}

.kpi-small {
    color: #00e676;
    font-size: 11px;
    margin-top: 7px;
}

/* Section */

.section-title {
    font-size: 18px;
    font-weight: 700;
    color: white;
    margin-top: 25px;
    margin-bottom: 12px;
}

/* Cards */

.panel {
    background: #10151f;
    border: 1px solid #202735;
    border-radius: 14px;
    padding: 20px;
}

/* Fraud card */

.fraud-card {
    background: linear-gradient(
        135deg,
        #171b27,
        #10151f
    );

    border: 1px solid #272e3d;
    border-radius: 16px;
    padding: 25px;
}

.risk-number {
    font-size: 42px;
    font-weight: 800;
    color: #ff5252;
}

.high-risk {
    display: inline-block;
    background: rgba(255,82,82,0.12);
    border: 1px solid rgba(255,82,82,0.3);
    color: #ff5252;
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

/* Buttons */

.stButton > button {
    width: 100%;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #1d4ed8;
}

/* Divider */

hr {
    border-color: #202735 !important;
}

/* Dataframe */

[data-testid="stDataFrame"] {
    border: 1px solid #202735;
    border-radius: 10px;
}

/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():

    model = joblib.load(MODEL_PATH)

    X_test = pd.read_csv(X_TEST_PATH)

    y_test = pd.read_csv(Y_TEST_PATH).squeeze()

    return model, X_test, y_test


model, X_test, y_test = load_model()

scores = model.predict_proba(X_test)[:, 1]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 💳 FraudShield AI")

    st.caption("Credit Card Fraud Detection")

    st.markdown("---")

    st.markdown("### 🤖 Active Model")

    st.info("""
XGBoost

Production Model
""")

    st.markdown("### 🎚 Decision Threshold")

    threshold = st.slider(
        "Fraud threshold",
        0.00,
        1.00,
        0.20,
        0.01
    )

    st.caption(
        "Transactions above this probability "
        "are classified as fraud."
    )

    st.markdown("---")

    st.markdown("### 💰 Business Settings")

    avg_fraud_val = st.number_input(
        "Average fraud amount ($)",
        min_value=0,
        value=350,
        step=25
    )

    fp_cost = st.number_input(
        "False positive cost ($)",
        min_value=0,
        value=15,
        step=5
    )

    st.markdown("---")

    st.caption("FraudShield AI • ML Monitoring")


# =========================================================
# PREDICTIONS
# =========================================================

preds = (
    scores >= threshold
).astype(int)

precision = precision_score(
    y_test,
    preds,
    zero_division=0
)

recall = recall_score(
    y_test,
    preds,
    zero_division=0
)

f1 = f1_score(
    y_test,
    preds,
    zero_division=0
)

cm = confusion_matrix(
    y_test,
    preds
)

tn, fp, fn, tp = cm.ravel()

pr_auc = average_precision_score(
    y_test,
    scores
)

fraud_prevented = tp * avg_fraud_val

false_alarm_cost = fp * fp_cost


# =========================================================
# HEADER
# =========================================================

col1, col2 = st.columns([4, 1])

with col1:

    st.markdown(
        '<div class="main-title">💳 Credit Card Fraud Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-powered transaction monitoring and fraud risk analysis'
        '</div>',
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        '<div class="status">● MODEL ONLINE</div>',
        unsafe_allow_html=True
    )


# =========================================================
# KPI ROW
# =========================================================

k1, k2, k3, k4, k5 = st.columns(5)

with k1:

    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">PRECISION</div>
        <div class="kpi-value">{precision:.3f}</div>
        <div class="kpi-small">Model accuracy on fraud alerts</div>
    </div>
    """, unsafe_allow_html=True)


with k2:

    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">RECALL</div>
        <div class="kpi-value">{recall:.3f}</div>
        <div class="kpi-small">Fraud detection rate</div>
    </div>
    """, unsafe_allow_html=True)


with k3:

    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">F1 SCORE</div>
        <div class="kpi-value">{f1:.3f}</div>
        <div class="kpi-small">Precision / Recall balance</div>
    </div>
    """, unsafe_allow_html=True)


with k4:

    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">PR-AUC</div>
        <div class="kpi-value">{pr_auc:.3f}</div>
        <div class="kpi-small">Fraud ranking performance</div>
    </div>
    """, unsafe_allow_html=True)


with k5:

    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">FRAUD PREVENTED</div>
        <div class="kpi-value">${fraud_prevented:,.0f}</div>
        <div class="kpi-small">Illustrative estimate</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">📊 Model Performance</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns([1, 1])


# -------------------------
# Confusion Matrix
# -------------------------

with c1:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.markdown("#### Confusion Matrix")

    fig = px.imshow(
        [[tn, fp], [fn, tp]],
        x=["Predicted Normal", "Predicted Fraud"],
        y=["Actual Normal", "Actual Fraud"],
        text_auto=True,
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        height=350,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------
# PR Curve
# -------------------------

with c2:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.markdown("#### Precision-Recall Curve")

    precision_curve, recall_curve, _ = (
        precision_recall_curve(
            y_test,
            scores
        )
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=recall_curve,
            y=precision_curve,
            mode="lines",
            name=f"PR-AUC {pr_auc:.3f}"
        )
    )

    fig.update_layout(
        height=350,
        xaxis_title="Recall",
        yaxis_title="Precision",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

st.markdown(
    '<div class="section-title">🔍 Important Fraud Features</div>',
    unsafe_allow_html=True
)

if hasattr(model, "feature_importances_"):

    importance_df = pd.DataFrame({
        "Feature": X_test.columns,
        "Importance": model.feature_importances_
    })

    importance_df = (
        importance_df
        .sort_values(
            "Importance",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h"
    )

    fig.update_layout(
        height=350,
        yaxis=dict(
            autorange="reversed"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TRANSACTION CHECKER
# =========================================================

st.markdown(
    '<div class="section-title">🧪 Transaction Fraud Checker</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1, 1])


# -------------------------
# INPUT
# -------------------------

with left:

    st.markdown(
        '<div class="fraud-card">',
        unsafe_allow_html=True
    )

    st.markdown("### Transaction Details")

    amount = st.number_input(
        "Transaction Amount ($)",
        min_value=0.0,
        value=150.0,
        step=10.0
    )

    st.caption(
        "The amount is evaluated using an average-feature "
        "baseline from the test data."
    )

    if st.button(
        "🔎 Analyze Transaction"
    ):

        input_row = (
            X_test
            .mean()
            .to_frame()
            .T
        )

        if "Amount" in input_row.columns:

            input_row["Amount"] = amount

        probability = (
            model
            .predict_proba(
                input_row
            )[:, 1][0]
        )

        st.session_state["fraud_probability"] = probability

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# -------------------------
# RESULT
# -------------------------

with right:

    probability = st.session_state.get(
        "fraud_probability",
        None
    )

    st.markdown(
        '<div class="fraud-card">',
        unsafe_allow_html=True
    )

    st.markdown("### AI Risk Assessment")

    if probability is None:

        st.info(
            "Enter a transaction amount and "
            "click Analyze Transaction."
        )

    else:

        st.markdown(
            f'<div class="risk-number">'
            f'{probability * 100:.2f}%'
            f'</div>',
            unsafe_allow_html=True
        )

        st.caption("Fraud Probability")

        if probability >= threshold:

            st.markdown(
                '<span class="high-risk">'
                '🚨 HIGH RISK TRANSACTION'
                '</span>',
                unsafe_allow_html=True
            )

            st.error(
                "Decision: BLOCK TRANSACTION"
            )

        else:

            st.success(
                "Decision: APPROVE TRANSACTION"
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# RECENT ALERTS
# =========================================================

st.markdown(
    '<div class="section-title">🚨 Recent Transaction Alerts</div>',
    unsafe_allow_html=True
)

recent = X_test.head(8).copy()

recent_scores = scores[:8]

recent_df = pd.DataFrame({

    "Transaction ID":
        [f"TXN-{10001+i}" for i in range(8)],

    "Card":
        [f"**** **** **** {1200+i}" for i in range(8)],

    "Amount":
        [12.50, 420.00, 89.99, 1250.00,
         5.00, 310.20, 780.00, 45.50],

    "Risk Score":
        np.round(recent_scores, 3),

    "Status":
        np.where(
            recent_scores >= threshold,
            "🚨 BLOCKED",
            "✅ APPROVED"
        )
})

st.dataframe(
    recent_df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "FraudShield AI • Credit Card Fraud Detection "
    "• XGBoost • Streamlit"
)