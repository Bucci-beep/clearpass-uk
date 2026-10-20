# Architecture decisions (20 October 2026)

## ADR 001: Contract-first, modular Python
Use Pydantic for strict boundaries, small service Protocols and deterministic privacy/abstention guards. No event bus, database, vector database or orchestration framework is necessary for initial scope.

## ADR 002: Evidence is separate from conclusions
Retrieval ranks candidates; it does not establish truth. Any supported or contradicted output must be justified by a passage from a human-reviewed evidence record with an appropriate jurisdiction, scope, limitations and date. Implementation must validate evidence IDs against the loaded corpus, check passage identity, and fail closed on conflicts, stale or out-of-scope material. These checks are **not implemented yet**.

## ADR 003: Consumer-controlled handover
Consumer-supplied circumstances and independently sourced insurance claims use separate contracts. The initial preview function returns only approved consumer fact fields. Future release must add explicit display and confirmation before export. It must never add other consumer data, full chat history or free-form generated recommendations.

## ADR 004: No dependency on native MCP connectivity
MCP tools `uk_grounding`, `verify_claims`, `build_passport` are specified but not implemented. They must call the same future engine as the fallback UI. Availability on ChatGPT, Claude and other hosts depends on actual host/account support; verify rather than promise.

## ADR 005: Independent evaluation
Fintech evaluation lead defines gold labels *before* observing backend outputs. No fabricated citations, invented regulatory claims, accuracy percentages or completed compliance checks.

## MVP exclusions
No hosted model integration, claims decisions, insurer recommendations, policy guarantees, production auth or personal-data storage at foundation stage.
