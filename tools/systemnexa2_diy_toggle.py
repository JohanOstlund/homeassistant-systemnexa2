
#!/usr/bin/env python3
"""
System Nexa 2 DIY mode toggler + config writer

Usage examples:
  # Enable DIY (disable cloud)
  python systemnexa2_diy_toggle.py --host 192.168.1.55 --token YOURTOKEN --enable

  # Disable DIY (re-enable cloud)
  python systemnexa2_diy_toggle.py --host 192.168.1.55 --disable

  # Enable DIY and write a Home Assistant config snippet (JSON)
  python systemnexa2_diy_toggle.py --host 192.168.1.55 --enable --write-config ./systemnexa2_config.json

Notes:
- The token header is optional; include it only if your device requires it.
- After enabling DIY mode, the Nexa cloud/app control is disabled and local HTTP API is used instead.
"""

import argparse
import json
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def http_json(method: str, url: str, headers: dict | None = None, data: dict | None = None, timeout: int = 8):
    body = None
    req_headers = headers.copy() if headers else {}
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        req_headers["Content-Type"] = "application/json"
    req = Request(url, data=body, headers=req_headers, method=method)
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            try:
                return json.loads(raw.decode("utf-8"))
            except Exception:
                return raw.decode("utf-8", errors="replace")
    except HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} for {url}: {e.read().decode('utf-8', errors='replace')}")
    except URLError as e:
        raise RuntimeError(f"Network error for {url}: {e}")

def main():
    p = argparse.ArgumentParser(description="Toggle DIY mode on System Nexa 2 and write HA config snippet.")
    p.add_argument("--host", required=True, help="Device IP or hostname, e.g. 192.168.1.55")
    p.add_argument("--token", default="", help="Optional token header value")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--enable", action="store_true", help="Enable DIY mode (disable cloud)")
    mode.add_argument("--disable", action="store_true", help="Disable DIY mode (enable cloud)")
    p.add_argument("--write-config", default="", help="Path to write a JSON config snippet for the HA custom component")
    args = p.parse_args()

    base = f"http://{args.host.strip('/')}/"
    headers = {}
    if args.token:
        headers["token"] = args.token

    desired = 1 if args.enable else 0
    payload = {"disable_cloud": desired}
    print(f"[i] POST {base}settings  payload={payload} headers={'token set' if args.token else 'no token'}")
    resp = http_json("POST", base + "settings", headers=headers, data=payload)
    print("[i] settings response:", resp)

    time.sleep(0.5)

    try:
        state = http_json("GET", base + "state", headers=headers)
        print("[i] state response:", state)
    except Exception as e:
        print("[!] Could not read /state:", e)

    if args.write_config:
        conf = {
            "host": args.host,
            "token": args.token,
            "poll_interval": 10,
            "name": "WPD-01"
        }
        with open(args.write_config, "w", encoding="utf-8") as f:
            json.dump(conf, f, indent=2, ensure_ascii=False)
        print(f"[i] Wrote Home Assistant config snippet to: {args.write_config}")
        print(json.dumps(conf, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
