"""
DocMind — Local Development Server
Serves static files + proxies /api/chat to the Groq API.
Run: python3 dev.py
"""

import os
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")


class DevHandler(SimpleHTTPRequestHandler):
    """Handles static files + /api/chat endpoint."""

    def do_POST(self):
        if self.path == "/api/chat":
            self._handle_chat()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _handle_chat(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self._json_response(400, {"error": "Invalid JSON"})
            return

        question = data.get("question", "").strip()
        context = data.get("context", "").strip()
        history = data.get("history", [])

        if not question:
            self._json_response(400, {"error": "Question is required"})
            return

        if not GROQ_API_KEY:
            self._json_response(500, {"error": "GROQ_API_KEY not set in .env"})
            return

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

{f"Previous conversation:\n{history_text}" if history_text else ""}

DOCUMENT CONTEXT:
{context[:12000]}"""

        try:
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
                temperature=0.1,
                max_tokens=1024,
            )
            answer = response.choices[0].message.content
            self._json_response(200, {"answer": answer})
        except Exception as e:
            self._json_response(500, {"error": f"LLM error: {str(e)}"})

    def _json_response(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        """Custom log with colors."""
        method = args[0].split()[0] if args else ""
        path = args[0].split()[1] if args and len(args[0].split()) > 1 else ""
        code = args[1] if len(args) > 1 else ""
        if "/api/" in str(path):
            print(f"  ⚡ API  {method} {path} → {code}")
        elif str(code) == "200":
            pass  # Don't log static 200s
        else:
            print(f"  📄 {method} {path} → {code}")


if __name__ == "__main__":
    port = 3000
    server = HTTPServer(("0.0.0.0", port), DevHandler)
    print(f"""
╔══════════════════════════════════════╗
║      🧠 DocMind Dev Server          ║
╠══════════════════════════════════════╣
║  Local:  http://localhost:{port}       ║
║  API:    http://localhost:{port}/api   ║
║  LLM:    {"✅ Groq connected" if GROQ_API_KEY else "❌ No GROQ_API_KEY"}        ║
╚══════════════════════════════════════╝
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
        server.server_close()
