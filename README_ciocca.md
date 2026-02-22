# 🌊 Ciocca Center / BEACH Chatbot Branch

**Your branch for the SCU project demo.**
Handles questions about the Ciocca Center for Innovation and Entrepreneurship and the
BEACH (Bronco Entrepreneurs' Applied Collaboration Hub) program.

---

## 🔀 Step 1 — Create Your Branch on GitHub

Run these commands **inside the cloned repo folder** (the same repo as `hchen850/frontend-demo`):

```bash
# 1. Make sure you're on main and up to date
git checkout main
git pull origin main

# 2. Create YOUR branch (replace with your actual name/preferred name)
git checkout -b ciocca-branch

# 3. Copy all the new files into the repo (from the zip or manually)
#    (see folder structure below)

# 4. Push your branch to GitHub
git push -u origin ciocca-branch
```

Now you'll see `ciocca-branch` in the GitHub branch dropdown alongside the others.

---

## 📁 Folder Structure

Place these files inside the repo:

```
your-repo/
├── main.py                          ← REPLACE existing main.py
├── ciocca_module.py                 ← NEW — Ciocca RAG handler
├── response_templates.py            ← NEW — response templates
├── requirements.txt                 ← UPDATED
├── test_ciocca.py                   ← NEW — mini test set
├── knowledge_base/
│   ├── __init__.py
│   └── ciocca_kb.py                 ← NEW — knowledge base (18 chunks)
└── frontend/
    └── src/
        ├── App.jsx                  ← UPDATE — points to CioccaChat
        └── CioccaChat.jsx           ← NEW — React chat UI with sources
```

---

## ⚙️ Step 2 — Backend Setup

```bash
# Install Python dependencies
pip install fastapi uvicorn requests python-dotenv

# Make sure Ollama is running with mistral pulled
ollama pull mistral
ollama serve          # (runs on localhost:11434 by default)

# Start FastAPI backend
uvicorn main:app --reload --port 8000
```

The server will be live at: http://localhost:8000

---

## 🖥️ Step 3 — Frontend Setup

```bash
cd frontend

# Install Node dependencies (first time)
npm install

# Start Vite dev server
npm run dev
```

Frontend will be at: http://localhost:5173

---

## 🧪 Step 4 — Run Tests

```bash
python test_ciocca.py
```

Expected output: **27/27 tests pass** ✅

---

## 🤖 How It Works

```
User message
     │
     ▼
Classifier (is_ciocca_question)
     │
     ├── YES → ciocca_module.handle_ciocca_query()
     │              │
     │              ├── retrieve_chunks() — keyword search KB
     │              ├── build RAG prompt with top 3 chunks
     │              ├── call Ollama/Mistral
     │              └── apply_template() + format_sources()
     │
     └── NO  → General Ollama handler
```

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/bot` | Main chat endpoint (auto-classifies) |
| POST | `/ciocca` | Direct Ciocca endpoint (skips classifier) |

### /bot Request Body
```json
{
  "message": "What is BEACH?",
  "category": null
}
```

### /bot Response
```json
{
  "reply": "📋 **Scope / What BEACH Can Help With**\n\nBEACH stands for...",
  "sources": [
    {
      "title": "What is BEACH?",
      "url": "https://www.scu.edu/cioccacenter/students/beach/",
      "category": "scope",
      "snippet": "BEACH stands for Bronco Entrepreneurs'..."
    }
  ],
  "category": "ciocca",
  "used_fallback": false
}
```

---

## 📚 Knowledge Base Coverage

The KB (`ciocca_kb.py`) has **18 chunks** covering:

| Category | Topics |
|----------|--------|
| `scope` | What BEACH is, what it's NOT, free?, topics covered |
| `eligibility` | Clients, students, mentors |
| `intake` | How to apply, session structure, Discovery Meeting |
| `resources` | All Ciocca programs, SCORE, SBA, Bronco Ventures |
| `contact` | How to reach Ciocca Center, application deadlines |
| `privacy` | Confidentiality, NDA, data handling |

**Hard fallback**: If no relevant chunk is found, bot says:
> "I wasn't able to find a confirmed answer in my knowledge base. Please visit [ciocca center link] or contact them directly."

---

## 🎯 Demo Script

1. Open http://localhost:5173
2. Click quick prompts:
   - **"What is BEACH?"** → Shows scope answer + 1 source
   - **"How do I apply as a client?"** → Shows intake process + source link
   - **"Can BEACH help with IP questions?"** → Shows IP info + disclaimer
   - **"What is the Bronco Ventures Accelerator?"** → Shows programs
   - **"How do I contact the Ciocca Center?"** → Shows contact info
3. Show **Sources dropdown** — click "▼ 1 Source" to expand and show the source card with URL
4. Show **category selector** — switch between Auto/Ciocca/General
5. Type an off-topic question (e.g., "What's 2+2?") → General handler responds

---

## 📝 KB Gaps Log

Whenever the bot can't answer → log the question here:

| Date | Question | Status |
|------|----------|--------|
| — | — | — |

> Add unanswered questions here and request policy content to fill the gap.

---

## 🔗 Official Sources Used

- https://www.scu.edu/cioccacenter/
- https://www.scu.edu/cioccacenter/students/beach/
- https://www.scu.edu/cioccacenter/students/beach/businesses/
- https://www.scu.edu/cioccacenter/students/beach/become-a-mentor/
- https://www.scu.edu/cioccacenter/bronco-ventures/bronco-venture-accelerator/
- https://www.scu.edu/cioccacenter/contact-us/
