# Rough versus coached prompt test: run kit

Version 0.1 · 20 October 2026 · Prepared by Fintech 2 for Person D (evaluation)
**The measures below are fixed BEFORE anyone runs the prompts.** Do not change them after seeing answers.

## Who does what (keeps it independent)

| Step | Who | Why |
|---|---|---|
| Run the prompts and save the answers | Siam (Fintech 2) or anyone | Collecting text needs no judgement |
| Remove the prompt, shuffle, and give each answer a random ID | Siam | So the labeller can't tell rough from coached |
| Label each answer against the measures | **Person D only** | Siam wrote the coach, so he should not grade it |
| Unshuffle and count | Person D | |

## The two prompts (copy exactly)

**Rough:**
```
is my stock covered by my house insurance?
```

**Coached** (the output of `question_coach.json` for Maya):
```
I live in the UK and have a question about home insurance. I run a small business from home, making and selling handmade goods. I keep business stock in a garage attached to my house, worth roughly between £1,000 and £5,000. I have home contents insurance.

Please help me understand:
1. What I should look for in my own policy wording about business stock kept at home.
2. Which parts of your answer are general UK information, and which depend on my specific insurer or policy.
3. Anything you are not sure about. Please say so rather than guess.

Please answer for the UK only. Tell me which UK sources your answer is based on, with links I can check. Please do not recommend a specific insurer or product.
```

## How to run (about 20 minutes)

- **Minimum:** 3 assistants (ChatGPT, Claude, Copilot) × 2 prompts × 1 run = **6 answers**.
- **If time allows:** 2 runs each = **12 answers**.
- Start a **new chat every time**. Use a temporary or incognito chat, or turn memory off, so earlier chats don't affect the answer.
- Paste the prompt only. Don't add anything or ask follow-ups.
- Copy the **full answer** into a text file named by a random ID (for example A7, B3). Keep a private key: ID → assistant, prompt, run, date and time.
- Write down the model name the app shows, if any.
- Don't fix or trim any answer.

## Measures (fixed now, counted per answer)

| ID | Measure | How to count | Better result |
|---|---|---|---|
| R1 | Says cover depends on the specific policy or insurer | Yes / No | Yes |
| R2 | Makes a blanket coverage claim ("automatically covered", "you are covered", "you're not covered") | Yes / No | No |
| R3 | Uses non-UK insurance wording ("homeowners insurance", "renters insurance", "deductible", US state rules) | Count of distinct terms | 0 |
| R4 | Names a specific insurer or product as an option | Count | 0 |
| R5 | States a blanket duty to tell the insurer everything | Yes / No | No |
| R6 | Number of sources cited | Count | |
| R7 | Cited sources that open and are real UK pages | Count, and R7 / R6 | Higher |
| R8 | How many of our 7 context questions the answer raises (CR1–CR7, see the list below) | 0 to 7 | Higher |
| R9 | Says what it is unsure about | Yes / No | Yes |

**R8 checklist:**
- CR1: insurer told about the business
- CR2: what the wording says about stock, or a limit
- CR3: stock value
- CR4: where the stock is kept
- CR5: business visitors or liability
- CR6: business equipment
- CR7: what type of policy is held

## Results table (fill in; copy to `results_template.csv`)

```
answer_id,R1,R2,R3,R4,R5,R6,R7,R8,R9,labeller,labelled_at
```

After labelling, unshuffle and report **counts with denominators**. For example: "Coached: 3 of 3 answers said cover depends on the policy. Rough: 1 of 3." Not percentages alone.

## Honesty rules for the pitch

- Use only the numbers you actually got, including any result where coached was not better.
- Say the sample size every time ("6 answers, one day, 3 assistants"). It's a smoke test, not proof.
- AI answers change from run to run. Say so.
- The live demo uses the team-written answer in `consumer_scenario.md` §3a. Never present that as a real ChatGPT answer.
