# SentinelAI

> AI-driven verification and fraud detection for parametric insurance platforms — built to challenge GPS claims instead of blindly trusting them.

Parametric insurance promises instant payouts during extreme events, but the foundation is shaky: GPS data is easy to spoof. SentinelAI verifies location claims intelligently, preserving speed while protecting platforms from coordinated, large-scale attacks.

---

## Why It Matters

Attackers can spoof GPS at scale and trigger payouts across thousands of fake claims. SentinelAI detects spoofed location data, abnormal movement, and coordinated fraud rings — so honest users get fast service and fraud gets blocked early.

---

## What It Does

- Distinguishes genuine vs. spoofed location claims
- Detects abnormal movement patterns and fake GPS signals
- Identifies coordinated fraud rings through group behavior
- Assigns real-time risk scores to claims
- Protects honest users while preventing large-scale financial exploitation

---

## System Architecture

```mermaid
flowchart TD
  A[Claim Intake API] --> B[Data Layer]
  B --> C[Feature Engineering]
  C --> D[AI/ML Layer]
  D --> E[Risk Scoring]
  E --> F[Decision Engine]
  F --> G[Action Router]

  subgraph Inputs
    I1[GPS Time-Series]
    I2[Device Metadata]
    I3[Sensor Signals]
    I4[Weather Feeds]
  end

  subgraph Models
    M1[Trajectory Anomaly]
    M2[Behavior Deviation]
    M3[Graph Fraud Detection]
  end

  I1 --> B
  I2 --> B
  I3 --> B
  I4 --> B

  D --> M1
  D --> M2
  D --> M3

  G --> O1[Auto-Approve]
  G --> O2[Step-Up Verification]
  G --> O3[Manual Review]
  G --> O4[Block / Escalate]
```

---

## End-to-End Flow

```mermaid
sequenceDiagram
  participant U as Claimant Device
  participant API as Claim Intake API
  participant DL as Data Layer
  participant FE as Feature Engineering
  participant ML as AI/ML Models
  participant RS as Risk Scoring
  participant DE as Decision Engine
  participant AO as Actions

  U->>API: Submit claim + location
  API->>DL: Ingest GPS, device, sensor, weather
  DL->>FE: Normalize, clean, enrich
  FE->>ML: Build trajectories + behavior features
  ML->>RS: Scores for anomaly/behavior/device
  RS->>DE: Aggregate risk score
  DE->>AO: Approve / Step-up / Review / Block
  AO-->>U: Decision response
```

---

## Core Pipeline Details

### 1) Data Layer
- GPS time-series
- Device metadata
- Sensor signals (accelerometer, gyroscope)
- Weather APIs

### 2) Feature Engineering
- Speed and acceleration profiles
- Trajectory consistency (path smoothness, teleport jumps)
- Behavioral baselines per device
- Environmental consistency (weather vs. motion)

### 3) AI/ML Layer
- Anomaly detection for unusual movement
- Sequence modeling for realistic trajectory validation
- Graph-based detection of coordinated fraud

### 4) Risk Scoring

```
Risk = w1 * A + w2 * B + w3 * C

A = trajectory anomaly
B = behavioral deviation
C = device/network risk
```

### 5) Decision Engine
- Classifies claims into low / medium / high risk
- Balances security with user experience

---

## Fraud Ring Detection (Graph View)

```mermaid
graph TD
  C1((Claim 1)) --> D1[Device A]
  C2((Claim 2)) --> D1
  C3((Claim 3)) --> D2[Device B]
  C4((Claim 4)) --> D2
  D1 --> N1[Network Cluster X]
  D2 --> N1
  N1 --> R1[Ring Detected]
```

---

## Risk Decision Matrix

```mermaid
flowchart LR
  L[Low Risk] --> LA[Auto-Approve]
  M[Medium Risk] --> MB[Step-Up Verification]
  H[High Risk] --> HR[Manual Review or Block]
```

---

## Challenges We Ran Into

- Differentiating real anomalies (e.g., bad weather disruptions) from fraud
- Detecting coordinated attacks instead of isolated incidents
- Handling noisy and unreliable GPS data
- Staying strict on fraud without harming genuine users

---

## Accomplishments

- Built a multi-signal anti-spoofing strategy
- Detected fraud rings, not just individuals
- Balanced security with UX using risk-based decisions
- Designed for real-time, scalable deployment

---

## What We Learned

- GPS alone is not trustworthy
- Fraud detection requires pattern awareness over time
- Real-world systems must handle adversarial behavior
- Minimizing false positives is as hard as catching fraud

---

## What’s Next

- Deploy real-time ML pipelines
- Strengthen device fingerprinting and anti-emulator checks
- Introduce federated learning for privacy-aware improvements
- Stress-test against large-scale simulated attacks

---

## Team

Built with a focus on trust, speed, and fraud resilience.

---

## License

Add your license here.

---

## Quickstart (Dummy Working Project)

This repo includes a minimal FastAPI service that exposes a risk-scoring endpoint and a sample payload.

### Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Test the API

```bash
curl -s http://127.0.0.1:8000/health
```

```bash
curl -s http://127.0.0.1:8000/claims/score \
  -H "Content-Type: application/json" \
  -d @data/sample_claim.json
```

### Output

Response includes `risk_score`, `risk_band`, and model factor breakdown.

---

## UI Demo

After starting the server, open:

```
http://127.0.0.1:8000/
```

You’ll see a lightweight web UI to paste a claim payload and score it.
