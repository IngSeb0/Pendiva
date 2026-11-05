# Pendiva — Three-minute demo video script

**Recording status:** The project owner records and uploads the video. This document is a guide, not evidence that recording has occurred. Keep the interface and spoken demo question in English. The instructions below are in Spanish for the presenter; read only the quoted narration aloud. Use fictional seeded data only.

## Before recording

Run the isolated English demo from the repository root:

```powershell
python -m scripts.iniciar_demo --demo --demo-language en --demo-no-finance --demo-db data/pendiva-final-recording-en.sqlite3
```

See the detailed [recording handoff](RECORDING_READY.md) for optional credentials, the isolated database path, screens, limitations, and fallbacks. Use a new database filename for a clean take.

Sign in with the fictional credentials printed by the launcher. Import `fixtures/demo/cleaning-sales-demo-en.csv` in the Sales page if showing the chart. The no-finance flag prevents duplicate demo transactions. Check the [English recording pack](../validation/demo-recording-pack-en.md) for setup details. Do not include real WhatsApp chats, credentials, browser notifications, or a public live-service claim.

## Storyboard and exact narration

| Time | Screen and action | Narration |
|---|---|---|
| 0:00–0:15 | **Overview**. Keep English and dark theme visible; briefly show Needs Attention. | “A service business can receive quote requests, scheduling questions, and follow-ups in WhatsApp. Pendiva helps the owner see what needs attention across the conversations it has received.” |
| 0:15–0:45 | Open **Customers → Ana Rojas**. Show her source messages, the saved fictional-example label, missing address/date, and next action. Click one evidence quote. | “Pendiva connects the customer’s actual messages to the details we know and the information still to confirm. This is a saved synthetic example, not a fresh Muse answer.” |
| 0:45–1:15 | Select **Carlos Díaz**. Show **Commercial Commitment**, advisor-authored source message, “Tomorrow” as stated, and **Not verified**. | “Pendiva also keeps track of what the business said it would do. Carlos’s fictional advisor promised to check availability and confirm tomorrow. We preserve the speaker and original timing; fulfillment is not verified, which does not mean it was broken.” |
| 1:15–1:30 | Point at **Confirm fulfillment** and **Dismiss commitment**. Do not click unless intentionally recording a human confirmation in the fictional seed. | “The owner decides whether this was fulfilled. Pendiva records that human decision; it does not infer completion from silence or send a message.” |
| 1:30–2:35 | Open the assistant bubble. Check the consent box. Start **voice conversation**, allow the microphone, and say: “What information is still missing before I can quote Ana Rojas, and what should I ask her next?” Stop speaking and let the 10-second silence timer send it. Let Pendiva speak. Show the source/coverage note and the speaker icon beside the response. | “I can also ask Pendiva by voice. After I finish speaking, it waits for ten seconds of silence, sends the transcript to Muse with my consent, and reads the answer aloud. I can replay any answer with its speaker button.” |
| 2:35–3:00 | Finish on the answer or return to the dashboard. | “Traditional CRMs remember customers. Pendiva helps businesses remember their commitments. It connects conversations, evidence, and decisions.” |

## Muse prompt

Use this exact prompt:

> “What do I need to know before replying to Ana Rojas? What is known, what is missing, and what should I do next? Cite the stored messages.”

**Expected response type, not guaranteed wording:** A short answer about Ana's available messages, missing details, next step, source references, and coverage limits. Review the actual answer before recording. Do not script an unobserved response as if Muse produced it live. The voice turn sends only after 10 seconds without new recognized speech; any additional speech resets that wait. A live answer requires a working Muse key, network, microphone permission, and the on-screen consent.

## Recommended demo customer and evidence

- **Customer:** Ana Rojas, a fictional seeded customer in the cleaning-business demo.
- **Evidence:** The exact conversation message asking about sofa cleaning; show it beside the related pending opportunity/recommendation.
- **Human action:** Open or resolve the recommendation only after checking its source. Do not imply that this sends a WhatsApp reply.
- **Commercial commitment:** Carlos Díaz's source message is explicitly tagged as advisor-authored in the fictional seed. The UI has no exact due date because “tomorrow” is preserved as written. A human confirmation is a demo review action, not an independently verified event.
- **Hands-free voice:** The browser's speech recognition transcribes the spoken question. Pendiva waits for 10 seconds of silence, submits the transcript after the existing Muse consent, and speaks the answer using device speech synthesis. The speaker icon beside each assistant answer replays it locally.
- **Optional media:** The synthetic sofa image may be shown only if it is present in this seed, consent is enabled, a current Muse call succeeds, and the observation is reviewed. Skip it otherwise.

## Backup if a live service fails

1. Do not retry repeatedly on camera or imply a successful live call.
2. Show the seeded recommendation and its exact source message instead.
3. State that the walkthrough uses fictional data and that current external connectivity is not verified.
4. If the answer is stale or from an earlier run, identify it as a saved demo result; do not call it a live response.

## Recording checklist

- [ ] English UI, customer content, prompt, and narration.
- [ ] Test the microphone, speech recognition, Muse request, and spoken answer before recording; the live assistant needs a working key and can use credits.
- [ ] Start from a fresh isolated database so Ana's and Carlos's demo review states are reset.
- [ ] Isolated `demo-en.sqlite3` database; only fictional customers and transactions.
- [ ] Browser zoom at 100–110%, 16:9 window, unrelated tabs closed.
- [ ] Muse consent visible before a live request; inspect answer and evidence before capture.
- [ ] Show the coverage/source note after the assistant response.
- [ ] No secrets, actual customer numbers, personal chats, notifications, or local-only URL presented as a public deployment.
- [ ] Explain that browser recognition may send audio to its recognition service; only the transcript is sent to Muse after consent. The voice loop is turn-based with a 10-second silence delay, not low-latency streaming.
- [ ] No claims of complete history sync, automatic replies, verified payments, bookings, revenue recovered, accuracy guarantees, or production readiness.
- [ ] Upload video and paste its actual URL into `SUBMISSION.md` and the checklist.

## Critical mistakes to avoid

Do not present a seeded customer or CSV value as a real business outcome. Do not say Muse analyzes every WhatsApp message: it sees the messages available to Pendiva and, in the owner assistant, a bounded subset of relevant excerpts. Do not present a test message as proof of outbound delivery. Do not describe the prototype as a deployed SaaS.
