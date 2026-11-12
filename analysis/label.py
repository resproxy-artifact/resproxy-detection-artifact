#!/usr/bin/env python3
"""
Attach ground-truth labels to extracted connections.

The experiment servers ran nginx -> Flask, and Flask logged every request with
its query parameters (`?src=`, `?proto=`, `?country=`) into SQLite. Because
Flask sits behind nginx, the recorded src_port is nginx's ephemeral port, not
the client's -- so the join is (client_ip, nearest request time), greedy and
without reuse, exactly as the original analysis pipeline did.

Connections that do not match a logged request are dropped: the honeypots are
on the public Internet and their captures contain a large volume of unrelated
scanner traffic.
"""
import argparse, json, sqlite3, sys
from collections import defaultdict, Counter

# param_src -> (class, family). class is what the detector is evaluated against.
#   direct        : no intermediary
#   resproxy      : commercial residential proxy (the detection target)
#   benign_tunnel : a relay that is not residential-proxy abuse
#   vpn           : IP-layer tunnel (must NOT be flagged)
LABELS = {
    "direct":        ("direct", "direct"),
    "scope_direct":  ("direct", "direct"),
    "vpn_direct_n100": ("direct", "direct"),
    "scope_vpn":     ("vpn", "vpn"),
    "vpn_n100":      ("vpn", "vpn"),
    "scope_tor":     ("benign_tunnel", "tor"),
    "scope_squid":   ("benign_tunnel", "squid"),
    "scope_labproxy": ("benign_tunnel", "labproxy"),
    "labproxy":      ("benign_tunnel", "labproxy"),
}
RESPROXY = ("brightdata", "soax", "iproyal", "oxylabs", "netnut",
            "oxylabs_isp", "oxylabs_mobile", "bd_mobile", "bd_isp",
            "scope_brightdata", "packetstream", "honeygain")


def classify(param_src):
    if not param_src:
        return None, None
    s = param_src.strip()
    if s in LABELS:
        return LABELS[s]
    low = s.lower()
    if low.startswith("direct"):
        return "direct", low.replace("direct_", "") or "direct"
    for p in RESPROXY:
        if low.startswith(p):
            return "resproxy", low
    return "other", low


def load_requests(db_paths):
    rows = []
    for p in db_paths:
        try:
            db = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
            db.row_factory = sqlite3.Row
            cur = db.execute(
                "select src_ip, epoch, param_src, param_proto, param_country,"
                " user_agent from requests where param_src is not null")
            rows.extend(dict(r) for r in cur)
            db.close()
        except Exception as e:
            print(f"  ! {p}: {e}", file=sys.stderr)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conns", required=True, help="extracted .jsonl")
    ap.add_argument("--db", nargs="+", required=True)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--window", type=float, default=10.0,
                    help="max |pcap_ts - request_epoch| seconds")
    a = ap.parse_args()

    conns = [json.loads(l) for l in open(a.conns)]
    reqs = load_requests(a.db)
    by_ip = defaultdict(list)
    for r in reqs:
        if r["src_ip"]:
            by_ip[r["src_ip"]].append(r)
    for v in by_ip.values():
        v.sort(key=lambda r: r["epoch"])

    used = set()
    n_lab = 0
    cls_count, fam_count = Counter(), Counter()
    with open(a.out, "w") as w:
        for c in sorted(conns, key=lambda z: z.get("first_ts") or 0):
            ts = c.get("first_ts")
            cand = by_ip.get(c["client_ip"], [])
            best, bestd = None, a.window
            for i, r in enumerate(cand):
                if (c["client_ip"], i) in used:
                    continue
                d = abs(r["epoch"] - (ts or 0))
                if d < bestd:
                    bestd, best = d, i
            if best is None:
                continue
            used.add((c["client_ip"], best))
            r = cand[best]
            cls, fam = classify(r["param_src"])
            if cls is None:
                continue
            c["label_class"] = cls
            c["label_family"] = fam
            c["param_src"] = r["param_src"]
            c["param_proto"] = r["param_proto"]
            c["param_country"] = r["param_country"]
            c["user_agent"] = r["user_agent"]
            c["match_dt"] = round(bestd, 4)
            w.write(json.dumps(c) + "\n")
            n_lab += 1
            cls_count[cls] += 1
            fam_count[fam] += 1

    print(f"{a.conns}: {len(conns)} conns -> {n_lab} labeled", file=sys.stderr)
    print(f"  class : {dict(cls_count)}", file=sys.stderr)
    print(f"  family: {dict(fam_count.most_common(12))}", file=sys.stderr)


if __name__ == "__main__":
    main()
