# Muse Spark evaluation: current evidence and next protocol

## Scope

The available evidence concerns structured extraction for a small set of fictional service-business messages and a few dated live calls to Meta Model API. It is useful for identifying failure modes, but it does not establish a general accuracy rate, production readiness, or performance on real customer data.

## Exploratory result

The October 31, 2026 exploratory run in [`../validation/evaluacion-extraccion.md`](../validation/evaluacion-extraccion.md) used eight synthetic text cases. In that run:

- The generated proposals cited valid source IDs.
- Cases with no stated price and an ambiguous future date did not produce a fabricated amount or exact date.
- The malicious instruction test did not create an opportunity or assert that a payment had been received.
- One amount described as the customer's budget was placed in a generic amount field that could be mistaken for the company's quote.
- At least two next-step suggestions were weak or ambiguously assigned to the customer versus business.
- The sample was reviewed by Codex, not independently by a service-business expert.

The denominator is eight synthetic prompts; outputs can vary by run and model version. The observations are not a precision, recall, safety, or production-quality score. Three additional dated live Muse checks and their limits are documented in `docs/validation/evaluacion-extraccion.md` and `docs/validation/muse.md`.

## Current verification status

The repository has unit tests using mocked provider responses. They verify request contracts, validation, consent gates, and failure behavior, not current Meta API availability or model quality. Historical real Muse requests completed in October 2026 with synthetic or specifically authorized sandbox text, as documented in the validation records. Current `.env` credentials, network connectivity, and a live request were not verified for this release. A current real request can consume credits; run it only with synthetic input and the project owner's configured key.

## Recommended repeatable evaluation

Before claiming a quality metric, create a versioned bilingual (English/Spanish) dataset with service requests, missing details, ambiguous dates, customer budgets versus company quotes, multiple services, unsupported payments, prompt injection, and contradictory/incorrect media observations. For every case, define expected opportunities, required evidence, prohibited inferences, and acceptable abstention. Run a fixed model/configuration, blind the reviewer to expected output where practical, and have at least one domain reviewer score each output.

Track at minimum: correct service identification, evidence validity, unsupported claim rate, price/date/payment confusion, useful next-step rate, abstention quality, language adherence, and review time. Publish counts, rubric, model/version, date, failures, and reviewer method. Keep synthetic data separate from any consented, anonymized pilot data.

## Product safeguards

- Muse output is a suggestion and is not automatically sent to a customer.
- Source IDs are checked by the server; semantic correctness still requires human review.
- The generic amount field cannot reliably distinguish customer budget, quote, payment, or other amounts; confirm the message context before using it.
- Never infer that a payment, booking, or completed job occurred merely because a model mentions it.
- Keep coverage limits visible; the owner assistant submits up to 36 selected excerpts after local search, rather than the complete conversation database.

## Sources

- [Meta Model API quickstart](https://dev.meta.ai/docs/quickstart)
- [Meta Responses API](https://dev.meta.ai/docs/protocols/responses)
- [Meta structured output](https://dev.meta.ai/docs/structured-output)
- Internal dated evidence: [`docs/validation/muse.md`](../validation/muse.md), [`docs/validation/evaluacion-extraccion.md`](../validation/evaluacion-extraccion.md)
