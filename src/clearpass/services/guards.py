"""Small deterministic controls used by future adapters."""

from clearpass.contracts.models import (
    ClaimStatus,
    PassportPreview,
    PassportRequest,
    VerificationDecision,
)


def abstain(claim_id: str, reason: str = "No verified decision is available") -> VerificationDecision:
    """Safe default. This does not make a claim about any UK policy."""
    return VerificationDecision(
        claim_id=claim_id, status=ClaimStatus.INSUFFICIENT_EVIDENCE, reasoning=reason
    )


def preview_approved_facts(request: PassportRequest) -> PassportPreview:
    """Preview the exact consumer facts selected; never include a chat transcript."""
    by_id = {fact.field_id: fact for fact in request.facts}
    selected = [by_id[field_id] for field_id in request.approved_field_ids]
    return PassportPreview(
        selected_facts=selected,
        excluded_field_ids=[
            fact.field_id for fact in request.facts if fact.field_id not in request.approved_field_ids
        ],
    )
