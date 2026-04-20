#!/usr/bin/env python3
"""
Anonymize raw CSV datasets for public release.

Replaces `client_ip` with HMAC-SHA256(IP, salt) and converts `timestamp`
to seconds elapsed from the minimum timestamp in the file. The salt is
generated once per run and discarded, so hashes are not reversible but
same-IP rows remain linkable within a single release.

Usage:
    python3 anonymize.py <input.csv> <output.csv>
"""

import csv
import hashlib
import hmac
import os
import secrets
import sys


def anonymize(src_path: str, dst_path: str) -> None:
    salt = secrets.token_bytes(32)
    with open(src_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fields = reader.fieldnames or []

    timestamps = [float(r["timestamp"]) for r in rows if r.get("timestamp")]
    t0 = min(timestamps) if timestamps else 0.0

    out_fields = ["t_rel"] + [f for f in fields if f != "timestamp"]
    with open(dst_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        for r in rows:
            if "timestamp" in r and r["timestamp"]:
                r["t_rel"] = f"{float(r['timestamp']) - t0:.3f}"
            if "client_ip" in r and r["client_ip"]:
                digest = hmac.new(salt, r["client_ip"].encode(), hashlib.sha256).hexdigest()
                r["client_ip"] = "ip_" + digest[:16]
            r.pop("timestamp", None)
            writer.writerow({k: r.get(k, "") for k in out_fields})
    print(f"wrote {dst_path} ({len(rows)} rows)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: anonymize.py <input.csv> <output.csv>")
    anonymize(sys.argv[1], sys.argv[2])
