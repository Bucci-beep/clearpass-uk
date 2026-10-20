"""Deterministic question refinement. Consumer input is never sent to a model."""

from dataclasses import dataclass

REGIONS = ("England", "Scotland", "Wales", "Northern Ireland", "Not sure")
POLICIES = ("Home contents", "Business insurance", "Both", "Not sure")


@dataclass(frozen=True)
class CoachInput:
    rough_question: str
    region: str = "Not sure"
    business: str = ""
    stock: str = ""
    insurance: str = "Not sure"


def build_question(data: CoachInput) -> str:
    """Keep original intent, identify unknown fields and ask for bounded UK evidence."""
    question = data.rough_question.strip()
    if not question:
        raise ValueError("Please enter your original question")
    if data.region not in REGIONS or data.insurance not in POLICIES:
        raise ValueError("Invalid predefined selection")

    facts = []
    missing = []
    if data.region != "Not sure":
        facts.append(f"I live in {data.region}, UK.")
    else:
        missing.append("which UK nation applies")
    if data.business.strip():
        facts.append(f"My home business is: {data.business.strip()}.")
    else:
        missing.append("the type of home business")
    if data.stock.strip():
        facts.append(f"My stock or equipment amount and storage details are: {data.stock.strip()}.")
    else:
        missing.append("the value and storage location of any business stock or equipment")
    if data.insurance != "Not sure":
        facts.append(f"My current insurance is: {data.insurance}.")
    else:
        missing.append("what insurance I currently hold")

    return "\n".join(
        [
            "Please answer my original UK insurance question without changing its intent.",
            f"Original question: {question}",
            "Consumer information (self-reported, not independently checked):",
            *(f"- {item}" for item in facts),
            "Missing or uncertain information: "
            + (
                "; ".join(missing) if missing else "None reported; policy wording is still unknown."
            ),
            "Use relevant, traceable UK sources and explain their scope and dates where available.",
            "Distinguish general guidance from what can only be confirmed in my "
            "own policy wording or with my insurer or broker.",
            "List unanswered questions and explicitly say when evidence is insufficient.",
            "Do not assume that my particular policy covers business stock "
            "or recommend a particular insurer or product.",
        ]
    )
