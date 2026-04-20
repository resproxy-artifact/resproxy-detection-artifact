#!/usr/bin/env python3
"""Create RIPE Atlas TLS measurement to direct.dns-insight.com."""

import json
import sys
import time
import requests
from pathlib import Path

try:
    from load_env import RIPE_ATLAS_API_KEY, CONFIG
    API_KEY = RIPE_ATLAS_API_KEY
    TARGET = CONFIG["server"]["domain_direct"]
except ImportError:
    CREDS = json.loads((Path(__file__).parent / "providers.json").read_text())
    API_KEY = CREDS["ripe_atlas"]["api_key"]
    TARGET = CREDS["server"]["domain_direct"]

API_BASE = "https://atlas.ripe.net/api/v2"


def create_measurement():
    """Create a TLS (sslcert) measurement from global probes."""
    payload = {
        "definitions": [
            {
                "type": "sslcert",
                "af": 4,
                "target": TARGET,
                "port": 443,
                "description": f"TLS measurement to {TARGET} for rproxy-detection research",
                "resolve_on_probe": True,
            }
        ],
        "probes": [
            {
                "type": "area",
                "value": "WW",
                "requested": 100,
                "tags": {"include": ["system-ipv4-works"], "exclude": ["system-anchor"]},
            }
        ],
        "is_oneoff": True,
    }

    print(f"Creating RIPE Atlas sslcert measurement to {TARGET}...")
    print(f"Requesting 100 probes worldwide")

    resp = requests.post(
        f"{API_BASE}/measurements/",
        json=payload,
        headers={"Authorization": f"Key {API_KEY}", "Content-Type": "application/json"},
    )

    if resp.status_code in (200, 201):
        result = resp.json()
        msm_id = result["measurements"][0]
        print(f"Measurement created: ID={msm_id}")
        print(f"URL: https://atlas.ripe.net/measurements/{msm_id}/")
        save_measurement_info(msm_id)
        return msm_id
    else:
        print(f"ERROR: {resp.status_code}")
        print(resp.text)
        sys.exit(1)


def check_measurement(msm_id):
    """Check measurement status."""
    resp = requests.get(f"{API_BASE}/measurements/{msm_id}/")
    if resp.status_code == 200:
        data = resp.json()
        status = data.get("status", {})
        print(f"Measurement {msm_id}: {status.get('name', 'unknown')}")
        print(f"  Probes requested: {data.get('probes_requested', '?')}")
        print(f"  Participants: {data.get('participant_count', '?')}")
        return status.get("id")
    return None


def fetch_results(msm_id):
    """Fetch measurement results."""
    resp = requests.get(f"{API_BASE}/measurements/{msm_id}/results/")
    if resp.status_code == 200:
        results = resp.json()
        outfile = Path(__file__).parent.parent / "data" / "ripe_atlas" / f"msm_{msm_id}.json"
        outfile.parent.mkdir(parents=True, exist_ok=True)
        outfile.write_text(json.dumps(results, indent=2))
        print(f"Results saved: {outfile} ({len(results)} probes)")
        return results
    else:
        print(f"ERROR fetching results: {resp.status_code}")
        return None


def save_measurement_info(msm_id):
    outfile = Path(__file__).parent.parent / "data" / "ripe_atlas" / "ripe_atlas_measurements.json"
    outfile.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if outfile.exists():
        existing = json.loads(outfile.read_text())
    existing.append({
        "measurement_id": msm_id,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "target": TARGET,
    })
    outfile.write_text(json.dumps(existing, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        msm_id = int(sys.argv[2])
        check_measurement(msm_id)
    elif len(sys.argv) > 1 and sys.argv[1] == "results":
        msm_id = int(sys.argv[2])
        fetch_results(msm_id)
    else:
        create_measurement()
