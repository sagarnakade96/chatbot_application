# Applications

One section per experiment in this repo: what it does, the files involved, how to
run it, and things to watch out for. See [README.md](README.md) for setup and
[AGENTS.md](AGENTS.md) for conventions.

---

## 1. Wind-turbine log summarizer (`01_agent.py`, `03_guardrails.py`, `02_streamlit.py`)

**Goal:** turn raw equipment logs into a 5-line, plain-English summary that
highlights errors, using Amazon Nova Pro through the low-level Bedrock API.

| File | Role |
|------|------|
| [`01_agent.py`](01_agent.py) | `invoke_agent(user_input)` — builds a `messages-v1` request, calls `bedrock-runtime.invoke_model`, returns `(status_code, text)`. |
| [`03_guardrails.py`](03_guardrails.py) | Same function, plus `guardrailIdentifier` / `guardrailVersion` on the call so Bedrock Guardrails filters the I/O. This is the version the UI imports. |
| [`02_streamlit.py`](02_streamlit.py) | Wide Streamlit page with custom CSS. Loads `invoke_agent` from `03_guardrails` via `importlib` (module name starts with a digit, so it cannot be a normal `import`), renders a textarea + "Summarize" button. |

**Run:**
```bash
streamlit run 02_streamlit.py          # UI
python -c "import importlib; m=importlib.import_module('03_guardrails'); print(m.invoke_agent('...logs...'))"
```

**Credentials:** `.env` (`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`), region `us-east-1`.

**Watch out:**
- `01_agent.py` and `03_guardrails.py` are near-duplicates; keep them in sync or
  collapse them.
- The guardrail id in `03_guardrails.py` (`myjz44g4d0n7`, version `1`) is
  account-specific — replace it with your own or the call fails.
- Model: `amazon.nova-pro-v1:0`.

---

## 2. Conversational chatbot with memory (`chatbot/`)

**Goal:** a chat UI ("Mira-AI") that remembers the conversation using
LangChain's summary-buffer memory (older turns are compressed into a running
summary once the token budget is exceeded).

| File | Role |
|------|------|
| [`chatbot/chatbot_backend.py`](chatbot/chatbot_backend.py) | `demo_chatbot()` builds a `ChatBedrockConverse` (Claude Sonnet 4.5). `demo_memory()` builds a `ConversationSummaryBufferMemory` (1000-token limit). `demo_conversation(input_text, memory)` runs a `ConversationChain` and returns the reply string. |
| [`chatbot/chatbot_fronend.py`](chatbot/chatbot_fronend.py) | Streamlit `st.chat_input` UI. Keeps `memory` and `chat_history` in `st.session_state` so they survive Streamlit re-runs; re-renders history each run. |

**Run:**
```bash
cd chatbot
streamlit run chatbot_fronend.py
```

**Credentials:** AWS profile `develop-admin`.

**Watch out:**
- Filename is `chatbot_fronend.py` (typo — "fronend"). The import inside it
  (`import chatbot_backend as demo`) only resolves when you run from inside
  `chatbot/`.
- `ConversationChain` / `ConversationSummaryBufferMemory` come from
  `langchain_classic` and are legacy APIs.

---

## 3. RAG Q&A over an HR policy PDF (`chatbot_rag/`)

**Goal:** answer HR questions grounded in a specific PDF using retrieval
(embeddings + FAISS) instead of the model's own knowledge.

| File | Role |
|------|------|
| [`chatbot_rag/rag_backend.py`](chatbot_rag/rag_backend.py) | `hr_index()` downloads the HR-policy PDF, splits it with `RecursiveCharacterTextSplitter`, embeds chunks with Titan embeddings, and builds a FAISS `VectorstoreIndexCreator`. `hr_llm()` builds the Claude Sonnet 4.5 chat model. `rag_response(index, question)` queries the index with the LLM. |
| [`chatbot_rag/rag_frontend.py`](chatbot_rag/rag_frontend.py) | Streamlit UI. `get_vector_index()` is wrapped in `@st.cache_resource` so the index is built once per session. Textarea + button -> `rag_response`. |

**Run:**
```bash
cd chatbot_rag
streamlit run rag_frontend.py
```

**Credentials:** AWS profile `develop-admin`.

**Watch out:**
- The PDF URL is hard-coded (`https://rikalp.in/.../HR-Policy.pdf`) — needs
  network access at startup.
- `hr_index()` both builds a FAISS store manually **and** a
  `VectorstoreIndexCreator`; only the latter is returned. There is dead/commented
  sample code (Marvel text) left in.
- Models: `amazon.titan-embed-text-v1` (embeddings),
  `us.anthropic.claude-sonnet-4-5-20250929-v1:0` (generation).

---

## 4. LangChain lessons (`langchain/`)

**Goal:** minimal standalone scripts, each demonstrating one LangChain concept.
Not an application — run them one at a time.

| File | Concept |
|------|---------|
| [`langchain/messages.py`](langchain/messages.py) | `SystemMessage` / `HumanMessage` / `AIMessage`, one `model.invoke(messages)` call. |
| [`langchain/chatbot.py`](langchain/chatbot.py) | Bare `while` loop CLI chat that accumulates raw strings into `chat_history`. Type `q` / `Q` to quit. |
| [`langchain/prompts.py`](langchain/prompts.py) | Loads a prompt from [`template.json`](langchain/template.json) via `load_prompt`, builds a `template | model` chain, drives it from a Streamlit form (research-paper summarizer). |
| [`langchain/template.json`](langchain/template.json) | Serialized `PromptTemplate` with `paper_input` / `style_input` / `length_input` variables. |
| [`langchain/user_structured_input_output.py`](langchain/user_structured_input_output.py) | A Pydantic `Student` model — validation / structured-data basics. |

**Run:**
```bash
python langchain/messages.py
python langchain/chatbot.py
cd langchain && streamlit run prompts.py     # template.json is resolved relative to CWD
```

**Credentials:** AWS profile `develop-admin`.

**Watch out:**
- `messages.py` appends `result.content` (a `str`) to a list of message objects —
  inconsistent typing, illustrative only.
- `chatbot.py` sends a growing list of plain strings to `model.invoke`, which
  works but is not the idiomatic message-object pattern.

---

## 5. LangGraph customer-support router (`langgraph/simple_chatbot/`)

**Goal:** classify each user message into `hr_policy`, `product_information`, or
`product_complaint` and route it to a category-specific node — a minimal but
complete LangGraph state machine.

Full deep-dive (execution order, per-file role, state flow, the graph diagram):
**[langgraph/simple_chatbot/ARCHITECTURE.md](langgraph/simple_chatbot/ARCHITECTURE.md)**.

| File | Role (summary) |
|------|----------------|
| `runner.py` | Entry point. Interactive REPL that calls the compiled graph once per turn. |
| `graph_build.py` | Builds, wires and compiles the graph into `app`; `draw_graph()` exports a PNG. |
| `packages_file.py` | Central re-export of all third-party imports. |
| `state_file.py` | `ChatState` TypedDict passed between nodes. |
| `input_output_format.py` | `Category` type + Pydantic models (`ChatInput`, `RoutingDecision`, `ChatOutput`) + `take_user_input()`. |
| `prompts.py` | `SYSTEM_PROMPT` for the classifier. |
| `llm_file.py` | Bedrock model + `with_structured_output`; the `invoke_llm` node. |
| `nodes_file.py` | `prepare_input` node + the three category terminal nodes (the ones actually used). |
| `routers.py` | `route_request` — the conditional-edge routing function. |
| `decision_nodes.py` | Superseded draft of the category nodes; **not imported**. |
| `customer_support_graph.png` | Rendered graph diagram (output of `draw_graph()`). |

**Run:**
```bash
cd langgraph/simple_chatbot
python runner.py            # type 'exit' to quit
```

**Credentials:** AWS profile `develop-admin`.

**Watch out:**
- All modules use flat imports (`from state_file import ...`), so you **must**
  run from inside `langgraph/simple_chatbot/`.
- Model: `us.anthropic.claude-sonnet-4-5-20250929-v1:0`.

---

## 6. Bedrock Knowledge Base retrieval (`learning_app_kb/`)

**Goal:** stream an answer from a Bedrock **Knowledge Base** via the
`bedrock-agent-runtime` agentic-retrieve API.

| File | Role |
|------|------|
| [`learning_app_kb/01_connection_file.py`](learning_app_kb/01_connection_file.py) | `invoke_bedrock_agent()` — sends a hard-coded question to `agentic_retrieve_stream`, consumes the event stream (partial text, final result, typed error events), returns `{statusCode, body}`. |

**Run:**
```bash
python learning_app_kb/01_connection_file.py
```

**Credentials:** `.env` (`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` +
`KNOWLEDGE_BASE_ID`).

**Watch out:**
- The prompt is hard-coded inside the function.
- There is unreachable code after the first `return` (leftover from an older
  non-streaming version).
- Requires a Knowledge Base already created in Bedrock and its id in `.env`.
