# Question Coach A/B evaluation protocol

Status: protocol only. No LLM responses or evaluation results have been collected.

Use the same independently authored, synthetic UK home-business scenario for both arms.

- Arm A: original rough question.
- Arm B: Question Coach v1 deterministic output, using the exact same scenario facts.
- Fix model provider, model identifier, model settings, run date, evidence snapshot and annotation rubric before comparing.
- Store complete test prompts and selected generated responses locally with a pseudonymous run ID. Never use real consumer information.
- Fintech evaluators should label atomic claims independently using reviewed, dated source excerpts. Do not use ClearPass predictions as gold labels.
- Record count and denominator for: correctly sourced claims, incorrect claims, verification-needed claims, missing consumer context, invalid citations and unsupported policy-cover assertions.
- If source material is missing, label the judgement unavailable. Do not assign a fabricated outcome.
- Keep source links, passages, dates and caveats alongside the label; document disagreement and adjudication.
- Consumer outcomes such as understanding still require testing with real participants and cannot be inferred from an offline A/B test.

Do not compare prompt wording alone as though it were evidence of improved answer quality.
