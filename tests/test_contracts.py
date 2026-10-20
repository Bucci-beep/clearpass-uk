import pytest
from pydantic import ValidationError

from clearpass.contracts.models import (
    ClaimStatus,
    ConsumerFact,
    ConsumerFactStatus,
    EvidenceReference,
    PassportRequest,
    VerificationDecision,
)
from clearpass.services.guards import abstain, preview_approved_facts


def test_default_abstention_has_no_unverified_citations():
    decision = abstain("claim-1")
    assert decision.status is ClaimStatus.INSUFFICIENT_EVIDENCE
    assert decision.evidence_refs == []


@pytest.mark.parametrize("status", [ClaimStatus.SUPPORTED, ClaimStatus.CONTRADICTED])
def test_non_abstention_requires_passage(status):
    with pytest.raises(ValidationError):
        VerificationDecision(claim_id="c", status=status, reasoning="unsupported")


def test_reference_satisfies_structural_contract_only():
    decision = VerificationDecision(
        claim_id="c",
        status=ClaimStatus.SUPPORTED,
        reasoning="Not externally validated here",
        evidence_refs=[EvidenceReference(evidence_id="e", passage="test passage")],
    )
    assert len(decision.evidence_refs) == 1


def test_missing_fact_cannot_contain_value():
    with pytest.raises(ValidationError):
        ConsumerFact(field_id="address", status=ConsumerFactStatus.MISSING_OR_UNCLEAR, value="x")


def test_passport_preview_exports_only_approved_fields():
    request = PassportRequest(
        facts=[
            ConsumerFact(field_id="business", value="online store", status="stated"),
            ConsumerFact(field_id="stock_value", value="illustrative value", status="stated"),
        ],
        approved_field_ids=["business"],
    )
    preview = preview_approved_facts(request)
    assert [fact.field_id for fact in preview.selected_facts] == ["business"]
    assert preview.excluded_field_ids == ["stock_value"]
    assert "illustrative value" not in preview.model_dump_json()


def test_empty_approval_exports_nothing():
    request = PassportRequest(
        facts=[ConsumerFact(field_id="business", value="synthetic", status="stated")],
        approved_field_ids=[],
    )
    assert preview_approved_facts(request).selected_facts == []


def test_unknown_approved_id_fails_closed():
    with pytest.raises(ValidationError):
        PassportRequest(facts=[], approved_field_ids=["unknown"])


def test_duplicate_fact_ids_fail():
    with pytest.raises(ValidationError):
        PassportRequest(
            facts=[
                ConsumerFact(field_id="same", value="a", status="stated"),
                ConsumerFact(field_id="same", value="b", status="stated"),
            ]
        )
