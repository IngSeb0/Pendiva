# Pendiva — Hackathon Submission Copy

**Status:** Reusable, judge-facing copy prepared from the implementation and dated evidence in this repository. Meta's public event page confirms the submission deadline and tracks/themes, but its detailed submission form and field limits were not publicly readable when checked on November 4, 2026. Confirm the actual form fields and limits before pasting. Do not treat an optional or placeholder field below as an official requirement.

## Project title

Pendiva — Evidence-backed follow-through for service businesses

## One-line pitch

Pendiva helps service businesses turn WhatsApp conversations into organized, evidence-backed next steps with Meta Muse Spark and human review.

## Short description (~300 characters)

Service businesses manage quote requests, scheduling, and follow-ups in chat. Pendiva organizes received WhatsApp messages into customer workflows, uses Meta Muse Spark to surface evidence-backed recommendations, and helps owners decide what to review next. People stay in control; it does not auto-reply.

## Medium description (~500–700 characters)

Pendiva is a local prototype for service businesses receiving customer requests through WhatsApp. It stores messages delivered to its configured webhook and organizes them into customer conversations. With consent, an owner can ask Meta Muse Spark to identify follow-ups or missing details. Recommendations link to source messages and require human review. Owners can search available conversations, use browser voice, review supported media, and chart sales and expenses from a local CSV. The demo uses fictional cleaning-business data. Pendiva does not import complete WhatsApp history, send automatic replies, or claim production SaaS readiness.

## Full description (~1,000–1,500 characters)

Small service businesses often receive quote requests, scheduling details, price concerns, and follow-up questions in WhatsApp. Important context can be hard to find when it is mixed into everyday chats. A conventional CRM organizes contacts and stages; a generic chatbot responds to prompts. Pendiva focuses on the work between a customer conversation and a business decision.

The prototype receives signed events from a configured WhatsApp sandbox webhook and stores the messages delivered to it in a local SQLite database. The owner reviews customers and conversations in one dashboard. With explicit consent, Pendiva sends bounded conversation context to Meta Model API, powered by Muse Spark, to suggest next steps or draft an owner-reviewed response. The server validates structured output and checks that cited message IDs exist. The owner can search across stored messages, review supported media, and ask questions by text or browser-based voice. A sales view charts locally imported CSV records.

Pendiva's central design choice is to keep the source evidence and human decision beside the AI suggestion. It does not silently message customers, verify payments, or infer revenue impact. The repeatable hackathon walkthrough uses fictional cleaning-business data. WhatsApp history completeness, current external credentials, production isolation, and model quality at scale remain unverified.

## Problem statement

Small service teams coordinate customer requests in conversational channels but often lack a fast way to find what was requested, what information is missing, and which follow-up needs a person's attention. A contact list alone does not connect an operational suggestion to the message that supports it.

## Solution

Pendiva turns the messages it receives into organized customer workflows and asks Muse Spark to help identify follow-ups. It presents source messages, coverage limits, and review controls alongside the recommendation. The owner decides whether to act.

## Innovation

Pendiva combines a service-business workflow with evidence-linked AI assistance: the owner can move from a customer request to a proposed next step while retaining the exact supporting message and the ability to correct or dismiss the suggestion. The goal is a reliable operational assistant rather than an autonomous sales bot. This is a product hypothesis demonstrated in a prototype, not a measured competitive advantage.

## How we use Meta AI

The current application uses Meta Model API and Muse Spark for conversation analysis, owner-facing questions, quote-reply drafts, opportunity suggestions, and supported media analysis. The server sends bounded context after explicit consent, requests structured output where appropriate, and validates output shape and evidence references before presenting a recommendation. Where implemented, requests set `store: false`. See [Muse validation history](docs/validation/muse.md) and [AI evaluation](docs/hackathon/AI_EVALUATION.md). Historical successful calls do not verify the current local key or guarantee current service availability.

## Technical architecture

The demo uses Python 3.12's standard library, a local HTTP server, static HTML/CSS/JavaScript, and SQLite. A WhatsApp webhook validates request signatures and deduplicates events for the configured sandbox number. Muse calls are server-side and use `MODEL_API_KEY`; the product does not fall back to Nebius. Voice uses browser speech recognition and device speech synthesis, with optional ElevenLabs transcription. Sales charts use locally imported CSV data. See the [root README](README.md) for setup and boundaries.

## Real-world impact

If validated with service businesses, Pendiva could reduce the effort of locating customer context and make follow-up needs easier to review. No time savings, conversion lift, revenue recovery, or customer outcome has been measured. The [impact statement](docs/hackathon/IMPACT.md) separates the problem hypothesis from available evidence and the validation still needed.

## Technical challenges

- Building evidence-linked structured recommendations while validating each cited message on the server.
- Managing signed, duplicate webhook events and keeping the local sandbox workflow separate from the seeded demo.
- Sending bounded context and exposing partial coverage instead of implying that Muse saw a complete WhatsApp history.
- Handling provider output variability, including incomplete structured output and the observed ambiguity between a customer's budget and the business's quote.
- Keeping voice, media analysis, and finance features explicit about external data transfer and their current prototype limits.

## Responsible AI

Pendiva requires consent before sending conversation context or media to Muse. Recommendations must cite available messages, but valid references do not prove an interpretation is correct. Owners should inspect the source, correct errors, and make all customer-facing decisions. Payments, prices, dates, bookings, and financial outcomes are not treated as verified solely because a model or message mentions them. The recording uses fictional data. Privacy, retention, and legal requirements need review before a real-business pilot.

## Evaluation

An exploratory eight-case synthetic text run is documented in `docs/validation/evaluacion-extraccion.md`. In that run, generated proposals cited valid source IDs and the tested ambiguous date and absent price did not become an invented exact date or price. One budget-versus-quote semantic ambiguity and weaker next-step suggestions were observed. Codex reviewed the sample; there was no independent business-expert review. This is not a production precision estimate. See `docs/hackathon/AI_EVALUATION.md`.

## Known limitations

The demo is local and not production SaaS. WhatsApp history is not backfilled, and current sandbox connectivity is unverified (the latest recorded outbound smoke test returned HTTP 401). Automatic customer replies, payment verification, booking automation, bank connections, and verified revenue analytics are not implemented. Muse performance needs broader bilingual and multimodal human evaluation. SaaS-grade tenant isolation, deployment, retention controls, and legal review remain incomplete.

## Repository

https://github.com/IngSeb0/Pendiva

## Demo video

**[VIDEO URL — TO BE ADDED BY THE PROJECT OWNER AFTER RECORDING AND UPLOADING]**

## Live demo

No verified public deployment URL is available. The prototype runs locally; do not enter the localhost URL as a public live demo.

## Theme and category

**Suggested theme:** Build for Your World — applying Meta AI to service-business operations. This is a suggested fit; choose the official form's category based on the options shown there.

**Suggested track:** Select Indie Developer or Startup according to the applicant/team's actual status and the official rules. This repository does not assert the applicant's track or eligibility.

**Meta product:** Muse Spark through Meta Model API.

## Official event references

- [Meta Global AI Developer Hackathon](https://dev.meta.ai/events/global-hackathon) — lists project submissions due November 4, 2026, at 9:00 p.m. ET, the two tracks, and the two themes. The page says dates may change and that changes will be posted there; no extension was listed when checked November 4, 2026.
- Detailed form fields and field limits were not publicly readable during this check. Use the application's live form as the source of truth.
