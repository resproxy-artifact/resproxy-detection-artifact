# Residential Proxy Detection — Artifact

Code, data, and deployment artifacts for the paper *"First Four Packets:
Passive Detection of Residential Proxy Tunnels."* This repository
supports reproduction of the main results (Figures 1–6, Tables 1–14)
from anonymized datasets.

> **Status:** anonymous submission — author information will be added
> upon acceptance / de-anonymization.

## Contents

| Path           | Description                                                       |
| -------------- | ----------------------------------------------------------------- |
| `analysis/`    | Python scripts that compute timing gaps, ROC, TCP fingerprint mismatch, causal regression, and generate `.dat` files for gnuplot. |
| `experiments/` | Proxy test runners (HTTP CONNECT / SOCKS5, browser automation, VPN, lab proxy). Requires provider credentials via environment variables; see `providers.json.template`. |
| `data/`        | Anonymized CSV datasets (client IPs → HMAC-SHA256, timestamps → relative offsets). |
| `figures/`     | Gnuplot scripts + pre-aggregated `.dat` files to rebuild every figure in the paper. |
| `nginx-module/`| Dynamic module (`ngx_http_proxy_detect_module`, 803 lines) for in-server detection. |
| `docs/`        | Deployment notes, data-format description, ethics statement. |

## Quick reproduction (figures only)

```bash
cd figures
gnuplot plot_cdf_providers.gnu      # Figure 2: provider CDFs
gnuplot fig_roc.gnu                  # Figure 4: ROC curve
gnuplot fig_packets_cdf.gnu          # Figure 5: packet-count CDF
gnuplot plot_labproxy_rtt.gnu        # Figure 6: lab proxy gap vs. RTT
```

All figures use `.dat` files in `figures/data/` that are already
aggregated — no IPs or raw timestamps.

## Rerunning the analysis

```bash
cd analysis
python3 main_evaluation.py ../data/unified_timing.csv
python3 analyze_fingerprint.py ../data/unified_fingerprint.csv
python3 analyze_labproxy.py                  # uses figures/data/labproxy_*.dat
python3 headtohead_clean.py ../data/unified_timing.csv
```

Scripts write intermediate `.dat` files into `figures/data/`.

## Rerunning live experiments

Experiments require paid accounts with the nine provider variants
evaluated in the paper. Populate credentials via environment variables:

```bash
cp experiments/providers.json.template experiments/providers.json
# Edit providers.json with real usernames/passwords
python3 experiments/run_proxy.py --provider brightdata --country us --count 50
```

Raw pcap captures are **not** included; experiments produce new CSVs
compatible with `analysis/` scripts.

## Data anonymization

`data/anonymize.py` is the exact script used to produce the released
CSVs from the raw measurement traces. It applies HMAC-SHA256 to each
`client_ip` with a fresh random salt per run and converts Unix
timestamps to seconds relative to the run's first observation.

## License

MIT (see `LICENSE`).
