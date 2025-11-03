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

```bash
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

```bash
#Create a .env file in the project root and fill in your configuration:

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
---
## 🛠️ Setup

### 1. Clone the repository
```bash
git remote add origin https://github.com/keshabshrestha007/1_Langgraph_Agent.git
```
```bash
cd 1_Langgraph_Agent
```
### 2. Create & activate a virtualenv (recommended)
```bash
python -m venv .venv
```
on windows
```bash
.venv\Scripts\activate
```
on linux/mac
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure secrets
```bash
GROQ_API_KEY=your_groq_api_key_here
DUCK_REGION=us-en
DUCK_SAFESEARCH=moderate
DUCK_TIME_RANGE=d
# edit .env and paste your GROQ_API_KEY
```

### 5. Run Streamlit
```bash
streamlit run app.py
```
---

## 🧩 How to add a new tool

1. Create the tool in `tools.py` with the `@tool` decorator:
   ```bash
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




