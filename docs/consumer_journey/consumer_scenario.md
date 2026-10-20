# ClearPass UK: Main demo scenario, "Maya's garage stock"

Version 0.1 · 20 October 2026 · Fintech 2 (consumer)
**Everything here is synthetic.** Maya is invented. The AI answer in Stage 2 was **written by our team** to show typical mistakes. It is not a real ChatGPT output and must not be presented as one. Person D runs the real ChatGPT comparison separately.

---

## 1. Who Maya is

| Fact | Value | Tag |
|---|---|---|
| Lives in | Wales, UK | Stated |
| Business | Makes and sells handmade candles online | Stated |
| Stock | About £3,000 of candles and wax, so the £1,000 to £5,000 band | Stated |
| Kept in | A garage attached to her house | Stated |
| Insurance | Home contents insurance (she thinks so, but hasn't checked the wording) | Stated |
| Equipment | Laptop and label printer used for the business | Stated (not asked by the coach) |
| Insurer told about the business? | She doesn't know | Missing or unclear |

**Her worry:** "If there's a fire in the garage, is my stock covered?"

**The risk we show:** an AI assistant tells her "yes, automatically". She believes it, never checks, and could find out too late.

---

## 2. Stage 1: Ask better (Question Coach)

**Her rough question:** "is my stock covered by my house insurance?"

| Coach question | Maya picks |
|---|---|
| Do you live in the UK? | Yes |
| What kind of business do you run from home? | Making and selling crafts or handmade goods |
| Where is your stock kept? / Roughly how much is it worth? | In a garage attached to the house / £1,000 to £5,000 |
| What insurance do you have now? | Home contents insurance |

**Coached question (built by the template in `question_coach.json`):**

> I live in the UK and have a question about home insurance. I run a small business from home, making and selling handmade goods. I keep business stock in a garage attached to my house, worth roughly between £1,000 and £5,000. I have home contents insurance.
>
> Please help me understand:
> 1. What I should look for in my own policy wording about business stock kept at home.
> 2. Which parts of your answer are general UK information, and which depend on my specific insurer or policy.
> 3. Anything you are not sure about. Please say so rather than guess.
>
> Please answer for the UK only. Tell me which UK sources your answer is based on, with links I can check. Please do not recommend a specific insurer or product.

**What the demo shows:** the rough and coached questions side by side. The rough one gives no country, no business, no amount and no policy type.

---

## 3. Stage 2: Check the answer

### 3a. The AI answer Maya pastes back (synthetic, written by the team)

Use this for the **live demo** so the result is predictable. It is the kind of answer a rough question can produce.

> Good news! Your home contents insurance will automatically cover the stock you keep in your garage, since it's part of your home. Most homeowners insurance policies include personal property in attached garages. Just remember that you must tell your insurer about absolutely everything that could affect your policy, or they can refuse to pay. When you answer your insurer's questions, you need to take reasonable care to answer them accurately. You may also want to consider business insurance, which covers things like public liability if customers visit, and your laptop and equipment. You should probably also check your deductible.

### 3b. Claims ClearPass should pull out, and the expected result

| # | Claim | Expected result | Why | Evidence |
|---|---|---|---|---|
| C1 | Home contents insurance automatically covers business stock kept in a garage | **Insufficient evidence** (or Contradicted, if Person B's source supports it) | Whether it's covered depends on the specific policy. Public guidance cannot confirm one person's cover. We must **not** flip it to "all policies exclude stock" | Person B's source on policies varying. **Still needed.** |
| C2 | You must tell your insurer about absolutely everything that could affect your policy | **Contradicted by evidence** | For consumer insurance, the duty is to take reasonable care not to misrepresent. The Act replaced the older duty to disclose | EV-LAW-02 (below). Verified 20 Oct 2026 |
| C3 | When you answer your insurer's questions, you need to take reasonable care to answer accurately | **Supported by evidence** | Matches the 2012 Act's duty of reasonable care | EV-LAW-01 (below). Verified 20 Oct 2026 |
| C4 | "Homeowners insurance", "deductible" | **Flag: may not be UK wording** | These are US terms. The UK usually says "home insurance" or "buildings and contents" and "excess" | Wording note only, not a verdict. Wording to be confirmed by Person B |
| C5 | "You may also want to consider business insurance" | **Not checked as a fact.** ClearPass shows no recommendation of its own | The AI gave a suggestion. ClearPass neither agrees nor repeats it | Advice boundary rule |

This gives the demo **one Supported, one Contradicted and one Insufficient evidence result**, which is what the brief's definition of done asks for. The first two have real legal passages.

**Scope caveat for C2 and C3:** the 2012 Act applies to *consumer* insurance contracts (taken out wholly or mainly for non-business purposes, s.1). A home with a business inside may be a grey area. ClearPass should show the line: *"This rule applies to consumer insurance. Whether your policy counts as consumer insurance is something to confirm with your insurer."*

### 3c. Ready-made evidence records (same fields as Person B's `evidence.json`)

```json
[
  {
    "evidence_id": "EV-LAW-01",
    "atomic_proposition": "Before a consumer insurance contract is entered into or varied, the consumer has a duty to take reasonable care not to make a misrepresentation to the insurer.",
    "source_name": "Consumer Insurance (Disclosure and Representations) Act 2012, section 2",
    "source_url": "https://www.legislation.gov.uk/ukpga/2012/6/section/2",
    "verbatim_supporting_passage": "It is the duty of the consumer to take reasonable care not to make a misrepresentation to the insurer.",
    "passage_location": "s.2(2)",
    "retrieved_on": "2026-10-20",
    "scope": "Consumer insurance contracts only (s.1). UK legislation.",
    "limitations": "Does not say what any policy covers. May not apply if the contract is mainly for business purposes.",
    "reviewed_by": "Fintech 2 draft. Person B to review."
  },
  {
    "evidence_id": "EV-LAW-02",
    "atomic_proposition": "The reasonable-care duty replaces any earlier duty of disclosure or representation by a consumer to an insurer in the same circumstances.",
    "source_name": "Consumer Insurance (Disclosure and Representations) Act 2012, section 2",
    "source_url": "https://www.legislation.gov.uk/ukpga/2012/6/section/2",
    "verbatim_supporting_passage": "The duty set out in subsection (2) replaces any duty relating to disclosure or representations by a consumer to an insurer which existed in the same circumstances before this Act applied.",
    "passage_location": "s.2(4)",
    "retrieved_on": "2026-10-20",
    "scope": "Consumer insurance contracts only (s.1). UK legislation.",
    "limitations": "Use to contradict 'you must tell your insurer everything'. Do not use it to say the consumer need not mention anything: s.2(3) says failing to confirm or amend details when the insurer asks can be a misrepresentation.",
    "reviewed_by": "Fintech 2 draft. Person B to review."
  }
]
```

### 3d. What Maya sees (wording from `coverage_context_rules.json` templates)

**Engineer note:** the banned-wording scan must skip the quoted `{claim}` slot. Otherwise the C2 card below gets blocked, because it quotes the AI's "you must tell your insurer…" in order to contradict it.

> **Claim:** "Your home contents insurance will automatically cover the stock you keep in your garage."
> **Result:** Insufficient evidence. The sources we checked do not settle this. Your policy wording or your insurer can confirm.

> **Claim:** "You must tell your insurer about absolutely everything that could affect your policy."
> **Result:** Contradicted by evidence within the sources we checked. Source: Consumer Insurance (Disclosure and Representations) Act 2012, s.2(4), passage: "The duty set out in subsection (2) replaces any duty relating to disclosure or representations by a consumer to an insurer…". This is general guidance, not a check of your policy.

> **Claim:** "When you answer your insurer's questions, you need to take reasonable care to answer them accurately."
> **Result:** Supported by evidence within the sources we checked. Source: Consumer Insurance (Disclosure and Representations) Act 2012, s.2(2), passage: "It is the duty of the consumer to take reasonable care not to make a misrepresentation to the insurer." This is general guidance, not a check of your policy.

> **Note:** Some wording in this answer ("homeowners insurance", "deductible") may describe insurance outside the UK. UK policies may work differently.

---

## 4. Missing-context questions that should appear for Maya

| Rule | Shows? | Why |
|---|---|---|
| CR1 Has your insurer been told about the business? | **Yes** | She runs a business from home and doesn't know |
| CR2 What does your policy wording say about business stock, including any limit? | **Yes** | She keeps stock at home and hasn't checked |
| CR3 Rough stock value | No | Answered in the coach (£1,000 to £5,000, Stated) |
| CR4 Where stock is kept | No | Answered in the coach (attached garage, Stated) |
| CR5 Business visitors | **Yes** | The AI answer mentions customers visiting and public liability |
| CR6 Business equipment | **Yes** | The AI answer mentions her laptop and equipment |
| CR7 What type of policy, and in whose name? | **Yes** | She *thinks* it's home contents (Stated), but it isn't Confirmed by consumer |

**Expected: 5 questions (CR1, CR2, CR5, CR6, CR7).** Person D can use this as the missing-context check for this case.

---

## 5. Stage 3: Share selectively

**Maya ticks:** her business, stock held, stock location, value band, the AI assumption, and the CR1, CR2 and CR7 questions.
**She leaves unticked:** visitors and equipment (her choice). **Never included:** the chat, her name, address, phone or policy number.

**Note she copies:**

```
PREPARATION NOTE (made with ClearPass UK, a research prototype)
Date: 20 October 2026

About my situation (my own statements, not checked by anyone)
- I run a small business from home, making and selling handmade goods. [Stated by me]
- I keep business stock at home. [Stated by me]
- The stock is kept in a garage attached to my house. [Stated by me]
- My rough stock value is £1,000 to £5,000. [Stated by me]

Things I would like to confirm
- I would like to confirm whether my insurer has been told about the business I run from home.
- I would like to confirm what my policy says about business stock kept at home, including any limit.
- I would like to confirm what type of policy I hold and who is named on it, given I run a business from home.

Something an AI assistant told me that I have not confirmed
- An AI assistant told me: my home contents insurance will automatically cover the stock in my garage. I have not confirmed this.

This note does not say what any policy covers and is not insurance advice.
```

**Outcome for Maya:** she goes from "it's covered automatically" to three clear questions for her insurer, carrying only the five facts she chose.

---

## 6. What each person uses this for

| Person | Use |
|---|---|
| A (engineer) | Fixed demo input (3a), expected verdicts (3b), two evidence records (3c), expected questions (4) and expected note (5). This is a ready-made end-to-end test |
| B (evidence) | Review EV-LAW-01 and EV-LAW-02. Supply the source for C1. Confirm the UK wording for C4 |
| D (evaluation) | This is a demo case, not a hidden test case. Run the real rough vs coached ChatGPT comparison separately and report real counts |
| Everyone | The story for the pitch. Use the 60-second script, which already follows it |

## 7. Do not say in the demo

- "Maya is covered" or "Maya is not covered"
- "This is what ChatGPT said" about the synthetic answer in 3a
- That ClearPass is "FCA compliant" or "safe"
