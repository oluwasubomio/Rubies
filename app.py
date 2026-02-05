import streamlit as st
import pandas as pd
from engine import RubiesEngine

st.set_page_config(page_title="Rubies Bank Scoring", layout="centered")
st.title("💎 Rubies Bank Customer Scoring System")

engine = RubiesEngine()

# ---------------- ADMIN SECTION ----------------
st.subheader("🧑‍💼 Admin: Upload Weekly Customer Data")

uploaded_file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    required_cols = {
        "customer_name", "savings", "balance", "transactions", "card_usage"
    }

    if not required_cols.issubset(df.columns):
        st.error("Invalid CSV format.")
    else:
        scored = engine.rank_customers(
            engine.calculate_scores(df)
        )

        scored[
            ["customer_name", "rubies_score", "rank_current", "tier"]
        ].to_json("rubies_output.json", orient="records", indent=2)

        st.success("All customers processed automatically.")
        st.dataframe(
            scored[["customer_name", "rubies_score", "rank_current", "tier"]],
            hide_index=True
        )

# ---------------- CUSTOMER SECTION ----------------
st.divider()
st.subheader("🔍 Customer: Check Your Ranking")

try:
    results = pd.read_json("rubies_output.json")
    cid = st.text_input("Enter your Customer Name")

    if cid:
        row = results[results["customer_name"] == cid]

        if row.empty:
            st.error("Customer not found.")
        else:
            st.dataframe(
                row[
                    ["customer_name", "rubies_score", "rank_current", "rank_prev", "tier"]
                ],
                hide_index=True
            )
except:
    st.info("Admin has not uploaded data yet.")
