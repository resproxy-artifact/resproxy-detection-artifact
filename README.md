# Artifact for an anonymous submission

Code, data, and deployment artifacts for an anonymous paper submission.
This repository reproduces the paper's reported statistics from an
anonymized, per-connection dataset.

> **Status:** anonymous submission — author information and a
> non-anonymized mirror will be added upon de-anonymization.

## Layout

| Path            | Description                                                                 |
| --------------- | --------------------------------------------------------------------------- |
| `analysis/`     | The analysis pipeline. Reads `analysis/out/dataset.jsonl` and regenerates every statistic the paper reports. |
| `analysis/out/` | The anonymized per-connection dataset (`dataset.jsonl`) and the regenerated outputs (`numbers.tex`, `eval_final.txt`, `compare_timing.txt`, `threshold_transfer.txt`, `tab_clientwork.tex`). |
| `experiments/`  | Data-collection runners (HTTP CONNECT / SOCKS5, browser automation, VPN, lab proxy). Credentials load from a local `providers.json`; a template is provided — **no real credentials are included.** |
| `nginx-module/` | The dynamic module (`ngx_http_proxy_detect_module`, 803 lines of C) used for live in-server detection. |
| `figures/`      | Gnuplot scripts and pre-aggregated `.dat` files for the paper's figures.     |

## What is and is not released

We release the **extracted per-connection dataset**, not the raw pcaps.
Each connection carries the timing features the paper uses (the
ACK-to-`ClientHello` gap, TCP RTT, the BADPASS TLS-minus-TCP residual,
SYN fingerprint fields, and per-packet directions/lengths). To protect
residential subscribers:

- Exit-node IP addresses (`client_ip`) are replaced by
  `exit_` + HMAC-SHA256 under a per-release salt that is generated once
  and discarded — irreversible, but same-exit rows stay linkable within
  this release.
- Measurement servers are relabelled `server_1..4`.
- All timestamps are relativized to each connection's first packet, so
  only intra-connection intervals remain.

Raw pcaps are withheld because they contain exit-node addresses that
could identify individual residential subscribers. Every number in the
paper is reproducible from the released dataset.

## Reproducing the paper's numbers

```bash
cd analysis
python3 emit_numbers.py        > out/numbers.tex          # the \newcommand macros used throughout the paper
python3 emit_eval.py           > out/eval_final.txt        # per-provider detection, LOO AUC, thresholds, scope
python3 compare_timing.py      > out/compare_timing.txt    # head-to-head vs BADPASS (op points, AUC, disagreement)
python3 threshold_transfer.py  > out/threshold_transfer.txt# published-threshold transfer across negative populations
python3 emit_clientwork.py                                  # writes out/tab_clientwork.tex + out/ppv.dat
```

`out/numbers.tex` is the authoritative macro file; the values there are
exactly those the paper compiles against.

### Pcap stage (transparency only — not runnable without the withheld pcaps)

`extract.py`, `build_dataset.py`, and `label.py` are the scripts that
built `dataset.jsonl` from the raw captures. They are included so the
extraction is auditable, but they require the pcaps we do not release.

## Requirements

Python 3.10+, NumPy, SciPy. The pcap-stage scripts additionally use
`dpkt`. No network access is required to reproduce the numbers.
