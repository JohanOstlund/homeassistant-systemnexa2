#!/usr/bin/env python3
import argparse
import requests
import sys

def set_diy_mode(host, port, enable):
    url = f"http://{host}:{port}/settings"
    payload = {"diy_mode": 1 if enable else 0, "store": 1}
    try:
        r = requests.post(url, json=payload, timeout=5)
        r.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Failed to set DIY mode: {e}")
        sys.exit(1)

def get_diy_status(host, port):
    url = f"http://{host}:{port}/settings"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        settings = r.json()
        return settings.get("diy_mode", 0)
    except Exception as e:
        print(f"[ERROR] Failed to read DIY status: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Toggle DIY mode on System Nexa 2 device")
    parser.add_argument("--host", required=True, help="Device IP address")
    parser.add_argument("--port", type=int, default=3000, help="Device API port (default 3000)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--enable", action="store_true", help="Enable DIY mode")
    group.add_argument("--disable", action="store_true", help="Disable DIY mode")
    args = parser.parse_args()

    if args.enable:
        set_diy_mode(args.host, args.port, True)
        status = get_diy_status(args.host, args.port)
        print("✅ DIY mode is now", "ENABLED" if status == 1 else "NOT ENABLED")
    elif args.disable:
        set_diy_mode(args.host, args.port, False)
        status = get_diy_status(args.host, args.port)
        print("✅ DIY mode is now", "DISABLED" if status == 0 else "STILL ENABLED")

if __name__ == "__main__":
    main()
