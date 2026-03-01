#!/usr/bin/env python3
"""
notify.py — True Webhook CLI Monitor (SSE)
==========================================
Connects to GET /webhook/stream and blocks.
The server pushes each notification instantly — zero polling.

Usage:
  uv run python notify.py
  uv run python notify.py --url http://localhost:8001
"""

import argparse
import json
import signal
import sys
import time
from datetime import datetime

import httpx

# ──────────────────────────────────────────────
# ANSI colors
# ──────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
RED    = "\033[91m"
WHITE  = "\033[97m"
YELLOW = "\033[93m"


def print_banner(url: str):
    print(f"""
{BOLD}{GREEN}┌─────────────────────────────────────────┐
│   🔔  Webhook Notification Monitor       │
│       True SSE — zero polling            │
└─────────────────────────────────────────┘{RESET}
{DIM}  Stream  :{RESET} {CYAN}{url}/webhook/stream{RESET}
{DIM}  Quit    :{RESET} Ctrl+C
{DIM}  Started :{RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{DIM}──────────────────────────────────────────{RESET}
{DIM}  Waiting for Postgres to push...{RESET}
""")


def print_notification(data: dict):
    ts  = data.get("received_at", "")
    nid = data.get("id", "?")
    msg = data.get("notification", "")

    try:
        dt     = datetime.fromisoformat(ts)
        ts_fmt = dt.strftime("%H:%M:%S")
    except Exception:
        ts_fmt = ts or "—"

    print(
        f"  {DIM}[{ts_fmt}]{RESET} "
        f"{BOLD}{GREEN}#{nid}{RESET} "
        f"{WHITE}{msg}{RESET}"
    )


def run(base_url: str):
    stream_url = f"{base_url.rstrip('/')}/webhook/stream"
    total      = 0

    print_banner(base_url)

    def handle_exit(sig, frame):
        print(f"\n\n{DIM}  Disconnected. Total notifications received: {total}{RESET}\n")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)

    while True:
        try:
            with httpx.Client(timeout=None) as client:
                with client.stream("GET", stream_url) as response:
                    response.raise_for_status()

                    event_type = "message"
                    data_buf: list[str] = []

                    for line in response.iter_lines():
                        if line.startswith("event:"):
                            event_type = line[len("event:"):].strip()

                        elif line.startswith("data:"):
                            data_buf.append(line[len("data:"):].strip())

                        elif line.startswith(":"):
                            pass  # keepalive — ignore

                        elif line == "":
                            if data_buf:
                                raw      = "\n".join(data_buf)
                                data_buf = []

                                if event_type == "connected":
                                    print(f"  {GREEN}✓ Connected to SSE stream{RESET}\n")

                                elif event_type == "notification":
                                    try:
                                        payload = json.loads(raw)
                                        total  += 1
                                        print_notification(payload)
                                    except json.JSONDecodeError:
                                        print(f"  {YELLOW}⚠ Could not parse: {raw}{RESET}")

                            event_type = "message"

        except httpx.ConnectError:
            print(f"\r  {RED}✕ Cannot connect to {base_url} — is the server running? Retrying in 3s...{RESET}")
            time.sleep(3)

        except httpx.RemoteProtocolError:
            print(f"\r  {YELLOW}⚠ Connection closed. Reconnecting...{RESET}")
            time.sleep(1)

        except Exception as e:
            print(f"\r  {RED}✕ Error: {e}. Retrying in 3s...{RESET}")
            time.sleep(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="🔔 True SSE webhook CLI monitor — zero polling.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python notify.py
  uv run python notify.py --url http://localhost:8001
        """,
    )
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL of the FastAPI server (default: http://localhost:8000)",
    )
    args = parser.parse_args()
    run(args.url)
