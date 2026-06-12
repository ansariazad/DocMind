"""
DocMind v2 — Summary API (Vercel Serverless)
Auto-generates document summary, key topics, and metadata.
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
                    {"role": "system", "content": "You are a document analysis expert. Always return valid JSON only, no markdown formatting."},
                    {"role": "user", "content": f"""Analyze this document and return ONLY valid JSON (no markdown code blocks):
{{
  "summary": "3-4 sentence executive summary of the document",
  "key_topics": ["topic1", "topic2", "topic3", "topic4", "topic5"],
  "document_type": "research_paper|contract|manual|report|textbook|other",
  "reading_time_minutes": <integer>,
  "language": "detected language of the document",
  "complexity": "beginner|intermediate|advanced"
}}

Document text (first 4000 chars):
{text[:4000]}"""},
                ],
                temperature=0.1,
                max_tokens=500,
            )

            raw = response.choices[0].message.content.strip()
            # Clean potential markdown code blocks
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
                raw = raw.rsplit("```", 1)[0]

            summary_data = json.loads(raw)
            self._respond(200, summary_data)

        except json.JSONDecodeError:
            self._respond(200, {
                "summary": response.choices[0].message.content.strip()[:500],
                "key_topics": [],
                "document_type": "other",
                "reading_time_minutes": 5,
                "language": "English",
                "complexity": "intermediate"
            })
        except Exception as e:
            self._respond(500, {"error": f"Summary generation failed: {str(e)}"})

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
