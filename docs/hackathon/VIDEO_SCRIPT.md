# Pendiva — Three-minute demo video script

**Recording status:** The project owner records and uploads the video. This document is a guide, not evidence that recording has occurred. Keep the interface and narration in English. Use fictional seeded data only.

## Before recording

Run the isolated English demo from the repository root:

```powershell
python -m scripts.iniciar_demo --demo --demo-language en --demo-no-finance --demo-db data/commitment-recording-en.sqlite3
```

See the detailed [recording handoff](RECORDING_READY.md) for optional credentials, the isolated database path, screens, limitations, and fallbacks. Use a new database filename for a clean take.

Sign in with the fictional credentials printed by the launcher. Import `fixtures/demo/cleaning-sales-demo-en.csv` in the Sales page if showing the chart. The no-finance flag prevents duplicate demo transactions. Check the [English recording pack](../validation/demo-recording-pack-en.md) for setup details. Do not include real WhatsApp chats, credentials, browser notifications, or a public live-service claim.

## Storyboard and exact narration

| Time | Screen and action | Narration |
|---|---|---|
| 0:00–0:20 | Home dashboard. Keep English and dark mode visible. | “A service business can receive quote requests, scheduling questions, and follow-ups in WhatsApp. Pendiva helps the owner see what needs attention across the conversations it has received.” |
| 0:20–0:55 | Open **Customers**. Select the fictional customer **Ana Rojas**. Show the Decision Brief: observed messages, saved-demo provenance, missing address/exact date, and next action. | “Pendiva connects the customer’s actual messages to the details we know and the information still to confirm. This is a saved synthetic example, not a fresh Muse answer.” |
| 0:55–1:30 | Select **Carlos Díaz**. Show **Commercial Commitment**, the advisor's source message, “Tomorrow” as stated, and the unverified status. | “Pendiva also keeps track of what the business said it would do. Carlos’s fictional advisor promised to check availability and confirm tomorrow. We preserve the speaker and the original timing; fulfillment is not verified, which does not mean it was broken.” |
| 1:30–1:50 | Point to **Confirm fulfillment** and **Dismiss commitment**. For a synthetic demo, optionally confirm after explaining it records a human review. | “The owner decides whether this was fulfilled. Pendiva records that human decision; it does not infer completion from silence or send a message.” |
| 1:50–2:05 | Return to Ana and choose **Open reply draft**. Show the editable composer; do not send. | “For a customer request, the same workflow connects missing details to an editable reply draft.” |
| 2:05–2:35 | Optionally choose **Ask Muse what is missing**. Confirm consent and explicitly submit only if the current real request succeeds. | “Muse supports evidence-backed interpretation of the conversation after consent. This saved commitment example is synthetic; live commitment extraction is not yet enabled.” |
| 2:35–3:00 | End on the Decision Brief or dashboard. | “Traditional CRMs remember customers. Pendiva helps businesses remember their commitments. It connects conversations, evidence, and decisions.” |

## Muse prompt

Use this exact prompt:

> “What do I need to know before replying to Ana Rojas? What is known, what is missing, and what should I do next? Cite the stored messages.”

**Expected response type, not guaranteed wording:** A short summary of the relevant seeded conversations, missing details, source references, and an uncertainty or coverage note. Review the actual answer before recording. Do not script an unobserved response as if Muse produced it live.

## Recommended demo customer and evidence

- **Customer:** Ana Rojas, a fictional seeded customer in the cleaning-business demo.
- **Evidence:** The exact conversation message asking about sofa cleaning; show it beside the related pending opportunity/recommendation.
- **Human action:** Open or resolve the recommendation only after checking its source. Do not imply that this sends a WhatsApp reply.
- **Commercial commitment:** Carlos Díaz's source message is explicitly tagged as advisor-authored in the fictional seed. The UI has no exact due date because “tomorrow” is preserved as written. A human confirmation is a demo review action, not an independently verified event.
- **Optional media:** The synthetic sofa image may be shown only if it is present in this seed, consent is enabled, a current Muse call succeeds, and the observation is reviewed. Skip it otherwise.

## Backup if a live service fails

1. Do not retry repeatedly on camera or imply a successful live call.
2. Show the seeded recommendation and its exact source message instead.
3. State that the walkthrough uses fictional data and that current external connectivity is not verified.
4. If the answer is stale or from an earlier run, identify it as a saved demo result; do not call it a live response.

## Recording checklist

- [ ] English UI, customer content, prompt, and narration.
- [ ] Start from a fresh isolated database so Ana's and Carlos's demo review states are reset.
- [ ] Isolated `demo-en.sqlite3` database; only fictional customers and transactions.
- [ ] Browser zoom at 100–110%, 16:9 window, unrelated tabs closed.
- [ ] Muse consent visible before a live request; inspect answer and evidence before capture.
- [ ] Show the coverage/source note after the assistant response.
- [ ] No secrets, actual customer numbers, personal chats, notifications, or local-only URL presented as a public deployment.
- [ ] Voice mode only if microphone permission and browser speech support work; explain it is browser-based and turn-by-turn.
- [ ] No claims of complete history sync, automatic replies, verified payments, bookings, revenue recovered, accuracy guarantees, or production readiness.
- [ ] Upload video and paste its actual URL into `SUBMISSION.md` and the checklist.

## Critical mistakes to avoid

Do not present a seeded customer or CSV value as a real business outcome. Do not say Muse analyzes every WhatsApp message: it sees the messages available to Pendiva and, in the owner assistant, a bounded subset of relevant excerpts. Do not present a test message as proof of outbound delivery. Do not describe the prototype as a deployed SaaS.
