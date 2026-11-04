# Pendiva — Final hackathon readiness report

**Review date:** November 4, 2026 (Bogotá). The official event page lists submissions due today at 9:00 p.m. ET / 9:00 p.m. Bogotá and had no extension notice when checked. Recheck the page and authenticated portal before the deadline.

## Product status

The local prototype includes a customer inbox, manually maintained opportunities, evidence-linked Muse recommendations, owner assistant, CSV-based sales/expense chart, browser-based voice, media workflows, service configuration, and synthetic demo data. These features are implemented in the repository; live availability of optional external services is separate.

The repeatable judge walkthrough uses fictional data and a separate SQLite file. Current command:

```powershell
python -m scripts.iniciar_demo --demo --demo-language en --demo-no-finance --demo-db data/demo-en.sqlite3
```

Import `fixtures/demo/cleaning-sales-demo-en.csv` only if showing the chart. This report does not claim that a fresh UI recording was made during this review.

## Meta AI integration

The application code uses Meta Model API with Muse Spark exclusively; legacy provider variables do not activate Nebius fallback. Historical real calls and their dates are recorded in `docs/validation/muse.md` and `docs/validation/evaluacion-extraccion.md`. The synthetic eight-case exploration and its weaknesses are summarized in [`AI_EVALUATION.md`](AI_EVALUATION.md). Current local credentials, network path, and a real Muse request were not checked during this release. Automated tests use mocks and do not prove current service availability.

## WhatsApp integration

A sandbox inbound text was historically received and stored once; Meta accepted a historical hello_world request, but phone delivery was not confirmed. On the latest recorded attempt, the outbound smoke test returned HTTP 401 and a subsequent network attempt could not resolve DNS. Treat current connectivity and token validity as unverified. The integration does not backfill full chat history and is not a production account connection. Details: [`live-sandbox.md`](../validation/live-sandbox.md) and [`mejoras-demo.md`](../validation/mejoras-demo.md).

## Automated tests

**Result:** `python -m unittest discover -v` — 137 tests passed; `node --test tests/voice_session.test.js` — 3 tests passed. These use mocked API responses where applicable and do not prove external service availability.

The English seeded demo command started successfully and loaded nine synthetic conversations. A separate HTTP status probe was blocked by the execution environment's local socket permissions, so an end-to-end browser/API health check could not be completed in this run. No WhatsApp message was sent and no Muse request was made by starting the demo.

## Security

The application keeps API keys on the server, reads local `.env` configuration, excludes `.env` and local `data/` from Git, uses signed webhook verification, gates AI data transfer on explicit consent, and validates recommendation evidence IDs. The final diff was checked for credential-like assignments and tracked `.env` files. This is not a comprehensive security certification. Review auth/session controls, tenant isolation, retention/deletion, and deployment configuration before any production use.

No owner-approved open-source license is declared. Do not infer redistribution rights from the public repository. License choice remains an owner action.

## Documentation and submission materials

The root README has been rewritten in English. The repository now includes `SUBMISSION.md`, this report, `VIDEO_SCRIPT.md`, `AI_EVALUATION.md`, `IMPACT.md`, and `SUBMISSION_CHECKLIST.md`. The official public page confirms tracks, themes, and deadline; its detailed form fields and limits were not publicly readable, so the submission copy is reusable content and must be adapted to the live form.

## Demo and video

The demo is reproducible from a local command with fictional data. A live Muse turn is optional and depends on a working local key, network, and explicit consent. The recording script supplies a seeded-data fallback. The project owner must record and upload the video and provide its URL; no recording or upload has been performed.

## Submission readiness

**Status: READY WITH USER ACTIONS.** Repository materials and automated tests are ready, but the video URL, final authenticated form, applicant/team details, eligibility/track selection, and actual submission remain outstanding. The local health endpoint could not be checked from this sandbox. This is not “READY FOR SUBMISSION” until the owner completes the live form and video actions.

## Outstanding requirements and risks

1. Check the authenticated portal's live submission fields, field limits, status, and deadline.
2. Record/upload the video and add its actual URL.
3. Verify current sandbox/API credentials only if needed for the chosen demo; do not expose keys.
4. Confirm applicant eligibility, track, repository access, and licensing decision.
5. Complete the final submission personally; it has not been sent.

Material product risks include unverified live connectivity, incomplete WhatsApp history, exploratory model evaluation, ambiguous amounts, no production deployment, and incomplete SaaS-grade isolation and privacy review.

## Official references

- [Meta Global AI Developer Hackathon](https://dev.meta.ai/events/global-hackathon)
- [Meta Model API quickstart](https://dev.meta.ai/docs/quickstart)
- [Meta Responses API](https://dev.meta.ai/docs/protocols/responses)
