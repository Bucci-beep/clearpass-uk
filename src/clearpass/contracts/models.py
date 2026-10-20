"""Provider-agnostic foundation contracts. No model-generated conclusions."""

from datetime import date
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ClaimStatus(str, Enum):
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class ConsumerFactStatus(str, Enum):
    STATED = "stated"
    CONSUMER_CONFIRMED = "consumer_confirmed"
    MISSING_OR_UNCLEAR = "missing_or_unclear"


class InsuranceClaim(StrictModel):
    claim_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    jurisdiction: Literal["UK"] = "UK"


class ConsumerFact(StrictModel):
    field_id: str = Field(min_length=1)
    value: str | None = None
    status: ConsumerFactStatus

    @model_validator(mode="after")
    def missing_has_no_value(self) -> "ConsumerFact":
        if self.status == ConsumerFactStatus.MISSING_OR_UNCLEAR and self.value is not None:
            raise ValueError("Missing or unclear facts must not contain a value")
        if self.status != ConsumerFactStatus.MISSING_OR_UNCLEAR and not self.value:
            raise ValueError("Stated or confirmed facts require a non-empty value")
        return self


class EvidenceRecord(StrictModel):
    evidence_id: str = Field(min_length=1)
    atomic_proposition: str = Field(min_length=1)
    source_name: str = Field(min_length=1)
    source_url: HttpUrl
    verbatim_supporting_passage: str = Field(min_length=1)
    passage_location: str = Field(min_length=1)
    retrieved_on: date
    scope: str = Field(min_length=1)
    limitations: str = Field(min_length=1)
    reviewed_by: str = Field(min_length=1)


class EvidenceReference(StrictModel):
    evidence_id: str = Field(min_length=1)
    passage: str = Field(min_length=1)


class VerificationDecision(StrictModel):
    claim_id: str = Field(min_length=1)
    status: ClaimStatus
    reasoning: str = Field(min_length=1)
    evidence_refs: list[EvidenceReference] = Field(default_factory=list)

    @model_validator(mode="after")
    def citation_requirements(self) -> "VerificationDecision":
        if self.status in {ClaimStatus.SUPPORTED, ClaimStatus.CONTRADICTED} and not self.evidence_refs:
            raise ValueError("Non-abstaining claims require passage-level evidence")
        return self


class ContextGap(StrictModel):
    gap_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    related_fact_ids: list[str] = Field(default_factory=list)


class PassportRequest(StrictModel):
    facts: list[ConsumerFact]
    approved_field_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_approval(self) -> "PassportRequest":
        available = [fact.field_id for fact in self.facts]
        if len(available) != len(set(available)):
            raise ValueError("Duplicate fact field IDs")
        if len(self.approved_field_ids) != len(set(self.approved_field_ids)):
            raise ValueError("Duplicate approved field IDs")
        if not set(self.approved_field_ids).issubset(available):
            raise ValueError("Cannot approve unavailable fields")
        return self


class PassportPreview(StrictModel):
    selected_facts: list[ConsumerFact]
    excluded_field_ids: list[str]
    disclosure_notice: str = (
        "Consumer-selected statements for discussion, not independent verification "
        "of policy cover or insurance advice."
    )
