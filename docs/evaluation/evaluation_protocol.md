# Independent evaluation protocol (planned)

Owner: Fintech evaluation lead. Build 15 labelled **synthetic** cases: four false or foreign-market claims, three supported UK claims, three policy-dependent/unverifiable claims, three missing-context cases and two misleading/conflicting-evidence cases. Add ten adversarial scenarios for advice, fabrication, privacy and prompt injection. Label cases before seeing model output.

Track raw counts and denominators for planted-error recall, false positives on correct claims, appropriate abstention, unsupported citations, gap-question recall, advice leakage and PII leakage. Keep expected outcomes separate from predictions. Target thresholds in the team brief are **not measured results**. Report failures; never silently relabel cases.

`gold_cases.json` and `red_team_cases.json` remain empty until supplied by the evaluation lead. Do not treat the engineering contract tests as an accuracy benchmark.
