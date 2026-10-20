"""Reviewed claim assessments for bounded verification."""

import json
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator

from clearpass.contracts.models import StrictModel


class ClaimAssessment(StrictModel):
    assessment_id: str = Field(min_length=1)
    canonical_claim: str = Field(min_length=1)
    expected_status: Literal["supported", "contradicted"]
    evidence_ids: list[str] = Field(min_length=1)
    justification: str = Field(min_length=1)
    scope: str = Field(min_length=1)
    reviewed_by: str = Field(min_length=1)
    reviewed_on: date

    @model_validator(mode="after")
    def unique_evidence(self):
        if len(self.evidence_ids) != len(set(self.evidence_ids)):
            raise ValueError("Duplicate evidence IDs")
        return self


def load_assessments(path: Path) -> list[ClaimAssessment]:
    raw = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(raw, list):
        raise ValueError("Assessments must be a list")

    assessments = [ClaimAssessment.model_validate(item) for item in raw]

    ids = [assessment.assessment_id for assessment in assessments]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate assessment IDs")

    return assessments
