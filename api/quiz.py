"""
DocMind v2 — Quiz API (Vercel Serverless)
Generates MCQ quizzes from document content.
"""

import os
import json
from http.server import BaseHTTPRequestHandler
from groq import Groq


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._respond(400, {"error": "Invalid JSON"})
            return

        context = data.get("context", "").strip()
        num_questions = min(data.get("num_questions", 5), 10)

        if not context:
            self._respond(400, {"error": "Document context is required"})
            return

        api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            self._respond(500, {"error": "GROQ_API_KEY not configured"})
            return

        try:
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an expert quiz generator. Always return valid JSON arrays only, no markdown."},
                    {"role": "user", "content": f"""Generate exactly {num_questions} multiple choice questions from this document.
Return ONLY a valid JSON array (no markdown code blocks):
[{{
  "question": "Clear, specific question",
  "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}},
  "correct": "A",
  "explanation": "Brief explanation citing the document",
  "page": 1
}}]

Make questions vary in difficulty. Test comprehension, not just recall.

Document context:
{context[:8000]}"""},
                ],
                temperature=0.3,
                max_tokens=2000,
            )

            raw = response.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
                raw = raw.rsplit("```", 1)[0]

            questions = json.loads(raw)
            self._respond(200, {"questions": questions})

        except json.JSONDecodeError:
            self._respond(500, {"error": "Failed to generate valid quiz. Try again."})
        except Exception as e:
            self._respond(500, {"error": f"Quiz generation failed: {str(e)}"})

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
