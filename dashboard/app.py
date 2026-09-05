import requests
import pandas as pd
import streamlit as st


API_URL = "http://127.0.0.1:8000"


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Risk Investigation Center",
    page_icon="🛡️",
    layout="wide"
)


# ---------------------------------------------------------
# HELPER
# ---------------------------------------------------------

def get_api(endpoint):

    try:

        response = requests.get(
            f"{API_URL}{endpoint}",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException:

        return None


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🛡️ AI Risk Investigation Center")

st.caption(
    "AI-powered risk monitoring, early warning, "
    "investigation and connected-risk analysis"
)


# ---------------------------------------------------------
# API STATUS
# ---------------------------------------------------------

health = get_api("/health")

if health is None:

    st.error(
        "Backend API is not running. "
        "Start FastAPI before opening the dashboard."
    )

    st.code(
        "python -m uvicorn backend.api:app --reload"
    )

    st.stop()

else:

    st.success("Risk Intelligence API: ONLINE")


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

summary = get_api("/risk/summary")

if summary is None:

    st.error("Unable to load risk summary.")
    st.stop()


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "Total Transactions",
    summary["total_transactions"]
)

col2.metric(
    "High Risk",
    summary["high_risk_transactions"]
)

col3.metric(
    "Critical",
    summary["critical_transactions"]
)

col4.metric(
    "Early Warnings",
    summary["early_warnings"]
)

col5.metric(
    "Average Risk",
    summary["average_risk_score"]
)


st.divider()


# ---------------------------------------------------------
# RISK TIMELINE
# ---------------------------------------------------------

st.subheader("📈 Risk Evolution")

timeline_data = get_api("/risk/timeline")

if timeline_data:

    timeline = pd.DataFrame(
        timeline_data["timeline"]
    )

    if not timeline.empty:

        timeline["time_bucket"] = pd.to_datetime(
            timeline["time_bucket"]
        )

        timeline = timeline.set_index(
            "time_bucket"
        )

        st.line_chart(
            timeline[
                [
                    "average_risk",
                    "maximum_risk"
                ]
            ]
        )

else:

    st.info("No timeline data available.")


st.divider()


# ---------------------------------------------------------
# HIGH RISK TRANSACTIONS
# ---------------------------------------------------------

st.subheader("🚨 Highest-Risk Events")

transaction_data = get_api(
    "/risk/transactions?limit=20"
)

if transaction_data:

    transactions = pd.DataFrame(
        transaction_data["transactions"]
    )

    if not transactions.empty:

        display_columns = [
            column
            for column in [
                "transaction_id",
                "timestamp",
                "user_id",
                "merchant_id",
                "overall_risk_score",
                "risk_level",
                "early_warning",
                "warning_level",
                "recommended_action"
            ]
            if column in transactions.columns
        ]

        st.dataframe(
            transactions[display_columns],
            use_container_width=True,
            hide_index=True
        )

else:

    st.info("No transaction data available.")


st.divider()


# ---------------------------------------------------------
# RISK CLUSTERS
# ---------------------------------------------------------

st.subheader("🔗 Connected Risk Clusters")

cluster_data = get_api(
    "/risk/clusters"
)

if cluster_data:

    clusters = pd.DataFrame(
        cluster_data["clusters"]
    )

    if not clusters.empty:

        display_columns = [
            column
            for column in [
                "cluster_id",
                "unique_users",
                "unique_devices",
                "unique_ips",
                "risky_event_count",
                "max_risk_score",
                "cluster_risk_level",
                "explanation"
            ]
            if column in clusters.columns
        ]

        st.dataframe(
            clusters[display_columns].head(15),
            use_container_width=True,
            hide_index=True
        )

else:

    st.info("No cluster data available.")


st.divider()


# ---------------------------------------------------------
# INVESTIGATION
# ---------------------------------------------------------

st.subheader("🔎 Transaction Investigation")

transaction_id = st.text_input(
    "Enter Transaction ID",
    placeholder="Example: TX1001"
)


if transaction_id:

    investigation = get_api(
        f"/risk/transaction/{transaction_id}"
    )

    if investigation is None:

        st.warning(
            "Transaction not found."
        )

    else:

        score = investigation.get(
            "overall_risk_score",
            "N/A"
        )

        risk_level = investigation.get(
            "risk_level",
            "N/A"
        )

        priority = investigation.get(
            "investigation_priority",
            "N/A"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Risk Score",
            score
        )

        col2.metric(
            "Risk Level",
            risk_level
        )

        col3.metric(
            "Investigation Priority",
            priority
        )

        st.markdown("### 🧠 AI Investigation Explanation")

        st.info(
            investigation.get(
                "explanation",
                "No explanation available."
            )
        )

        st.markdown("### 🎯 Recommended Response")

        st.warning(
            investigation.get(
                "recommended_action",
                "No recommendation available."
            )
        )

        st.markdown("### 🔍 Evidence Source")

        st.write(
            investigation.get(
                "evidence_source",
                "Not available"
            )
        )

        st.markdown("### 🛡️ Hallucination Guard")

        st.write(
            investigation.get(
                "hallucination_guard",
                "Not available"
            )
        )


st.divider()


# ---------------------------------------------------------
# AUDIT TRAIL
# ---------------------------------------------------------

st.subheader("📋 Recent Audit Decisions")

audit_data = get_api(
    "/audit?limit=20"
)

if audit_data:

    audit = pd.DataFrame(
        audit_data["records"]
    )

    if not audit.empty:

        display_columns = [
            column
            for column in [
                "audit_id",
                "transaction_id",
                "timestamp",
                "overall_risk_score",
                "investigation_priority",
                "recommended_action",
                "audit_status"
            ]
            if column in audit.columns
        ]

        st.dataframe(
            audit[display_columns],
            use_container_width=True,
            hide_index=True
        )

else:

    st.info("No audit records available.")


st.caption(
    "Prototype system using synthetic transaction data. "
    "Risk decisions should be reviewed by authorized investigators."
)