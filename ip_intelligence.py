#!/usr/bin/env python3
# intel_tool.py — dorukcodes

import argparse
import json
import socket
import sys
import requests

# renkler
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

BANNER = f"""
╔══════════════════════════════════════╗
║       IP INTELLIGENCE TOOL           ║
║       github.com/dorukcodes          ║
╚══════════════════════════════════════╝
"""

API_URL = "https://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,isp,org,as,query,mobile,proxy,hosting"

HEADERS = {
    "User-Agent": "dorukcodes-intel-tool"
}


def resolve_to_ip(target):
    try:
        socket.inet_aton(target)
        return target
    except socket.error:
        pass

    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        return None


def fetch_intel(ip):
    try:
        resp = requests.get(API_URL.format(ip=ip), timeout=5, headers=HEADERS)
        resp.raise_for_status()
        return resp.json()
    except requests.Timeout:
        print(f"{RED}[!] Request timed out.{RESET}")
        sys.exit(1)
    except requests.RequestException as e:
        print(f"{RED}[!] API error: {e}{RESET}")
        sys.exit(1)


def risk_label(data):
    if data.get("proxy") or data.get("hosting"):
        return f"{YELLOW}Proxy / Hosting — dikkatli ol{RESET}"
    if data.get("mobile"):
        return "Mobil ağ"
    return f"{GREEN}Büyük ihtimalle normal{RESET}"


def print_results(target, ip, data):
    print(f"  {'─' * 42}")
    print(f"  Target      : {target}")
    print(f"{GREEN}  IP          : {ip}{RESET}")
    print(f"  Country     : {data.get('country', 'N/A')}")
    print(f"  Region      : {data.get('regionName', 'N/A')}")
    print(f"  City        : {data.get('city', 'N/A')}")
    print(f"  ISP         : {data.get('isp', 'N/A')}")
    print(f"  Org         : {data.get('org', 'N/A')}")
    print(f"  AS          : {data.get('as', 'N/A')}")
    print(f"  {'─' * 42}")

    flags = []
    if data.get("proxy"):  flags.append("proxy")
    if data.get("hosting"): flags.append("hosting")
    if data.get("mobile"):  flags.append("mobile")

    print(f"  Flags       : {', '.join(flags) if flags else 'none'}")
    print(f"  Assessment  : {risk_label(data)}")
    print(f"  {'─' * 42}\n")


def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="IP Intelligence Tool — dorukcodes"
    )
    parser.add_argument("-t", "--target", required=True, help="Domain veya IP")
    parser.add_argument("--json", action="store_true", help="Ham JSON çıktısı")
    args = parser.parse_args()

    target = args.target.strip().lower().replace("http://","").replace("https://","").rstrip("/")

    print(f"[*] Resolving {target}...")
    ip = resolve_to_ip(target)

    if not ip:
        print(f"{RED}[!] Domain çözülemedi{RESET}")
        sys.exit(1)

    print(f"[*] Fetching data for {ip}...\n")
    data = fetch_intel(ip)

    if data.get("status") == "fail":
        print(f"{RED}[!] API error: {data.get('message', 'unknown')}{RESET}")
        sys.exit(1)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print_results(target, ip, data)


if __name__ == "__main__":
    main()
