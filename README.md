# Support Triage

An AI system that triages customer support tickets: it classifies intent and urgency, retrieves the right help articles, drafts a grounded reply, takes simple actions through tools, and escalates anything risky to a human. Every draft is approved by a human agent before it's sent.

> **Status:** Week 0 of 17, in progress.

## Built alongside the book

[![Book: AI Engineering by Chip Huyen](https://img.shields.io/badge/Book-AI%20Engineering%20%C2%B7%20Chip%20Huyen-1f6feb?style=for-the-badge)](https://www.oreilly.com/library/view/ai-engineering/9781098166298/)
[![Companion repo](https://img.shields.io/badge/Companion%20repo-chiphuyen%2Faie--book-24292f?style=for-the-badge&logo=github)](https://github.com/chiphuyen/aie-book)

This project is my hands-on companion to ***AI Engineering: Building Applications with Foundation Models*** by Chip Huyen (O'Reilly, 2025). Each phase pairs one or two chapters with one working piece of the system, so the repo doubles as a record of my journey through the book. The reasoning behind each decision lives in [`LEARNINGS.md`](LEARNINGS.md), and the numbers in [`evals/history.csv`](evals/history.csv).

### Book journey

| Phase | Weeks | Chapters | What it builds | Status |
| --- | --- | --- | --- | --- |
| Setup | 0 | Preface, Ch 1 (intro) | Repo, dataset download and exploration | 🔄 |
| 1 | 1–2 | Ch 1 Building AI Applications · Ch 2 Understanding Foundation Models | Spec, off-the-shelf baseline, sampling and structured-output experiments | ⬜ |
| 2 | 3–5 | Ch 3 Evaluation Methodology · Ch 4 Evaluate AI Systems | Eval sets, validated AI judge, one-command eval pipeline | ⬜ |
| 3 | 6–7 | Ch 5 Prompt Engineering | Versioned prompts, triage → reply chain, prompt-attack testing | ⬜ |
| 4 | 8–10 | Ch 6 RAG and Agents | Hybrid retrieval, grounded replies, tool-using agent | ⬜ |
| 5 | 11–13 | Ch 7 Finetuning · Ch 8 Dataset Engineering | Curated dataset, fine-tuning vs. prompting comparison | ⬜ |
| 6 | 14 | Ch 9 Inference Optimization | Latency and cost optimization | ⬜ |
| 7 | 15–16 | Ch 10 AI Engineering Architecture and User Feedback | Guardrails, router, gateway, monitoring, dashboard, deployment | ⬜ |
| Finish | 17 | Epilogue | Write-up and demo | ⬜ |

✅ done · 🔄 in progress · ⬜ not started

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

- [*AI Engineering: Building Applications with Foundation Models*](https://www.oreilly.com/library/view/ai-engineering/9781098166298/) by Chip Huyen (O'Reilly, 2025), which this project follows chapter by chapter, and its [companion repo](https://github.com/chiphuyen/aie-book).
- Bitext, for the customer support dataset.
