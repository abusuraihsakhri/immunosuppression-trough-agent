# Immunosuppression Trough Agent

Prototype rule-evaluation tools for exploring immunosuppression trough-monitoring software. The source contains several related Python entry points, a generic multi-worker evaluator, and a static browser demonstration.

**Clinical limitation:** This is **not** a validated therapeutic drug monitoring, genotype-guided dosing, or medication titration engine. Its fixed generic demonstration thresholds (primary metric >25 and secondary metric >12 in the generic worker system, with other prototype thresholds in the transplant modules) are **not** tacrolimus, cyclosporine, or everolimus reference ranges. Drug, indication, transplant type, post-transplant interval, specimen timing, units, interactions, and patient context are not modeled appropriately for clinical use. **Do not enter patient records or use outputs for treatment decisions.**

## Browser demonstration

The static demo is at [`web/index.html`](web/index.html). Open it directly in a modern browser, or serve this repository as a static site. The root `index.html` redirects to `web/` for static hosting and GitHub Pages.

The browser module:
- evaluates synthetic, unitless demonstration inputs locally using the generic workers' rules;
- distinguishes routine, elevated, and manually critical scenarios;
- validates numeric fields and synthetic identifiers;
- exports the demonstration dossier as JSON.

No Pyodide or external API is needed: the rules are simple enough to run in JavaScript. The browser page does not transmit inputs to a server or use persistent storage. It does not provide a cryptographic audit trail.

## Installation and CLI

Requires Python 3.10 or newer. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[api,dev]"
pytest -q
```

The installed `immunosuppression-trough-agent` command evaluates a generic multi-worker task:

```bash
immunosuppression-trough-agent audit --task-id DEMO-1 --target SPEC-1 --primary 10 --secondary 4 --status NOMINAL
immunosuppression-trough-agent chat "status"
immunosuppression-trough-agent verify-audit
immunosuppression-trough-agent batch -i examples.csv -o results.csv
```

Batch CSV fields: `task_id,target_identifier,primary_metric,secondary_metric,status_descriptor,is_critical_flag`. Boolean flags accept `true/false`, `yes/no`, and `1/0`. Invalid rows are skipped with a warning.

Two additional legacy demonstration entry points are provided and retain different field names and rule sets:

```bash
immunosuppression-trough-engine audit --primary 10 --secondary 4
transplant-tdm audit --primary 10 --secondary 4
```

Neither legacy entry point calculates genotype-specific doses or actual transplant drug target windows. Consult the source modules before adapting the algorithms for research.

## Local API

```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

The generic FastAPI service provides `GET /health`, `GET /metrics`, `POST /api/audit`, `POST /api/chat`, and `GET /api/audit/logs`. API schema and interactive documentation are available at `http://127.0.0.1:8000/docs` while running. Sample input:

```bash
curl -X POST http://127.0.0.1:8000/api/audit \
  -H 'Content-Type: application/json' \
  -d '{"task_id":"DEMO-1","target_identifier":"SPEC-1","primary_metric":10,"secondary_metric":4,"status_descriptor":"NOMINAL","is_critical_flag":false}'
```

The API and Python CLI use an in-memory HMAC-SHA256 audit chain; signatures are checked during integrity verification. Entries are **not persisted** across restarts. Use `AUDIT_SECRET_KEY` to configure a process key, but do not treat this memory-only chain as a durable compliance log.

**Security and privacy:** The API has no authentication and its identifier screening uses incomplete regex-based checks; it is **not HIPAA-certified, PHI-safe, or appropriate for exposed networks**. Keep it bound to localhost or behind a properly secured private gateway. Use synthetic data exclusively. The mock chat provider is deterministic and is not a clinical LLM. The Docker Compose example binds the service to localhost and requires an audit secret.

## Tests and development

```bash
python -m pip install -e ".[api,dev]"
pytest -v
node --test web/app.test.mjs
python -m compileall -q agents immunosuppression_trough_agent cli.py transplant_tdm.py
```

CI runs Python tests on 3.10–3.12 and the browser module tests. Docker deployment is optional:

```bash
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
docker compose up --build
```

The Python services use Pydantic, FastAPI, and Uvicorn; the browser demo uses standard HTML, CSS, and JavaScript. Modern desktop and mobile browsers with ES modules are supported. This is a research/software demonstration, not a regulated clinical application.

## License

[MIT](LICENSE).
