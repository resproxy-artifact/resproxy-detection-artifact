#!/usr/bin/env python3
"""
Generate timing CDF figure: direct baseline vs 9 proxied variants.
Outputs per-provider CDF .dat files + gnuplot script → EPS/PNG.
"""

import csv
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
GNUPLOT_DIR = ROOT / "data" / "analysis" / "gnuplot"
FIGURES_DIR = ROOT / "data" / "figures"
STYLE = ROOT / "style.gnu"

UNIFIED_CSV = ROOT / "new-data" / "unified" / "unified_timing.csv"
BD_CSV = ROOT / "new-data" / "unified" / "bd_mobile_isp" / "bd_mobile_isp_timing.csv"
DIRECT_CSV = ROOT / "new-data" / "unified" / "direct_baseline" / "direct_baseline_timing.csv"

# Display names and colors for the 9 variants + direct
PROVIDERS = {
    "brightdata":        ("BrightData",        "#e41a1c"),
    "brightdata_mobile": ("BD Mobile",         "#ff7f00"),
    "brightdata_isp":    ("BD ISP",            "#a65628"),
    "soax":              ("SOAX",              "#377eb8"),
    "oxylabs":           ("Oxylabs Resi",      "#4daf4a"),
    "oxylabs_mobile":    ("Oxylabs Mobile",    "#984ea3"),
    "oxylabs_isp":       ("Oxylabs ISP",       "#999999"),
    "iproyal":           ("IPRoyal",           "#f781bf"),
    "netnut":            ("NetNut",            "#a6d854"),
}


def load_gaps():
    """Load gap_ms values grouped by provider."""
    gaps = defaultdict(list)

    # Core 7 providers
    with open(UNIFIED_CSV) as f:
        for row in csv.DictReader(f):
            p = row["provider"]
            if p in PROVIDERS:
                gaps[p].append(float(row["gap_ms"]))

    # BD Mobile + BD ISP
    with open(BD_CSV) as f:
        for row in csv.DictReader(f):
            p = row["provider"]
            if p in PROVIDERS:
                gaps[p].append(float(row["gap_ms"]))

    # Direct baseline (Real Chrome)
    with open(DIRECT_CSV) as f:
        for row in csv.DictReader(f):
            gaps["direct"].append(float(row["gap_ms"]))

    return gaps


def write_cdf_dat(gaps, name):
    """Write sorted CDF .dat file, return path."""
    vals = sorted(gaps)
    n = len(vals)
    dat = GNUPLOT_DIR / f"cdf_provider_{name}.dat"
    with open(dat, "w") as f:
        for i, v in enumerate(vals):
            f.write(f"{v} {(i + 1) / n:.6f}\n")
    return dat


def main():
    gaps = load_gaps()

    # Print summary
    print(f"{'Provider':<20} {'N':>6} {'Median':>8} {'P5':>8} {'P95':>8}")
    print("-" * 55)
    for p in ["direct"] + list(PROVIDERS.keys()):
        g = sorted(gaps[p])
        n = len(g)
        if n == 0:
            continue
        med = g[n // 2]
        p5 = g[int(n * 0.05)]
        p95 = g[int(n * 0.95)]
        print(f"{p:<20} {n:>6} {med:>8.1f} {p5:>8.1f} {p95:>8.1f}")

    # Write CDF data files
    dat_files = {}
    for name in ["direct"] + list(PROVIDERS.keys()):
        if gaps[name]:
            dat_files[name] = write_cdf_dat(gaps[name], name)

    # Generate gnuplot script
    plot_lines = []
    # Direct first (thick black dashed)
    plot_lines.append(
        f'"{dat_files["direct"]}" using 1:2 '
        f'title "Direct (Chrome, N={len(gaps["direct"])})" '
        f'with lines lw 3.0 lc rgb "#000000" dt 2'
    )
    # Then 9 providers
    for p, (label, color) in PROVIDERS.items():
        if p not in dat_files:
            continue
        n = len(gaps[p])
        plot_lines.append(
            f'"{dat_files[p]}" using 1:2 '
            f'title "{label} ({n})" '
            f'with lines lw 2.0 lc rgb "{color}"'
        )

    script = f"""load "{STYLE}"
set terminal postscript eps enhanced color font "Helvetica,14" size 6.0,3.5
set output "{FIGURES_DIR}/timing_cdf_providers.eps"

set xlabel "TCP-to-TLS Gap (ms)" font "Helvetica,16"
set ylabel "CDF" font "Helvetica,16"
set key right bottom font "Helvetica,10" spacing 1.1 maxrows 5

set xrange [0:600]
set yrange [0:1.05]
set xtics 100
set ytics 0.2

set arrow from 10,0 to 10,1.05 nohead lw 1.5 lc rgb "#888888" dt 2
set label "t = 10 ms" at 15,0.5 font "Helvetica,11" tc rgb "#888888"

plot {", ".join(chr(92) + chr(10) + "     " + l for l in plot_lines)}
"""

    script_path = GNUPLOT_DIR / "plot_cdf_providers.gnu"
    script_path.write_text(script)

    # Run gnuplot
    r = subprocess.run(["gnuplot", str(script_path)], capture_output=True, text=True)
    if r.returncode == 0:
        print(f"\nEPS: {FIGURES_DIR}/timing_cdf_providers.eps")
        subprocess.run(["gs", "-dBATCH", "-dNOPAUSE", "-dEPSCrop",
                        "-sDEVICE=png16m", "-r300",
                        f"-sOutputFile={FIGURES_DIR}/timing_cdf_providers.png",
                        str(FIGURES_DIR / "timing_cdf_providers.eps")],
                       capture_output=True)
        print(f"PNG: {FIGURES_DIR}/timing_cdf_providers.png")
    else:
        print(f"gnuplot error: {r.stderr[:500]}")


if __name__ == "__main__":
    main()
