# ClearPass UK

**Status: foundation only. No live verification, evidence corpus, integration, or accuracy claims.**

ClearPass UK is a proposed evidence-grounded verification companion for people researching UK insurance with existing AI assistants. It separates insurance claims from consumer-stated facts, records evidence-grounded decisions and unknowns, identifies unanswered context questions, and prepares a consumer-selected handover.

The first scenario concerns UK home insurance and business stock stored in a garage. General public guidance **cannot establish individual policy cover**.

## Scope and boundaries

- Work alongside existing LLMs via a future FastMCP adapter where supported, with an independent selected-response fallback.
- Three claim statuses: `supported`, `contradicted`, `insufficient_evidence`. Only the last is a safe default in the absence of verified evidence and a justified decision.
- Distinguish `stated`, `consumer_confirmed`, and `missing_or_unclear` consumer context.
- Never assume private insurer data, pass a full chat automatically, recommend policies, or imply regulated advice or compliance approval.
- Evidence must include a real URL, exact supporting passage, scope and limitations after human review; this foundation ships **no substantive evidence records**.

## Quick start

Requires Python 3.11+.

```sh
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
```

Windows activation: `.venv\Scripts\activate`.

API, Streamlit and MCP dependencies are optional for subsequent milestones. No runnable consumer product is claimed here.

## Structure

- `src/clearpass/contracts/` Pydantic schemas, stable vocabulary, validation
- `src/clearpass/services/` deliberately unimplemented engine interfaces
- `src/clearpass/adapters/` future API, MCP and UI connectors
- `data/evidence/` human-reviewed public source records
- `data/context/` consumer journey rules supplied by Fintech lead
- `data/evaluation/` independent synthetic evaluation cases
- `docs/` architecture, role instructions, evaluation protocol
- `tests/` contract, abstention and consent-boundary tests

## Workflow ownership

The AI engineer owns `src/`, `tests/` and engineering contracts. Fintech teammates contribute research, validated source excerpts, journey documentation and independent evaluation fixtures in `data/` and `docs/`; see [CONTRIBUTING.md](CONTRIBUTING.md). Changes to contracts or code need the engineer's review. Fintech contributions must never silently change gold labels or claim that evidence proves individual policy coverage.

## Implementation priorities

1. Human-reviewed evidence records and independently labelled synthetic cases.
2. One end-to-end verification path with deterministic abstention and receipts.
3. Gap rules, explicit field selection and preview for a safe handover.
4. Streamlit fallback, measured evaluation and optional MCP connection.

The supplied AI Wales challenge brief is authoritative over team implementation preferences if they conflict. See `docs/architecture/decisions.md`.

**Research prototype, not insurance advice.**
