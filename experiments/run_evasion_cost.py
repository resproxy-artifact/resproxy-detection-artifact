#!/usr/bin/env python3
"""
Speculative buffering evasion cost experiment.
Tests failure scenarios and measures error behavior differences
between normal and speculative CONNECT proxies.
"""

import subprocess
import random
import json
import csv
import time
import sys
from datetime import datetime, timezone
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent / "data" / "experiment_logs" / "evasion"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

NORMAL_PORT = 8888
SPECULATIVE_PORT = 8889
PROXY_HOST = "127.0.0.1"


def curl_request(proxy_port, url, timeout=10):
    """Send request through proxy, return detailed result."""
    start = time.time()
    try:
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null",
             "-w", "%{http_code}|%{time_total}|%{exitcode}|%{ssl_verify_result}",
             "--connect-timeout", str(timeout),
             "--max-time", str(timeout + 5),
             "--proxy", f"http://{PROXY_HOST}:{proxy_port}",
             url],
            capture_output=True, text=True, timeout=timeout + 10,
        )
        elapsed = time.time() - start
        parts = result.stdout.strip().split("|")
        return {
            "http_code": parts[0] if len(parts) > 0 else "000",
            "time_total": parts[1] if len(parts) > 1 else "0",
            "curl_exit": result.returncode,
            "stderr": result.stderr.strip()[:300],
            "elapsed": round(elapsed, 3),
        }
    except subprocess.TimeoutExpired:
        return {
            "http_code": "000",
            "time_total": "0",
            "curl_exit": 28,
            "stderr": "timeout",
            "elapsed": round(time.time() - start, 3),
        }
    except Exception as e:
        return {
            "http_code": "000",
            "time_total": "0",
            "curl_exit": -1,
            "stderr": str(e)[:300],
            "elapsed": round(time.time() - start, 3),
        }


def run_scenario_tests():
    """Experiment 1: Test specific failure scenarios."""
    print("=" * 70)
    print("EXPERIMENT 1: FAILURE SCENARIO TESTS")
    print("=" * 70)

    scenarios = {
        "normal_target": "https://direct.dns-insight.com/?scenario=normal&ts={}",
        "dns_failure": "https://nonexistent-domain-xyz-{}.com/",
        "conn_refused": "https://direct.dns-insight.com:9999/?scenario=refused",
    }

    N = 30
    results = []

    for scenario_name, url_template in scenarios.items():
        print(f"\n--- Scenario: {scenario_name} ---")

        for variant, port in [("normal", NORMAL_PORT), ("speculative", SPECULATIVE_PORT)]:
            successes = 0
            errors = []

            for i in range(1, N + 1):
                if scenario_name == "dns_failure":
                    url = url_template.format(random.randint(10000, 99999))
                else:
                    url = url_template.format(int(time.time() * 1000))

                r = curl_request(port, url, timeout=8)

                is_success = r["http_code"] == "200"
                if is_success:
                    successes += 1

                results.append({
                    "scenario": scenario_name,
                    "variant": variant,
                    "seq": i,
                    "http_code": r["http_code"],
                    "curl_exit": r["curl_exit"],
                    "elapsed": r["elapsed"],
                    "stderr_snippet": r["stderr"][:100],
                })

                time.sleep(0.3)

            rate = successes / N * 100
            avg_time = sum(r["elapsed"] for r in results[-N:]) / N
            print(f"  {variant:>12}: {successes}/{N} success ({rate:.0f}%), avg {avg_time:.1f}s")

    # Write CSV
    out = LOGS_DIR / "evasion_failure_scenarios.csv"
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved: {out}")
    return results


def run_batch_test():
    """Experiment 2: Batch failure rate with mixed traffic."""
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: BATCH FAILURE RATE (500 requests)")
    print("=" * 70)

    targets = {
        "normal": "https://direct.dns-insight.com/?batch=1&ts={}",
        "dns_fail": "https://nonexistent-xyz-{}.com/",
        "conn_refuse": "https://direct.dns-insight.com:9999/",
    }

    N = 500
    results = []

    for i in range(N):
        # 90% normal, 10% failure
        if random.random() < 0.9:
            scenario = "normal"
            url = targets["normal"].format(int(time.time() * 1000))
        else:
            scenario = random.choice(["dns_fail", "conn_refuse"])
            if scenario == "dns_fail":
                url = targets["dns_fail"].format(random.randint(10000, 99999))
            else:
                url = targets["conn_refuse"]

        for variant, port in [("normal", NORMAL_PORT), ("speculative", SPECULATIVE_PORT)]:
            r = curl_request(port, url, timeout=8)
            results.append({
                "i": i,
                "scenario": scenario,
                "variant": variant,
                "http_code": r["http_code"],
                "curl_exit": r["curl_exit"],
                "elapsed": r["elapsed"],
            })

        if (i + 1) % 100 == 0:
            print(f"  {i + 1}/{N} done")

        time.sleep(0.3)

    # Write CSV
    out = LOGS_DIR / "evasion_batch_results.csv"
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved: {out}")
    return results


def run_client_error_test():
    """Experiment 3: Error behavior across different clients."""
    print("\n" + "=" * 70)
    print("EXPERIMENT 3: CLIENT ERROR BEHAVIOR")
    print("=" * 70)

    test_url = "https://nonexistent-domain-xyz-99999.com/"
    results = []

    # curl
    for variant, port in [("normal", NORMAL_PORT), ("speculative", SPECULATIVE_PORT)]:
        r = curl_request(port, test_url, timeout=8)
        results.append({
            "client": "curl",
            "variant": variant,
            "http_code": r["http_code"],
            "curl_exit": r["curl_exit"],
            "elapsed": r["elapsed"],
            "error_msg": r["stderr"][:200],
        })
        print(f"  curl/{variant}: exit={r['curl_exit']} code={r['http_code']} {r['elapsed']}s")
        print(f"    error: {r['stderr'][:100]}")

    # Python requests
    for variant, port in [("normal", NORMAL_PORT), ("speculative", SPECULATIVE_PORT)]:
        start = time.time()
        try:
            import requests
            proxies = {"https": f"http://{PROXY_HOST}:{port}"}
            resp = requests.get(test_url, proxies=proxies, timeout=8)
            elapsed = time.time() - start
            results.append({
                "client": "python_requests",
                "variant": variant,
                "http_code": str(resp.status_code),
                "curl_exit": 0,
                "elapsed": round(elapsed, 3),
                "error_msg": "",
            })
            print(f"  requests/{variant}: {resp.status_code} {elapsed:.1f}s")
        except Exception as e:
            elapsed = time.time() - start
            error_type = type(e).__name__
            results.append({
                "client": "python_requests",
                "variant": variant,
                "http_code": "000",
                "curl_exit": -1,
                "elapsed": round(elapsed, 3),
                "error_msg": f"{error_type}: {str(e)[:150]}",
            })
            print(f"  requests/{variant}: {error_type} {elapsed:.1f}s")
            print(f"    {str(e)[:100]}")

    # wget
    for variant, port in [("normal", NORMAL_PORT), ("speculative", SPECULATIVE_PORT)]:
        start = time.time()
        try:
            r = subprocess.run(
                ["wget", "-q", "-O", "/dev/null",
                 "-e", f"https_proxy=http://{PROXY_HOST}:{port}",
                 "--timeout=8", test_url],
                capture_output=True, text=True, timeout=15,
            )
            elapsed = time.time() - start
            results.append({
                "client": "wget",
                "variant": variant,
                "http_code": "000",
                "curl_exit": r.returncode,
                "elapsed": round(elapsed, 3),
                "error_msg": r.stderr.strip()[:200],
            })
            print(f"  wget/{variant}: exit={r.returncode} {elapsed:.1f}s")
            if r.stderr:
                print(f"    {r.stderr.strip()[:100]}")
        except subprocess.TimeoutExpired:
            elapsed = time.time() - start
            results.append({
                "client": "wget",
                "variant": variant,
                "http_code": "000",
                "curl_exit": 28,
                "elapsed": round(elapsed, 3),
                "error_msg": "timeout",
            })
            print(f"  wget/{variant}: timeout {elapsed:.1f}s")

    out = LOGS_DIR / "evasion_client_errors.csv"
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"\nSaved: {out}")
    return results


def print_summary(scenario_results, batch_results, client_results):
    """Print comprehensive summary."""
    print("\n" + "=" * 70)
    print("SUMMARY: EVASION COST ANALYSIS")
    print("=" * 70)

    # Scenario summary
    print(f"\n--- Failure Scenario Comparison ---")
    print(f"{'Scenario':<18} {'Normal Result':<25} {'Speculative Result':<25}")
    print("-" * 70)

    for scenario in ["normal_target", "dns_failure", "conn_refused"]:
        for variant in ["normal", "speculative"]:
            entries = [r for r in scenario_results
                       if r["scenario"] == scenario and r["variant"] == variant]
            if not entries:
                continue
            successes = sum(1 for e in entries if e["http_code"] == "200")
            avg_time = sum(e["elapsed"] for e in entries) / len(entries)
            # Most common exit code for failures
            fail_exits = [e["curl_exit"] for e in entries if e["http_code"] != "200"]
            common_exit = max(set(fail_exits), key=fail_exits.count) if fail_exits else 0

            if variant == "normal":
                normal_str = f"{successes}/{len(entries)} OK, {avg_time:.1f}s avg"
                if fail_exits:
                    normal_str += f", exit={common_exit}"
            else:
                spec_str = f"{successes}/{len(entries)} OK, {avg_time:.1f}s avg"
                if fail_exits:
                    spec_str += f", exit={common_exit}"

        print(f"{scenario:<18} {normal_str:<25} {spec_str:<25}")

    # Batch summary
    print(f"\n--- Batch Test (N=500, 90% normal / 10% failure) ---")
    for variant in ["normal", "speculative"]:
        entries = [r for r in batch_results if r["variant"] == variant]
        total = len(entries)
        success = sum(1 for e in entries if e["http_code"] == "200")
        fail = total - success
        avg_ok_time = 0
        avg_err_time = 0
        ok_entries = [e for e in entries if e["http_code"] == "200"]
        err_entries = [e for e in entries if e["http_code"] != "200"]
        if ok_entries:
            avg_ok_time = sum(e["elapsed"] for e in ok_entries) / len(ok_entries)
        if err_entries:
            avg_err_time = sum(e["elapsed"] for e in err_entries) / len(err_entries)

        print(f"  {variant:>12}: {success}/{total} success, "
              f"OK avg={avg_ok_time:.2f}s, ERR avg={avg_err_time:.2f}s")

    # Client error summary
    print(f"\n--- Client Error Behavior (DNS failure scenario) ---")
    print(f"{'Client':<18} {'Normal Error':<30} {'Speculative Error':<30}")
    print("-" * 80)

    clients = sorted(set(r["client"] for r in client_results))
    for client in clients:
        normal = [r for r in client_results if r["client"] == client and r["variant"] == "normal"]
        spec = [r for r in client_results if r["client"] == client and r["variant"] == "speculative"]
        n_str = f"exit={normal[0]['curl_exit']}, {normal[0]['elapsed']}s" if normal else "N/A"
        s_str = f"exit={spec[0]['curl_exit']}, {spec[0]['elapsed']}s" if spec else "N/A"
        print(f"{client:<18} {n_str:<30} {s_str:<30}")
        if spec and spec[0]["error_msg"]:
            print(f"{'':>18} → {spec[0]['error_msg'][:60]}")


def main():
    print(f"Start: {datetime.now(timezone.utc).isoformat()}")

    # Verify proxy is running
    r = curl_request(NORMAL_PORT, "https://direct.dns-insight.com/health", timeout=5)
    if r["http_code"] != "200":
        print(f"ERROR: Normal proxy not responding (code={r['http_code']})")
        print("Start lab proxy first: python3 experiments/lab_proxy.py &")
        sys.exit(1)

    scenario_results = run_scenario_tests()
    batch_results = run_batch_test()
    client_results = run_client_error_test()
    print_summary(scenario_results, batch_results, client_results)

    print(f"\nFinished: {datetime.now(timezone.utc).isoformat()}")


if __name__ == "__main__":
    main()
