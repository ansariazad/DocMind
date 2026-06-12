# 🧠 DocMind — AI Document Intelligence

> Upload any PDF. Ask questions. Get AI-powered answers with page citations.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-docmind--self.vercel.app-indigo?style=for-the-badge)](https://docmind-self.vercel.app)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=flat)](https://groq.com)
[![Vercel](https://img.shields.io/badge/Deployed_on-Vercel-black?style=flat&logo=vercel)](https://vercel.com)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📄 **PDF Upload** | Client-side parsing with PDF.js — no server upload needed |
| 💬 **AI Chat** | Ask questions, get answers with **[Page X]** citations |
| 📋 **Auto Summary** | Instant document analysis: summary, topics, type, reading time |
| 💡 **Smart Questions** | AI-suggested questions to explore the document |
| 📝 **Quiz Mode** | Generate MCQ quizzes with scoring and explanations |
| 🌍 **Multilingual** | Answers in 7 languages: EN, HI, ES, FR, AR, ZH, JA |
| 📤 **Export** | Download chat history as Markdown |
| 📱 **Mobile Responsive** | Full experience on any device |

## 🏗️ Architecture

```
PDF Upload → PDF.js (client-side) → Text Extraction → Page Chunking
                                                          ↓
User Query → Vercel Serverless → Groq LLM (llama-3.3-70b) → Answer + Citations
```

## 🔧 Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JS (ES6+), PDF.js, marked.js
- **Backend**: Python Vercel Serverless Functions
- **LLM**: Groq API (llama-3.3-70b-versatile)
- **Deployment**: Vercel (zero-config)

## 📁 Project Structure

```
docmind/
├── index.html           # Complete app UI
├── static/style.css     # Design system (dark theme)
├── api/
│   ├── chat.py          # Q&A endpoint with citations
│   ├── summary.py       # Auto-summary generation
│   ├── quiz.py          # MCQ quiz generation
│   └── questions.py     # Smart question suggestions
├── vercel.json          # Deployment config
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Deploy your own

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ansariazad/DocMind&env=GROQ_API_KEY)

### Run locally

```bash
git clone https://github.com/ansariazad/DocMind.git
cd DocMind

# Set your Groq API key
echo "GROQ_API_KEY=your-key" > .env

# Install dependencies
pip install -r requirements.txt

# Start dev server
python3 -m http.server 3000
```

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key ([get one free](https://console.groq.com)) |

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Ask questions with document context |
| `POST` | `/api/summary` | Generate document summary |
| `POST` | `/api/quiz` | Generate MCQ quiz |
| `POST` | `/api/questions` | Suggest smart questions |

## 👨‍💻 Author

**Azad Ansari** — AI Automation Engineer

- 🌐 [Portfolio](https://ansariazad.github.io/hire.html)
- 💼 [LinkedIn](https://linkedin.com/in/azad-ansari-902035297)
- 🐙 [GitHub](https://github.com/ansariazad)

---

*Built with ❤️ using Groq LLM for near-instant AI inference.*
