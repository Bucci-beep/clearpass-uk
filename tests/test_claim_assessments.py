import json

import pytest
from pydantic import ValidationError

from clearpass.services.claim_assessments import (
    ClaimAssessment,
    load_assessments,
)


def test_empty_assessments_are_valid(tmp_path):
    path = tmp_path / "assessments.json"
    path.write_text("[]")

    assert load_assessments(path) == []


def test_assessment_requires_evidence():
    with pytest.raises(ValidationError):
        ClaimAssessment(
            assessment_id="A1",
            canonical_claim="Synthetic example",
            expected_status="supported",
            evidence_ids=[],
            justification="Test",
            scope="Synthetic",
            reviewed_by="Tester",
            reviewed_on="2026-10-20",
        )


def test_duplicate_assessment_ids_rejected(tmp_path):
    assessment = {
        "assessment_id": "A1",
        "canonical_claim": "Synthetic example",
        "expected_status": "supported",
        "evidence_ids": ["E1"],
        "justification": "Synthetic fixture",
        "scope": "Synthetic only",
        "reviewed_by": "Tester",
        "reviewed_on": "2026-10-20",
    }

    path = tmp_path / "assessments.json"
    path.write_text(json.dumps([assessment, assessment]))

    with pytest.raises(ValueError, match="Duplicate"):
        load_assessments(path)
