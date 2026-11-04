# Pendiva recording handoff

Use this checklist to record the English, fictional-data walkthrough. The local UI and browser journey could not be opened from the verification sandbox because its socket policy blocks localhost access; startup and database seeding were verified. Confirm the visible UI before recording.

## Start the isolated demo

From the repository root in PowerShell, use a new database filename if you want a clean recording state:

```powershell
python -m scripts.iniciar_demo --demo --demo-language en --demo-no-finance --demo-db data/demo-recording-en.sqlite3
```

The command seeds nine fictional conversations and starts the local panel and isolated webhook receiver. The demo initializer is idempotent. It does not send a WhatsApp message or call Muse automatically. Stop both services with `Ctrl+C`.

**Supported Python:** 3.12 or newer.

## Configuration and demo login

- The seeded walkthrough needs no API credentials and no extra Python packages.
- Use the fictional demo email and password printed by the launcher. They are local demo credentials; never reuse them for a real account.
- For a live assistant answer, configure `MODEL_API_KEY` in the ignored local `.env` and confirm the on-screen consent before submitting. The key's current validity and Meta connectivity were not verified in this sprint. A live request may consume credits.
- `PENDIVA_COOKIE_SECURE=1` is only for HTTPS; leave it unset for this localhost demo.
- WhatsApp, ElevenLabs, and finance import are optional. The scripted path does not require WhatsApp or ElevenLabs. Import the included fictional CSV only if showing the sales chart.
- Do not display `.env`, terminal history beyond the printed demo credentials, browser notifications, personal chats, or real customer data.

## Recommended story

- **Customer:** Ana Rojas, fictional.
- **Opportunity:** Deep sofa cleaning, pending confirmation before a quote.
- **Evidence:** Ana's messages state that she wants a three-seat sofa cleaned in Chapinero this week and asks for a quote. The recommendation is to confirm the service address and preferred date before preparing the quote.
- **Human review:** Show the evidence and the review/edit controls. Do not claim that the customer was ignored, that a quote was sent, or that revenue was earned.

## Screens and Muse question

1. Keep the interface in English. Start on **Overview** and show the **Needs Attention** queue, source/evidence label, priority, and any explicit due date.
2. Open **Customers**, select Ana Rojas, and show the Decision Brief. Explain that the current recommendation is a saved fictional example, not fresh Muse output.
3. Show the customer messages, the exact missing address/date details, and the suggested next action. Click a source quote to jump to its message.
4. Select **Review recommendation** to reach the existing human review controls. Do not complete or dismiss the item unless you intend to demonstrate that action.
5. Select **Open reply draft**. Show the source message and editable composer; do not send it.
6. Select **Ask Muse what is missing**. Check the Meta/Muse consent and explicitly submit the prefilled question, if the live key is available:

   > What do I need to know before replying to Ana Rojas? What is known, what is missing, and what should I do next? Cite the stored messages.

7. Inspect the actual answer, cited messages, and coverage note. Wording may vary; do not present an expected answer as a live result.
8. Optionally open **Finances** and import `fixtures/demo/cleaning-sales-demo-en.csv`. State that it contains fictional example transactions and is not a bank connection or accounting report.

## If Muse is unavailable

Do not keep retrying on camera. Show Ana's seeded recommendation and its source message instead. Describe it as the saved fictional demo record, not a live Muse result. The rest of the core walkthrough remains available without external credentials.

## Skip during recording

- WhatsApp outbound or live sandbox claims: the latest recorded smoke test returned HTTP 401 and current connectivity is unverified.
- Live media analysis, voice mode, or ElevenLabs unless separately checked on the recording machine.
- Any statement that Pendiva sees a complete WhatsApp history, automatically replies, verifies payments, guarantees sales, or runs as a production SaaS.
- Any unreviewed Muse claim, amount, date, appointment, or payment status.

## Known limits and freeze identifier

- The demo data is fictional and covers only seeded conversations. The WhatsApp sandbox does not backfill old chat history.
- The owner assistant searches locally and can send a bounded set of relevant excerpts to Muse after explicit consent; it does not send the full database.
- Login throttling is process-local; tenant isolation, retention/deletion, production authentication, and deployment are not production-certified.
- A 24-case bilingual regression fixture exists, but it was not run against Muse in this sprint and is not an accuracy score.
- **Application freeze commit:** `9709e47da452dccfcebb8f3c13662bc65ccb1a46`. The recording instructions in this handoff are committed immediately after that code freeze; the final repository HEAD is reported in the delivery message.
- **Video recording and upload:** not performed; the project owner records and supplies the actual URL.
