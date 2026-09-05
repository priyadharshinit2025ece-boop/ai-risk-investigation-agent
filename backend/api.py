from fastapi import FastAPI, HTTPException
import pandas as pd
from pathlib import Path


app = FastAPI(
    title="AI Risk Investigation API",
    description=(
        "Backend API for the AI Risk Investigation "
        "and Early Warning system."
    ),
    version="1.0.0"
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"


def load_csv(filename):
    path = DATA_DIR / filename

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"{filename} not found."
        )

    return pd.read_csv(path)


@app.get("/")
def root():
    return {
        "system": "AI Risk Investigation & Early Warning Agent",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/risk/summary")
def risk_summary():

    df = load_csv("response_results.csv")

    summary = {
        "total_transactions": len(df),
        "high_risk_transactions": int(
            (df["overall_risk_score"] >= 60).sum()
        ),
        "critical_transactions": int(
            (df["overall_risk_score"] >= 80).sum()
        ),
        "early_warnings": int(
            df["early_warning"].sum()
        ),
        "average_risk_score": round(
            float(df["overall_risk_score"].mean()),
            2
        )
    }

    return summary


@app.get("/risk/transactions")
def risk_transactions(limit: int = 20):

    df = load_csv("response_results.csv")

    df = df.sort_values(
        "overall_risk_score",
        ascending=False
    )

    result = df.head(limit).fillna("").to_dict(
        orient="records"
    )

    return {
        "count": len(result),
        "transactions": result
    }


@app.get("/risk/clusters")
def risk_clusters():

    df = load_csv("risk_clusters.csv")

    df = df.sort_values(
        "max_risk_score",
        ascending=False
    )

    return {
        "count": len(df),
        "clusters": df.fillna("").to_dict(
            orient="records"
        )
    }


@app.get("/risk/timeline")
def risk_timeline():

    df = load_csv("risk_timeline.csv")

    return {
        "count": len(df),
        "timeline": df.fillna("").to_dict(
            orient="records"
        )
    }


@app.get("/audit")
def audit_trail(limit: int = 50):

    df = load_csv("audit_trail.csv")

    df = df.sort_values(
        "audit_id",
        ascending=False
    )

    result = df.head(limit).fillna("").to_dict(
        orient="records"
    )

    return {
        "count": len(result),
        "records": result
    }


@app.get("/risk/transaction/{transaction_id}")
def transaction_details(transaction_id: str):

    df = load_csv("ai_investigation_reports.csv")

    result = df[
        df["transaction_id"].astype(str)
        == str(transaction_id)
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found."
        )

    return result.iloc[0].fillna("").to_dict()