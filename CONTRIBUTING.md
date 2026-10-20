# Contributing to ClearPass UK

We are one AI engineer and three Fintech specialists. Work on separate branches and propose pull requests. Do not directly modify `main` for collaborative submissions.

## Fintech 1: insurance evidence
Edit `data/evidence/evidence.json` and `docs/research/`. Each evidence record must meet `EvidenceRecord` contract fields. Quote a directly checked, limited supporting passage; identify exact source and location; include URL, retrieval date, jurisdiction/scope, limitations and reviewer. Do not invent passages, infer an individual insurer's policy coverage from general sources or copy large copyrighted texts. Begin with a few useful records, not hundreds.

## Fintech 2: consumer journey and advice boundary
Edit `docs/consumer_journey/` and `data/context/coverage_context_rules.json`. Supply context questions, how each is triggered, forbidden phrasing, consent field proposals, and differences between consumer statements, public guidance and advice. Flag regulatory interpretations for legal review; avoid declaring FCA approval or blanket disclosure duties.

## Fintech 3: evaluation and pitch
Edit `data/evaluation/` and `docs/evaluation/`. Define synthetic, anonymised gold cases and adversarial cases **independently**. Preserve initial labels when evaluating. Log all results with denominators, failures and version metadata. Do not claim target figures are actual measured results.

## AI engineer
Own `src/clearpass/`, `tests/`, dependency configuration and integrations. Review contract changes, merge data submissions after validation, and run CI. When evidence or gold fixtures are submitted, add parsing checks without changing domain conclusions silently.

## Pull request checklist

- State changed files, reason and relevant source or scenario.
- Confirm no real consumer PII, secret keys or entire user conversations are committed.
- Evidence claims have human-verified URLs, exact passages and limitations.
- Gold cases were labelled before observing the verifier's output.
- `pytest -q` passes (and `ruff check .` for engineering changes).
- Request review from relevant owner; only the AI engineer changes program code.

Suggested branches: `evidence/home-business`, `journey/consent-rules`, `evaluation/gold-cases`, `engineering/mvp`.
