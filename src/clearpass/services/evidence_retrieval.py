"""Local evidence retrieval with an explicit human review gate."""

import json
import re
from pathlib import Path

from clearpass.contracts.models import EvidenceRecord, InsuranceClaim

DEFAULT_STORE = Path("data/evidence/evidence.json")

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "do",
    "for",
    "from",
    "has",
    "have",
    "i",
    "in",
    "is",
    "it",
    "my",
    "of",
    "on",
    "or",
    "the",
    "to",
    "was",
    "what",
    "when",
    "where",
    "which",
    "will",
    "with",
    "you",
    "your",
}


def tokens(value: str) -> set[str]:
    return {token for token in TOKEN_PATTERN.findall(value.lower()) if token not in STOPWORDS}


class LocalEvidenceRetriever:
    """Retrieves reviewed evidence, without making truth judgements."""

    def __init__(self, path: Path = DEFAULT_STORE):
        raw = json.loads(Path(path).read_text(encoding="utf-8"))

        if not isinstance(raw, list):
            raise ValueError("Evidence store must contain a list")

        self.records = []
        seen = set()

        for item in raw:
            record = EvidenceRecord.model_validate(
                {key: item[key] for key in EvidenceRecord.model_fields}
            )

            if record.evidence_id in seen:
                raise ValueError("Duplicate evidence ID")

            seen.add(record.evidence_id)

            approved = (
                item.get("approved_for_verification") is True
                and item.get("review_status") == "human_reviewed_approved"
                and bool(item.get("human_reviewer"))
                and bool(item.get("human_reviewed_on"))
            )

            if approved:
                self.records.append(record)

    def retrieve(self, claim: InsuranceClaim) -> list[EvidenceRecord]:
        query = tokens(claim.text)

        if not query:
            return []

        ranked = []

        for record in self.records:
            # This is candidate retrieval only.
            # Similarity does not establish factual support.
            document = tokens(record.atomic_proposition + " " + record.verbatim_supporting_passage)

            score = len(query & document)

            if score:
                ranked.append((score, record))

        ranked.sort(key=lambda item: (-item[0], item[1].evidence_id))

        return [record for _, record in ranked[:5]]
