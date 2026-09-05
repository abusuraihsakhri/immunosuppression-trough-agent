# Immunosuppression Trough Agent

> **Domain:** Clinical Pharmacology & Precision Pharmacotherapy
> **Reference Guidelines & Standards:** CPIC Guidelines & FDA Table of Pharmacogenomic Biomarkers

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Immunosuppression Trough Agent** is an advanced analytical and computational platform implementing Post-Transplant Tacrolimus/Cyclosporine Target Trough Titrator. It provides:

- **Multi-agent consensus evaluation** of immunosuppressant trough levels
- **PHI outbound protection** with regex-based pattern detection
- **HMAC-SHA256 tamper-evident audit trail** for all evaluations
- **FastAPI REST API** for integration with clinical systems
- **CLI interface** for batch processing and interactive use

---

## 🚀 Installation

### Prerequisites
- Python 3.10, 3.11, or 3.12
- pip (Python package manager)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/immunosuppression-trough-agent.git
cd immunosuppression-trough-agent

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
pip install fastapi uvicorn pydantic pytest  # Optional: for API and testing
```

### Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set your configuration
# IMPORTANT: Generate a strong secret key for production:
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## ⚙️ Key Capabilities & Algorithmic Modules

### 🔬 Core Algorithmic & Evaluation Engines

- **`Severity`** — dedicated module for severity evaluation and state verification.
- **`DomainKnowledgeRegistry`**: Enterprise domain rules, guideline matrices, and evidence benchmarks.
- **`AgentAlert`** — dedicated module for agent alert evaluation and state verification.
- **`TroughTargetWindowAuditorAgent`**: Specialized Sub-Agent 1 for immunosuppression-trough-agent
- **`CYP3A5GenotypeModifierAgent`**: Specialized Sub-Agent 2 for immunosuppression-trough-agent
- **`DoseTitrationCalculatorAgent`**: Specialized Sub-Agent 3 for immunosuppression-trough-agent

### 🛡️ Security Architecture

- **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, emails, DOBs, and patient identifiers.
- **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
- **Path Traversal Protection:** Input validation prevents directory traversal attacks on file operations.
- **Configurable Secret Key:** Audit trail secret configurable via `AUDIT_SECRET_KEY` environment variable.

---

## 💻 CLI Quickstart & Usage

### 1. Guided Interactive Mode
```bash
python cli.py audit
```

### 2. Direct Parameterized Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 3. Batch Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail Integrity
```bash
python cli.py verify-audit
```

### 5. Chat with Supervisor
```bash
python cli.py chat "What is the system status?"
```

### 6. Launch API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
| Flag | Description | Default |
|:-----|:------------|:--------|
| `--task-id` | Unique task identifier | TASK-2026-001 |
| `--target` | Target identifier | KEY-TARGET-01 |
| `--primary` | Primary metric value (float) | 28.5 |
| `--secondary` | Secondary metric value (float) | 14.2 |
| `--critical` | Critical flag (boolean) | False |
| `--status` | Status descriptor | DISCORDANT |

### Input Data Schema (CSV Batch)

| Field | Description | Requirement |
|:------|:------------|:------------|
| `task_id` | Unique task identifier | Required |
| `target_identifier` | Target or specimen identifier | Required |
| `primary_metric` | Primary measurement value | Required |
| `secondary_metric` | Secondary measurement value | Required |
| `status_descriptor` | Status code or phenotype | Required |
| `is_critical_flag` | Emergency escalation flag | Optional |

---

## 🔌 API Endpoints

When running the server (`python cli.py serve`), the following endpoints are available:

| Method | Endpoint | Description |
|:-------|:---------|:------------|
| GET | `/health` | Health check |
| GET | `/metrics` | Prometheus-style metrics |
| POST | `/api/audit` | Submit task for evaluation |
| POST | `/api/chat` | Query supervisory chat |
| GET | `/api/audit/logs` | Get audit trail |

### Example API Usage

```bash
# Submit audit task
curl -X POST http://localhost:8000/api/audit \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "TASK-001",
    "target_identifier": "SPECIMEN-01",
    "primary_metric": 28.5,
    "secondary_metric": 14.2,
    "status_descriptor": "DISCORDANT",
    "is_critical_flag": true
  }'

# Get audit logs
curl http://localhost:8000/api/audit/logs
```

---

## 🧪 Testing & Verification

### Run All Tests
```bash
pytest -v
```

### Run Security Tests Only
```bash
pytest tests/test_security.py -v
```

### Execute High-Throughput Simulation Benchmark
```bash
python simulator.py 1000
```

---

## 🐳 Container Deployment

### Docker Build & Run
```bash
docker build -t immunosuppression-trough-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key immunosuppression-trough-agent
```

### Docker Compose
```bash
# Set your secret key
export AUDIT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 📁 Project Structure

```
immunosuppression-trough-agent/
├── agents/                    # Core agent modules
│   ├── __init__.py
│   ├── api.py                 # FastAPI REST server
│   ├── base.py                # Security, PHI guard, audit trail
│   ├── learning.py            # Bayesian calibration engine
│   ├── llm_factory.py         # LLM provider factory
│   ├── metrics.py             # Prometheus metrics
│   ├── models.py              # Pydantic data models
│   ├── streamer.py            # WebSocket telemetry
│   ├── supervisor.py          # Supervisor orchestrator
│   └── workers.py             # Specialized worker agents
├── tests/                     # Test suite
│   ├── test_immunosuppression_trough_agent.py
│   ├── test_enrichment.py
│   └── test_security.py       # Security-focused tests
├── cli.py                     # Main CLI entry point
├── simulator.py               # High-throughput simulation
├── enrichment.py              # Enrichment feature modules
├── transplant_tdm.py          # Transplant TDM module
├── immunosuppression_trough_agent_app.py
├── transplant_tdm_app.py
├── web/                       # Web dashboard
├── .env.example               # Environment configuration template
├── .github/workflows/ci.yml   # CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
