# Pendiva

**Turn WhatsApp conversations into clear, evidence-backed follow-through for service businesses.**

Pendiva is a local hackathon prototype for service teams. It organizes the messages received by its webhook into customer conversations, asks Meta Muse Spark to help identify what needs attention, and keeps the supporting message visible so a person can review the suggestion. The owner can also ask questions across the available conversation data by text or browser voice.

> **Prototype status:** The repeatable judge demo uses fictional data. WhatsApp is an experimental sandbox integration, not a production connection. Pendiva does not automatically reply to customers.

## Why Pendiva

Small service businesses often manage quote requests, scheduling details, objections, and follow-ups inside chat. A conventional CRM can store contacts and stages; a generic chatbot can answer a prompt. Pendiva focuses on the operational handoff between conversation and work: organize a signal, show its source, surface what remains unknown, and let the owner decide the next action.

## What the prototype does

- **Customer decision brief:** move from a pending customer request to known context, missing details, a next action, source messages, and the existing human-review/reply-draft controls in one place.
- **Customer inbox:** review contacts, conversations, message evidence, and manually tracked opportunities. Saved rule-based demo examples are labeled as synthetic rather than as live Muse output.
- **Needs-attention queue:** combines current Muse suggestions with team-recorded dated follow-ups; cards distinguish their origin, show explicit dates and evidence, and do not infer an ignored customer.
- **Muse-assisted analysis:** request structured recommendations for a conversation and review the cited source messages before resolving them.
- **Owner assistant:** search the tenant's stored messages locally, send a bounded set of relevant excerpts to Muse after consent, and disclose the coverage used.
- **Voice interaction:** dictate a question with browser speech recognition and hear Muse's response using device speech synthesis. The loop is turn-based, not low-latency voice-to-voice.
- **Service-business workflow:** keep service details, missing information, follow-ups, and human-reviewed quote drafts together. Drafts are not sent to customers.
- **Safer amount handling:** label an amount as customer budget, business quote, payment claim, estimate, other, or unknown. Every amount remains unverified until a person confirms it; no amount type proves revenue.
- **Multimodal workspace:** upload or explicitly fetch supported media and ask Muse to analyze it after consent. AI observations are unverified and must be checked against the file.
- **Sales view:** chart monthly sales and expenses from a local CSV. This is not a bank connection or accounting system, and imported amounts have no currency unless supplied separately.
- **Custom views:** propose and review simple business views based on supported fields. This feature does not generate or run arbitrary code.
- **English and Spanish UI:** select the interface language; new Muse requests receive the selected language. Previously saved content keeps its original language.
- **Dark theme and demo data:** use the synthetic cleaning-business seed for a reproducible walkthrough.

## Demo video

**Recording and URL pending.** Use the three-minute [video script](docs/hackathon/VIDEO_SCRIPT.md) and the detailed [recording handoff](docs/hackathon/RECORDING_READY.md). The demo seed and CSV contain fictional customers and figures.

## Screenshots

No judge-facing screenshots are included yet. Add screenshots only after capturing the current application with fictional demo data and checking that no local credentials, personal chats, or private notifications are visible.

## How it works

1. A signed Meta WhatsApp webhook can deliver sandbox events to the local receiver. The receiver checks the signature, accepts the configured test phone-number ID, and deduplicates message events before storing them in SQLite.
2. The owner reviews the stored conversation in the Pendiva dashboard. The sandbox does not import earlier chat history; it contains only events delivered to the webhook.
3. On explicit consent, the app sends message text and limited business context to Meta Model API (Muse Spark). For the cross-conversation assistant, local search ranks stored messages and sends up to 36 relevant excerpts, not the entire database.
4. The server validates the returned structure and evidence IDs. The owner reviews each suggestion and decides whether to keep, edit, complete, or dismiss it.
5. Sales charts are calculated from locally imported CSV records. Voice uses browser speech recognition and device speech synthesis; neither makes the conversation a real-time Muse audio stream.

## Built with Meta AI

The product's current AI provider is **Meta Model API with Muse Spark**. Muse supports evidence-grounded conversation analysis, owner questions, reply drafts, opportunity suggestions, and analysis of supported media. The server calls Meta's Responses API, requests structured output for workflows that need it, and validates source references before accepting a recommendation. Requests use `store: false` where implemented. Consent is required before the app sends conversation context or media to Meta.

Meta Model API use is separate from WhatsApp Cloud API credentials. A configured key does not prove that a live call works. Historical successful calls are documented with date, scope, and limitations in [`docs/validation/muse.md`](docs/validation/muse.md); current credentials and network connectivity were not verified for this release.

## Technical architecture

| Area | Implementation |
|---|---|
| Application | Python 3.12 standard library; local HTTP server and static HTML/CSS/JavaScript interface |
| Persistence | SQLite for the local prototype and seeded demo |
| AI | Meta Model API Responses endpoint; Muse Spark; server-side key and consent gates |
| Messaging | Meta WhatsApp Cloud API webhook for a configured sandbox number; signed event validation and deduplication |
| Media | Local media handling plus optional explicit WhatsApp media fetch and Muse analysis |
| Voice | Browser speech recognition and device speech synthesis; optional ElevenLabs transcription integration |
| Finance | Local CSV import and aggregation/charting; no bank or accounting connection |
| Demo | Fictional, idempotent seed data in a separate SQLite database |

The repository also contains an early SaaS foundation with tenants, users, memberships, roles, and domain tables. Its presence does not mean full production-grade tenant isolation, PostgreSQL migrations, deployment operations, or SaaS readiness have been established. See the [roadmap](docs/roadmap.md) and [known limitations](docs/hackathon/FINAL_READINESS_REPORT.md).

## Quick start

Requires Python 3.12+. The core demo does not require third-party Python packages or API keys.

```powershell
python -m scripts.iniciar_demo --demo --demo-language en --demo-no-finance --demo-db data/demo-en.sqlite3
```

Open the local URL printed by the command and sign in with the fictional credentials printed in the terminal. To show the sales chart without duplicating seed records, import [`fixtures/demo/cleaning-sales-demo-en.csv`](fixtures/demo/cleaning-sales-demo-en.csv) from the Sales page. Stop the server with `Ctrl+C`.

For a new local business without fictional seed data, start the app with `python -m scripts.iniciar_demo`, then call the one-time `/api/auth/bootstrap` endpoint as documented in the launcher or the in-app setup. Keep SQLite bound to localhost; it is not suitable for direct Internet exposure.

The first-account setup is available only while the database has no users. It permits that bootstrap request plus login/status and a minimal `/health` endpoint; other APIs require authentication. Owner, manager, and advisor roles can write; viewers are read-only. Login attempts are throttled in memory per IP and normalized account identifier. The session bearer is kept in an HttpOnly cookie; the separate CSRF token is returned for the request header. Set `PENDIVA_COOKIE_SECURE=1` only when serving the panel over HTTPS. This lightweight local throttle and auth implementation are not a substitute for production identity infrastructure.

### Optional Muse calls

Set `MODEL_API_KEY` in the ignored local `.env` file. Do not commit or paste the key into chat. To make one real request with synthetic input (may consume credits):

```powershell
python -m scripts.iniciar_demo --check-model --provider meta
```

The interactive conversation analysis also requires on-screen consent. Legacy Nebius or other provider variables do not enable an alternate provider in the product.

### Optional WhatsApp sandbox

The sandbox requires Meta app configuration, a public HTTPS callback, `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_VERIFY_TOKEN`, `WHATSAPP_APP_SECRET`, and a configured test recipient where applicable. See the [sandbox guide](docs/validation/live-sandbox.md). Use only an authorized test number and never commit credentials. In the latest recorded attempt, an outbound smoke test returned HTTP 401 and a later external request could not resolve DNS; live connectivity is therefore unverified. The prior inbound sandbox message and historical Muse analysis are documented as dated evidence, not current availability.

## Evaluation results

The recorded eight-case synthetic Muse exploration and its limitations are documented in [`docs/hackathon/AI_EVALUATION.md`](docs/hackathon/AI_EVALUATION.md). The repository now includes a separate, bilingual 24-case labeled fixture for regression and future evaluation. The fixture has not been run against Muse in this sprint and is not an accuracy score.

## Security and responsible AI

- API credentials stay on the server in local environment configuration; `.env` and local `data/` are excluded from Git.
- Conversation and media analysis require explicit consent before sending content to Muse.
- The application limits the context it sends and maps temporary evidence aliases back locally.
- Server-side checks require recommendations to refer to available evidence; valid structure does not guarantee truth.
- The owner must verify AI observations, prices, dates, payments, and suggested actions. No customer reply is sent automatically.
- Use synthetic demo data for screen recordings. Do not expose real customer messages or phone numbers.
- Review retention, deletion, access control, and applicable privacy obligations before any real-business pilot.

## Known limitations

- No production deployment or live demo URL is verified.
- Current WhatsApp credentials/connectivity are unverified; the latest outbound smoke test returned HTTP 401.
- The sandbox does not import complete WhatsApp history, and webhook coverage may omit outbound messages.
- Pendiva does not auto-reply, book jobs, verify payments, connect to banks, or claim recovered revenue.
- Muse quality has only exploratory synthetic evaluation; independent human validation and a larger bilingual/multimodal set remain needed.
- Voice depends on browser/device speech capabilities and permissions; it is not real-time audio streaming. Browser transcription and optional ElevenLabs calls can transmit audio to those providers.
- Sales amounts do not carry a guaranteed currency or accounting status.
- SaaS-grade isolation, operational controls, production database migration, and legal/privacy review remain incomplete.
- The project has no owner-approved open-source license in the repository; see [`docs/hackathon/FINAL_READINESS_REPORT.md`](docs/hackathon/FINAL_READINESS_REPORT.md).

## Roadmap

Near-term priorities are a reproducible English demo, broader and independently reviewed Muse evaluation, current sandbox verification, transparent coverage and retention controls, and owner-approved licensing. Product milestones and external dependencies are tracked in [`docs/roadmap.md`](docs/roadmap.md).

## Documentation

- [Hackathon submission copy](SUBMISSION.md)
- [Video script and recording checklist](docs/hackathon/VIDEO_SCRIPT.md)
- [AI evaluation](docs/hackathon/AI_EVALUATION.md)
- [Impact statement](docs/hackathon/IMPACT.md)
- [Submission checklist](docs/hackathon/SUBMISSION_CHECKLIST.md)
- [Final readiness report](docs/hackathon/FINAL_READINESS_REPORT.md)
- [English demo recording pack](docs/validation/demo-recording-pack-en.md)
- [Product MVP](docs/product/mvp.md)
- [Development roadmap](docs/roadmap.md)
- [Muse validation history](docs/validation/muse.md)
- [WhatsApp sandbox guide](docs/validation/live-sandbox.md)

## Tests

Run the automated Python and voice tests from the repository root:

```powershell
python -m unittest discover -v
node --test tests/voice_session.test.js
```

Test success verifies software behavior against the test suite; mocked API tests do not verify current Meta availability or model quality.

## License

No license is currently declared. Reuse and redistribution terms require a decision from the project owner; no license is implied by public repository access.
