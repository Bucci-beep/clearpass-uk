"""Human-review CLI for ClearPass claim assessments."""

import json
import os
import sys
from datetime import UTC, date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from clearpass.contracts.models import InsuranceClaim  # noqa: E402
from clearpass.services.claim_assessments import (  # noqa: E402
    ClaimAssessment,
    load_assessments,
)
from clearpass.services.evidence_retrieval import (  # noqa: E402
    LocalEvidenceRetriever,
)

EVIDENCE = ROOT / "data/evidence/evidence.json"
ASSESSMENTS = ROOT / "data/evidence/claim_assessments.json"
AUDIT = ROOT / "data/evidence/claim_review_audit.jsonl"


def ask(label):
    return input(label).strip()


def required(label):
    value = ask(label)
    if not value:
        raise ValueError(f"{label} cannot be empty.")
    return value


def save_json(path, data):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def main():
    print("\nCLEARPASS — HUMAN CLAIM REVIEW")
    print("This tool does not decide whether a claim is true.")
    print("An authorised human reviewer must assess the cited passages.")
    print("Do not use an AI-generated assessment as human approval.\n")

    retriever = LocalEvidenceRetriever(EVIDENCE)
    approved = {item.evidence_id: item for item in retriever.records}
    assessments = load_assessments(ASSESSMENTS)

    print(f"Approved evidence records: {len(approved)}")
    print(f"Existing claim assessments: {len(assessments)}\n")

    claim_text = required("Exact claim to review: ")

    if any(a.canonical_claim.strip().casefold() == claim_text.casefold() for a in assessments):
        raise ValueError(
            "An assessment for this exact claim already exists. "
            "Review the existing record instead of duplicating it."
        )

    claim = InsuranceClaim(claim_id="review", text=claim_text)

    print("\nRelevant candidate sources (NOT automatic proof):")
    for item in retriever.retrieve(claim):
        print(f"\n{item.evidence_id} | {item.source_name}")
        print(f"URL: {item.source_url}")
        print(f"Proposition: {item.atomic_proposition}")
        print(f"Passage: {item.verbatim_supporting_passage}")

    print("\nAll approved evidence IDs:")
    print(", ".join(sorted(approved)))

    print("\nReviewer: examine the evidence, including scope and limits.")
    print("For claims about Maya's specific policy coverage,")
    print("general guidance alone does NOT establish coverage.")
    print("If the evidence cannot settle the claim, choose abstain.")

    verdict = required("\nReview outcome [supported/contradicted/abstain]: ").lower()

    if verdict == "abstain":
        print("No assessment saved. The app will show Insufficient Evidence.")
        return

    if verdict not in {"supported", "contradicted"}:
        raise ValueError("Invalid outcome. No assessment saved.")

    ids = [
        item.strip()
        for item in required(
            "Evidence IDs supporting this exact verdict (comma-separated): "
        ).split(",")
        if item.strip()
    ]

    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Evidence IDs must be present and unique.")

    invalid = [item for item in ids if item not in approved]
    if invalid:
        raise ValueError(f"Evidence not approved or not found: {invalid}")

    justification = required("Reviewer justification (what the passages establish): ")
    scope = required("Scope and limitations (what this does NOT establish): ")
    reviewer = required("Human reviewer name: ")

    if reviewer.casefold() in {
        "ai",
        "chatgpt",
        "claude",
        "copilot",
        "automated",
    }:
        raise ValueError("Human approval is required.")

    assessment = ClaimAssessment(
        assessment_id=f"CA-{len(assessments) + 1:04d}",
        canonical_claim=claim_text,
        expected_status=verdict,
        evidence_ids=ids,
        justification=justification,
        scope=scope,
        reviewed_by=reviewer,
        reviewed_on=date.today(),
    )

    print("\nREVIEW SUMMARY")
    print(
        json.dumps(
            assessment.model_dump(mode="json"),
            indent=2,
            ensure_ascii=False,
        )
    )

    confirmation = ask(
        "\nType APPROVE to attest that YOU reviewed the passages and authorise this assessment: "
    )

    if confirmation != "APPROVE":
        print("Cancelled. No assessment saved.")
        return

    # Recheck current store and assessments immediately before writing.
    current = load_assessments(ASSESSMENTS)
    current_approved = {item.evidence_id for item in LocalEvidenceRetriever(EVIDENCE).records}

    if any(a.canonical_claim.strip().casefold() == claim_text.casefold() for a in current):
        raise ValueError("Claim was already assessed. No changes saved.")

    if not set(ids) <= current_approved:
        raise ValueError("Evidence approval changed. No changes saved.")

    if any(a.assessment_id == assessment.assessment_id for a in current):
        assessment = assessment.model_copy(update={"assessment_id": f"CA-{len(current) + 1:04d}"})

    save_json(
        ASSESSMENTS,
        [a.model_dump(mode="json") for a in [*current, assessment]],
    )

    event = {
        "event": "human_claim_assessment_approved",
        "recorded_at_utc": datetime.now(UTC).isoformat(),
        **assessment.model_dump(mode="json"),
    }

    with AUDIT.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")

    print("\nAssessment saved.")
    print("Return to Streamlit and click 'Check this claim' again.")
    print("The exact reviewed claim can now receive its approved verdict.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyboardInterrupt) as exc:
        print(f"\nReview not completed: {exc}")
        sys.exit(1)
