"""
DocMind v2 — Chat API (Vercel Serverless)
Handles document Q&A with Groq LLM, citations, and conversation memory.
"""

import os
import json
from http.server import BaseHTTPRequestHandler
from groq import Groq

SYSTEM_PROMPT = """You are DocMind, an expert AI document analyst built by Azad Ansari.
You answer questions ONLY based on the provided document context.

Rules:
1. Always cite page numbers using format: **[Page X]** inline in your answer
2. If information is not in the context, say "I couldn't find this information in the document."
3. Be concise but thorough. Use markdown: **bold**, bullet points, `code` where helpful
4. Never fabricate information or use external knowledge
5. For numbers, quotes, or specific facts — always cite the exact page
6. Structure long answers with clear sections using markdown headings
7. If asked to explain, provide clear examples from the document"""


def generate_answer(question, context, history, language="English"):
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return {"error": "GROQ_API_KEY not configured"}

    client = Groq(api_key=api_key)

    history_text = ""
    if history:
        for msg in history[-8:]:
            role = "User" if msg.get("role") == "user" else "Assistant"
            history_text += f"{role}: {msg.get('content', '')}\n"

    lang_instruction = f"\nRespond in {language}. Keep technical terms in English." if language != "English" else ""

    prompt = f"""{SYSTEM_PROMPT}{lang_instruction}

DOCUMENT CONTEXT:
{context[:14000]}

{f"CONVERSATION HISTORY:{chr(10)}{history_text}" if history_text else ""}

USER QUESTION: {question}

Provide a detailed, well-structured answer with inline **[Page X]** citations:"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are DocMind, a precise document analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=1500,
        )
        return {"answer": response.choices[0].message.content}
    except Exception as e:
        return {"error": f"AI service error: {str(e)}", "retry": True}


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._respond(400, {"error": "Invalid JSON"})
            return

        question = data.get("question", "").strip()
        context = data.get("context", "").strip()
        history = data.get("history", [])
        language = data.get("language", "English")

        if not question:
            self._respond(400, {"error": "Question is required"})
            return

        result = generate_answer(question, context, history, language)
        self._respond(200 if "answer" in result else 500, result)

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self._cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
