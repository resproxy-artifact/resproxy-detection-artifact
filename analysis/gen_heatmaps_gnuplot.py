#!/usr/bin/env python3
"""
Generate heatmap .dat (matrix format) + gnuplot scripts for:
  1. heatmap_1row: median gap (ms) by provider × (country, server)
  2. heatmap_tcp_rtt: median TCP RTT (ms) same layout
All rendering via gnuplot + style.gnu.
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

PROVIDER_ORDER = [
    "brightdata", "brightdata_mobile", "brightdata_isp", "soax",
    "oxylabs", "oxylabs_mobile", "oxylabs_isp", "iproyal", "netnut",
]
PROVIDER_LABELS = [
    "BrightData", "BD Mobile", "BD ISP", "SOAX",
    "Oxylabs Resi", "Oxylabs Mob", "Oxylabs ISP", "IPRoyal", "NetNut",
]

COUNTRY_ORDER = ["us", "ca", "mx", "br", "gb", "de", "fr", "ru", "za",
                 "in", "sg", "id", "jp", "kr", "au"]
COUNTRY_UPPER = [c.upper() for c in COUNTRY_ORDER]

SERVER_ORDER = ["us", "eu", "ap", "sa"]


def load_data():
    gap = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    rtt = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for csv_path in [UNIFIED_CSV, BD_CSV]:
        with open(csv_path) as f:
            for row in csv.DictReader(f):
                p = row["provider"]
                if p not in PROVIDER_ORDER:
                    continue
                c, s = row["country"], row["server"]
                gap[p][c][s].append(float(row["gap_ms"]))
                rtt[p][c][s].append(float(row["tcp_rtt_ms"]))
    return gap, rtt


def median(vals):
    s = sorted(vals)
    return s[len(s) // 2]


def write_matrix_dat(data, out_path):
    """Write gnuplot matrix .dat: rows = providers, cols = country×server."""
    n_cols = len(COUNTRY_ORDER) * len(SERVER_ORDER)
    with open(out_path, "w") as f:
        # Header: column indices
        f.write("# rows=providers, cols=country×server (4 servers per country)\n")
        for pi, prov in enumerate(PROVIDER_ORDER):
            vals = []
            for country in COUNTRY_ORDER:
                for server in SERVER_ORDER:
                    v = data[prov][country][server]
                    if v:
                        vals.append(f"{median(v):.1f}")
                    else:
                        vals.append("NaN")
            f.write(" ".join(vals) + "\n")
    return n_cols


def write_xyz_dat(data, out_path):
    """Write gnuplot x,y,z format: one line per cell, blank lines between rows."""
    with open(out_path, "w") as f:
        f.write("# x(col) y(provider) z(median_ms)\n")
        for pi, prov in enumerate(PROVIDER_ORDER):
            for ci, country in enumerate(COUNTRY_ORDER):
                for si, server in enumerate(SERVER_ORDER):
                    x = ci * len(SERVER_ORDER) + si
                    v = data[prov][country][server]
                    z = f"{median(v):.1f}" if v else "NaN"
                    f.write(f"{x} {pi} {z}\n")
            f.write("\n")  # blank line between rows


def gen_heatmap_script(dat_path, out_name, title, cbrange, palette, cblabel):
    """Generate gnuplot script for a heatmap using plot with image."""
    n_providers = len(PROVIDER_ORDER)
    n_countries = len(COUNTRY_ORDER)
    n_servers = len(SERVER_ORDER)
    n_cols = n_countries * n_servers

    # Y-tics: provider labels
    ytics = ", ".join(f'"{PROVIDER_LABELS[i]}" {i}' for i in range(n_providers))

    # X-tics: country labels at center of each 4-server group
    xtics = ", ".join(
        f'"{COUNTRY_UPPER[ci]}" {ci * n_servers + 1.5}'
        for ci in range(n_countries)
    )

    # Vertical separator lines between countries
    vlines = "\n".join(
        f'set arrow from {ci * n_servers - 0.5},-0.5 to {ci * n_servers - 0.5},{n_providers - 0.5} nohead lw 0.8 lc rgb "#ffffff" front'
        for ci in range(1, n_countries)
    )

    script = f"""load "{STYLE}"
set terminal postscript eps enhanced color font "Helvetica,11" size 8.5,2.8
set output "{FIGURES_DIR}/{out_name}.eps"

set title "{title}" font "Helvetica,12"

# Margins to prevent clipping
set lmargin 12
set rmargin 8
set tmargin 2.5
set bmargin 2.5

# Palette
set palette defined ({palette})
set cbrange [{cbrange}]
set cblabel "{cblabel}" font "Helvetica,10" offset 1,0

unset key

# Axes
set xrange [-0.5:{n_cols - 0.5}]
set yrange [{n_providers - 0.5}:-0.5]
set xtics ({xtics}) font "Helvetica,8" offset 0,0.3
set ytics ({ytics}) font "Helvetica,9"
set tics nomirror out
set border 0

# Country separators
{vlines}

# Plot
plot "{dat_path}" using 1:2:3 with image notitle
"""
    script_path = GNUPLOT_DIR / f"plot_{out_name}.gnu"
    script_path.write_text(script)
    return script_path


def run_gnuplot(script_path, out_name):
    r = subprocess.run(["gnuplot", str(script_path)], capture_output=True, text=True)
    if r.returncode == 0:
        eps = FIGURES_DIR / f"{out_name}.eps"
        png = FIGURES_DIR / f"{out_name}.png"
        subprocess.run(["gs", "-dBATCH", "-dNOPAUSE", "-dEPSCrop",
                        "-sDEVICE=png16m", "-r300",
                        f"-sOutputFile={png}", str(eps)],
                       capture_output=True)
        print(f"  {eps}")
        print(f"  {png}")
    else:
        print(f"  gnuplot error: {r.stderr[:300]}")


def main():
    print("Loading data...")
    gap_data, rtt_data = load_data()

    GNUPLOT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # Write dat files (both matrix and xyz format)
    gap_mat_dat = GNUPLOT_DIR / "heatmap_gap_matrix.dat"
    rtt_mat_dat = GNUPLOT_DIR / "heatmap_rtt_matrix.dat"
    gap_xyz_dat = GNUPLOT_DIR / "heatmap_gap_xyz.dat"
    rtt_xyz_dat = GNUPLOT_DIR / "heatmap_rtt_xyz.dat"

    write_matrix_dat(gap_data, gap_mat_dat)
    write_matrix_dat(rtt_data, rtt_mat_dat)
    write_xyz_dat(gap_data, gap_xyz_dat)
    write_xyz_dat(rtt_data, rtt_xyz_dat)

    # Gap heatmap (warm colors: yellow → red)
    print("\nGenerating heatmap_1row (gap)...")
    gap_palette = '0 "#ffffb2", 1 "#fecc5c", 2 "#fd8d3c", 3 "#f03b20", 4 "#bd0026"'
    gap_script = gen_heatmap_script(gap_xyz_dat, "heatmap_1row",
                                    "Median TCP-to-TLS Gap (ms)",
                                    "0:500", gap_palette, "ms")
    run_gnuplot(gap_script, "heatmap_1row")

    # RTT heatmap (cool colors: light blue → dark blue)
    print("\nGenerating heatmap_tcp_rtt (RTT)...")
    rtt_palette = '0 "#eff3ff", 1 "#bdd7e7", 2 "#6baed6", 3 "#3182bd", 4 "#08519c"'
    rtt_script = gen_heatmap_script(rtt_xyz_dat, "heatmap_tcp_rtt",
                                    "Median TCP RTT (ms)",
                                    "0:400", rtt_palette, "ms")
    run_gnuplot(rtt_script, "heatmap_tcp_rtt")

    print("\nDone.")


if __name__ == "__main__":
    main()
