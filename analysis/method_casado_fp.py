#!/usr/bin/env python3
"""
Casado & Freedman (NSDI 2007) proxy test -- "Peering Through the Shroud: The
Effect of Edge Opacity on IP-Based Client Identification".

THE RULE, verbatim from the paper
---------------------------------
  "we flag a host as a proxy if its SYN-FP host-type differs sufficiently from
   its User-Agent host-type, and mark it as a non-proxy if they are the same"

and the premise they state:

  "In the case of web proxies, which terminate their clients' TCP sessions, the
   SYN fingerprint corresponds to the proxy's TCP stack, not that of the
   clients."

So the method needs exactly two inputs per connection:
  (1) an OS ("host-type") inferred from the client SYN packet, and
  (2) an OS claimed by the HTTP User-Agent header.
It fires when (1) and (2) disagree.

WHAT THIS FILE IMPLEMENTS
-------------------------
  * a p0f-v2-style SYN signature matcher built by hand (p0f is not installed on
    this machine; see DEVIATIONS), over the SYN fields our extractor captured:
    syn_ttl -> initial TTL, syn_window, syn_mss, syn_wscale, syn_optlayout;
  * a User-Agent -> host-type parser;
  * the disagreement test, expressed as a graded confidence in [0,1] so that
    the binary rule can be turned into an ROC curve.  Casado & Freedman's own
    wording is "differs *sufficiently*", i.e. they too had a tunable margin.

DEVIATIONS FORCED BY OUR DATA  (all of these are reported in the summary too)
-----------------------------------------------------------------------------
D1. p0f v2/v3 is not installed and its signature database is not available
    here, so the signature table below is written by hand from well-known,
    publicly documented stack characteristics (see SIGNATURES).  It is a
    reimplementation, not the original tool.
D2. Our extractor does not record the IP Don't-Fragment bit, the total SYN
    packet size, or p0f's "quirks" field.  p0f v2 signatures are
    (window, iTTL, DF, syn_size, option_layout, quirks); we can only match on
    (window, iTTL, option_layout) plus MSS and window scale.  Three of p0f's
    six discriminants are therefore unavailable.
D3. Our captures are TLS on port 443, so the User-Agent is NOT recoverable
    from the packet trace.  It comes from the honeypot's server-side
    application log (label.py joins it in).  Casado & Freedman read the UA
    from a cleartext HTTP web bug in 2007.  This method consequently needs
    server-side application-layer access that the other compared methods do
    not; only 1 wire packet (the client SYN) is used, so pkts_used = 1.
D4. THE BIG ONE.  Our measurement client is `curl/8.5.0` for the overwhelming
    majority of connections (exact count printed by the summary).
    `curl/8.5.0` contains no OS token at all, so the
    "User-Agent host-type" that Casado & Freedman's rule compares against is
    undefined.  A further set of connections carry no UA at all.  Under a strict
    reading of the rule the test simply cannot be evaluated on those
    connections, and they are emitted with applicable=false.  We do NOT
    substitute a guessed host-type for them in the primary output.
    A clearly-labelled sensitivity variant (--oracle output file, see
    UA-ORACLE VARIANT below) is written to a SEPARATE file so the strict
    result is never contaminated.
D5. Android is Linux-derived and is not separable from desktop Linux at the
    SYN layer; we therefore treat {linux, android, chromeos} as ONE host-type
    group.  This is exactly the false-negative mode reported by Mi et al.
    (NDSS 2021) for residential proxies whose exit nodes are Android phones.
D6. Initial TTL is recovered by rounding the observed TTL up to the next of
    64/128/255.  A small number of connections have an observed TTL <=32 where
    an initial TTL of 32 (ancient Windows) would also be arithmetically
    possible; we do not model iTTL 32.  The summary prints how many.

UA-ORACLE VARIANT (secondary, explicitly labelled, separate output file)
------------------------------------------------------------------------
Because D4 makes the primary evaluation degenerate (no resproxy connection is
scoreable at all), we additionally run the identical test with ONE input
replaced: for connections whose UA carries no OS token, the UA host-type is
set to the host-type of the machine that actually ran curl.  That machine is
Linux, and we verify it from the data rather than assuming it: the SYN
fingerprints of the `direct` baselines (which ARE our client's own SYNs) are
printed in the summary.  This is a substitution, which is why it lives in its
own file and its own reported number.  It is *favourable* to Casado & Freedman
-- it hands the test a perfectly truthful client-OS claim that our traffic
never actually carried, and it makes the `direct` negatives trivially correct
by construction.  Read the two numbers accordingly.

OUTPUT
------
  out/scores_casado_fp.jsonl           strict (primary)
  out/scores_casado_fp_uaoracle.jsonl  UA-oracle sensitivity variant
"""
import argparse
import json
import math
import os
import sys
from collections import Counter, defaultdict

try:
    from sklearn.metrics import roc_auc_score
except Exception:  # pragma: no cover
    roc_auc_score = None


# ---------------------------------------------------------------------------
# SIGNATURES
# ---------------------------------------------------------------------------
# Hand-written p0f-v2-style table.  Every value below is a well-known, publicly
# documented characteristic of the named TCP stack, NOT something fitted to
# this dataset.
#
# `layouts` are TCP option-kind sequences as emitted by our extractor:
#     0 = EOL, 1 = NOP, 2 = MSS, 3 = window scale, 4 = SACK-permitted,
#     8 = timestamps
#   Linux            MSS,SACKOK,TS,NOP,WS              -> "2-4-8-1-3"
#   Windows Vista+   MSS,NOP,WS,NOP,NOP,SACKOK         -> "2-1-3-1-1-4"
#   Windows XP       MSS,NOP,NOP,SACKOK                -> "2-1-1-4"
#   macOS/iOS        MSS,NOP,WS,NOP,NOP,TS,SACKOK,EOL,EOL -> "2-1-3-1-1-8-4-0-0"
#   FreeBSD          MSS,NOP,WS,SACKOK,TS              -> "2-1-3-4-8"
#
# `win_literals` are documented default advertised windows; `win_mss_mult` are
# the MSS multipliers Linux-family stacks use for their initial receive window.
# These are canonical published values only -- nothing here was read off this
# dataset.  Window contributes W_WIN=0.15 to a match and never decides the
# host-type on its own: the group decision is carried by initial TTL (a hard
# gate) plus the TCP option layout.  Verified by re-running with the two
# non-canonical windows this dataset happens to show (62727, 64320) added and
# removed: the strict result, the truthful-claim oracle AUC, and the known-OS
# accuracy are all identical either way.
#
# NOTE on the Linux/macOS separation the task flags: both have initial TTL 64.
# p0f v2 separates them primarily on window size (Linux advertises an MSS
# multiple such as 5840/14600/29200/64240; Darwin advertises a literal 65535).
# In THIS dataset that discriminant alone is not sufficient -- many thousands
# of connections have iTTL 64 with window 65535 and a Linux option layout (the
# summary prints the count) -- so
# the option layout, which p0f also matches on, is what actually carries the
# Linux-vs-Darwin decision here.  Both fields are scored below and the summary
# reports how often window size alone would have been wrong.
SIGNATURES = [
    dict(
        os="linux", group="LINUXOID",
        ittl=64,
        layouts={"2-4-8-1-3", "2-4-8-1-1-3", "2-4-8"},
        win_literals={5840, 5792, 14600, 29200, 28960, 64240, 65535, 26883},
        win_mss_mult={2, 4, 8, 10, 16, 20, 44},
        wscales={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14},
        mss={1460, 1440, 1452, 1412, 1400, 1380, 1360, 1340, 1250, 1448, 536},
    ),
    dict(
        # Android: Linux kernel, same option layout; merged into LINUXOID.
        os="android", group="LINUXOID",
        ittl=64,
        layouts={"2-4-8-1-3"},
        win_literals={65535, 64240, 14600, 28960},
        win_mss_mult={2, 4, 10, 20, 44},
        wscales={6, 7, 8},
        mss={1460, 1430, 1400, 1412, 1358},
    ),
    dict(
        os="windows_modern", group="WINDOWS",
        ittl=128,
        layouts={"2-1-3-1-1-4", "2-1-3-1-1-8-4"},
        win_literals={8192, 16384, 64240, 65535, 65392, 8760, 17520},
        win_mss_mult=set(),
        wscales={0, 2, 5, 6, 8},
        mss={1460, 1440, 1400, 1380, 1360, 1250},
    ),
    dict(
        os="windows_xp", group="WINDOWS",
        ittl=128,
        layouts={"2-1-1-4", "2-1-1-4-1-3"},
        win_literals={8192, 16384, 64240, 65535, 65392},
        win_mss_mult=set(),
        wscales={0, 1, 2},
        mss={1460, 1440, 1400},
    ),
    dict(
        os="macos", group="DARWIN",
        ittl=64,
        layouts={"2-1-3-1-1-8-4-0-0", "2-1-3-1-1-8-4-0", "2-1-3-1-1-8-4"},
        win_literals={65535},
        win_mss_mult=set(),
        wscales={4, 5, 6, 7},
        mss={1460, 1440, 1424, 1380, 1360},
    ),
    dict(
        os="ios", group="DARWIN",
        ittl=64,
        layouts={"2-1-3-1-1-8-4-0-0", "2-1-3-1-1-8-4"},
        win_literals={65535},
        win_mss_mult=set(),
        wscales={4, 5, 6},
        mss={1460, 1440, 1420, 1400, 1358},
    ),
    dict(
        os="freebsd", group="BSD",
        ittl=64,
        layouts={"2-1-3-4-8", "2-1-3-4-8-0-0"},
        win_literals={65535},
        win_mss_mult=set(),
        wscales={6, 7},
        mss={1460, 1440},
    ),
    dict(
        os="netdev_solaris", group="NETDEV",
        ittl=255,
        layouts={"2", "2-4-8-1-3", "2-1-3-4-8", "2-1-3-1-1-4"},
        win_literals={4128, 8760, 16384, 32768, 65535, 64240},
        win_mss_mult={2, 4, 8},
        wscales={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
        mss={1460, 536, 1440},
    ),
]

# Two host-types "are the same" (Casado's non-proxy branch) iff they are in the
# same group.  D5: android is inside LINUXOID on purpose.
GROUP_OF_UA = {
    "windows": "WINDOWS",
    "macos": "DARWIN",
    "ios": "DARWIN",
    "linux": "LINUXOID",
    "android": "LINUXOID",
    "chromeos": "LINUXOID",
    "freebsd": "BSD",
}

# Weights of the five discriminants we can actually observe (D2).
W_ITTL, W_LAYOUT, W_WIN, W_WSCALE, W_MSS = 0.35, 0.35, 0.15, 0.10, 0.05
MIN_FAMILY_CONF = 0.60   # below this the SYN-FP yields no host-type at all


def initial_ttl(observed):
    """Round the observed TTL up to the next standard initial TTL (D6)."""
    if observed is None:
        return None
    for b in (64, 128, 255):
        if observed <= b:
            return b
    return 255


def _win_ok(sig, win, mss):
    if win is None:
        return False
    if win in sig["win_literals"]:
        return True
    if mss and sig["win_mss_mult"]:
        for m in sig["win_mss_mult"]:
            if win == m * mss:
                return True
    return False


def syn_similarity(sig, ittl, win, mss, wscale, layout):
    """Similarity in [0,1] between an observed SYN and one signature entry.

    Initial TTL is a hard gate: p0f treats it as the anchor field, and a stack
    does not change its initial TTL.
    """
    if ittl is None or ittl != sig["ittl"]:
        return 0.0
    s = W_ITTL
    if layout and layout in sig["layouts"]:
        s += W_LAYOUT
    if _win_ok(sig, win, mss):
        s += W_WIN
    if wscale is None:
        if not sig["wscales"] or 0 in sig["wscales"]:
            s += W_WSCALE * 0.5
    elif wscale in sig["wscales"]:
        s += W_WSCALE
    if mss in sig["mss"]:
        s += W_MSS
    return s


def syn_fingerprint(rec):
    """Return (best_os, best_group, best_conf, per_group_conf dict)."""
    ittl = initial_ttl(rec.get("syn_ttl"))
    win = rec.get("syn_window")
    mss = rec.get("syn_mss")
    wscale = rec.get("syn_wscale")
    layout = rec.get("syn_optlayout")

    per_group = defaultdict(float)
    best_os, best_conf = None, 0.0
    for sig in SIGNATURES:
        s = syn_similarity(sig, ittl, win, mss, wscale, layout)
        if s > per_group[sig["group"]]:
            per_group[sig["group"]] = s
        if s > best_conf:
            best_conf, best_os = s, sig["os"]
    if best_conf < MIN_FAMILY_CONF:
        return None, None, best_conf, dict(per_group)
    best_group = None
    for sig in SIGNATURES:
        if sig["os"] == best_os:
            best_group = sig["group"]
            break
    return best_os, best_group, best_conf, dict(per_group)


# ---------------------------------------------------------------------------
# User-Agent -> host-type
# ---------------------------------------------------------------------------
def ua_host_type(ua):
    """Return (host_type, reason). host_type is None when the UA carries no OS.

    Order matters: 'Android' must be tested before 'Linux' (Android UAs contain
    'Linux'), and 'Windows Phone' before 'Windows'.
    """
    if ua is None or not ua.strip():
        return None, "ua_missing"
    u = ua
    low = u.lower()
    if "android" in low:
        return "android", "ok"
    if "cros " in low or "cros_" in low or "; cros" in low:
        return "chromeos", "ok"
    if "iphone" in low or "ipad" in low or "ipod" in low or " ios " in low:
        return "ios", "ok"
    if "mac os x" in low or "macintosh" in low or "darwin" in low:
        return "macos", "ok"
    if "windows nt" in low or "windows phone" in low or "win64" in low \
            or "windows" in low:
        return "windows", "ok"
    if "freebsd" in low or "openbsd" in low or "netbsd" in low:
        return "freebsd", "ok"
    if "linux" in low or "x11" in low or "ubuntu" in low or "fedora" in low:
        return "linux", "ok"
    # curl/8.5.0, python-requests/x.y, Wget/x.y, Go-http-client/... : these
    # name the *client program*, never the OS.  Casado & Freedman's rule has no
    # host-type to compare against here (D4).
    return None, "ua_no_os_token"


# ---------------------------------------------------------------------------
# The test itself
# ---------------------------------------------------------------------------
def mismatch_score(syn_group, syn_conf, per_group, ua_type):
    """Casado's 'differs sufficiently', graded into [0,1].

    0.0  -> SYN host-type and UA host-type are the same group (non-proxy)
    ->1  -> some other stack explains the SYN much better than the UA's claim

    score = best_similarity - similarity_of_the_UA-claimed_group
    """
    claimed_group = GROUP_OF_UA.get(ua_type)
    claimed_conf = per_group.get(claimed_group, 0.0) if claimed_group else 0.0
    if claimed_group is not None and syn_group == claimed_group:
        return 0.0
    return max(0.0, min(1.0, syn_conf - claimed_conf))


def score_record(rec, ua_override=None):
    """Return dict(applicable, score, reason, syn_os, syn_group, ua_type)."""
    have_syn = rec.get("syn_ttl") is not None and rec.get("syn_optlayout")
    syn_os, syn_group, syn_conf, per_group = syn_fingerprint(rec)

    ua_type, ua_reason = ua_host_type(rec.get("user_agent"))
    from_oracle = False
    if ua_type is None and ua_override is not None and ua_reason == "ua_no_os_token":
        ua_type, ua_reason, from_oracle = ua_override, "ua_oracle", True

    if not have_syn:
        return dict(applicable=False, score=None, reason="syn_not_captured",
                    syn_os=syn_os, syn_group=syn_group, ua_type=ua_type,
                    syn_conf=syn_conf, ua_from_oracle=from_oracle)
    if ua_type is None:
        return dict(applicable=False, score=None, reason=ua_reason,
                    syn_os=syn_os, syn_group=syn_group, ua_type=None,
                    syn_conf=syn_conf, ua_from_oracle=from_oracle)
    if syn_group is None:
        # p0f returns "UNKNOWN" for unmatched SYNs; there is no host-type to
        # compare, so the rule cannot fire either way.
        return dict(applicable=False, score=None, reason="syn_fp_unknown",
                    syn_os=None, syn_group=None, ua_type=ua_type,
                    syn_conf=syn_conf, ua_from_oracle=from_oracle)
    return dict(applicable=True,
                score=mismatch_score(syn_group, syn_conf, per_group, ua_type),
                reason="ok", syn_os=syn_os, syn_group=syn_group,
                ua_type=ua_type, syn_conf=syn_conf,
                ua_from_oracle=from_oracle)


# ---------------------------------------------------------------------------
def auc_between(rows, pos_classes, neg_classes, keep=None):
    y, s = [], []
    for r in rows:
        if not r["applicable"]:
            continue
        if keep is not None and not keep(r):
            continue
        if r["label_class"] in pos_classes:
            y.append(1)
        elif r["label_class"] in neg_classes:
            y.append(0)
        else:
            continue
        s.append(r["score"])
    npos, nneg = y.count(1), y.count(0)
    if len(set(y)) < 2 or roc_auc_score is None:
        return None, npos, nneg
    return float(roc_auc_score(y, s)), npos, nneg


def auc_resproxy_vs_direct(rows, keep=None):
    return auc_between(rows, {"resproxy"}, {"direct"}, keep=keep)


def write_scores(path, rows):
    with open(path, "w") as w:
        for r in rows:
            w.write(json.dumps({
                "conn_key": r["conn_key"],
                "score": r["score"],
                "applicable": r["applicable"],
                "pkts_used": r["pkts_used"],
                "label_class": r["label_class"],
                "label_family": r["label_family"],
            }) + "\n")


def run(records, ua_override=None):
    rows = []
    for rec in records:
        out = score_record(rec, ua_override=ua_override)
        rows.append(dict(
            conn_key=rec["conn_key"],
            score=out["score"],
            applicable=out["applicable"],
            # D3: exactly one wire packet -- the client SYN -- is consumed.
            # The UA is out-of-band (server application log).
            pkts_used=1 if out["applicable"] else 0,
            label_class=rec["label_class"],
            label_family=rec["label_family"],
            reason=out["reason"],
            syn_os=out["syn_os"],
            syn_group=out["syn_group"],
            ua_type=out["ua_type"],
            syn_conf=out["syn_conf"],
            ua_from_oracle=out["ua_from_oracle"],
        ))
    return rows


def pct(a, b):
    return f"{100.0 * a / b:.2f}%" if b else "n/a"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="out/dataset.jsonl")
    ap.add_argument("--out", default="out/scores_casado_fp.jsonl")
    ap.add_argument("--out-oracle", default="out/scores_casado_fp_uaoracle.jsonl")
    a = ap.parse_args()

    records = [json.loads(l) for l in open(a.dataset)]
    n = len(records)
    ua_kinds = Counter()
    for rec in records:
        t, why = ua_host_type(rec.get("user_agent"))
        ua_kinds[why if t is None else f"os={t}"] += 1
    n_lowttl = sum(1 for rec in records
                   if rec.get("syn_ttl") is not None and rec["syn_ttl"] <= 32)

    # ---------------- primary: strict ------------------------------------
    strict = run(records, ua_override=None)
    write_scores(a.out, strict)

    print("=" * 74)
    print("Casado & Freedman (NSDI'07) SYN-FP vs User-Agent proxy test")
    print("=" * 74)
    print(f"connections read              : {n}")
    print(f"class composition             : "
          f"{dict(Counter(r['label_class'] for r in records).most_common())}")
    print(f"UA host-type availability     : {dict(ua_kinds.most_common())}")
    print(f"observed SYN TTL <=32 (D6)    : {n_lowttl}  "
          f"(iTTL 32 would also be arithmetically possible; not modelled)")

    ap_rows = [r for r in strict if r["applicable"]]
    print(f"scoreable (applicable=true)   : {len(ap_rows)}  ({pct(len(ap_rows), n)})")
    print(f"not scoreable                 : {n - len(ap_rows)}  ({pct(n - len(ap_rows), n)})")
    reasons = Counter(r["reason"] for r in strict if not r["applicable"])
    for k, v in reasons.most_common():
        print(f"    reason {k:<20s}: {v}")

    print("\n-- scoreable rows by class ------------------------------------")
    by_cls = Counter(r["label_class"] for r in ap_rows)
    for k, v in by_cls.most_common():
        flagged = sum(1 for r in ap_rows if r["label_class"] == k and r["score"] > 0)
        print(f"    {k:<15s}: {v:6d} scoreable, {flagged:6d} flagged as proxy "
              f"({pct(flagged, v)})")

    auc, npos, nneg = auc_resproxy_vs_direct(strict)
    print("\n-- AUC, resproxy(+) vs direct(-), scoreable subset ------------")
    print(f"    positives (resproxy) : {npos}")
    print(f"    negatives (direct)   : {nneg}")
    if auc is None:
        print("    AUC                  : UNDEFINED -- one of the two classes "
              "has zero scoreable connections.")
        print("    (D4: every resproxy connection in this dataset carries the "
              "UA 'curl/8.5.0',")
        print("     which contains no OS token, so the rule has nothing to "
              "compare against.)")
    else:
        print(f"    AUC                  : {auc:.4f}")

    # Discriminative power on the only subset the strict test CAN score.
    print("\n-- diagnostic: is the strict test discriminative at all here? --")
    sc = Counter(round(r["score"], 4) for r in ap_rows)
    print(f"    distinct scores over the {len(ap_rows)} scoreable rows: "
          f"{dict(sorted(sc.items()))}")
    auc_bt, p_bt, n_bt = auc_between(strict, {"benign_tunnel"}, {"direct"})
    print(f"    AUC benign_tunnel(+) vs direct(-): "
          + (f"{auc_bt:.4f}" if auc_bt is not None else "UNDEFINED")
          + f"   (n+={p_bt}, n-={n_bt})")
    print("    CAVEAT: at Casado & Freedman's own BINARY decision (flag iff the")
    print("    two host-types differ) the rule flags 100% of `direct` and 100%")
    print("    of `benign_tunnel` here -- i.e. zero discrimination.  The AUC")
    print("    above is above 0.5 only because of the graded confidence we")
    print("    added to make an ROC possible; that ordering has no counterpart")
    print("    in the paper and should not be read as the method separating")
    print("    tunnels from direct clients.")
    print("    Those 400 connections come from the `scope_*` runs, whose")
    print("    harness sent a Chrome-on-Windows UA from a Linux host.  The")
    print("    SYN-FP/UA disagreement is therefore present for the `direct`")
    print("    baseline too, and the rule flags every one of them.  This is a")
    print("    property of OUR harness spoofing its UA, not a measurement of")
    print("    the method's false-positive rate on honest clients.")
    n_spoof = sum(1 for rec, r in zip(records, strict)
                  if rec["label_class"] == "direct" and r["applicable"]
                  and r["ua_type"] is not None
                  and GROUP_OF_UA.get(r["ua_type"]) != r["syn_group"])
    print(f"    direct connections whose own UA contradicts their own SYN-FP: "
          f"{n_spoof}")

    # ---------------- SYN-FP OS accuracy on known-OS direct subset --------
    print("\n-- SYN-FP OS inference accuracy, direct subset with known OS ---")
    print("   (provenance ground truth from build_dataset.py; note these 150")
    print("    connections carry NO User-Agent, so the full Casado test is")
    print("    inapplicable to them -- this measures the fingerprinter alone.)")
    truth_group = {"linux": "LINUXOID", "windows": "WINDOWS", "macos": "DARWIN"}
    per_fam = defaultdict(Counter)
    for rec, r in zip(records, strict):
        fam = rec["label_family"]
        if rec["label_class"] != "direct" or fam not in truth_group:
            continue
        per_fam[fam][r["syn_group"] or "UNKNOWN"] += 1
    overall_c = overall_n = 0
    for fam in ("linux", "windows", "macos"):
        c = per_fam[fam]
        tot = sum(c.values())
        corr = c.get(truth_group[fam], 0)
        overall_c += corr
        overall_n += tot
        detail = ", ".join(f"{k}={v}" for k, v in c.most_common())
        print(f"    {fam:<8s} n={tot:<4d} correct={corr:<4d} "
              f"acc={pct(corr, tot):<8s} [{detail}]")
    print(f"    {'ALL':<8s} n={overall_n:<4d} correct={overall_c:<4d} "
          f"acc={pct(overall_c, overall_n)}")

    # what our own client looks like on the wire (grounds the oracle variant)
    print("\n-- SYN-FP of the `direct` baselines (= our own measurement host) -")
    c = Counter(r["syn_group"] or "UNKNOWN"
                for rec, r in zip(records, strict) if rec["label_class"] == "direct")
    print(f"    {dict(c.most_common())}")
    c2 = Counter(r["syn_group"] or "UNKNOWN"
                 for rec, r in zip(records, strict)
                 if rec["label_class"] == "direct" and rec["label_family"] == "direct")
    print(f"    family='direct' only (curl + spoofed-Chrome runs): "
          f"{dict(c2.most_common())}")

    # window-size-alone check for the Linux/Darwin separation
    n_l64_65535 = sum(1 for rec in records
                      if initial_ttl(rec["syn_ttl"]) == 64
                      and rec["syn_window"] == 65535
                      and rec["syn_optlayout"] == "2-4-8-1-3")
    n_darwin = sum(1 for r in strict if r["syn_group"] == "DARWIN")
    print("\n-- Linux vs macOS separation (both have initial TTL 64) --------")
    print(f"    iTTL=64, window=65535, Linux option layout : {n_l64_65535}")
    print(f"    SYN-FP called DARWIN                       : {n_darwin}")
    print("    -> window size alone (p0f v2's main Linux/Darwin discriminant)")
    print("       would misread those Linux connections as Darwin here; the")
    print("       TCP option layout is what actually separates them.")

    # ---------------- SYN-FP host-type per resproxy family ----------------
    print("\n-- SYN-FP host-type by label_family ---------------------------")
    fam_g = defaultdict(Counter)
    for rec, r in zip(records, strict):
        fam_g[(rec["label_class"], rec["label_family"])][r["syn_group"] or "UNKNOWN"] += 1
    for k in sorted(fam_g):
        c = fam_g[k]
        tot = sum(c.values())
        lx = c.get("LINUXOID", 0)
        print(f"    {k[0]:<14s}/{k[1]:<18s} n={tot:<6d} "
              f"LINUXOID={lx} ({pct(lx, tot)})  "
              + ", ".join(f"{a}={b}" for a, b in c.most_common() if a != "LINUXOID"))

    # ---------------- secondary: UA-oracle variant ------------------------
    oracle = run(records, ua_override="linux")
    write_scores(a.out_oracle, oracle)
    ap2 = [r for r in oracle if r["applicable"]]
    auc2, npos2, nneg2 = auc_resproxy_vs_direct(oracle)
    print("\n" + "=" * 74)
    print("SECONDARY, NOT THE PAPER'S METHOD: UA-oracle variant")
    print("  UA host-type for OS-less UAs (curl) replaced by 'linux', the")
    print("  actual OS of the machine that ran curl.  This is a SUBSTITUTION")
    print("  for an input our traffic does not carry, and it is favourable to")
    print("  the method (perfect client-OS claim; `direct` negatives are")
    print("  correct by construction).  Separate file: " + a.out_oracle)
    print("=" * 74)
    print(f"    scoreable                : {len(ap2)}  ({pct(len(ap2), n)})")
    r2 = Counter(r["reason"] for r in oracle if not r["applicable"])
    for k, v in r2.most_common():
        print(f"    reason {k:<20s}: {v}")
    print(f"    positives (resproxy)     : {npos2}")
    print(f"    negatives (direct)       : {nneg2}")
    print(f"    AUC (all scoreable)      : "
          + (f"{auc2:.4f}" if auc2 is not None else "UNDEFINED"))

    # The 100 `scope_direct` connections keep their REAL (spoofed
    # Chrome-on-Windows) UA even in the oracle run, so they stay false
    # positives and drag the AUC below 0.5.  Report the sub-AUC restricted to
    # connections whose UA host-type is truthful, i.e. supplied by the oracle.
    auc3, npos3, nneg3 = auc_resproxy_vs_direct(
        oracle, keep=lambda r: r["ua_from_oracle"])
    print("\n    restricted to rows whose host-type claim is TRUTHFUL")
    print("    (oracle-supplied only; excludes the 100 scope_direct runs whose")
    print("     harness spoofed a Chrome-on-Windows UA from a Linux host):")
    print(f"      positives (resproxy)   : {npos3}")
    print(f"      negatives (direct)     : {nneg3}")
    print(f"      AUC                    : "
          + (f"{auc3:.4f}" if auc3 is not None else "UNDEFINED"))
    print("\n    flag rate (score>0) by class, oracle variant:")
    byc = Counter(r["label_class"] for r in ap2)
    for k, v in byc.most_common():
        f = sum(1 for r in ap2 if r["label_class"] == k and r["score"] > 0)
        print(f"      {k:<15s}: {f}/{v} ({pct(f, v)})")
    print("\n    per-resproxy-family recall (score>0), oracle variant:")
    for fam in sorted({r["label_family"] for r in ap2
                       if r["label_class"] == "resproxy"}):
        sub = [r for r in ap2 if r["label_family"] == fam]
        f = sum(1 for r in sub if r["score"] > 0)
        print(f"      {fam:<20s}: {f}/{len(sub)} ({pct(f, len(sub))})")

    print(f"\nwrote {a.out} ({len(strict)} lines)")
    print(f"wrote {a.out_oracle} ({len(oracle)} lines)")


if __name__ == "__main__":
    main()
