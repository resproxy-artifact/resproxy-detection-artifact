#!/usr/bin/env python3
"""
Universal proxy experiment runner for all providers.

Usage:
  python3 run_proxy.py <provider> <protocol> <target> [--countries us,kr,...] [--n 20] [--dry-run]

Examples:
  python3 run_proxy.py brightdata http_connect direct
  python3 run_proxy.py oxylabs socks5 direct --countries us,kr,de --n 10
  python3 run_proxy.py netnut http_connect cf
  python3 run_proxy.py all http_connect direct        # run all providers
  python3 run_proxy.py all all direct                  # all providers, all protocols
"""

import argparse
import json
import subprocess
import sys
import time
import random
import csv
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
try:
    from load_env import PROVIDERS, CONFIG
    SERVER = CONFIG["server"]
except ImportError:
    CREDS = json.loads((SCRIPT_DIR / "providers.json").read_text())
    PROVIDERS = CREDS["providers"]
    SERVER = CREDS["server"]

DEFAULT_COUNTRIES = ["us", "kr", "de", "jp", "br", "gb", "au", "in", "sg", "fr"]
CF_COUNTRIES = ["us", "kr", "de", "jp", "br"]


def build_proxy_url(provider_name, protocol, country):
    """Build proxy URL for a given provider/protocol/country."""
    p = PROVIDERS[provider_name]

    if protocol == "socks5" and p.get("socks5_port") is None:
        return None  # provider doesn't support SOCKS5

    username = p["username"]
    password = p["password"]
    host = p["host"]

    # Add country to username or password
    fmt = p.get("country_format", "-country-{country}")
    if p.get("country_mode") == "username_suffix":
        username = username + fmt.format(country=country)
    elif p.get("country_mode") == "password_suffix":
        password = password + fmt.format(country=country)

    if protocol == "socks5":
        port = p["socks5_port"]
        return f"socks5h://{username}:{password}@{host}:{port}"
    else:
        port = p["http_connect_port"]
        return f"http://{username}:{password}@{host}:{port}"


def send_request(proxy_url, target_domain, provider, protocol, country, seq, ts):
    """Send a single request through the proxy."""
    url = (f"https://{target_domain}/?src={provider}&proto={protocol}"
           f"&country={country}&n={seq}&ts={ts}")

    cmd = [
        "curl", "-s", "-o", "/dev/null",
        "-w", "%{http_code},%{time_total},%{remote_ip}",
        "--proxy", proxy_url,
        "--connect-timeout", "30",
        "--max-time", "60",
        url,
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=65)
        parts = result.stdout.strip().split(",")
        return {
            "http_code": parts[0] if len(parts) > 0 else "000",
            "time_total": parts[1] if len(parts) > 1 else "0",
            "exit_ip": parts[2] if len(parts) > 2 else "error",
        }
    except (subprocess.TimeoutExpired, Exception) as e:
        return {"http_code": "000", "time_total": "0", "exit_ip": f"error:{e}"}


def run_experiment(provider_name, protocol, target, countries, n_requests,
                   sleep_range=(2, 3), dry_run=False, domain_override=None):
    """Run experiment for one provider/protocol/target combination."""
    if domain_override:
        target_domain = domain_override
    else:
        target_domain = SERVER["domain_cf"] if target == "cf" else SERVER["domain_direct"]

    if provider_name not in PROVIDERS:
        print(f"ERROR: Unknown provider '{provider_name}'")
        print(f"Available: {', '.join(PROVIDERS.keys())}")
        return False

    p = PROVIDERS[provider_name]
    arch = p.get("architecture", "unknown")

    if protocol == "socks5" and p.get("socks5_port") is None:
        print(f"SKIP: {provider_name} does not support SOCKS5")
        return False

    # Check if credentials are placeholder
    if p["username"].endswith("_USER"):
        print(f"SKIP: {provider_name} credentials not configured (placeholder)")
        return False

    print(f"\n{'='*70}")
    print(f"Provider: {provider_name} ({arch})")
    print(f"Protocol: {protocol}")
    print(f"Target: {target_domain}")
    print(f"Countries: {', '.join(countries)}")
    print(f"Requests/country: {n_requests}")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print(f"{'='*70}\n")

    # Log file
    log_dir = SCRIPT_DIR.parent / "data" / "experiment_logs" / provider_name
    log_dir.mkdir(parents=True, exist_ok=True)
    ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Include server region in filename if using domain override
    server_tag = ""
    if domain_override:
        # Extract region from domain: direct-ap.example.com -> ap
        parts = domain_override.split(".")
        if parts[0].startswith("direct-"):
            server_tag = f"_{parts[0].replace('direct-', '')}"
        else:
            server_tag = f"_{parts[0]}"
    log_file = log_dir / f"{provider_name}_{protocol}_{target}{server_tag}_{ts_str}.csv"

    total = 0
    success = 0

    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "provider", "architecture", "country",
                         "protocol", "target", "server", "seq", "http_code", "time_total", "exit_ip"])

        for country in countries:
            print(f"--- {country} ---")
            proxy_url = build_proxy_url(provider_name, protocol, country)
            if proxy_url is None:
                print(f"  Cannot build proxy URL, skipping")
                continue

            for i in range(1, n_requests + 1):
                ts = str(int(time.time() * 1000))

                if dry_run:
                    print(f"  [DRY RUN] {country}/{i}: {proxy_url[:60]}...")
                    continue

                result = send_request(
                    proxy_url, target_domain,
                    provider_name, protocol, country, i, ts,
                )

                row = [ts, provider_name, arch, country, protocol, target,
                       target_domain, i, result["http_code"], result["time_total"], result["exit_ip"]]
                writer.writerow(row)
                f.flush()

                total += 1
                if result["http_code"] == "200":
                    success += 1

                status = "OK" if result["http_code"] == "200" else f"ERR:{result['http_code']}"
                print(f"  {country}/{i:>2}: {status} {result['time_total']}s "
                      f"exit={result['exit_ip']}")

                sleep_time = random.uniform(*sleep_range)
                time.sleep(sleep_time)

    print(f"\n{'='*70}")
    print(f"Complete: {success}/{total} successful")
    print(f"Log: {log_file}")
    print(f"Finished: {datetime.now(timezone.utc).isoformat()}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Universal proxy experiment runner")
    parser.add_argument("provider", help="Provider name or 'all'")
    parser.add_argument("protocol", help="http_connect, socks5, or 'all'")
    parser.add_argument("target", help="direct or cf")
    parser.add_argument("--countries", default=None,
                        help="Comma-separated country codes (default: 10 countries)")
    parser.add_argument("--n", type=int, default=20, help="Requests per country")
    parser.add_argument("--domain", default=None,
                        help="Override target domain (e.g., direct-ap.example.com)")
    parser.add_argument("--sleep-min", type=float, default=2)
    parser.add_argument("--sleep-max", type=float, default=3)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Determine countries
    if args.countries:
        countries = args.countries.split(",")
    elif args.target == "cf":
        countries = CF_COUNTRIES
    else:
        countries = DEFAULT_COUNTRIES

    # Determine providers
    if args.provider == "all":
        provider_list = list(PROVIDERS.keys())
    else:
        provider_list = [args.provider]

    # Determine protocols
    if args.protocol == "all":
        protocol_list = ["http_connect", "socks5"]
    else:
        protocol_list = [args.protocol]

    # Run
    for provider in provider_list:
        for protocol in protocol_list:
            run_experiment(
                provider, protocol, args.target, countries, args.n,
                sleep_range=(args.sleep_min, args.sleep_max),
                dry_run=args.dry_run,
                domain_override=args.domain,
            )


if __name__ == "__main__":
    main()
