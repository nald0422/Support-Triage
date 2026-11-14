# Support Triage

An AI system that triages customer support tickets: it classifies intent and urgency, retrieves the right help articles, drafts a grounded reply, takes simple actions through tools, and escalates anything risky to a human. Every draft is approved by a human agent before it's sent.

> **Status:** in progress (Week 0 of 17). Built while working through *AI Engineering* by Chip Huyen (O'Reilly, 2025), one chapter pair per phase.

## What it will do

1. **Triage** each ticket into one of 27 intents, with urgency, sentiment, and an escalation flag.
2. **Retrieve** relevant help-center articles with hybrid search (BM25 + embeddings + reranking).
3. **Draft** a reply that cites its sources and makes no promises outside policy.
4. **Act** through tools (order lookup, refund eligibility), where any write action only creates a pending request for a human to approve.
5. **Guard** inputs and outputs: personal data is masked before reaching an external model, and every draft is checked before approval.
6. **Learn** from agent feedback: rejected or heavily edited drafts become new evaluation cases.

## Planned architecture

```
Incoming ticket
  → Input guardrails (PII masking, injection checks)
  → Triage classifier (intent, urgency, confidence)
  → Model router ──── low confidence / critical ──→ Human queue
  → Reply agent  ←→  Help center (pgvector)  ·  Order tools (pending-only writes)
  → Output guardrails (policy check)
  → Agent dashboard (approve / edit / reject)  →  Eval set
```

All model calls go through a single gateway module with retries, fallback (Gemini → local model), cost tracking, and logging.

## Tech stack

| Area | Tools |
| --- | --- |
| Language and tooling | Python 3.14, uv, ruff, pytest |
| Models | Gemini API (Flash-Lite, Flash), local models via Ollama |
| Data | pandas, pyarrow, Hugging Face `datasets` |
| Validation | Pydantic |
| Retrieval (planned) | rank_bm25, sentence-transformers, Chroma → pgvector |
| Fine-tuning (planned) | scikit-learn, Hugging Face `transformers`, PEFT |
| App (planned) | FastAPI, React, Supabase Postgres |

## Getting started

**Prerequisites:** [uv](https://docs.astral.sh/uv/), [Ollama](https://ollama.com), and a free Gemini API key from Google AI Studio.

```bash
git clone https://github.com/<your-username>/support-triage.git
cd support-triage

# install dependencies from uv.lock
uv sync

# add your Gemini key
cp .env.example .env
# then edit .env: GEMINI_API_KEY=your-key

# pull a local model
ollama pull gemma3:4b

# download the dataset to data/raw/
uv run python scripts/download_data.py
```

> Free-tier Gemini requests may be used to improve Google's products. This project only uses the synthetic dataset below; don't send real customer data on the free tier.

## Dataset

[Bitext Customer Support dataset](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset): 26,872 synthetic customer messages labeled with 27 intents across 10 categories, each with a sample agent response. Licensed under CDLA-Sharing-1.0.

Raw data is downloaded to `data/raw/` and never edited; everything derived from it lives in `data/processed/`. The `data/` folder is gitignored and fully reproducible from the scripts.

## Project structure

```
support-triage/
├── data/raw/          # original downloads, never edited (gitignored)
├── data/processed/    # derived data (gitignored)
├── evals/             # eval sets, scoring scripts, history.csv
├── prompts/           # versioned prompt files with metadata
├── scripts/           # download and processing scripts
├── src/triage/        # system code
├── notebooks/         # exploration only
├── LEARNINGS.md       # weekly notes on what worked and what didn't
└── README.md
```

## Roadmap

- [ ] **Week 0:** setup and data exploration *(in progress)*
- [ ] **Phase 1 (Weeks 1–2):** spec, off-the-shelf baseline, sampling and structured-output experiments
- [ ] **Phase 2 (Weeks 3–5):** eval sets, validated AI judge, one-command evaluation pipeline
- [ ] **Phase 3 (Weeks 6–7):** versioned prompts, triage → reply chain, prompt-attack testing
- [ ] **Phase 4 (Weeks 8–10):** hybrid retrieval, grounded replies, tool-using agent
- [ ] **Phase 5 (Weeks 11–13):** dataset curation and a fine-tuning vs. prompting comparison
- [ ] **Phase 6 (Week 14):** latency and cost optimization
- [ ] **Phase 7 (Weeks 15–16):** guardrails, router, gateway, monitoring, dashboard, deployment
- [ ] **Week 17:** write-up and demo

## Results

Filled in as each phase lands. Every number comes from `evals/history.csv` and is reported on a held-out test set.

| Metric | Baseline | Current |
| --- | --- | --- |
| Intent accuracy | — | — |
| Escalation recall (must-escalate cases) | — | — |
| Reply factual consistency | — | — |
| Prompt-attack violation rate | — | — |
| False refusal rate | — | — |
| Agent scenario pass rate | — | — |
| p95 time to first draft token | — | — |
| Cost per 1,000 tickets | — | — |

## Acknowledgments

- *AI Engineering: Building Applications with Foundation Models* by Chip Huyen (O'Reilly, 2025), which this project follows chapter by chapter.
- Bitext, for the customer support dataset.
