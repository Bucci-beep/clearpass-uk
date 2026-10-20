"""Bounded verification using explicit reviewed claim assessments."""

from clearpass.contracts.models import (
    ClaimStatus,
    EvidenceRecord,
    EvidenceReference,
    InsuranceClaim,
    VerificationDecision,
)
from clearpass.services.claim_assessments import ClaimAssessment
from clearpass.services.guards import abstain


class BoundedClaimVerifier:
    """Only exact reviewed claims may receive non-abstaining results."""

    def __init__(
        self,
        assessments: list[ClaimAssessment] | None = None,
    ):
        self.assessments = assessments or []

    def verify(
        self,
        claim: InsuranceClaim,
        candidates: list[EvidenceRecord],
    ) -> VerificationDecision:
        matches = [
            assessment
            for assessment in self.assessments
            if assessment.canonical_claim.strip().casefold() == claim.text.strip().casefold()
        ]

        if len(matches) != 1:
            return abstain(
                claim.claim_id,
                "No unique reviewed assessment matches this claim.",
            )

        assessment = matches[0]
        evidence_by_id = {record.evidence_id: record for record in candidates}

        if not all(evidence_id in evidence_by_id for evidence_id in assessment.evidence_ids):
            return abstain(
                claim.claim_id,
                "Required reviewed evidence is unavailable.",
            )

        references = [
            EvidenceReference(
                evidence_id=evidence_id,
                passage=evidence_by_id[evidence_id].verbatim_supporting_passage,
            )
            for evidence_id in assessment.evidence_ids
        ]

        return VerificationDecision(
            claim_id=claim.claim_id,
            status=ClaimStatus(assessment.expected_status),
            reasoning=assessment.justification,
            evidence_refs=references,
        )
