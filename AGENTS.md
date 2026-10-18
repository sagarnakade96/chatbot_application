# AGENTS.md

Guidance for AI coding agents working in this repository. Humans: see
[README.md](README.md) and [APPLICATIONS.md](APPLICATIONS.md).

## What this repo is

A personal research sandbox of small, independent LLM-chatbot experiments on
**AWS Bedrock**, using **boto3**, **LangChain**, **LangGraph**, **FAISS** and
**Streamlit**. Each top-level folder stands alone. There is no package, no build
step, no test suite, and (currently) no git history.

## Project map

```
Chatbot_Code/
├── 01_agent.py            boto3 -> Nova Pro: summarize turbine logs
├── 03_guardrails.py       01_agent.py + Bedrock Guardrail (UI imports this)
├── 02_streamlit.py        Streamlit UI over 03_guardrails
├── chatbot/               LangChain ConversationChain + summary-buffer memory
├── chatbot_rag/           FAISS RAG over an HR-policy PDF
├── langchain/             standalone LangChain lessons + template.json
├── langgraph/simple_chatbot/   LangGraph classifier/router  <-- see ARCHITECTURE.md
├── learning_app_kb/       Bedrock Knowledge Base streaming retrieval
├── backend/               FastAPI multi-app backend (see backend/README.md, backend/AGENTS.md)
├── requirement.txt        pinned deps (NOTE: singular filename)
├── .env / .env.example    credentials for the boto3 scripts
└── venv/                  local virtualenv (git-ignored)
```

## Setup / commands

```bash
python -m venv venv && venv\Scripts\activate      # Windows (PowerShell/cmd)
pip install -r requirement.txt                     # NOT requirements.txt
```

Run targets (each from the location shown — imports are not packaged):

| App | Command | From |
|-----|---------|------|
| Turbine summarizer UI | `streamlit run 02_streamlit.py` | repo root |
| Memory chatbot | `streamlit run chatbot_fronend.py` | `chatbot/` |
| RAG Q&A | `streamlit run rag_frontend.py` | `chatbot_rag/` |
| LangGraph bot | `python runner.py` | `langgraph/simple_chatbot/` |
| KB retrieval | `python 01_connection_file.py` | `learning_app_kb/` |
| LangChain lessons | `python <file>.py` | varies (`prompts.py` needs `langchain/` as CWD) |

There are no linters or formatters configured, though `black` is in
`requirement.txt`. If you reformat, use `black` defaults and keep it to files you
are already editing.

## Credentials

Two mechanisms coexist — match the file you are editing:

- **`.env` + `python-dotenv`** (explicit keys): `01_agent.py`,
  `03_guardrails.py`, `learning_app_kb/01_connection_file.py`.
- **AWS shared-credentials profile `develop-admin`**: everything under
  `chatbot/`, `chatbot_rag/`, `langchain/`, `langgraph/`.

Region is `us-east-1` everywhere. Models in use:
`amazon.nova-pro-v1:0`, `us.anthropic.claude-sonnet-4-5-20250929-v1:0`,
`amazon.titan-embed-text-v1`.

**Never commit real credentials.** `.env` is git-ignored; update
`.env.example` (placeholders only) when you add a new variable. If you see a real
key in the working tree or history, flag it — it must be rotated in AWS.

## Conventions in this codebase

- **Flat imports.** Modules import siblings by bare name
  (`from state_file import ChatState`). Scripts therefore only run with their own
  folder as the working directory. Don't "fix" this into packages unless asked.
- **`print()` for tracing.** Nodes and functions narrate themselves with
  `print("\n[name]")`. Match that style rather than adding a logging framework.
- **Numeric filename prefixes** (`01_`, `02_`, `03_`) imply run order and force
  `importlib.import_module(...)` instead of `import`.
- **Pydantic models** for I/O contracts and for LLM structured output
  (`.with_structured_output(Model)`).
- Docstrings: Google-style, present on `langgraph/simple_chatbot/`. Other folders
  are largely undocumented — add docstrings when you touch a function.

## Known rough edges (don't be surprised)

- `requirement.txt` (singular), `chatbot_fronend.py` (misspelled).
- `01_agent.py` vs `03_guardrails.py` are near-duplicates.
- `chatbot_rag/rag_backend.py` builds a FAISS store it never returns, plus
  commented-out Marvel sample text.
- `learning_app_kb/01_connection_file.py` has unreachable code after `return`.
- `langgraph/simple_chatbot/decision_nodes.py` is a dead draft;
  `nodes_file.py` holds the live nodes.
- Hard-coded values: guardrail id, PDF URL, KB question.

## When making changes

- Work in `backend/` follows `backend/AGENTS.md`, including its mandatory
  documentation-update rule.

- Keep experiments independent; don't add cross-folder imports.
- Preserve pinned versions in `requirement.txt`; add new deps with an explicit
  `==` pin.
- Test by actually running the relevant app (needs live AWS Bedrock access) —
  there is no offline test path.
- Prefer small, local edits that match the surrounding rough-prototype style.
