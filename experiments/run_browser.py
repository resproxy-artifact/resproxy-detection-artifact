#!/usr/bin/env python3
"""
Browser-based proxy experiment using Playwright.
Sends real Chrome traffic through residential proxies to capture:
1. Realistic User-Agent with OS info (for TCP fingerprint mismatch detection)
2. Full browser HTTP headers (Accept, Sec-CH-UA, etc.)
3. TLS ClientHello with browser-specific cipher suites (JA3/JA4)

Usage:
  python3 run_browser.py <provider> <protocol> <target> [--countries us,kr] [--n 5]
  python3 run_browser.py brightdata http_connect direct --n 5
  python3 run_browser.py soax socks5 direct --countries us,kr,de --n 10
  python3 run_browser.py direct none direct --n 10   # direct baseline with browser
"""

import argparse
import json
import time
import random
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

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


def build_proxy_config(provider_name, protocol, country):
    """Build Playwright proxy config dict."""
    if provider_name == "direct":
        return None

    p = PROVIDERS[provider_name]
    if protocol == "socks5" and p.get("socks5_port") is None:
        return None

    username = p["username"]
    password = p["password"]
    fmt = p.get("country_format", "-country-{country}")
    if p.get("country_mode") == "username_suffix":
        username = username + fmt.format(country=country)
    elif p.get("country_mode") == "password_suffix":
        password = password + fmt.format(country=country)
    host = p["host"]

    if protocol == "socks5":
        port = p["socks5_port"]
        server = f"socks5://{host}:{port}"
    else:
        port = p["http_connect_port"]
        server = f"http://{host}:{port}"

    return {"server": server, "username": username, "password": password}


def run_browser_request(playwright, proxy_config, url, ua_profile="windows_chrome",
                        timeout_ms=60000):
    """Launch browser, navigate to URL, return response data.

    ua_profile controls the spoofed User-Agent and Client Hints:
    - "windows_chrome": Windows 10 + Chrome (most common real-world scenario)
    - "macos_chrome": macOS + Chrome
    - "windows_firefox": Windows 10 + Firefox
    - "native": use Playwright's default (Linux headless)
    """
    UA_PROFILES = {
        "windows_chrome": {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec_ch_ua_platform": '"Windows"',
            "sec_ch_ua_mobile": "?0",
        },
        "macos_chrome": {
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "sec_ch_ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec_ch_ua_platform": '"macOS"',
            "sec_ch_ua_mobile": "?0",
        },
        "windows_firefox": {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "sec_ch_ua": None,
            "sec_ch_ua_platform": None,
            "sec_ch_ua_mobile": None,
        },
        "native": {
            "user_agent": None,
            "sec_ch_ua": None,
            "sec_ch_ua_platform": None,
            "sec_ch_ua_mobile": None,
        },
    }

    profile = UA_PROFILES.get(ua_profile, UA_PROFILES["windows_chrome"])

    launch_args = {"headless": True}
    if proxy_config:
        launch_args["proxy"] = proxy_config

    browser = None
    try:
        browser = playwright.chromium.launch(**launch_args)

        context_args = {
            "viewport": {"width": 1920, "height": 1080},
            "locale": "en-US",
        }
        if profile["user_agent"]:
            context_args["user_agent"] = profile["user_agent"]

        # Set extra HTTP headers for Client Hints
        extra_headers = {}
        if profile.get("sec_ch_ua"):
            extra_headers["Sec-CH-UA"] = profile["sec_ch_ua"]
        if profile.get("sec_ch_ua_platform"):
            extra_headers["Sec-CH-UA-Platform"] = profile["sec_ch_ua_platform"]
        if profile.get("sec_ch_ua_mobile"):
            extra_headers["Sec-CH-UA-Mobile"] = profile["sec_ch_ua_mobile"]
        if extra_headers:
            context_args["extra_http_headers"] = extra_headers

        context = browser.new_context(**context_args)
        page = context.new_page()

        start = time.time()
        response = page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
        elapsed = time.time() - start

        status = response.status if response else 0
        body = page.content()

        # Try to extract JSON response
        try:
            import re
            json_match = re.search(r'\{.*\}', body, re.DOTALL)
            if json_match:
                resp_data = json.loads(json_match.group())
            else:
                resp_data = {}
        except (json.JSONDecodeError, AttributeError):
            resp_data = {}

        return {
            "http_code": str(status),
            "time_total": f"{elapsed:.3f}",
            "your_ip": resp_data.get("your_ip", ""),
            "error": "",
        }
    except Exception as e:
        return {
            "http_code": "000",
            "time_total": "0",
            "your_ip": "",
            "error": str(e)[:200],
        }
    finally:
        if browser:
            browser.close()


def run_experiment(provider_name, protocol, target, countries, n_requests,
                   sleep_range=(3, 5), dry_run=False, ua_profile="windows_chrome"):
    """Run browser experiment."""
    target_domain = SERVER["domain_cf"] if target == "cf" else SERVER["domain_direct"]

    if provider_name != "direct" and provider_name not in PROVIDERS:
        print(f"ERROR: Unknown provider '{provider_name}'")
        return

    if provider_name != "direct":
        p = PROVIDERS[provider_name]
        if p["username"].endswith("_USER"):
            print(f"SKIP: {provider_name} credentials not configured")
            return
        arch = p.get("architecture", "unknown")
    else:
        arch = "direct"

    print(f"\n{'='*70}")
    print(f"BROWSER EXPERIMENT")
    print(f"Provider: {provider_name} ({arch})")
    print(f"Protocol: {protocol}")
    print(f"Target: {target_domain}")
    print(f"Countries: {', '.join(countries)}")
    print(f"Requests/country: {n_requests}")
    print(f"UA Profile: {ua_profile}")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print(f"{'='*70}\n")

    log_dir = SCRIPT_DIR.parent / "data" / "experiment_logs" / provider_name
    log_dir.mkdir(parents=True, exist_ok=True)
    ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"browser_{provider_name}_{protocol}_{target}_{ts_str}.csv"

    total = 0
    success = 0

    with sync_playwright() as pw:
        with open(log_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "provider", "architecture", "country",
                             "protocol", "target", "seq", "http_code", "time_total",
                             "your_ip", "error"])

            for country in countries:
                print(f"--- {country} ---")

                for i in range(1, n_requests + 1):
                    ts = str(int(time.time() * 1000))
                    url = (f"https://{target_domain}/?src={provider_name}"
                           f"&proto={protocol}&country={country}"
                           f"&n={i}&ts={ts}&client=playwright_chrome")

                    if dry_run:
                        print(f"  [DRY RUN] {country}/{i}")
                        continue

                    proxy_config = build_proxy_config(provider_name, protocol, country)
                    result = run_browser_request(pw, proxy_config, url,
                                                 ua_profile=ua_profile)

                    row = [ts, provider_name, arch, country, protocol, target,
                           i, result["http_code"], result["time_total"],
                           result["your_ip"], result["error"]]
                    writer.writerow(row)
                    f.flush()

                    total += 1
                    if result["http_code"] == "200":
                        success += 1

                    status = "OK" if result["http_code"] == "200" else f"ERR:{result['http_code']}"
                    err = f" ({result['error'][:50]})" if result["error"] else ""
                    print(f"  {country}/{i:>2}: {status} {result['time_total']}s "
                          f"ip={result['your_ip']}{err}")

                    sleep_time = random.uniform(*sleep_range)
                    time.sleep(sleep_time)

    print(f"\n{'='*70}")
    print(f"Complete: {success}/{total} successful")
    print(f"Log: {log_file}")
    print(f"Finished: {datetime.now(timezone.utc).isoformat()}")


def main():
    parser = argparse.ArgumentParser(description="Browser proxy experiment (Playwright)")
    parser.add_argument("provider", help="Provider name or 'direct'")
    parser.add_argument("protocol", help="http_connect, socks5, or 'none' (for direct)")
    parser.add_argument("target", help="direct or cf")
    parser.add_argument("--countries", default=None)
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--ua", default="windows_chrome",
                        choices=["windows_chrome", "macos_chrome", "windows_firefox", "native"],
                        help="User-Agent profile to spoof")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.countries:
        countries = args.countries.split(",")
    elif args.provider == "direct":
        countries = ["local"]
    elif args.target == "cf":
        countries = CF_COUNTRIES
    else:
        countries = DEFAULT_COUNTRIES

    run_experiment(args.provider, args.protocol, args.target, countries, args.n,
                   dry_run=args.dry_run, ua_profile=args.ua)


if __name__ == "__main__":
    main()
