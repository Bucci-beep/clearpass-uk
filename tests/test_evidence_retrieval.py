import json

from clearpass.contracts.models import InsuranceClaim
from clearpass.services.evidence_retrieval import LocalEvidenceRetriever


def test_unreviewed_records_are_excluded(tmp_path):
    store = tmp_path / "evidence.json"
    store.write_text(
        json.dumps(
            [
                {
                    "evidence_id": "E1",
                    "atomic_proposition": "Business stock insurance",
                    "source_name": "Synthetic test source",
                    "source_url": "https://example.org/test",
                    "verbatim_supporting_passage": "Business stock.",
                    "passage_location": "Section 1",
                    "retrieved_on": "2026-10-20",
                    "scope": "Synthetic test only",
                    "limitations": "Not genuine insurance evidence",
                    "reviewed_by": "Synthetic fixture",
                    "review_status": "source_verified_human_review_pending",
                    "approved_for_verification": False,
                    "human_reviewer": None,
                    "human_reviewed_on": None,
                }
            ]
        )
    )

    retriever = LocalEvidenceRetriever(store)

    assert retriever.retrieve(InsuranceClaim(claim_id="C1", text="Business stock")) == []


def test_empty_store_returns_no_evidence(tmp_path):
    store = tmp_path / "evidence.json"
    store.write_text("[]")

    retriever = LocalEvidenceRetriever(store)

    assert retriever.retrieve(InsuranceClaim(claim_id="C1", text="Business stock")) == []
