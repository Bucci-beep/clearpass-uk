# ClearPass UK
## Shared hackathon project brief, team assignments and AI assistant context

**Version:** 20 October 2026  
**Status:** Agreed proposed direction, not an implemented or validated product  
**Team:** 1 AI engineer, 3 Fintech specialists  
**Time constraint:** Assume approximately 4 to 5 productive hackathon hours unless organisers confirm otherwise

> **One sentence:** ClearPass UK helps people who research insurance using existing AI assistants check evidence behind insurance claims, identify important unanswered questions and share only a consumer approved handover with an insurer, broker or comparison service.

**Tagline:** The chat stays. The claims get checked. The consumer stays in control.

---

## 1. The actual challenge

The AI Wales insurance LLM hackathon asks how consumers can get accurate, useful and trustworthy insurance information from the LLMs they already use so they make better informed decisions. Its relevant journey runs from early research through approaching a comparison site, broker or insurer.

Three problems identified in the challenge brief:

1. Answer quality varies with consumers' prompting and knowledge.
2. General LLMs may lack current or accurate UK specific insurance information.
3. Consumers may arrive at insurance services with incorrect assumptions from AI.

Hard constraints in the supplied challenge brief:

- Work with existing LLMs rather than requiring a totally new AI platform.
- Address misinformation, omissions, outdated content and foreign market assumptions.
- Do not assume access to private insurer systems or proprietary data.
- Do not automatically pass full conversations to third parties. Share consumer approved summaries only.
- Respect the boundary between general information and regulated financial advice.
- Explain **how improved consumer outcomes will be measured**.

**We are not building:** a new insurance chatbot, a price comparison site, a product recommender, a claims decision engine or proof that a particular policy covers a particular consumer.

---

## 2. Why we changed the earlier proposals

The earlier documents described two overlapping concepts, ClearPass based on a purported Jev harness and InsurePass based on three generative agents. Both identified a useful handover problem, but their implementations conflicted. The draft also contained corrupted code, generic unsupported insurance rules, weak compliance checks and self reported evaluation figures.

We retain the best ideas: evidence retrieval, bounded AI decisions, deterministic guardrails, consumer needs identification, privacy controlled handover and evaluation.

We reject for the MVP: the unverified Jev dependency, three separate creative agents, a full Chrome extension, large vector infrastructure, insurer APIs, self grading metrics and universal policy coverage claims.

**The differentiator is not a passport alone.** It is a source traceable, abstaining claim verifier **plus** a context gap detector **plus** a user controlled handover.

---

## 3. Narrow product scope

**Primary domain:** UK home insurance for someone working or running a small online business from home.

**Primary demo scenario:** A consumer stores business inventory in their garage. A general AI assistant says their ordinary contents insurance automatically covers it. ClearPass identifies that blanket assumption as unjustified, shows applicable general guidance, and says specific cover must be confirmed from policy wording or the insurer. It asks whether the business activity, stock value and appropriate cover have been discussed. The consumer chooses what information to include in a short handover.

**Secondary evaluation scenario:** An AI assistant overstates Flood Re eligibility or guarantees. This is for tests, not a second complete product flow.

**Important nuance:** Insurance cover can vary by insurer and policy. Do not claim that *all* household policies exclude business stock. Do not claim Flood Re automatically insures every high flood risk property. Never turn a consumer stated circumstance into a verified external fact.

---

## 4. Product experience

1. The person researches insurance in ChatGPT, Claude or another existing LLM.
2. If supported, they invoke ClearPass via an MCP tool. A fallback demonstration accepts only a selected response or structured claims in a small web app. We do not require the entire chat transcript.
3. Claims and consumer stated facts are extracted or entered in a small structured form.
4. ClearPass retrieves curated public UK guidance and checks individual insurance claims.
5. Each insurance claim receives one of: **Supported by evidence**, **Contradicted by evidence**, **Insufficient evidence**. Every non abstaining result needs a source and passage. These labels reflect evidence within scope; they do not certify a policy.
6. Consumer circumstances are separately marked **Stated**, **Confirmed by consumer**, or **Missing or unclear**. A stated fact is not something a public document can verify.
7. Context rules identify relevant unanswered questions, e.g. whether business stock cover is confirmed in this specific policy.
8. The person selects individual fields to share in a concise handover. The full chat is not included by default.

**User outcome:** fewer misconceptions, better context questions, better calibrated uncertainty, less unnecessary data sharing before contacting an insurance professional.

---

## 5. Architecture, deliberately small

```text
Existing LLM chat (ChatGPT/Claude etc.)
         |
         | supported MCP tool call OR selected-response fallback
         v
FastAPI + Pydantic contracts
         |
         v
Structured extraction: atomic insurance claims / consumer-stated facts
         |
         v
Local, curated UK evidence retrieval (JSON + BM25/TF-IDF)
         |
         v
Bounded verifier: supported / contradicted / insufficient evidence
         |
         v
Deterministic checks: valid evidence ID, passage, scope, abstain on uncertainty
         |
         v
Context dependency rules + safe information/advice boundary
         |
         v
Consent selected passport (copyable text/JSON) + evaluation receipt
```

Suggested stack: Python, FastAPI, Pydantic, one structured output capable LLM, local JSON evidence store, lightweight lexical retrieval, pytest, Streamlit demonstration, FastMCP adapter where feasible.

**Important technical guardrail:** A high retrieval similarity score does **not** prove a claim is true. Supported or contradicted labels require passage level evidence, scope checking and a bounded claim versus evidence judgement. Low quality, absent, conflicting or insufficient evidence must cause abstention. A constrained enum alone does not guarantee correctness.

**Proposed MCP tools:**

- `uk_grounding(topic, jurisdiction, context)` returns relevant UK passages, source URLs, retrieval/verification metadata and limitations.
- `verify_claims(claims, evidence_refs)` returns validated structured decisions and gaps, or abstentions.
- `build_passport(approved_fields)` exports only selected, permitted data.

MCP use depends on host, account and remote connectivity support. **Test the native integration early; do not make the whole demo depend on it.** If only a paste/select fallback works, acknowledge the challenge alignment limitation and show that both routes use the same engine.

**Privacy statement we can defend:** ClearPass does not require complete conversation histories and does not include them in handovers by default. We cannot promise that users' existing LLM provider has never processed their own chat. Consent selection needs a real preview of all exported fields. If a remote API is used for extraction, disclose the specific data that travels there; don't call that path fully local/private.

**Advice statement:** This is a research prototype for informational checking and question preparation, not regulated insurance advice or legal confirmation of FCA compliance. A restricted output schema and adversarial tests are risk controls, not regulatory approval.

---

## 6. Four distinct workstreams

### Person A: AI engineer, system owner

**Mission:** Deliver the smallest working, testable end to end system.

Own the data contracts; claim extraction; evidence retrieval; bounded support/contradiction/abstention; deterministic validators and context rule execution; API; integration to Streamlit; optional FastMCP adapter; test runner; reproducibility; backend failure handling.

**Deliver:** runnable demo, documented API/contracts, evidence based results, test execution output and a stable fallback for live presentation.

**Do not own alone:** source interpretation, consumer disclosures, regulatory analysis, UX copy or gold labels. Request validated inputs from the Fintech colleagues.

### Person B: Fintech 1, UK insurance evidence and domain lead

**Mission:** Supply a small, reliable, audit friendly UK insurance knowledge base.

Investigate the specific home business scenario. Identify 8 to 12 narrowly phrased propositions from authoritative public UK sources (such as MoneyHelper, ABI, FCA, Citizens Advice, or relevant public insurer documentation). Keep general insurance guidance and specific policy terms separate. Identify exceptions and limitations.

**Deliver:** `evidence.json` or a spreadsheet with `evidence_id`, `atomic_proposition`, `source_name`, `source_url`, `verbatim_supporting_passage`, `passage_location`, `retrieved_on`, `scope`, `limitations`, `reviewed_by`. Provide 4 consumer misunderstandings with source justified corrections. Mark anything unverified; never invent URLs or exact quotations.

**Acceptance condition:** Every asserted UK rule has a real supporting passage and clearly stated limits. No unsupported categorical claims about coverage.

### Person C: Fintech 2, consumer journey and regulatory boundary lead

**Mission:** Define the real consumer risk and what a useful handover must contain.

Investigate how to distinguish general insurance information, personalised recommendations and advice about particular contracts. Examine the FCA Handbook, especially PERG 5.8 and relevant ICOBS provisions, and the Consumer Insurance (Disclosure and Representations) Act 2012. Do not claim consumers have a blanket duty to volunteer every material fact; the 2012 Act requires reasonable care not to make a misrepresentation in the consumer insurance context. Turn this into practical output prohibitions and acceptable example wording, not an unsupported certification of legal compliance.

Map the home business consumer journey; list 5 to 8 important missing context questions; define which consumer facts are useful and which sensitive details should not be collected. Define the fields and plain language copy for a one page broker preparation handover and the consent preview.

**Deliver:** `consumer_journey.md`, `coverage_context_rules.json`, `handover_schema.md`, `advice_boundary_examples.md` and one 60 second scenario script.

**Acceptance condition:** The outputs distinguish consumer assertions from sourced facts, and preparation questions from assertions of coverage or product advice.

### Person D: Fintech 3, independent evaluation and presentation lead

**Mission:** Prove that this is evaluated rather than merely demonstrated.

Create 15 labelled synthetic cases independently of backend predictions, with the proposed mix: 4 false or foreign market claims; 3 correct UK claims; 3 policy dependent/unverifiable claims; 3 missing context cases; 2 conflicting/misleading evidence cases. Each case must have expected decisions and the source backed rationale. Add 10 adversarial inputs targeting product advice, source fabrication, privacy leaks and prompt injection. Use synthetic identities and data only.

Design metrics: planted error recall, false positive rate on correct claims, appropriate abstention, unsupported citation rate, missing context question recall, advice leakage and PII leakage. Report actual counts with denominators, not just percentages; label thresholds as targets rather than achieved results.

Help prepare the presentation's problem, live demonstration, independent test results, limitations and proposed consumer study. Design a future 20 person study measuring comprehension, relevant information identified, confidence calibration and unnecessary disclosures.

**Deliver:** `gold_cases.json`, `red_team_cases.json`, `evaluation_protocol.md`, `results_template.csv`, `pitch_outline.md`.

**Acceptance condition:** Test labels were defined before seeing system outputs. Failures are shown transparently and do not disappear from the report.

---

## 7. Handoffs and interfaces

**At the start:** All four agree on the primary scenario and vocabulary: consumer facts, evidence claims, uncertainty, consent selected handover. Freeze the core schema before building separate workstreams.

**Fintech 1 to AI engineer:** Structured evidence propositions + source excerpts. The engineer loads these but does not silently change domain conclusions.

**Fintech 2 to AI engineer:** Context dependencies, prohibited outputs and passport fields. The engineer implements and tests these deterministic rules.

**Fintech 3 to AI engineer:** Hidden gold scenarios and adversarial examples. The engineer runs a benchmark; labels must not be adjusted to improve results.

**AI engineer to everyone:** API contracts, runnable outputs and constraints early, then a demonstrated full flow. Do not wait for complete polished documents before testing integration.

**Team review:** Domain lead audits 2 sampled citations; regulatory lead checks 2 handovers; evaluation lead checks 2 cases; engineer demonstrates 1 end to end example. Fix critical issues before polishing slides.

---

## 8. Suggested five hour schedule

**Hour 1:** Freeze scope/contracts; Fintech 1 begins source pack; Fintech 2 defines context rules and consent; Fintech 3 writes gold labels; AI engineer scaffolds API and verified data contracts.

**Hour 2:** AI engineer builds core extraction/retrieval/verifier; Fintech inputs land as minimal usable files, even if incomplete. Independently check the initial source claims.

**Hour 3:** Integrate context rules and safe passport; complete the primary consumer journey. Start tests immediately rather than leaving them to the end.

**Hour 4:** Connect Streamlit demo; run independent evaluation; optionally complete an MCP integration only if core path is stable.

**Hour 5:** Rehearse a clean start, verify displayed citations, conduct adversarial tests, prepare an offline/recorded fallback, share actual results and known limitations.

**Stop rule:** If a feature threatens the working end to end demo, defer it. Essential sequence is **one scenario -> real evidence -> defensible abstention -> unresolved questions -> consent selected passport -> measured tests**.

---

## 9. Definition of done and metrics

Core MVP conditions:

- A consumer selected AI response or extracted claims can enter the working backend.
- At least one supported, one contradicted and one insufficient evidence decision can be produced from defensible inputs, with real evidence receipts for the first two.
- General evidence never claims to establish a particular policy's coverage.
- Consumer stated needs and sourced insurance claims are separate data types.
- Unresolved coverage questions follow from explicit context rules.
- Handover fields are selected by the consumer; full chats and unselected fields are excluded.
- Prohibited recommendation content cannot appear in the deterministic final passport format.
- The team can run a reproducible independent benchmark and report both successes and failures.
- A complete demo works without relying on native MCP connectivity.

Proposed evaluation **targets, not existing results:** planted error recall >= 80%; false positive rate <= 10%; correct abstention on all three unverifiable cases; unsupported citation rate 0; advice leakage 0/10 adversarial cases; PII leakage 0. With tiny samples, these numbers provide a smoke test, not scientific proof of broad safety.

No team member should publish fabricated measured outcomes, regulatory certification, claims of insurer endorsement or consumer study results that have not occurred.

---

## 10. Source starting points (verify passage and current applicability before using)

- Challenge brief supplied by the team: `AI Wales Insurance LLM Hackathon Challenge Brief.md`
- Previous concept draft supplied by the team: `1.md` (superseded by this unified plan)
- UK legislation, Consumer Insurance (Disclosure and Representations) Act 2012, s. 2: https://www.legislation.gov.uk/ukpga/2012/6/section/2
- FCA Handbook PERG 5.8: https://handbook.fca.org.uk/handbook/PERG/5/8.html
- FCA Handbook ICOBS: https://handbook.fca.org.uk/handbook/ICOBS/
- MoneyHelper insurance guidance: https://www.moneyhelper.org.uk/en/everyday-money/insurance
- Association of British Insurers: https://www.abi.org.uk/
- Flood Re: https://www.floodre.co.uk/

These URLs are starting points, **not** a substitute for verifying and saving exact, dated supporting passages.

---

## 11. Common AI assistant instructions for every team member

Copy the following into your preferred AI assistant **together with this file** and your assigned workstream. Also attach the original challenge brief if possible.

```text
We are a four person team taking part in an AI Wales insurance LLM hackathon.
One person is our AI engineer, and three have Fintech backgrounds.
The agreed concept is ClearPass UK. The attached unified team brief is our project source of truth. The original hackathon challenge brief outranks our project decisions if there is a conflict.

Goal: help UK insurance consumers use their existing LLMs more safely, through evidence bounded claim verification, context gap detection and consent controlled handover. Initial scope: home insurance for a person running a business with stock at home.

Important distinctions:
- A consumer statement is not externally verified by a public insurance source.
- Public guidance is not proof that a particular policy covers a consumer.
- A high retrieval similarity score is not proof of support or contradiction.
- When evidence is insufficient, say so and formulate a useful validation question.
- Never fabricate legal obligations, source URLs, quotations, dates, citations, test scores or implemented features.
- Do not assume ClearPass is authorised to provide regulated financial advice.
- Do not assume an MCP integration is available or working on every LLM account.
- Never require or share full consumer chats by default.

My assigned workstream is: [PASTE YOUR TEAM ROLE FROM SECTION 6].

Produce its named deliverables in concrete, usable formats. For each factual assertion include an authoritative source URL, a direct supporting excerpt where lawful and practical, a date checked, and stated caveats. Clearly mark everything still needing verification. Prioritise deliverables we can ship in a few hours, not a large production roadmap. Do not rewrite or expand the project beyond the agreed scope without explicitly labelling the suggestion as optional.

Start by producing the smallest usable deliverable for my role, then identify what must be handed to the AI engineer and any unresolved decisions.
```

### Suggested specialist followups

**Fintech 1:** "Produce eight evidence records for the primary home business scenario. Separate legal requirements, general consumer guidance and policy dependent examples. Do not claim a passage proves more than it says."

**Fintech 2:** "Define five to eight missing context questions and a short consumer controlled passport. Explain why none of the wording recommends an insurance product or falsely asserts a disclosure duty."

**Fintech 3:** "Create 15 independently labelled synthetic cases and 10 adversarial prompts with objective expected outcomes. Design an evaluation spreadsheet using true/false counts and abstentions, not self reported pass flags."

**AI engineer:** "Using the frozen contracts and source pack, implement the thinnest vertical slice: input -> atomic claim -> retrieval -> bounded decision -> deterministic abstention -> context questions -> consent selected passport. Give runnable steps and tests, defer optional infrastructure."

---

## 12. Pitch structure

1. **Problem:** AI answers can sound credible while hiding policy dependent assumptions.
2. **Consumer story:** An online seller assumes business stock in their garage is automatically insured.
3. **Verification:** ClearPass separates claims from consumer facts, retrieves UK sources and refuses unsupported conclusions.
4. **Outcome:** Relevant unanswered questions and a minimal handover selected by the consumer.
5. **Evidence:** Independent benchmark, red team examples, limitations and a proposed consumer outcome study.
6. **Next step:** Extend the domain and test with insurance practitioners and consumers after the hackathon; no claim of completed regulatory approval.

**Pitch statement:** "We are not asking consumers to stop using ChatGPT or Claude. ClearPass helps them tell the difference between a sourced insurance claim, a policy specific unknown and information they should confirm before continuing. They take the questions and only the facts they approve into the regulated journey, not the entire AI conversation."

---

## 13. Decisions to freeze as a group

- Project name: **ClearPass UK**.
- First vertical: **UK home insurance for home based business stock**.
- Main output: **claim evidence decisions + context questions + consumer approved handover**.
- Integration: **existing LLM via MCP if supported, same backend with fallback selected response web UI**.
- Never claim to provide a specific insurer recommendation or guaranteed policy coverage.
- Evaluate against **independently labelled synthetic cases** rather than self grading.
- Prioritise a credible working demonstration over complexity or feature count.

This document is ready to share as the team's common context. It is not evidence that the project has already been built or evaluated.
