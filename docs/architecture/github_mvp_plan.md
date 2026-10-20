# Proposed GitHub milestones and issues

These are **planning definitions**, not a claim that GitHub milestones/issues exist remotely.

## Milestone 1: Verified foundation and team inputs
1. `[Evidence] Curate reviewed UK home-business evidence records` — Fintech 1; source URL, actual narrow passage, limitation, dated retrieval, scope, reviewer; validate against EvidenceRecord.
2. `[Journey] Draft consumer gaps and approved handover fields` — Fintech 2; map 5–8 questions to explicit consumer context; mark advice boundaries.
3. `[Evaluation] Label 15 synthetic gold cases and 10 adversarial cases` — Fintech 3; independent labels, rationale, no consumer PII; lock labels before predictions.
4. `[Engineering] Enforce evidence references and scope before any claim verdict` — AI Engineer; ID lookup, passage identity, conflict and stale/out-of-scope abstention; tests.

## Milestone 2: One end-to-end MVP
5. `[Engineering] Implement local evidence retrieval and bounded verifier` — AI Engineer; first UK home-business scenario, decision receipt, abstention tests.
6. `[Engineering] Implement context gap rules and safe passport export` — AI Engineer; deterministic questions, preview, explicit selection and no unselected data.
7. `[Engineering] Add FastAPI and Streamlit selected-response fallback` — AI Engineer; same engine, basic display and reproducible smoke test.
8. `[Evaluation] Run blind cases and publish measured counts` — Fintech 3 + AI Engineer; outcomes and failures with denominators; no inflated success claims.
9. `[Engineering] Explore three FastMCP tools only if core flow is stable` — AI Engineer; host availability verified and honest fallback.
10. `[Team] Rehearse primary scenario, audit two citations, handovers and cases` — all; record limitations and show reproducible outcome.

Milestone 1 and 2 are proposed workflow stages within roughly five productive hackathon hours, **not** promises of timeline or delivery.
