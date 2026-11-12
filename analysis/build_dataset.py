#!/usr/bin/env python3
"""
Merge all labeled connection files into one evaluation dataset.

Two label sources are combined:
  * DB-joined labels (label.py) for captures whose experiment logged
    `?src=` parameters to the server-side SQLite.
  * Provenance labels for the Experiment-D direct baselines, whose whole
    capture is one condition and whose per-IP OS mapping is fixed.

Emits one JSONL with a `label_class` in {direct, resproxy, benign_tunnel, vpn}
plus `label_family`, and prints the composition so the negative class size is
never quoted from memory.
"""
import argparse, json, os, sys
from collections import Counter

# client_ip -> (class, family) for captures labelled by provenance.
PROVENANCE = {
    "out/direct_v3.jsonl": {
        "<direct-linux-host>": ("direct", "linux"),
        "<direct-windows-host>": ("direct", "windows"),
    },
    "out/direct_macos.jsonl": {
        "<direct-macos-host>": ("direct", "macos"),
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labeled", nargs="*", default=[],
                    help="JSONL already carrying label_class (from label.py)")
    ap.add_argument("--provenance", nargs="*", default=[],
                    help="JSONL labelled by the PROVENANCE table")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    n = 0
    cls, fam, src = Counter(), Counter(), Counter()
    with open(a.out, "w") as w:
        for p in a.labeled:
            if not os.path.exists(p):
                print(f"  ! missing {p}", file=sys.stderr)
                continue
            for line in open(p):
                r = json.loads(line)
                if not r.get("label_class"):
                    continue
                w.write(json.dumps(r) + "\n")
                n += 1
                cls[r["label_class"]] += 1
                fam[r["label_family"]] += 1
                src[os.path.basename(p)] += 1
        for p in a.provenance:
            table = PROVENANCE.get(p) or PROVENANCE.get(os.path.normpath(p))
            if table is None:
                print(f"  ! no provenance table for {p}", file=sys.stderr)
                continue
            for line in open(p):
                r = json.loads(line)
                hit = table.get(r["client_ip"])
                if not hit:
                    continue
                r["label_class"], r["label_family"] = hit
                r["param_src"] = "direct_" + hit[1]
                w.write(json.dumps(r) + "\n")
                n += 1
                cls[hit[0]] += 1
                fam[hit[1]] += 1
                src[os.path.basename(p)] += 1

    print(f"dataset: {n} labeled connections -> {a.out}")
    print("  by class :", dict(cls.most_common()))
    print("  by family:", dict(fam.most_common(20)))
    print("  by source:", dict(src.most_common()))


if __name__ == "__main__":
    main()
