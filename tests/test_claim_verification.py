from clearpass.contracts.models import (
    ClaimStatus,
    EvidenceRecord,
    InsuranceClaim,
)
from clearpass.services.claim_verification import BoundedClaimVerifier


def test_verifier_abstains_without_evidence():
    decision = BoundedClaimVerifier().verify(
        InsuranceClaim(claim_id="C1", text="Business stock is covered"),
        [],
    )

    assert decision.status == ClaimStatus.INSUFFICIENT_EVIDENCE
    assert decision.evidence_refs == []


def test_relevant_passage_does_not_automatically_prove_claim():
    candidate = EvidenceRecord(
        evidence_id="TEST-1",
        atomic_proposition="Business stock may require checking",
        source_name="Synthetic test",
        source_url="https://example.org/synthetic",
        verbatim_supporting_passage="Business stock may require checking.",
        passage_location="Test section",
        retrieved_on="2026-10-20",
        scope="Synthetic tests only",
        limitations="Not actual insurance evidence",
        reviewed_by="Synthetic fixture",
    )

    decision = BoundedClaimVerifier().verify(
        InsuranceClaim(
            claim_id="C1",
            text="My contents policy automatically covers stock",
        ),
        [candidate],
    )

    assert decision.status == ClaimStatus.INSUFFICIENT_EVIDENCE
    assert decision.evidence_refs == []


def test_matching_assessment_without_evidence_abstains():
    from clearpass.services.claim_assessments import ClaimAssessment

    assessment = ClaimAssessment(
        assessment_id="A1",
        canonical_claim="Synthetic claim",
        expected_status="supported",
        evidence_ids=["E1"],
        justification="Synthetic assessment only",
        scope="Synthetic tests",
        reviewed_by="Test reviewer",
        reviewed_on="2026-10-20",
    )

    verifier = BoundedClaimVerifier([assessment])

    result = verifier.verify(
        InsuranceClaim(claim_id="C1", text="Synthetic claim"),
        [],
    )

    assert result.status == ClaimStatus.INSUFFICIENT_EVIDENCE
    assert result.evidence_refs == []


def test_conflicting_assessments_abstain():
    from clearpass.services.claim_assessments import ClaimAssessment

    assessments = [
        ClaimAssessment(
            assessment_id=f"A{number}",
            canonical_claim="Synthetic claim",
            expected_status=status,
            evidence_ids=["E1"],
            justification="Synthetic assessment only",
            scope="Synthetic tests",
            reviewed_by="Test reviewer",
            reviewed_on="2026-10-20",
        )
        for number, status in [
            (1, "supported"),
            (2, "contradicted"),
        ]
    ]

    verifier = BoundedClaimVerifier(assessments)

    result = verifier.verify(
        InsuranceClaim(claim_id="C1", text="Synthetic claim"),
        [],
    )

    assert result.status == ClaimStatus.INSUFFICIENT_EVIDENCE


def test_unmatched_claim_abstains():
    verifier = BoundedClaimVerifier()

    result = verifier.verify(
        InsuranceClaim(
            claim_id="C1",
            text="My specific policy covers business stock",
        ),
        [],
    )

    assert result.status == ClaimStatus.INSUFFICIENT_EVIDENCE
