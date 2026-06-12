"""
DocMind — Serverless API for Groq LLM
Deployed on Vercel as a serverless function.
"""

import os
import json
from http.server import BaseHTTPRequestHandler
from groq import Groq


def handle_chat(question: str, context: str, history: list) -> str:
    """Generate answer using Groq LLM with document context."""
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        return "⚠️ Server error: GROQ_API_KEY not configured."

    client = Groq(api_key=api_key)

    # Build conversation history
    history_text = ""
    if history:
        for msg in history[-6:]:
            role = "User" if msg.get("role") == "user" else "Assistant"
            history_text += f"{role}: {msg.get('content', '')}\n"

    system_prompt = f"""You are DocMind, a precise AI document analyst. Answer questions based ONLY on the document context provided below.

Rules:
1. Answer ONLY from the context. If the answer isn't there, say "I couldn't find this information in the document."
2. Always cite the section or relevant text when referencing information.
3. Be concise but complete. Use bullet points for lists.
4. If the question is a greeting or not about the document, respond briefly and redirect to document questions.
5. Format your answer with markdown for readability.

{f"Previous conversation:{chr(10)}{history_text}" if history_text else ""}

DOCUMENT CONTEXT:
{context[:12000]}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.1,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error generating response: {str(e)}"


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
            return

        question = data.get("question", "").strip()
        context = data.get("context", "").strip()
        history = data.get("history", [])

        if not question:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Question is required"}).encode())
            return

        answer = handle_chat(question, context, history)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"answer": answer}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
