#!/usr/bin/env python3
# ip_intelligence.py — dorukcodes

import argparse
import json
import socket
import sys
import requests

# renkler
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

BANNER = f"""
{CYAN}
╔══════════════════════════════════════╗
║       IP INTELLIGENCE TOOL           ║
║       github.com/dorukcodes          ║
╚══════════════════════════════════════╝
{RESET}
"""

API_URL = "http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,org,as,query,proxy,hosting"

HEADERS = {
    "User-Agent": "dorukcodes-intel-tool"
}


def resolve_ip(target):
    try:
        socket.inet_aton(target)
        return target
    except:
        pass

    try:
        return socket.gethostbyname(target)
    except:
        return None


def get_info(ip):
    try:
        r = requests.get(API_URL.format(ip=ip), timeout=5, headers=HEADERS)
        return r.json()
    except:
        print(f"{RED}[!] API error{RESET}")
        sys.exit(1)


def print_box(title, value):
    print(f"{MAGENTA}➤ {title:<12}{RESET}: {GREEN}{value}{RESET}")


def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description="IP Intelligence Tool — dorukcodes")
    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    target = args.target.strip().lower().replace("http://", "").replace("https://", "").rstrip("/")

    print(f"{CYAN}[*] Resolving {target}...{RESET}")
    ip = resolve_ip(target)

    if not ip:
        print(f"{RED}[!] Domain çözülemedi{RESET}")
        return

    print(f"{CYAN}[*] Fetching info for {ip}...{RESET}\n")
    data = get_info(ip)

    if data.get("status") != "success":
        print(f"{RED}[!] API error: {data.get('message')}{RESET}")
        return

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print(f"{'═'*42}")

    print_box("Target", target)
    print_box("IP", ip)
    print_box("Country", data.get("country"))
    print_box("Region", data.get("regionName"))
    print_box("City", data.get("city"))
    print_box("ISP", data.get("isp"))
    print_box("Org", data.get("org"))
    print_box("AS", data.get("as"))

    print(f"{'═'*42}")

    # risk
    if data.get("proxy") or data.get("hosting"):
        print(f"{YELLOW}⚠ Risk: Proxy / Hosting (dikkat){RESET}")
    else:
        print(f"{GREEN}✔ Risk: Normal{RESET}")

    print(f"{'═'*42}\n")


if __name__ == "__main__":
    main()
