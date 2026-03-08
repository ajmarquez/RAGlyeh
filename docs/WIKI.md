# RAGlyeh Wiki: Step-by-Step Milestone Guide

This guide is your execution playbook for the roadmap.
Use it to decide:
- what to focus on next
- what "done" looks like before moving on
- what to read right now (not everything at once)

Scope rule: depth over tool sprawl. Finish each milestone before adding new tools.

## How to use this guide every session

1. Open the roadmap page and find your current milestone.
2. Pick the first unchecked item in that milestone.
3. Read only the "Read now" links for that item.
4. Implement one small slice end-to-end.
5. Run a quick verification.
6. Mark the checkbox.
7. If blocked for more than 45-60 minutes, do the fallback task listed for that milestone.

## Milestone A: Foundations

### Focus now
Get a stable local FastAPI service running with reproducible setup.

### Next actions
1. Create `.venv`, install dependencies, freeze `requirements.txt`.
2. Implement `GET /health`.
3. Confirm server runs with hot reload.
4. Verify project structure exists: `app/`, `scripts/`, `data/`.

### Done when
- `uvicorn app.main:app --reload` starts cleanly.
- `GET /health` returns `{ "status": "ok" }`.
- Another machine could reproduce dependencies from `requirements.txt`.

### Read now
- FastAPI first steps: https://fastapi.tiangolo.com/tutorial/first-steps/
- Uvicorn settings: https://www.uvicorn.org/settings/

### If blocked
Skip optimization. Keep only one endpoint and one dependency set that works.

## Milestone B: First Usable API

### Focus now
Build ingestion and retrieval endpoints without DB complexity.

### Next actions
1. Define Pydantic models for `StoryCreate` and `Story`.
2. Add `POST /stories` ingestion.
3. Add `GET /stories` and `GET /stories/{id}`.
4. Add basic 404 and validation handling.

### Done when
- You can ingest a local text story and fetch it back via API.
- Invalid input returns useful error messages.

### Read now
- FastAPI request body models: https://fastapi.tiangolo.com/tutorial/body/
- FastAPI error handling: https://fastapi.tiangolo.com/tutorial/handling-errors/

### If blocked
Use in-memory storage first; persistence comes later.

## Milestone C: Retrieval MVP (Grounded)

### Focus now
Ship the first grounded `POST /ask` with citations and refusal behavior.

### Next actions
1. Chunk text with stable chunk IDs (`story_id:chunk_index`).
2. Add lexical/BM25-style retrieval endpoint (`POST /search`).
3. Add `POST /ask` that uses retrieved context.
4. Return answer + citation IDs.
5. Enforce refusal/uncertainty when support is missing.

### Done when
- `POST /ask` returns citation-backed answers.
- Unsupported questions produce "I don't know" style behavior.

### Read now
- BM25 overview: https://en.wikipedia.org/wiki/Okapi_BM25
- RAG paper (conceptual grounding): https://arxiv.org/abs/2005.11401

### If blocked
Cut chunking complexity. Use fixed-size chunks first, then iterate.

## Milestone D: Persistence + Hybrid Retrieval + Reranking

### Focus now
Move to realistic retrieval: lexical + vector + hybrid + reranking.

### Next actions
1. Add Postgres via Docker Compose.
2. Persist stories/chunks with metadata:
   - `title`, `author`, `publication_year`, `source_url`
   - `entities`, `setting`, `motifs`
3. Enable pgvector and store embeddings.
4. Implement vector retrieval.
5. Implement hybrid retrieval by combining keyword + vector candidate sets.
6. Add metadata-aware filters.
7. Add reranking:
   - retrieve top candidates first
   - rerank candidates
   - pass best chunks to generation
8. Compare lexical vs vector vs hybrid, before/after reranking.

### Done when
- All three retrieval modes run (`lexical`, `vector`, `hybrid`).
- Metadata filters work and are useful in debugging.
- Reranking improves quality on at least part of your eval set.

### Read now
- PostgreSQL docs: https://www.postgresql.org/docs/
- pgvector docs: https://github.com/pgvector/pgvector
- Hybrid search intro: https://www.pinecone.io/learn/hybrid-search-intro/
- Reranking intro: https://www.pinecone.io/learn/series/rag/rerankers/

### If blocked
Keep a very simple hybrid strategy (union + weighted score) before trying advanced fusion.

## Milestone E: Evaluation + Observability

### Focus now
Measure quality and latency with evidence, not intuition.

### Next actions
1. Build eval set with categories:
   - factual
   - comparative
   - interpretive
   - refusal/unsupported
2. Add retrieval eval metrics (for example `hit@k`).
3. Add full answer eval with citation-grounding checks.
4. Save baseline report before tuning.
5. Add request IDs and traces.
6. Log operational metrics per request:
   - retrieval time
   - generation time
   - chunk count
   - prompt tokens
   - completion tokens
   - refusal rate
7. Add a simple trace inspection endpoint/view.

### Done when
- You can explain quality deltas using metrics and traces.
- You can identify where failures happen: retrieval, ranking, or generation.

### Read now
- RAGAs paper: https://arxiv.org/abs/2401.01313
- OpenTelemetry concepts: https://opentelemetry.io/docs/concepts/signals/traces/
- Lost in the Middle: https://arxiv.org/abs/2307.03172

### If blocked
Start with a tiny eval set (8-12 questions) and expand after pipeline works.

## Milestone F: Product Behavior + Demo Polish

### Focus now
Make behavior trustworthy in ambiguous or weak-retrieval situations.

### Next actions
1. Build minimal demo UI connected to `POST /ask`.
2. Improve citation display for quick verification.
3. Add graceful fallback behavior for weak retrieval.
4. Handle ambiguous questions with clarification or explicit uncertainty.
5. Polish README quickstart and architecture notes.

### Done when
- Demo makes uncertainty visible (not hidden).
- Users can inspect why an answer is given.
- Failure behavior is calm and explicit, not overconfident.

### Read now
- Gradio docs: https://www.gradio.app/docs
- Streamlit docs: https://docs.streamlit.io/
- Anthropic engineering guide (grounded behavior): https://www.anthropic.com/engineering/building-effective-agents

### If blocked
Keep one UI path and one provider. Avoid feature branching until behavior is clear.

## Decision rule: What to do next

When you finish any checklist item, use this order:
1. Improve correctness first (grounding/citations).
2. Improve retrieval quality second (hybrid/reranking/filters).
3. Improve observability third (metrics/traces).
4. Improve UX and polish last.

If two tasks compete, choose the one that improves measurable grounding.

## Weekly cadence (4h/week)

- Session 1 (2h): implement one small vertical slice.
- Session 2 (1h): run evals and inspect traces.
- Session 3 (1h): targeted fix + short notes in README.

Keep every week shippable, even if small.

## Definition of project success

By the end, you should be able to say:
"I built a small grounded AI system over a literary corpus. I learned retrieval tradeoffs, reranking, evaluation design, latency/observability instrumentation, and product behavior under uncertainty."
