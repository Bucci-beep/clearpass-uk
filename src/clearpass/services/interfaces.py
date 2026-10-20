"""Ports for the future implementation. These protocols are NOT working engines."""

from typing import Protocol

from clearpass.contracts.models import (
    ContextGap,
    ConsumerFact,
    EvidenceRecord,
    InsuranceClaim,
    PassportPreview,
    PassportRequest,
    VerificationDecision,
)


class EvidenceRetriever(Protocol):
    def retrieve(self, claim: InsuranceClaim) -> list[EvidenceRecord]: ...


class ClaimVerifier(Protocol):
    def verify(
        self, claim: InsuranceClaim, candidates: list[EvidenceRecord]
    ) -> VerificationDecision: ...


class ContextGapDetector(Protocol):
    def find_gaps(self, facts: list[ConsumerFact]) -> list[ContextGap]: ...


class PassportGenerator(Protocol):
    def preview(self, request: PassportRequest) -> PassportPreview: ...
