# 1_LangGraph_Agent (Streamlit + Tools)

A production-ready starter for your LangGraph tool-using agent with Streamlit UI, **no secrets committed**, GitHub Actions CI.

## ✨ Features

- LangGraph graph with tool routing
- Tooling: DuckDuckGo search, file read/write, PDF read/write
- Streamlit chat UI with threaded history
- SQLite checkpointing (LangGraph)
- `.env`-driven secrets (no hard-coded API keys)
- GitHub Actions: lint, type-check, and tests
- Ready-to-clone repository structure

---

## 🗂 Project Structure

```
.
├── .env              
├── .gitignore
├── requirements.txt
├── app.py            
├── langgraph_helper.py
├── tools.py         
├── toolnode.py       
└── README.md
```

---

## 🔑 Environment Variables

```
Create a .env file in the project root and fill in your configuration:

GROQ_API_KEY=your_groq_api_key_here
DUCK_REGION=us-en
DUCK_SAFESEARCH=moderate
DUCK_TIME_RANGE=d
```

**Required:**

- `GROQ_API_KEY` – your Groq API key for `ChatGroq`

**Optional:**

- `DUCK_REGION` (default: `us`)
- `DUCK_SAFESEARCH` (default: `Moderate`)
- `DUCK_TIME_RANGE` (default: `y`)

> ⚠️ Never commit `.env` to Git. `.gitignore` already protects it.

---

## 🚀 Quickstart (Local)

```bash
# 1) Create & activate a virtualenv (recommended)
python -m venv .venv
.venv\Scripts\activate

# 2) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3) Configure secrets
GROQ_API_KEY=your_groq_api_key_here
DUCK_REGION=us-en
DUCK_SAFESEARCH=moderate
DUCK_TIME_RANGE=d
# edit .env and paste your GROQ_API_KEY

# 4) Run Streamlit
streamlit run app.py
```

Open the app at http://localhost:8501

---

## 🧪 Run quality checks

```bash
# Lint & type-check
ruff check .
mypy .

# Tests
pytest -q
```

You can also run everything via:
```bash
make qa
```



## 🧩 How to add a new tool

1. Create the tool in `tools.py` with the `@tool` decorator:
   ```python
   @tool
   def my_cool_tool(param: str) -> str:
       """Explain what the tool does here."""
       return f\"You passed {param}\"
   ```
2. Add it to the `tools = [...]` list in `langgraph_helper.py`.
3. The agent can now call it when relevant.

---

## 🔒 Security & Secrets

- API keys must come from `.env` (via `python-dotenv`), not from source code.
- CI does **not** run any model calls—tests cover just the pure Python tools.
- If you ever need secrets in CI, use **GitHub Repository Secrets**, not plaintext.

---

## 🧰 Troubleshooting

- **`No module named 'exceptions'`**: remove any `exceptions`-related packages. This starter doesn't use that module.
- **PDF text extraction empty**: Some PDFs are scans. Consider OCR (e.g., `pytesseract`). This repo uses `PyPDF2` for text PDFs.
- **DuckDuckGo rate limits**: The community tool is best-effort and may be rate-limited. Add caching or backoff if needed.

---

## 📤 Push to GitHub (step-by-step)

```bash
# From project root
git init
git add .
git commit -m "Initial commit: LangGraph Agent Starter"
git branch -M main

# Create a new GitHub repo (via web UI or GH CLI)
# Then add your remote, e.g.:
git remote add origin https://github.com/keshabshrestha007/1_Langgraph_Agent.git
git push -u origin main
```


