#!/usr/bin/env python3
"""Local outreach dashboard.

    python scripts/dashboard.py                 # http://localhost:8765
    python scripts/dashboard.py --port 9000 --data "C:/Users/ragha/Documents/cold-email-outreach-data"

Reads tracker.csv and runs.csv from the data folder on every page load (nothing is cached or written),
so re-running an outreach day and refreshing the page shows the new numbers. Binds to 127.0.0.1 only.
"""
import argparse, csv, json, os, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
KEEP = ["company", "email", "track", "location", "status", "date_found", "date_sent", "reply_date",
        "reply_snippet", "bounce_reason", "followup_count", "gmail_thread_id", "source_type", "priority"]


def default_data():
    if os.environ.get("OUTREACH_DATA"):
        return Path(os.environ["OUTREACH_DATA"])
    docs = Path.home() / "Documents" / "cold-email-outreach-data"
    return docs if docs.exists() else HERE.parent / "data"


def read(p):
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def payload(data):
    rows = [{k: r.get(k, "") for k in KEEP} for r in read(data / "tracker.csv")]
    return {"data_dir": str(data), "rows": rows, "runs": read(data / "runs.csv")}


def make_handler(data):
    class H(BaseHTTPRequestHandler):
        def _send(self, body, ctype, code=200):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = self.path.split("?")[0]
            if path in ("/", "/index.html"):
                self._send((HERE / "dashboard.html").read_bytes(), "text/html; charset=utf-8")
            elif path == "/api/data":
                try:
                    self._send(json.dumps(payload(data)).encode(), "application/json")
                except Exception as e:  # show the error in the page instead of a blank screen
                    self._send(json.dumps({"error": str(e)}).encode(), "application/json", 500)
            else:
                self._send(b"not found", "text/plain", 404)

        def log_message(self, *a):
            pass
    return H


def main():
    ap = argparse.ArgumentParser(description="Local outreach stats dashboard")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--data", type=Path, default=None, help="folder with tracker.csv (default: OUTREACH_DATA, "
                    "then ~/Documents/cold-email-outreach-data, then ./data)")
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    data = a.data or default_data()
    if not (data / "tracker.csv").exists():
        raise SystemExit(f"tracker.csv not found in {data} - pass --data <folder>")
    url = f"http://localhost:{a.port}"
    print(f"Outreach dashboard: {url}  (data: {data})  Ctrl+C to stop")
    if not a.no_browser:
        webbrowser.open(url)
    ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(data)).serve_forever()


if __name__ == "__main__":
    main()
