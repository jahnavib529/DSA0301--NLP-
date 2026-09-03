"""
HealthScribe AI — Python Web Server & Application Host
Serves the HealthScribe AI frontend and provides API endpoints for medical document analysis.
"""

import http.server
import socketserver
import os
import sys
import json
import webbrowser
import subprocess
import threading
from urllib.parse import urlparse

# Set default console encoding to UTF-8 if possible
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PORT = int(os.environ.get("PORT", 5000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")

def check_and_build():
    """Ensure frontend dist bundle exists; if not, build it."""
    if not os.path.exists(DIST_DIR) or not os.path.exists(os.path.join(DIST_DIR, "index.html")):
        print("[HealthScribe] 'dist' folder not found. Building production bundle with npm...", flush=True)
        node_paths = ["C:\\Program Files\\nodejs", "C:\\Program Files (x86)\\nodejs"]
        for np in node_paths:
            if os.path.exists(np) and np not in os.environ.get("PATH", ""):
                os.environ["PATH"] = np + os.pathsep + os.environ.get("PATH", "")
        
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
        subprocess.run([npm_cmd, "run", "build"], cwd=BASE_DIR, check=True)
        print("[HealthScribe] Build complete!", flush=True)

class HealthScribeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Health check endpoint
        if path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "healthy",
                "app": "HealthScribe AI",
                "version": "1.0.0",
                "mode": "Educational Patient Guidance"
            }).encode("utf-8"))
            return

        # Check if the requested file exists in dist
        file_path = os.path.join(DIST_DIR, path.lstrip("/"))
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            return super().do_GET()

        # SPA Fallback: serve index.html for all client-side routes
        index_path = os.path.join(DIST_DIR, "index.html")
        if os.path.exists(index_path):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(index_path, "rb") as f:
                self.wfile.write(f.read())
            return

        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Simulated AI Chat API endpoint
        if path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            query = data.get("query", "")

            response_data = {
                "message": f"HealthScribe AI received your query: '{query}'. Consult your physician for clinical diagnosis.",
                "disclaimer": "Educational support tool only. Not medical advice."
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        self.send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        sys.stderr.write(f"[HealthScribe] {self.address_string()} - {format % args}\n")

def run_server():
    check_and_build()
    
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), HealthScribeHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60, flush=True)
        print("HealthScribe AI - Clinical Simplification Assistant", flush=True)
        print(f"Server running live at: {url}", flush=True)
        print("Mode: Client-Side Sandbox & Educational Guidance", flush=True)
        print("Press Ctrl+C to stop the server", flush=True)
        print("=" * 60, flush=True)
        
        def open_browser():
            import time
            time.sleep(0.8)
            try:
                webbrowser.open(url)
            except Exception:
                pass
            
        threading.Thread(target=open_browser, daemon=True).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down HealthScribe AI server...", flush=True)
            httpd.server_close()

if __name__ == "__main__":
    run_server()
