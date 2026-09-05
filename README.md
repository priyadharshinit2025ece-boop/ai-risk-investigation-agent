# AI Risk Investigation & Early Warning Agent

An agentic AI-powered risk investigation system designed to detect emerging abnormal payment patterns, investigate connected events, explain why risk is increasing, and recommend bounded responses.

## Problem

Traditional fraud detection often focuses on individual transactions. However, emerging fraud and coordinated abuse can appear as a sequence of connected events across transactions, accounts, devices, and networks.

Our system continuously monitors transaction behaviour and investigates these connected signals before potential losses escalate.

## Core Risk Signals

1. Card-testing detection
2. Account-takeover verification
3. Device/IP relationship analysis

## Core Workflow

Transaction Stream
→ Risk Detection
→ Signal Correlation
→ AI Investigation
→ Risk Scoring
→ Early Warning
→ Explanation
→ Bounded Response
→ Audit Trail

## Main Components

- Synthetic transaction data generator
- Feature engineering pipeline
- Risk detection models
- Investigation agent
- Risk scoring engine
- Early-warning engine
- Explainable AI layer
- Response recommendation engine
- Risk monitoring dashboard
- Audit logging
- Evaluation pipeline

## Evaluation

The system will be evaluated using a held-out test dataset.

Metrics include:

- Precision
- Recall
- F1-score
- False-positive rate
- False-positive cost
- Detection latency

## Technology

- Python
- FastAPI
- Scikit-learn
- Pandas
- NumPy
- MongoDB/PostgreSQL
- React
- LLM API

## Project Status

🚧 Under Development