# Chatbot_Code

A personal research sandbox for building LLM chatbots on **AWS Bedrock** with
**LangChain** and **LangGraph**. Each top-level folder is a small, self-contained
experiment that explores one idea — raw Bedrock calls, conversational memory,
retrieval-augmented generation (RAG), prompt templating, structured output, and
graph-based routing.

> This is learning / prototype code, not a production system. Expect hard-coded
> values, print-statement debugging, and rough edges.

---

## Repository layout

| Path | What it explores | Stack |
|------|------------------|-------|
| [`01_agent.py`](01_agent.py) | Direct `bedrock-runtime` call that summarizes wind-turbine equipment logs | boto3 + Amazon Nova Pro |
| [`03_guardrails.py`](03_guardrails.py) | Same as above, plus a Bedrock **Guardrail** attached to the call | boto3 + Nova Pro |
| [`02_streamlit.py`](02_streamlit.py) | Styled Streamlit UI wrapping the guardrails agent | Streamlit |
| [`chatbot/`](chatbot/) | Conversational chatbot with summary-buffer **memory** | LangChain + Streamlit |
| [`chatbot_rag/`](chatbot_rag/) | **RAG** Q&A over an HR-policy PDF using FAISS | LangChain + FAISS |
| [`langchain/`](langchain/) | Bite-size LangChain lessons: messages, prompt templates, structured output | LangChain |
| [`langgraph/simple_chatbot/`](langgraph/simple_chatbot/) | Customer-support classifier that **routes** to category-specific nodes | LangGraph |
| [`learning_app_kb/`](learning_app_kb/) | Streaming retrieval from a Bedrock **Knowledge Base** agent | boto3 |

For a walk-through of what each application does and how to run it, see
[APPLICATIONS.md](APPLICATIONS.md).
For an architecture deep-dive of the LangGraph bot (execution order, per-file
role, state flow), see
[langgraph/simple_chatbot/ARCHITECTURE.md](langgraph/simple_chatbot/ARCHITECTURE.md).
If you are an AI coding agent, start with [AGENTS.md](AGENTS.md).

---

## Prerequisites

- **Python 3.11+**
- An **AWS account with Amazon Bedrock access** in `us-east-1`, with the models
  enabled in the Bedrock console:
  - `amazon.nova-pro-v1:0`
  - `us.anthropic.claude-sonnet-4-5-20250929-v1:0`
  - `amazon.titan-embed-text-v1`
- Credentials configured **one of two ways**, depending on the script (see
  [AGENTS.md](AGENTS.md#credentials) for which is which):
  - a `.env` file with `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`, **or**
  - an AWS shared-credentials **profile** named `develop-admin`
    (`~/.aws/credentials`).

---

## Setup

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirement.txt

cp .env.example .env        # then edit .env with real values
```

## Running

Each experiment runs on its own. A few examples:

```bash
# Streamlit apps must run from inside their folder (imports are not packaged)
cd chatbot && streamlit run chatbot_fronend.py
cd chatbot_rag && streamlit run rag_frontend.py

# LangGraph customer-support bot (interactive CLI)
cd langgraph/simple_chatbot && python runner.py

# One-off scripts
python langchain/messages.py
```

See [APPLICATIONS.md](APPLICATIONS.md) for per-app instructions and notes.

---

## Security note

Older commits of this repo contained a real `.env` with live AWS keys.
`.env` is now git-ignored, but **any key that was ever committed must be rotated**
in the AWS console — git history keeps it forever. Never commit real credentials;
use [`.env.example`](.env.example) as the template.

---

## Dependencies

All Python dependencies are pinned in [`requirement.txt`](requirement.txt)
(note the singular filename). Key libraries: `boto3`, `langchain`, `langchain-aws`,
`langgraph`, `faiss-gpu`, `streamlit`, `pydantic`.
