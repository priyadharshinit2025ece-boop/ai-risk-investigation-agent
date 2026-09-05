# AI Risk Investigation & Early Warning Agent

Detecting emerging fraud patterns, not just isolated bad transactions.

![Python](https://img.shields.io/badge/python-3.9-blue)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-teal)
![Streamlit](https://img.shields.io/badge/dashboard-Streamlit-red)
![Status](https://img.shields.io/badge/status-buildathon%20prototype-yellow)

> **Note:** This is a prototype built for the Razorpay AI Buildathon (AI Risk Manager track). It runs on synthetic transaction data, is not connected to any production payment system, and does not make final fraud decisions on its own.

---

## Overview

The AI Risk Investigation & Early Warning Agent is a prototype risk-monitoring system that goes beyond scoring individual transactions. It continuously watches transaction behaviour, looks for abnormal patterns as they emerge, connects related suspicious events across users/devices/IPs, and produces an evidence-grounded explanation of why risk is rising — along with a bounded, human-reviewable response recommendation.

The system was designed around a simple idea: most real fraud does not look suspicious one transaction at a time. It looks suspicious when you zoom out and look at patterns, timing, and relationships.

## Problem Statement

Payment platforms process large volumes of transactions every day. Fraud actors have adapted to per-transaction fraud checks by spreading their activity across:

- Many low-value transactions instead of one large one (card testing)
- Multiple devices and IP addresses to avoid single-point detection
- Slow, incremental account behaviour changes instead of one obvious takeover event
- Shared infrastructure (devices, IPs, payment identifiers) across seemingly unrelated accounts

A system that only checks "is this one transaction suspicious?" will miss all of the above, because none of the individual events looks alarming on its own.

## Why Traditional Transaction Monitoring Is Not Enough

Traditional, rule-based, transaction-level monitoring typically:

- Evaluates each transaction independently, with little to no memory of related activity
- Struggles to detect low-and-slow attacks such as card testing bursts spread over time
- Cannot easily see that ten "unrelated" accounts share the same device or IP
- Provides a decision (approve/decline/flag) without a clear, evidence-based explanation
- Offers investigators a list of alerts rather than a narrative of what is actually happening

This makes it hard for a human investigator to understand the bigger picture, prioritize their time, or trust the system's output.

## Our Solution

Our solution reframes risk detection as a continuous investigation process rather than a one-shot classification task:

1. Monitor transaction behaviour continuously and derive engineered features.
2. Run specialized detectors for card testing, account takeover, and coordinated device/IP activity.
3. Combine detector outputs into a unified risk score and risk level.
4. Track how risk evolves over time to catch emerging incidents early.
5. Build a relationship graph to expose coordinated fraud rings.
6. Generate a structured, evidence-grounded investigation report explaining the risk.
7. Recommend a bounded response (not an automatic ban or block) for human review.
8. Log every decision to an audit trail for transparency and traceability.

All of this is surfaced through a FastAPI backend and a Streamlit investigator dashboard.

## Key Features

- Card-testing detection based on rapid, low-value authorization bursts
- Account-takeover verification based on behavioural/device/location change combinations
- Coordinated fraud ring detection via a device/IP/user/merchant relationship graph
- Continuous risk monitoring with a dedicated early-warning agent
- Unified risk scoring across multiple detectors
- Risk timeline to visualize how risk builds up over time
- Structured, evidence-grounded AI investigation reports
- Bounded response recommendations with human-in-the-loop review
- Full audit trail of risk decisions and investigation history
- FastAPI backend exposing risk, cluster, timeline, and audit data
- Streamlit dashboard for end-to-end investigator workflows

## How the AI Risk Investigation Works

The AI Risk Investigation & Early Warning Agent sits at the center of the pipeline. It does not generate risk signals itself — it consumes them. Its job is to:

1. Continuously monitor the risk signals produced by the individual detectors.
2. Detect when a pattern of signals crosses from "normal noise" into "emerging abnormal behaviour."
3. Pull in related events (same entity, same cluster, same time window) to build context.
4. Combine this structured evidence into a single investigation case.
5. Generate a human-readable explanation of why the case is risky, grounded in the underlying data rather than free-form speculation.
6. Assign an investigation priority so human reviewers know what to look at first.
7. Recommend a bounded response appropriate to the risk level.
8. Write the full decision, evidence, and reasoning to the audit trail.

## Risk Detection Modules

### Card-Testing Early Warning Agent
Looks for rapid-fire, low-value authorization attempts that are characteristic of attackers testing stolen card numbers. It examines bursts of activity across cards/payment identifiers, devices, and IP addresses, and raises early warnings before larger fraudulent transactions can occur.

### Account-Takeover (ATO) Verification Agent
Looks for suspicious combinations of behavioural change, device change, location change, and transaction activity on an account. Rather than declaring an account "compromised" outright, it escalates the case with supporting evidence for investigation.

### Coordinated Fraud Ring / Device-IP Farm Detector
Looks at connections between users, devices, IP addresses, payment identifiers, and merchants. It looks for unusual concentration or sharing patterns — for example, many accounts funneling through the same device or IP — and groups these into connected suspicious clusters instead of treating each transaction independently.

## Coordinated Risk / Relationship Graph

The Risk Relationship Graph represents entities (users, devices, IPs, payment identifiers, merchants) as nodes and their interactions as edges. By examining this graph rather than isolated transactions, the system can surface coordinated activity — such as a cluster of accounts sharing infrastructure — that would be invisible to a purely transaction-level view. Graph data is exposed via `risk_graph_nodes.csv`, `risk_graph_edges.csv`, and summarized cluster information in `risk_clusters.csv`.

## Investigation and Explainability

Each investigation case produced by the AI Investigation module includes:

- The structured evidence that triggered the case
- A plain-language explanation of why the case is considered risky
- An investigation priority
- A recommended response

**Hallucination control / evidence grounding:** explanations are constructed from the structured evidence already collected by the detectors (risk signals, feature values, cluster membership, timeline events) rather than being generated freely. The goal is that every statement in an investigation report should be traceable back to a specific piece of evidence in the underlying data, reducing the risk of the system inventing reasons that are not supported by the data.

## Bounded Response and Human-in-the-Loop

The system intentionally does not make final, irreversible decisions on its own. Instead of automatically blocking a user or reversing a transaction, it recommends a bounded response — for example, flagging for manual review, temporarily limiting an action, or escalating priority — appropriate to the assessed risk level. A human investigator is expected to review the evidence and explanation before any consequential action is taken. Response outcomes are logged to `response_results.csv`.

## Audit Trail

Every risk decision and investigation is recorded to preserve transparency and traceability. The audit trail stores, for each decision:

- Risk score and risk level
- Generated explanation
- Recommended response
- Evidence source(s) used
- Decision metadata (e.g., timestamps, related case/entity identifiers)

This is stored in `audit_trail.csv` and is browsable through both the API and the dashboard, so that any recommendation can be traced back to the evidence that produced it.

## System Architecture

```
Transaction Data
      ↓
Feature Engineering
      ↓
Risk Detectors
      ↓
Risk Scoring
      ↓
Early Warning
      ↓
Risk Relationship Graph
      ↓
AI Investigation
      ↓
Response Recommendation
      ↓
Audit Trail
      ↓
FastAPI Backend
      ↓
Streamlit Investigator Dashboard
```

## End-to-End Workflow

1. Synthetic transaction data is ingested from `data/raw/`.
2. Feature engineering derives behavioural, device, and timing features, producing `features.csv`.
3. Risk detectors (card testing, ATO, coordinated fraud) evaluate these features and produce risk signals.
4. Risk scoring combines detector outputs into an overall score, written to `risk_scores.csv`.
5. The early-warning agent monitors these scores over time, generating `risk_timeline.csv` and `incident_timeline.csv` for emerging patterns.
6. The relationship graph is built from shared entities, producing `risk_graph_nodes.csv`, `risk_graph_edges.csv`, and `risk_clusters.csv`.
7. The AI Investigation module combines all of the above into structured reports, written to `ai_investigation_reports.csv`.
8. A bounded response is recommended and logged to `response_results.csv`.
9. All decisions are written to `audit_trail.csv`.
10. The FastAPI backend serves this data; the Streamlit dashboard presents it to investigators.
11. `tests/end_to_end_check.py` validates the pipeline and writes `final_test_results.csv`.

## Technology Stack

- Python 3.9
- Pandas
- NumPy
- FastAPI
- Uvicorn
- Streamlit
- Requests
- CSV-based synthetic transaction data
- Git/GitHub

## Project Structure

```
AI-Risk-Manager/
├── agents/
├── backend/
│   └── api.py
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── tests/
│   └── end_to_end_check.py
├── requirements.txt
└── README.md
```

## API Endpoints

The FastAPI backend (`backend/api.py`) currently exposes:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Service health check |
| GET | `/risk/summary` | Aggregated risk overview |
| GET | `/risk/transactions` | List of scored transactions |
| GET | `/risk/clusters` | Detected coordinated-risk clusters |
| GET | `/risk/timeline` | Risk evolution over time |
| GET | `/audit` | Audit trail of risk decisions |
| GET | `/risk/transaction/{transaction_id}` | Details for a specific transaction |

## Dashboard

The Streamlit dashboard (`dashboard/app.py`) provides:

- KPI cards summarizing current risk posture
- A risk evolution chart over time
- A view of the highest-risk transactions
- Connected risk clusters (coordinated fraud rings)
- A transaction investigation view
- The AI-generated investigation explanation
- The recommended bounded response
- Audit decision history

## Installation

Requires Python 3.9 on Windows (or any OS with an equivalent Python 3.9 environment).

```
python -m pip install -r requirements.txt
```

## How to Run

**1. Start the backend API:**

```
python -m uvicorn backend.api:app --reload
```

**2. Start the dashboard (in a separate terminal):**

```
streamlit run dashboard/app.py
```

## Testing

Run the end-to-end pipeline check:

```
python tests/end_to_end_check.py
```

This validates the pipeline stages from feature engineering through to the audit trail and writes results to `final_test_results.csv`.

## Example Investigation Flow

1. A burst of low-value authorization attempts is detected across a small set of devices and IPs — the Card-Testing Early Warning Agent raises a risk signal.
2. Around the same time, one of the associated accounts shows a location and device change combined with unusual transaction activity — the ATO Verification Agent escalates it for investigation.
3. The Coordinated Fraud Ring Detector notices that several of the involved devices and IPs are also linked to other accounts, and groups them into a cluster.
4. The Risk Scoring module combines these signals into an overall elevated risk score for the cluster.
5. The AI Risk Investigation & Early Warning Agent pulls together this evidence, generates an explanation grounded in the detected signals, assigns an investigation priority, and recommends a bounded response (e.g., flag the cluster for manual review).
6. The decision, evidence, and explanation are written to the audit trail and surfaced on the investigator dashboard.
7. A human investigator reviews the case in the dashboard and decides on the final action.

## Responsible AI and Safety

- The system is designed to support human investigators, not replace them — it does not autonomously block accounts or reverse transactions.
- Risk scores and investigation reports are treated as investigation support, not proof of fraud.
- Explanations are grounded in structured evidence already produced by the detectors, rather than generated as free-form, unverified narrative.
- Every recommendation is logged to an audit trail, so decisions can be reviewed and traced back to their evidence.
- The system currently operates on synthetic data only and has not been evaluated against real production traffic.

## Limitations

- Built and tested against synthetic transaction data, not real Razorpay production data.
- Detection logic reflects patterns the team anticipated within the buildathon timeframe and has not been validated at production scale.
- No claims are made about accuracy, false-positive/false-negative rates, or financial impact, as these have not been formally measured.
- The system does not process a live/real-time transaction stream in this prototype; it operates on batch/CSV-based data.
- The relationship graph and clustering logic are heuristic-based and may need tuning against real-world data distributions.
- The AI Investigation module's explanations are only as good as the structured evidence available to it.

## Future Improvements

- Validate detectors and scoring against real (or more realistic) transaction datasets.
- Add real-time/streaming ingestion instead of batch CSV processing.
- Expand the relationship graph with additional entity types and richer graph analytics.
- Add configurable thresholds and feedback loops so investigator decisions can improve detector tuning over time.
- Add authentication and role-based access control to the API and dashboard.
- Expand automated test coverage beyond the current end-to-end check.

## Buildathon Track Fit

This project directly targets the **AI Risk Manager** track by addressing risk management as an end-to-end, continuous process rather than a single detection task. It combines multiple specialized risk detectors, correlates them through a relationship graph, produces investigation-grade explanations, recommends bounded (not blind) responses, and maintains a full audit trail — mirroring how a real risk management function would need to operate: detect, investigate, explain, respond, and record.

## Why This Solution Is Different

- It does not stop at flagging isolated transactions — it looks for **emerging risk patterns** over time.
- It brings together **card testing, account takeover, and coordinated device/IP risk** under one investigation framework instead of treating them as separate, disconnected checks.
- It actively **investigates relationships** between users, devices, IPs, payment identifiers, and merchants rather than analyzing each transaction in isolation.
- It produces **evidence-grounded explanations**, aiming to keep the reasoning traceable to actual data rather than generic or speculative statements.
- It recommends **bounded responses** for human review instead of automatically blocking users or accounts.
- It maintains a complete **audit trail** of risk decisions for transparency and traceability.
- It gives investigators a **single, unified dashboard** covering detection, clustering, investigation, response, and audit history in one place.

## Conclusion

The AI Risk Investigation & Early Warning Agent demonstrates how a risk management system can move beyond isolated transaction scoring toward continuous, evidence-based investigation. By combining specialized detectors, a relationship graph, explainable investigation reports, bounded response recommendations, and a full audit trail, this buildathon prototype shows a practical path toward more transparent and investigator-friendly fraud risk management — while remaining clear about its current scope as a prototype built on synthetic data.