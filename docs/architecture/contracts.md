# Contract notes

Canonical schemas are in `src/clearpass/contracts/models.py`. Names, enumerations and required fields are intentionally strict; proposed changes require review by the AI engineer and appropriate Fintech domain lead.

- `InsuranceClaim`: atomic insurer-related assertion, UK jurisdiction; **not** a consumer fact.
- `ConsumerFact`: declared consumer input; values are `stated`, `consumer_confirmed`, `missing_or_unclear`. Even confirmed means confirmed **by consumer**, not insurer.
- `EvidenceRecord`: proposition, URL, exact passage, passage location, retrieval date, scope, limitations and reviewer.
- `VerificationDecision`: `supported`, `contradicted`, `insufficient_evidence`; non-abstentions require a cited passage. Existence of a reference **does not** mean it was checked against the corpus; that validator is future work.
- `ContextGap`: relevant unresolved question, not a coverage verdict.
- `PassportRequest`: selected field IDs only; `PassportPreview` contains selected values and exclusion manifest.

Future adapters may expose `uk_grounding(topic, jurisdiction, context)`, `verify_claims(claims, evidence_refs)`, `build_passport(approved_fields)`. There is no working MCP, API or UI in this version.
