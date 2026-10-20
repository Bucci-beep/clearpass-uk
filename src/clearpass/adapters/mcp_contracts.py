"""Future MCP adapter input/output contracts only. No MCP server is started."""

from pydantic import Field

from clearpass.contracts.models import (
    EvidenceReference,
    InsuranceClaim,
    PassportRequest,
    StrictModel,
    VerificationDecision,
)


class UKGroundingRequest(StrictModel):
    topic: str = Field(min_length=1)
    jurisdiction: str = "UK"
    context: dict[str, str] = Field(default_factory=dict)


class VerifyClaimsRequest(StrictModel):
    claims: list[InsuranceClaim]
    evidence_refs: list[EvidenceReference] = Field(default_factory=list)


class VerifyClaimsResponse(StrictModel):
    decisions: list[VerificationDecision]


class BuildPassportRequest(PassportRequest):
    """Only explicitly approved fields may be included in the output."""
