# RAGlyeh Wiki: Step-by-Step Milestone Guide

This guide is the tutorial companion to the roadmap.
Use it to decide:
- what to build next
- what concepts matter before coding
- what tools, accounts, and files you need
- what "done" looks like before moving on

Scope rule: finish one milestone cleanly before adding more tools.

## How to use this guide every session

1. Open the roadmap page and find your current milestone.
2. Pick the first unchecked item in that milestone.
3. Read only the "Concepts first" and "Read now" links for that item.
4. Implement one small slice end-to-end.
5. Run the verification step before moving on.
6. Mark the checkbox only after the behavior works.
7. If blocked for more than 45-60 minutes, do the fallback task listed for that milestone.

## Before you start

### Core tools you will need across the project
- Python 3.11+ or similar recent version
- A virtual environment (`.venv`)
- FastAPI and Uvicorn
- A terminal and `curl` or your API collection client
- A plain text editor or IDE
- Git

### Tools you do not need yet
- Docker
- Postgres
- pgvector
- embeddings
- an LLM provider account

Those appear later on purpose. Do not front-load them.

### Project folders you should expect
- `app/`: running application code
- `scripts/`: one-off helpers like ingestion or eval scripts
- `data/`: local data files and later eval datasets
- `docs/`: roadmap and tutorial material

## Milestone A: Foundations

### Focus now
Get a stable local FastAPI service running with reproducible setup.

### You need before starting
- Python installed
- terminal access
- a new `.venv`
- `requirements.txt`

### Concepts first
- FastAPI is your web framework.
- Uvicorn is the ASGI server that runs the app.
- `uvicorn app.main:app --reload` means:
  - import the `app` object
  - from the module `app.main`
  - and restart automatically when files change

### Next actions
1. Create `.venv`, install dependencies, freeze `requirements.txt`.
2. Implement `GET /health`.
3. Confirm server runs with hot reload.
4. Verify project structure exists: `app/`, `scripts/`, `data/`.

### Verification
- `uvicorn app.main:app --reload` starts cleanly.
- `GET /health` returns `{ "status": "ok" }`.
- Another machine could reproduce dependencies from `requirements.txt`.

### Done when
- `/health` runs locally and dependencies are reproducible on another machine.

### Read now
- FastAPI first steps: https://fastapi.tiangolo.com/tutorial/first-steps/
- Uvicorn settings: https://www.uvicorn.org/settings/

### If blocked
Skip optimization. Keep only one endpoint and one dependency set that works.

## Milestone B: First Usable API

### Focus now
Build story ingestion and read endpoints without DB complexity.

### You need before starting
- Milestone A complete
- one or two local `.txt` files to use as sample stories
- in-memory storage only

### Concepts first
- A Pydantic schema is your API DTO. It validates request/response shape.
- In-memory storage means data is lost when the app restarts. That is fine for now.
- `POST` creates data.
- `GET` reads data.
- `404` means the client asked for something that does not exist.

### Next actions
1. Define Pydantic models for `StoryCreate` and `Story`.
2. Add `POST /stories` ingestion.
3. Add `GET /stories` and `GET /stories/{id}`.
4. Read text from a local file or accept raw text directly.
5. Add basic 404 and validation handling.

### Recommended implementation path

#### Step B0: Confirm your current state
Before editing anything else, confirm:
- `GET /health` still works
- your app boots cleanly

Verification:
- Run `uvicorn app.main:app --reload`.
- Visit `/health` or call it with `curl`.

#### Step B1: Define the request and response schemas
Start with simple data shapes.

Good first version:
- `StoryCreate`
  - `title`
  - `author` optional
  - `source_url` optional
  - `text`
- `Story`
  - everything above plus `id` and `created_at`

Why this matters:
- the request schema validates input
- the response schema keeps your API output consistent

Verification:
- Your route functions can type their input/output with these models.

#### Step B2: Add in-memory storage
Do not add a database yet.

Use:
- one module-level dictionary keyed by `id`

Why this matters:
- you are learning API behavior first
- persistence is a later milestone

Verification:
- You can create one object in memory and fetch it back before worrying about restarts.

#### Step B3: Implement `POST /stories`
This route should:
- accept a `StoryCreate`
- validate non-empty text
- generate an `id`
- assign `created_at`
- store the story in memory
- return the created object

Verification:
- This command returns `201` and a JSON body with an `id`:

```bash
curl -X POST http://127.0.0.1:8000/stories \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Call of Cthulhu",
    "author": "H. P. Lovecraft",
    "text": "The most merciful thing in the world..."
  }'
```

#### Step B4: Implement `GET /stories`
This route should return:
- an empty list when there are no stories
- all current stories when the store has data

Verification:
- `curl http://127.0.0.1:8000/stories` returns a JSON list.

#### Step B5: Implement `GET /stories/{id}`
This route should:
- return the story when the ID exists
- return `404` when it does not

Verification:
- `GET /stories/{real_id}` returns the story.
- `GET /stories/not-a-real-id` returns a `404` with a clean error message.

#### Step B6: Support local text ingestion cleanly
If you want beginner-friendly progress, you can support either:
- direct raw `text` in the request body
- a separate helper later that reads `.txt` files and sends them to the API

For now, prefer direct `text` in the API contract because it keeps HTTP behavior easy to understand.

Why:
- file-upload or path-based ingestion adds extra complexity
- Milestone B is about learning request/response design, not filesystem APIs

Verification:
- You can paste text directly in a JSON request and create a story.

#### Step B7: Add basic error handling
Add predictable errors for:
- empty text
- missing story ID
- invalid request shape

Verification:
- Bad input gives `400` or validation errors, not a server crash.

### Concrete checkpoints against your current code
- [stories.py](/Users/ajmarquez/Development/RAGlyeh/app/api/routes/stories.py) should own the `POST /stories`, `GET /stories`, and `GET /stories/{id}` routes.
- [story.py](/Users/ajmarquez/Development/RAGlyeh/app/models/story.py) currently holds your Pydantic models and is acting as your schema layer.
- [main.py](/Users/ajmarquez/Development/RAGlyeh/app/main.py) should only wire routers, not hold story logic itself.

### Verification
- You can create one story.
- `GET /stories` returns a list.
- `GET /stories/{id}` returns the created story.
- Invalid input returns useful error messages instead of a stack trace.

### Done when
- You can ingest a local text story and fetch it back via API.
- Invalid input returns useful error messages.

### Read now
- FastAPI request body models: https://fastapi.tiangolo.com/tutorial/body/
- FastAPI error handling: https://fastapi.tiangolo.com/tutorial/handling-errors/
- Pydantic models: https://docs.pydantic.dev/latest/concepts/models/
- FastAPI path params: https://fastapi.tiangolo.com/tutorial/path-params/

### If blocked
Use in-memory storage first; persistence comes later.

## Milestone C: Retrieval MVP (Grounded)

### Why this milestone feels bigger
This is the first milestone that combines:
- data transformation
- search/retrieval
- prompting
- model integration
- product behavior under uncertainty

That is a real complexity jump from Milestone B. The right fix is not to skip it. The right fix is to split it into smaller sub-steps and state prerequisites clearly.

### Focus now
Ship the first grounded `POST /ask` with citations and refusal behavior.

### You need before starting
- Milestone B complete
- at least 1 real story loaded into the app
- enough story text to produce multiple chunks
- a decision about your first LLM provider

### External tools and accounts required

#### Required for `POST /search`
- No external account required
- No Docker required
- No database required

#### Required for `POST /ask`
- An LLM provider connection is required
- One of these:
  - OpenAI API key
  - Anthropic API key
  - local Ollama installation with a pulled model

#### Recommended first choice
- Use one hosted provider first if your goal is learning FastAPI and RAG concepts quickly.
- Use Ollama first if your goal is learning local model tooling and you are comfortable debugging local setup.

### Concepts first

#### Chunking
Large documents are too big to search or send to a model as one block. Chunking breaks a story into smaller units.

#### Retrieval
Given a question, retrieval finds the chunks most likely to contain the answer.

#### Grounding
The model should answer only from retrieved text, not from its general world knowledge.

#### Citations
Each chunk needs a stable ID like `story_id:chunk_index`. That is the proof trail for the answer.

#### Refusal
If the retrieved chunks do not support an answer, the API should return an explicit "I don't know" style response.

#### Why retrieval comes before a better model
If retrieval is bad, a stronger model still gets bad context. Retrieval quality is upstream.

### Recommended implementation path

#### Step C0: Introduce chunk data shape
Create a chunk structure before writing retrieval logic.

Add fields like:
- `chunk_id`
- `story_id`
- `text`
- `chunk_index`

Verification:
- You can print or return a sample chunk object for one story.

#### Step C1: Build a simple chunker
Start with fixed-size chunks. Do not start with advanced chunk heuristics.

Good first version:
- 800-1200 characters
- optional overlap of 100-150 characters

Do not optimize yet:
- sentence-aware splitting
- semantic chunking
- metadata enrichment

Verification:
- One story becomes multiple chunks.
- Chunk IDs are stable across repeated runs if the source text does not change.

#### Step C2: Add a chunk debug endpoint
Before search, make chunks visible.

Example:
- `GET /stories/{id}/chunks`

Verification:
- You can inspect chunk IDs and text snippets in the browser or with `curl`.

#### Step C3: Implement retrieval without any LLM
Build `POST /search` first. This is the easiest way to test retrieval quality separately from model behavior.

First version options:
- simple keyword counting
- BM25-style library if you want a slightly better lexical baseline

Start simple. A working lexical baseline is more valuable than an incomplete vector system.

Verification:
- A query like "Innsmouth" returns chunks containing Innsmouth.
- A query for a specific entity or setting returns plausible chunk IDs.

#### Step C4: Connect the first LLM call in the simplest possible way
Do not connect the model to the full retrieval pipeline immediately.

First working `POST /ask` can do:
- accept a question
- use the top 1 retrieved chunk
- build a strict prompt
- return `{answer, citations}`

Your prompt should say:
- answer only from the provided context
- if the answer is not supported, say you do not know
- do not invent citations

Verification:
- You can ask an answerable question and get a response with a chunk ID.

#### Step C5: Move from top-1 to top-k retrieved chunks
After the first model call works, send a small set of retrieved chunks, such as top 3.

Keep it simple:
- preserve chunk order
- include chunk IDs
- return only the IDs actually used as citations

Verification:
- Multi-part questions work better than with top-1.
- Answers still stay tied to cited chunk IDs.

#### Step C6: Add refusal behavior deliberately
This is not a side effect. Implement it on purpose.

Test with:
- unsupported questions
- cross-story questions with weak evidence
- vague questions with no direct support

Verification:
- Unsupported questions produce an explicit uncertainty response.
- The model does not confidently fabricate details.

### Suggested API shape for Milestone C

#### `POST /search`
Input:
- `query`
- optional `story_id`
- optional `k`

Output:
- list of chunks with:
  - `chunk_id`
  - `story_id`
  - `score`
  - preview text

#### `POST /ask`
Input:
- `question`
- optional `story_id`
- optional `k`

Output:
- `answer`
- `citations`
- optional `used_chunks` in debug mode

### Minimum environment additions for Milestone C

If using a hosted provider:
- `.env`
- provider API key
- a small client wrapper in your app

If using Ollama:
- Ollama installed locally
- one pulled model such as `qwen2.5:7b-instruct`
- base URL configured in your app

### What not to add yet
- Postgres
- pgvector
- embeddings
- hybrid retrieval
- reranking
- eval frameworks

Those belong to later milestones. Adding them now will hide the actual learning objective.

### Verification checklist
- One story can be chunked into stable chunk IDs.
- `POST /search` returns sensible chunks for obvious questions.
- `POST /ask` returns an answer with citations for supported questions.
- `POST /ask` refuses unsupported questions.

### Done when
- `POST /ask` returns citation-backed answers.
- Unsupported questions produce "I don't know" style behavior.

### Read now
- BM25 overview: https://en.wikipedia.org/wiki/Okapi_BM25
- RAG paper (conceptual grounding): https://arxiv.org/abs/2005.11401
- FastAPI response models: https://fastapi.tiangolo.com/tutorial/response-model/
- OpenAI quickstart: https://platform.openai.com/docs/quickstart
- Anthropic API docs: https://docs.anthropic.com/en/api/getting-started
- Ollama docs: https://ollama.com/library

### If blocked
- Cut chunking complexity. Use fixed-size chunks first.
- Build `POST /search` before `POST /ask`.
- Use top-1 chunk before top-k retrieval.
- If model setup blocks you, stop at `POST /search` and verify retrieval quality first.

## Milestone D: Persistence + Vector Retrieval

### Focus now
Move from an in-memory prototype to a realistic retrieval system with persistent storage and vector search.

### You need before starting
- Milestone C complete
- Docker installed
- enough free disk space to run Postgres locally
- a chosen embedding source:
  - hosted embeddings API
  - or local embedding model

### External tools and accounts required
- Docker Desktop or equivalent
- Postgres via Docker Compose
- pgvector-enabled Postgres image
- embedding provider or local embedding runtime

### Concepts first
- Persistence means your stories and chunks survive restarts.
- Vectors are numeric representations of text meaning.
- Vector retrieval finds semantically related chunks, not just keyword matches.

### Next actions
1. Add Postgres via Docker Compose.
2. Persist stories and chunks in DB tables.
3. Enable pgvector and store embeddings.
4. Implement vector retrieval.
5. Compare keyword retrieval against vector retrieval.

### Verification
- Restarting the app does not lose stories/chunks.
- Vector retrieval works for at least a few semantically phrased questions.
- You can compare lexical vs vector results side by side.

### Done when
- Vector retrieval works and can be compared against keyword retrieval.

### Read now
- PostgreSQL docs: https://www.postgresql.org/docs/
- pgvector docs: https://github.com/pgvector/pgvector
- OpenAI embeddings guide: https://platform.openai.com/docs/guides/embeddings

### If blocked
Keep the schema simple. Persist only stories and chunks first, then add embeddings.

## Milestone E: Evaluation + Observability

### Focus now
Measure system quality and debugging signals with evidence, not intuition.

### You need before starting
- Milestone D complete
- a small stable question set
- a way to run scripts locally

### External tools and accounts required
- No external SaaS required for the first version
- optional tracing tool later

### Concepts first
- Retrieval quality and answer quality are different things.
- A baseline report matters because otherwise you cannot tell if a change helped.
- Traces let you inspect what happened for one request.

### Next actions
1. Build `eval_questions.json` with categories:
   - factual
   - comparative
   - interpretive
   - refusal/unsupported
2. Add retrieval eval metrics such as `hit@k`.
3. Add full answer eval with citation checks.
4. Save a baseline report before tuning.
5. Add request IDs and traces.
6. Log retrieval time, generation time, chunk count, and token counts if available.
7. Add a simple trace inspection endpoint or debug view.

### Verification
- You can run one command/script and produce an eval report.
- You can inspect one failed answer and see retrieved chunks plus timings.

### Done when
- You can run an eval script and inspect traces to debug failures.

### Read now
- RAGAs paper: https://arxiv.org/abs/2401.01313
- OpenTelemetry traces concept: https://opentelemetry.io/docs/concepts/signals/traces/
- Lost in the Middle: https://arxiv.org/abs/2307.03172

### If blocked
Start with 8-12 eval questions. Small and runnable beats ambitious and unfinished.

## Milestone F: Demo + Polish

### Focus now
Turn the system into a clear, shareable demo and reusable template.

### You need before starting
- Milestone E complete
- one UI tool choice:
  - Gradio
  - Streamlit

### External tools and accounts required
- No extra external account required
- provider switching is optional, not primary

### Concepts first
- A demo is not just pretty UI. It should make grounded behavior visible.
- Citations and uncertainty handling are part of the product, not debug leftovers.

### Next actions
1. Build a minimal demo UI connected to `POST /ask`.
2. Improve citation display for quick verification.
3. Show graceful fallback behavior for weak retrieval.
4. Polish README quickstart and architecture notes.
5. Explain how to reuse the project with a non-Lovecraft corpus.

### Verification
- Someone can run the demo locally without reading much code.
- The demo shows answers, citations, and uncertainty clearly.

### Done when
- A small demo UI makes the project easy to show to others.

### Read now
- Gradio docs: https://www.gradio.app/docs
- Streamlit docs: https://docs.streamlit.io/
- Anthropic engineering guide (grounded behavior): https://www.anthropic.com/engineering/building-effective-agents

### If blocked
Keep one UI path and one provider. Avoid branching into optional features before the demo is solid.

## Decision rule: What to do next

When you finish any checklist item, use this order:
1. Improve correctness first (grounding and citations).
2. Improve retrieval quality second.
3. Improve observability third.
4. Improve UX and polish last.

If two tasks compete, choose the one that improves measurable grounded behavior.

## Weekly cadence (4h/week)

- Session 1 (2h): implement one small vertical slice.
- Session 2 (1h): run verification and inspect failures.
- Session 3 (1h): targeted fix and short notes in README.

Keep every week shippable, even if small.

## Definition of project success

By the end, you should be able to say:
"I built a small grounded AI system over a literary corpus. I learned retrieval tradeoffs, evaluation design, latency and observability instrumentation, and product behavior under uncertainty."
