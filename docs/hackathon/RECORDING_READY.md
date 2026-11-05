# Pendiva recording handoff

Use this checklist to record the English, fictional-data walkthrough. The local UI and browser journey could not be opened from the verification sandbox because its socket policy blocks localhost access; startup and database seeding were verified. Confirm the visible UI before recording.

## Start the isolated demo

From the repository root in PowerShell, use a new database filename if you want a clean recording state:

```powershell
python -m scripts.iniciar_demo --demo --demo-language en --demo-no-finance --demo-db data/pendiva-final-recording-en.sqlite3
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
- **Commitment:** Carlos Díaz asks about Saturday morning availability. The fictional advisor message says, “I will check the schedule and confirm tomorrow.” Its role is explicitly seeded as business-advisor authored. The original relative timing is preserved; no exact due date is inferred. Fulfillment starts unverified, which does not mean the promise was broken.

## Screens and Muse question

1. Keep the interface in English. Start on **Overview** and show the **Needs Attention** queue briefly.
2. Open **Customers → Ana Rojas**. Show the Decision Brief, the saved fictional-example label, missing address/date, suggested action, and one clickable source message.
3. Select **Carlos Díaz**. Show the advisor-authored promise, “Tomorrow” as stated, source message, and **Not verified**. Point to **Confirm fulfillment** and **Dismiss commitment** without clicking; this is a fictional example, not live Muse detection.
4. Open the assistant bubble. Check the consent box and click **Start voice conversation**. Allow microphone access if prompted. Ask aloud:

   > What information is still missing before I can quote Ana Rojas, and what should I ask her next?

5. Stop speaking and wait. Pendiva submits after 10 seconds without new recognized speech. Let it speak the answer; show its citations/coverage and the speaker icon beside the answer. Click that icon only if you want to replay the answer.

6. If a fresh Muse answer is available, inspect its sources and coverage. Wording may vary; do not present an expected answer as a live result.

7. Optionally return to Ana and select **Open reply draft**. Show the editable composer; do not send it.

8. Close with: “Traditional CRMs remember customers. Pendiva helps businesses remember their commitments.”

## Before showing a live Muse voice turn

Test the microphone, browser speech recognition, current Muse key/network, and spoken response before recording. A live request requires consent and may use credits. If it fails, do not retry repeatedly on camera. Continue with Ana and Carlos's clearly labeled fictional records; do not imply that their seeded analyses came from a live Muse call.

The browser may send microphone audio to its speech-recognition service. The transcript is sent to Muse only after the on-screen consent. The 10-second timer resets if more speech is recognized. To test replay, each assistant answer has a speaker icon. The mic and speaker depend on browser/device support.

If you choose to demonstrate the typed Muse path instead, check the same Meta/Muse consent and explicitly submit:

   > What do I need to know before replying to Ana Rojas? What is known, what is missing, and what should I do next? Cite the stored messages.

The current assistant does not retrieve commitment records; do not ask it to enumerate all commitments.

## If Muse is unavailable

Do not keep retrying on camera. Show Ana's seeded recommendation and its source message instead. Describe it as the saved fictional demo record, not a live Muse result. The rest of the core walkthrough remains available without external credentials.

## Skip during recording

- WhatsApp outbound or live sandbox claims: the latest recorded smoke test returned HTTP 401 and current connectivity is unverified.
- Live media analysis or ElevenLabs unless separately checked on the recording machine.
- Any statement that Pendiva sees a complete WhatsApp history, automatically replies, verifies payments, guarantees sales, or runs as a production SaaS.
- Any unreviewed Muse claim, amount, date, appointment, or payment status.

## Known limits and freeze identifier

- The demo data is fictional and covers only seeded conversations. The WhatsApp sandbox does not backfill old chat history.
- The owner assistant searches locally and can send a bounded set of relevant excerpts to Muse after explicit consent; it does not send the full database. Voice capture uses browser recognition, waits for 10 seconds of silence, then submits the transcript and reads the answer with device speech synthesis.
- Login throttling is process-local; tenant isolation, retention/deletion, production authentication, and deployment are not production-certified.
- A 24-case bilingual regression fixture exists, but it was not run against Muse in this sprint and is not an accuracy score.
- Carlos's commitment is a synthetic seeded example reviewed through the existing recommendation controls. Live Muse commitment extraction, dedicated commitment records, automatic due-date resolution, and commitment-aware assistant retrieval are deferred. No live Muse call was made for this release.
- **Application freeze commit:** `14c05da` (`Make Pendiva voice assistant hands-free`). The recording instructions in this handoff are committed immediately after that code freeze; the final repository HEAD is reported in the delivery message.
- **Video recording and upload:** not performed; the project owner records and supplies the actual URL.
