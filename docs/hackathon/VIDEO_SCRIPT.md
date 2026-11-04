# Pendiva — Three-minute demo video script

**Recording status:** The project owner records and uploads the video. This document is a guide, not evidence that recording has occurred. Keep the interface and narration in English. Use fictional seeded data only.

## Before recording

Run the isolated English demo from the repository root:

```powershell
python -m scripts.iniciar_demo --demo --demo-language en --demo-no-finance --demo-db data/demo-en.sqlite3
```

See the detailed [recording handoff](RECORDING_READY.md) for optional credentials, a safe clean database path, screens, limitations, and fallbacks.

Sign in with the fictional credentials printed by the launcher. Import `fixtures/demo/cleaning-sales-demo-en.csv` in the Sales page if showing the chart. The no-finance flag prevents duplicate demo transactions. Check the [English recording pack](../validation/demo-recording-pack-en.md) for setup details. Do not include real WhatsApp chats, credentials, browser notifications, or a public live-service claim.

## Storyboard and exact narration

| Time | Screen and action | Narration |
|---|---|---|
| 0:00–0:20 | Home dashboard. Keep English and dark mode visible. | “A service business can receive quote requests, scheduling questions, and follow-ups in WhatsApp. Pendiva helps the owner see what needs attention across the conversations it has received.” |
| 0:20–0:50 | Open **Customers**. Select the fictional customer **Ana Rojas**. Show her conversation and a pending opportunity. | “Here, Ana is asking about sofa cleaning. The conversation is organized with the customer workflow, so the team can see the request and what still needs to be confirmed.” |
| 0:50–1:20 | Open the recommendation and its evidence. Point to the source message. | “Muse can suggest a next step, but the source stays visible. The owner can check whether the recommendation is supported, then edit it, complete it, or dismiss it.” |
| 1:20–1:55 | Open the assistant bubble. Confirm the on-screen Muse consent. Enter the prompt below and submit. | “The owner can also ask across the available conversations. Pendiva searches locally, sends a limited set of relevant excerpts to Muse after consent, and shows that the answer covers only the evidence available to it.” |
| 1:55–2:20 | Show the answer's source/coverage details. If the call is not available, show the pre-seeded recommendation instead. | “This is an assistant for the business workflow: it helps surface missing information and follow-ups. It does not send customer messages automatically, and the owner remains responsible for checking the answer.” |
| 2:20–2:45 | Show Sales chart with imported English CSV and source note. | “The sales view summarizes example transactions imported from a local CSV. These records are fictional and have no declared currency; this is not a bank connection or accounting report.” |
| 2:45–3:00 | Return to Home or the customer evidence view. | “Pendiva keeps the conversation, the evidence, and the next decision close together: less buried in chat, more clear on what needs attention.” |

## Muse prompt

Use this exact prompt:

> “Which quotes need attention, and what information is missing before we can reply? Cite the supporting customer messages, separate facts from suggestions, and do not invent prices, dates, availability, or payment status.”

**Expected response type, not guaranteed wording:** A short summary of the relevant seeded conversations, missing details, source references, and an uncertainty or coverage note. Review the actual answer before recording. Do not script an unobserved response as if Muse produced it live.

## Recommended demo customer and evidence

- **Customer:** Ana Rojas, a fictional seeded customer in the cleaning-business demo.
- **Evidence:** The exact conversation message asking about sofa cleaning; show it beside the related pending opportunity/recommendation.
- **Human action:** Open or resolve the recommendation only after checking its source. Do not imply that this sends a WhatsApp reply.
- **Optional media:** The synthetic sofa image may be shown only if it is present in this seed, consent is enabled, a current Muse call succeeds, and the observation is reviewed. Skip it otherwise.

## Backup if a live service fails

1. Do not retry repeatedly on camera or imply a successful live call.
2. Show the seeded recommendation and its exact source message instead.
3. State that the walkthrough uses fictional data and that current external connectivity is not verified.
4. If the answer is stale or from an earlier run, identify it as a saved demo result; do not call it a live response.

## Recording checklist

- [ ] English UI, customer content, prompt, and narration.
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
