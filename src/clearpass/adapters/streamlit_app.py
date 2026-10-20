"""ClearPass consumer journey. Run with streamlit run."""

import json
from pathlib import Path

import streamlit as st

from clearpass.contracts.models import ConsumerFact, InsuranceClaim, PassportRequest
from clearpass.services.claim_assessments import load_assessments
from clearpass.services.claim_verification import BoundedClaimVerifier
from clearpass.services.consumer_context import (
    POLICY_TYPES,
    STOCK_BANDS,
    STORAGE,
    build_context_facts,
    consumer_state,
)
from clearpass.services.context_gaps import RuleBasedContextGapDetector
from clearpass.services.evidence_retrieval import LocalEvidenceRetriever
from clearpass.services.guards import abstain, preview_approved_facts
from clearpass.services.question_coach import POLICIES, REGIONS, CoachInput, build_question

st.set_page_config(page_title="ClearPass UK", page_icon="🛡️", layout="centered")
st.title("ClearPass UK")
st.caption("Ask Better → Check the Answer → Share Selectively")
st.info(
    "Research prototype using self-reported consumer information. "
    "Only the insurer and policy wording can confirm specific cover. "
    "Claim verification in this interface is not yet connected."
)

st.header("1. Ask Better")
rough = st.text_area("Your original insurance question", key="rough")
region = st.selectbox("Where in the UK do you live?", REGIONS)
business = st.text_input("What business do you run from home?")
has_stock = st.checkbox("I keep business stock at home")
stock_details = st.text_input("What kind of stock? (optional)") if has_stock else ""
stock_band = (
    st.selectbox("Rough stock value", list(STOCK_BANDS)) if has_stock else next(iter(STOCK_BANDS))
)
storage = st.selectbox("Where is the stock kept?", list(STORAGE)) if has_stock else "Not sure"
insurance = st.selectbox("What insurance do you currently have?", POLICIES)
policy_type = st.selectbox("Which specific policy type have you identified?", list(POLICY_TYPES))

stock_prompt = (
    ", ".join(
        item
        for item in (
            stock_details.strip(),
            stock_band if STOCK_BANDS[stock_band] else "",
            storage if STORAGE[storage] else "",
        )
        if item
    )
    if has_stock
    else ""
)
if rough.strip():
    st.code(
        build_question(CoachInput(rough, region, business, stock_prompt, insurance)),
        language=None,
    )
    st.caption("Copy this prompt into your chosen AI tool. Only your entries are included.")
else:
    st.caption("Enter your question to create a copyable prompt.")

st.header("2. Check the Answer")
answer = st.text_area("Paste a selected AI answer, not your entire chat", height=140)
if answer.strip():
    st.warning(
        "Claim-by-claim verification is not connected to this screen. "
        "The pasted response is NOT marked supported or contradicted."
    )
    st.json(
        abstain("unverified-response", "Claim verification not connected").model_dump(mode="json")
    )


st.subheader("Check an individual claim")
st.caption(
    "Copy one factual statement from the AI response below. "
    "ClearPass checks whether a human-reviewed assessment exists."
)

claim_text = st.text_area(
    "Claim to check",
    placeholder="For example: My home insurance automatically covers business stock.",
    key="individual_claim",
)

if st.button("Check this claim", type="primary"):
    if not claim_text.strip():
        st.warning("Enter one specific claim first.")
    else:
        claim = InsuranceClaim(
            claim_id="consumer-selected-claim",
            text=claim_text.strip(),
        )

        try:
            root = Path(__file__).resolve().parents[3]
            retriever = LocalEvidenceRetriever(root / "data/evidence/evidence.json")
            assessments = load_assessments(root / "data/evidence/claim_assessments.json")

            # Supply only explicitly approved source records.
            # Lexical retrieval is for discovery, not truth assessment.
            candidates = retriever.retrieve(claim)

            verifier = BoundedClaimVerifier(assessments)
            decision = verifier.verify(claim, retriever.records)

            st.session_state["claim_result"] = {
                "claim_text": claim.text,
                "decision": decision.model_dump(mode="json"),
                "candidates": [
                    {
                        "evidence_id": record.evidence_id,
                        "source_name": record.source_name,
                        "source_url": record.source_url,
                        "passage": record.verbatim_supporting_passage,
                    }
                    for record in candidates
                ],
                "assessment_count": len(assessments),
            }

        except (OSError, ValueError) as exc:
            st.error(f"Verification unavailable: {exc}")

result = st.session_state.get("claim_result")

if result:
    if claim_text.strip() != result["claim_text"]:
        st.caption("Claim changed. Run the check again for this text.")
    else:
        decision = result["decision"]
        status = decision["status"]

        st.write("**Verification result**")

        if status == "supported":
            st.success("Supported within the reviewed assessment's scope")
        elif status == "contradicted":
            st.error("Contradicted within the reviewed assessment's scope")
        else:
            st.warning("Insufficient evidence for a reviewed verdict")

        st.json(decision)

        st.write("**Relevant approved UK source passages**")
        st.caption(
            "These are retrieval candidates, not proof that a claim is true. "
            "Only an explicitly reviewed assessment can establish a verdict."
        )

        if not result["candidates"]:
            st.info("No matching approved source passages were retrieved.")

        for record in result["candidates"]:
            with st.expander(f"{record['evidence_id']}: {record['source_name']}"):
                st.write(record["passage"])
                st.write(record["source_url"])

        if not result["assessment_count"]:
            st.info(
                "No claim assessments have been approved yet. "
                "ClearPass correctly abstains from issuing claim verdicts."
            )


st.subheader("What is known, and what still needs checking?")
st.caption("A consumer statement is never treated as independent policy verification.")
insurer_told = st.checkbox(
    "I have asked/told my insurer about the business and received a response"
)
stock_cover_checked = st.checkbox("I checked my policy wording or insurer about business stock")
visitors = st.selectbox(
    "Do customers or business visitors come to your home?", ("Not sure", "Yes", "No")
)
equipment = st.selectbox("Do you keep business equipment at home?", ("Not sure", "Yes", "No"))

context_facts = build_context_facts(
    business=business,
    has_stock=has_stock,
    stock_band=stock_band,
    storage=storage,
    policy_type=policy_type,
    insurer_told=insurer_told,
    stock_cover_checked=stock_cover_checked,
    visitors=visitors,
    equipment=equipment,
)
for label, value in consumer_state(context_facts).items():
    st.write(f"**{label}:** {value}")

st.caption("Select only the topics that actually apply. No topics are inferred from AI text.")
topics = set()
if business.strip():
    topics.add("business_activity_disclosure")
    topics.add("policy_type_for_home_business")
if has_stock:
    topics.add("business_stock_cover")
if st.checkbox("Check questions about business visitors / liability"):
    topics.add("home_business_liability")
if st.checkbox("Check questions about business equipment"):
    topics.add("business_equipment_cover")

gaps = RuleBasedContextGapDetector(topics=topics).find_gaps(context_facts)
if gaps:
    st.write("**Still worth confirming:**")
    for gap in gaps:
        st.info(f"{gap.gap_id}: {gap.question}")
else:
    st.caption("No unresolved questions match the currently selected topics and facts.")

st.header("3. Share Selectively")
st.caption("Everything below is opt-in. No AI response, raw chat or unchecked item is exported.")

# Keep original consumer values as separate optional sharing choices.
shareable: list[ConsumerFact] = []
if region != "Not sure":
    shareable.append(ConsumerFact(field_id="region", value=region, status="stated"))
if business.strip():
    shareable.append(ConsumerFact(field_id="business", value=business.strip(), status="stated"))
if has_stock:
    if stock_details.strip():
        shareable.append(
            ConsumerFact(field_id="stock_kind", value=stock_details.strip(), status="stated")
        )
    if STOCK_BANDS[stock_band]:
        shareable.append(
            ConsumerFact(field_id="stock_value_band", value=stock_band, status="stated")
        )
    if STORAGE[storage]:
        shareable.append(
            ConsumerFact(field_id="stock_storage_location", value=storage, status="stated")
        )
if insurance != "Not sure":
    shareable.append(ConsumerFact(field_id="insurance", value=insurance, status="stated"))
if POLICY_TYPES[policy_type]:
    shareable.append(ConsumerFact(field_id="policy_type", value=policy_type, status="stated"))

approved = [
    fact.field_id
    for fact in shareable
    if st.checkbox(
        f"Share: {fact.field_id.replace('_', ' ').title()} ({fact.value})",
        key=f"share_{fact.field_id}",
    )
]
preview = preview_approved_facts(PassportRequest(facts=shareable, approved_field_ids=approved))
chosen_questions = [
    {"gap_id": gap.gap_id, "question": gap.question}
    for gap in gaps
    if st.checkbox(f"Include question {gap.gap_id}: {gap.question}", key=f"question_{gap.gap_id}")
]
handover = {
    "consumer_facts": [f.model_dump(mode="json") for f in preview.selected_facts],
    "questions_to_confirm": chosen_questions,
    "notice": preview.disclosure_notice,
}
st.json(handover)
st.download_button(
    "Download approved handover JSON",
    data=json.dumps(handover, indent=2),
    file_name="clearpass_handover.json",
    mime="application/json",
)
