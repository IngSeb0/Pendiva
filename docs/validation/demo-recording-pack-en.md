# Pendiva — English Demo Recording Pack

## What the demo shows

Pendiva helps a service-business owner turn WhatsApp conversations into visible follow-ups and
evidence-backed decisions. This recording uses fictional cleaning-business data. It shows the
customer inbox, a quote needing more details, the owner assistant, a hands-free voice turn, and
monthly sales-versus-expenses imported from CSV.

**Do not claim:** full WhatsApp history sync, automatic customer replies, verified payments,
bookings, accounting-grade revenue, a live bank connection, or production SaaS readiness. The demo
does not send replies to customers. Muse answers the owner after explicit consent. The voice loop
uses browser speech recognition and device speech synthesis; browser recognition may process audio
through its own service.

## Pitch

### 20 seconds

> Service businesses receive valuable customer signals in WhatsApp, but those signals get buried in
> chat. Pendiva turns the conversations it receives into organized follow-ups, shows the message
> behind each recommendation, and lets the owner ask Muse what needs attention—in text or by voice.

### 60 seconds

> A cleaning team can have quotes waiting, price objections, scheduling questions, and payments that
> still need verification—all mixed together in WhatsApp. Pendiva gives the owner one place to review
> those conversations, see what needs attention, and open the exact message supporting a suggestion.
> The owner can ask Muse across the available conversations, in English or Spanish, and get a
> grounded answer with clear coverage limits. The hands-free voice mode listens, sends a transcribed
> question to Muse, reads the answer aloud, and listens for the next turn. The sales view adds monthly
> sales and expenses from a local CSV. Pendiva is designed for service operations: it helps teams
> follow through; it does not silently message customers or claim that an unverified payment is real.

## Three-minute recording script

| Time | Screen / action | Narration |
|---|---|---|
| 0:00–0:20 | Show Home. Keep the English language toggle visible. | “Pendiva helps a service-business owner see what needs attention across WhatsApp conversations.” |
| 0:20–0:55 | Open Customers. Select Ana Rojas. Show her messages and the recommendation/evidence. | “Ana asked for a sofa-cleaning quote. Pendiva keeps the request organized and shows the message behind its suggested next step: confirm the address and preferred date before quoting.” |
| 0:55–1:20 | Show the customer workflow fields and optional image attachment. Do not trigger AI unless consent and network are ready. | “The team can track service, location, date, and next step. Attachments can be reviewed separately; this recording uses synthetic files.” |
| 1:20–2:05 | Open the assistant bubble. Tick the Muse consent. Click **Start voice conversation** and ask: “Which quotes need attention, and what details are missing?” Let Muse answer. | “The owner can ask about the available conversations. Pendiva searches locally, sends a bounded set of relevant excerpts to Muse, and reports how much evidence was included. I can ask by voice and hear the answer without clicking submit.” |
| 2:05–2:35 | Stop voice. Open the sales page. Show the monthly chart. Point to data source/CSV note. | “The owner can compare imported monthly sales and expenses. These are synthetic CSV records; Pendiva does not connect to a bank, and the file does not specify a currency.” |
| 2:35–3:00 | Return Home and show priorities / review controls. | “Pendiva gives service teams a clearer way to follow up, while keeping people responsible for reviewing recommendations and deciding what to do.” |

## Exact voice and text prompts

1. **Cross-conversation:** “Which quotes need attention, and what information is missing before we can reply?”
2. **Prioritization:** “Which conversations should I review first today? Explain the evidence and any uncertainty.”
3. **Cleaning operations:** “For the cleaning requests, group the services customers asked about and list the details we still need before quoting. Do not invent prices or availability.”
4. **Sales and service signals:** “Compare the available conversation signals with the imported monthly sales and expenses. Separate observed data from hypotheses, state the number of records behind each point, and do not claim causation.”
5. **Single conversation:** “What should I ask Ana before preparing a quote for the sofa? Cite the message that supports each question.”

Use one prompt in the recording; four or five questions can make Muse latency and output quality
less predictable. The sample turns are prompts, not guaranteed model responses.

### Optional multimodal insert

If you want to show the service-specific multimodal workflow, use the synthetic sofa image already
attached to Ana and ask: **“Describe only what is visible in this sofa image. What should our team
ask the customer before quoting? Separate visual observations from unknown details; do not estimate
a price.”** Confirm consent first, review the model result, and label it as an AI observation. Skip
this insert if the network is unstable or the returned observation has not been checked. The core
three-minute recording does not depend on a live media-model call.

## English finance CSV

Files: [`fixtures/demo/cleaning-sales-demo-en.csv`](../../fixtures/demo/cleaning-sales-demo-en.csv)
and [`fixtures/demo/muse-prompts-en.csv`](../../fixtures/demo/muse-prompts-en.csv).

Import it from the Sales page after launching with `--demo-no-finance`. The default `--demo` seed
already creates six synthetic sales/expense records, so importing this CSV into that seeded demo
would duplicate them. The app currently does not store a currency; present these as unlabelled
example amounts, not USD or COP.

## Recording setup

1. From the project root, start a clean, isolated English demo database:

   ```powershell
   python -m scripts.iniciar_demo --demo --demo-language en --demo-no-finance --demo-db data/demo-en.sqlite3
   ```

2. Open the printed local URL and sign in with the fictional credentials printed by the launcher.
3. Set the interface language to **English**. Keep the display zoom at 100% or 110%, close unrelated
   tabs, and use a 16:9 browser window.
4. Use Chrome or another browser with `SpeechRecognition`; allow microphone access when asked. The
   voice-mode button requires the Muse key in the local environment and the on-screen consent.
5. Import `fixtures/demo/cleaning-sales-demo-en.csv` into the new demo before recording; it starts
   without finance rows so the chart will not double-count. Then check English labels, messages,
   chart, and voice-state animation before recording the narrated take.
6. If Muse or network fails, do not present a fabricated answer as live. Keep the written prompt
   ready, use the pre-seeded evidence-backed customer recommendation, and say the live call is
   temporarily unavailable.
7. Stop the demo with `Ctrl+C`. The English seed lives in a separate database so it does not mix
   with real or Spanish demo records.

## Capture checklist

- [ ] English labels, prompts, customer messages, business profile, and chart categories are visible.
- [ ] No real customer number, token, browser notification, or personal WhatsApp chat is on screen.
- [ ] Muse consent is shown before the live question.
- [ ] The voice indicator changes through listening, thinking, and speaking; stop the voice session
      before moving to another page.
- [ ] Show the source/coverage note after the assistant response.
- [ ] Say “synthetic” when describing seeded customers and CSV figures.
- [ ] No fabricated claim of outbound automation, full history, payment verification, or currency.

## Suggested title and closing card

**Title:** Pendiva — Turn WhatsApp conversations into service-business follow-through

**Closing line:** “Less buried in chat. More clear on what needs attention.”

**On-screen footer:** “Prototype demo · fictional data · recommendations require human review”

## Likely judge questions

**How is this different from a CRM with a chatbot?**
> The demo focuses on the owner's operational view across conversations: what needs follow-up,
> which message supports that signal, and what information is missing. It does not claim that a
> generic bot can safely close a service job or send replies without review.

**Does Pendiva analyze every WhatsApp message?**
> It searches all messages currently stored for this business locally, then sends a bounded set of
> relevant excerpts to Muse. WhatsApp history and outgoing messages may be missing, so each answer
> reports its coverage.

**Can it reply to customers automatically today?**
> Not in this prototype. It prepares owner-facing recommendations and drafts for human review; it
> does not send customer replies.

**How does it avoid inventing business facts?**
> It links recommendations to source messages, marks uncertainty, and distinguishes imported or
> manually recorded information from verified business events. The owner makes the final decision.
