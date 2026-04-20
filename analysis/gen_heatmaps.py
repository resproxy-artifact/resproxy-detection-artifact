#!/usr/bin/env python3
"""
Generate heatmap figures:
  1. heatmap_1row: median gap (ms) by provider × (country × server)
  2. heatmap_tcp_rtt: median TCP RTT (ms) by provider × (country × server)
"""

import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
FIGURES_DIR = ROOT / "data" / "figures"
GNUPLOT_DIR = ROOT / "data" / "analysis" / "gnuplot"

UNIFIED_CSV = ROOT / "new-data" / "unified" / "unified_timing.csv"
BD_CSV = ROOT / "new-data" / "unified" / "bd_mobile_isp" / "bd_mobile_isp_timing.csv"

# Provider order (grouped by architecture)
PROVIDER_ORDER = [
    "brightdata",        # super-proxy
    "brightdata_mobile", # super-proxy (mobile)
    "brightdata_isp",    # super-proxy (ISP)
    "soax",              # super-proxy
    "oxylabs",           # super-proxy
    "oxylabs_mobile",    # centralized (mobile)
    "oxylabs_isp",       # centralized (ISP)
    "iproyal",           # P2P
    "netnut",            # ISP/datacenter
]

PROVIDER_LABELS = {
    "brightdata": "BrightData",
    "brightdata_mobile": "BD Mobile",
    "brightdata_isp": "BD ISP",
    "soax": "SOAX",
    "oxylabs": "Oxylabs Resi",
    "oxylabs_mobile": "Oxylabs Mobile",
    "oxylabs_isp": "Oxylabs ISP",
    "iproyal": "IPRoyal",
    "netnut": "NetNut",
}

COUNTRY_ORDER = ["us", "ca", "mx", "br", "gb", "de", "fr", "ru", "za",
                 "in", "sg", "id", "jp", "kr", "au"]
COUNTRY_LABELS = {
    "us": "US", "ca": "CA", "mx": "MX", "br": "BR", "gb": "GB",
    "de": "DE", "fr": "FR", "ru": "RU", "za": "ZA", "in": "IN",
    "sg": "SG", "id": "ID", "jp": "JP", "kr": "KR", "au": "AU",
}

SERVER_ORDER = ["us", "eu", "ap", "sa"]
SERVER_LABELS = {"us": "US", "eu": "EU", "ap": "AP", "sa": "SA"}


def load_data():
    """Load gap and RTT by provider × country × server."""
    gap_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    rtt_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for csv_path in [UNIFIED_CSV, BD_CSV]:
        with open(csv_path) as f:
            for row in csv.DictReader(f):
                p = row["provider"]
                if p in ("scope_direct", "scope_squid", "scope_tor"):
                    continue
                c = row["country"]
                s = row["server"]
                gap_data[p][c][s].append(float(row["gap_ms"]))
                rtt_data[p][c][s].append(float(row["tcp_rtt_ms"]))

    return gap_data, rtt_data


def build_matrix(data):
    """Build (n_providers × n_cols) matrix, n_cols = n_countries × n_servers."""
    n_providers = len(PROVIDER_ORDER)
    n_countries = len(COUNTRY_ORDER)
    n_servers = len(SERVER_ORDER)
    n_cols = n_countries * n_servers

    matrix = np.full((n_providers, n_cols), np.nan)

    for pi, prov in enumerate(PROVIDER_ORDER):
        for ci, country in enumerate(COUNTRY_ORDER):
            for si, server in enumerate(SERVER_ORDER):
                vals = data[prov][country][server]
                if vals:
                    matrix[pi, ci * n_servers + si] = sorted(vals)[len(vals) // 2]

    return matrix


def plot_heatmap(matrix, title, filename, cmap, vmin, vmax, use_log=False):
    """Plot the heatmap."""
    n_providers = len(PROVIDER_ORDER)
    n_countries = len(COUNTRY_ORDER)
    n_servers = len(SERVER_ORDER)

    fig, ax = plt.subplots(figsize=(14, 4.5))

    if use_log:
        norm = LogNorm(vmin=max(vmin, 1), vmax=vmax)
    else:
        norm = Normalize(vmin=vmin, vmax=vmax)

    # Masked array for NaN
    masked = np.ma.masked_invalid(matrix)
    im = ax.imshow(masked, aspect="auto", cmap=cmap, norm=norm,
                   interpolation="nearest")

    # X-axis: country groups with server sub-labels
    ax.set_xticks([])
    # Country group labels (centered over 4 server columns)
    for ci, country in enumerate(COUNTRY_ORDER):
        center = ci * n_servers + (n_servers - 1) / 2
        ax.text(center, n_providers + 0.3, COUNTRY_LABELS[country],
                ha="center", va="top", fontsize=8, fontweight="bold")

    # Server sub-labels
    for ci in range(n_countries):
        for si, server in enumerate(SERVER_ORDER):
            x = ci * n_servers + si
            ax.text(x, -0.7, SERVER_LABELS[server],
                    ha="center", va="bottom", fontsize=5, color="#666666")

    # Y-axis: providers
    ax.set_yticks(range(n_providers))
    ax.set_yticklabels([PROVIDER_LABELS[p] for p in PROVIDER_ORDER], fontsize=9)

    # Vertical separators between countries
    for ci in range(1, n_countries):
        ax.axvline(ci * n_servers - 0.5, color="white", lw=1.5)

    # Annotate cells with values
    for pi in range(n_providers):
        for col in range(matrix.shape[1]):
            val = matrix[pi, col]
            if not np.isnan(val):
                # Choose text color based on background
                txt_color = "white" if val > (vmax * 0.6) else "black"
                ax.text(col, pi, f"{val:.0f}", ha="center", va="center",
                        fontsize=5, color=txt_color)
            else:
                ax.text(col, pi, "—", ha="center", va="center",
                        fontsize=5, color="#cccccc")

    # Hatching for missing cells
    for pi in range(n_providers):
        for col in range(matrix.shape[1]):
            if np.isnan(matrix[pi, col]):
                ax.add_patch(plt.Rectangle((col - 0.5, pi - 0.5), 1, 1,
                             fill=False, hatch="///", edgecolor="#dddddd", lw=0.5))

    ax.set_xlim(-0.5, matrix.shape[1] - 0.5)
    ax.set_ylim(n_providers - 0.5, -0.5)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.02)
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label(title.split(":")[-1].strip() if ":" in title else "ms",
                   fontsize=9)

    ax.set_title(title, fontsize=12, pad=25)
    fig.tight_layout()

    # Save EPS + PNG
    eps_path = FIGURES_DIR / f"{filename}.eps"
    png_path = FIGURES_DIR / f"{filename}.png"
    fig.savefig(eps_path, format="eps", dpi=300, bbox_inches="tight")
    fig.savefig(png_path, format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"  {eps_path}")
    print(f"  {png_path}")

    return eps_path


def write_dat_files(gap_data, rtt_data):
    """Write gnuplot-compatible .dat files for reference."""
    for metric, data, prefix in [("gap", gap_data, "heatmap_gap"),
                                  ("rtt", rtt_data, "heatmap_rtt")]:
        for prov in PROVIDER_ORDER:
            dat_path = GNUPLOT_DIR / f"{prefix}_{prov}.dat"
            with open(dat_path, "w") as f:
                f.write(f"# country server median_{metric}_ms N\n")
                for country in COUNTRY_ORDER:
                    for server in SERVER_ORDER:
                        vals = data[prov][country][server]
                        if vals:
                            med = sorted(vals)[len(vals) // 2]
                            f.write(f"{country} {server} {med:.1f} {len(vals)}\n")
                        else:
                            f.write(f"{country} {server} NaN 0\n")


def main():
    print("Loading data...")
    gap_data, rtt_data = load_data()

    gap_matrix = build_matrix(gap_data)
    rtt_matrix = build_matrix(rtt_data)

    print(f"\nMatrix shape: {gap_matrix.shape}")
    print(f"Gap range: {np.nanmin(gap_matrix):.0f} – {np.nanmax(gap_matrix):.0f} ms")
    print(f"RTT range: {np.nanmin(rtt_matrix):.0f} – {np.nanmax(rtt_matrix):.0f} ms")

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    GNUPLOT_DIR.mkdir(parents=True, exist_ok=True)

    print("\nGenerating heatmap_1row (median gap)...")
    plot_heatmap(gap_matrix,
                 "Median TCP-to-TLS Gap (ms): Exit Country × Server",
                 "heatmap_1row", "YlOrRd", vmin=0, vmax=500)

    print("\nGenerating heatmap_tcp_rtt (median TCP RTT)...")
    plot_heatmap(rtt_matrix,
                 "Median TCP RTT (ms): Exit Country × Server",
                 "heatmap_tcp_rtt", "YlGnBu", vmin=0, vmax=400)

    print("\nWriting .dat files...")
    write_dat_files(gap_data, rtt_data)
    print("Done.")


if __name__ == "__main__":
    main()
