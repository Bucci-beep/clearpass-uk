"""Deterministic context gap detection using team-reviewed rules."""

import json
from pathlib import Path

from clearpass.contracts.models import (
    ConsumerFact,
    ContextGap,
)

DEFAULT_RULES = Path("data/context/coverage_context_rules.json")


class RuleBasedContextGapDetector:
    def __init__(
        self,
        path: Path = DEFAULT_RULES,
        topics: set[str] | None = None,
    ):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.rules = data["context_rules"]
        self.topics = topics or set()

    def find_gaps(
        self,
        facts: list[ConsumerFact],
    ) -> list[ContextGap]:
        facts_by_id = {fact.field_id: fact for fact in facts}

        results = []

        for rule in self.rules:
            conditions = rule["fires_if"]

            required_topics = set(conditions.get("claim_topics_any", []))
            required_facts = set(conditions.get("consumer_facts_any", []))

            topic_matches = bool(required_topics & self.topics) if required_topics else True

            fact_matches = bool(required_facts & facts_by_id.keys()) if required_facts else True

            if not topic_matches or (
                not fact_matches
                and not (rule["id"] in {"CR5", "CR6"} and bool(required_topics & self.topics))
            ):
                continue

            resolved = rule["resolved_if"]
            resolved_fact = facts_by_id.get(resolved["fact_key"])

            status_mapping = {
                "Stated": "stated",
                "Confirmed by consumer": "consumer_confirmed",
                "Missing or unclear": "missing_or_unclear",
            }

            if resolved_fact is not None and resolved_fact.status.value == status_mapping.get(
                resolved["status"]
            ):
                continue

            results.append(
                ContextGap(
                    gap_id=rule["id"],
                    question=rule["question"],
                    related_fact_ids=list(required_facts),
                )
            )

        return results
