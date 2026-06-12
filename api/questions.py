"""
DocMind v2 — Questions API (Vercel Serverless)
Suggests smart questions based on document content.
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

        text = data.get("text", "").strip()
        if not text:
            self._respond(400, {"error": "Document text is required"})
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
                    {"role": "system", "content": "You generate smart questions. Return only a JSON array of strings."},
                    {"role": "user", "content": f"""Based on this document, generate 5 smart questions that would extract the most valuable insights.
Return ONLY a JSON array of strings, no markdown:
["Question 1?", "Question 2?", "Question 3?", "Question 4?", "Question 5?"]

Make questions specific to the document content, not generic.
Mix different types: factual, analytical, comparative, and "what if" questions.

Document text (first 3000 chars):
{text[:3000]}"""},
                ],
                temperature=0.4,
                max_tokens=400,
            )

            raw = response.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
                raw = raw.rsplit("```", 1)[0]

            questions = json.loads(raw)
            self._respond(200, {"questions": questions})

        except json.JSONDecodeError:
            self._respond(200, {"questions": [
                "What are the main findings?",
                "What methodology was used?",
                "What are the key conclusions?",
                "What limitations are mentioned?",
                "What are the practical implications?"
            ]})
        except Exception as e:
            self._respond(500, {"error": f"Question generation failed: {str(e)}"})

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
