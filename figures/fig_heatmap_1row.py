#!/usr/bin/env python3
"""Generate 1x7 per-provider heatmap from heatmap_medians.csv"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

# --- Config ---
CSV = '../figures/heatmap_medians.csv'
OUT_EPS = '../figures/heatmap_1row.eps'
OUT_PDF = '../figures/heatmap_1row.pdf'

FIG_W, FIG_H = 14, 7  # 2:1 ratio

PROVIDERS = [
    'brightdata', 'soax', 'oxylabs', 'iproyal',
    'netnut', 'oxylabs_isp', 'oxylabs_mobile',
]
SERVERS = ['VA', 'TK', 'PA', 'SP']
COUNTRIES = ['us','ca','mx','gb','de','fr','ru','br','jp','sg','id','kr','in','au','za']
COUNTRY_NAMES = {
    'us':'United States','ca':'Canada','mx':'Mexico',
    'gb':'United Kingdom','de':'Germany','fr':'France','ru':'Russia',
    'br':'Brazil','jp':'Japan','sg':'Singapore','id':'Indonesia',
    'kr':'South Korea','in':'India','au':'Australia','za':'South Africa',
}

# Continent separators: after mx(2), ru(6), br(7), au(13)
CONTINENT_SEPS = [2.5, 6.5, 7.5, 13.5]

VMIN, VMAX = 0, 500

# Blue -> White -> Red
CMAP = LinearSegmentedColormap.from_list('bwr_custom', [
    (0.0,  '#2166ac'),
    (0.25, '#67a9cf'),
    (0.5,  '#ffffff'),
    (0.75, '#ef8a62'),
    (1.0,  '#b2182b'),
])

# --- Load data ---
df = pd.read_csv(CSV)

# --- Plot ---
fig = plt.figure(figsize=(FIG_W, FIG_H))
gs = gridspec.GridSpec(1, len(PROVIDERS) + 1,
                       width_ratios=[1]*len(PROVIDERS) + [0.05],
                       wspace=0.08)

for pi, prov in enumerate(PROVIDERS):
    ax = fig.add_subplot(gs[0, pi])
    sub = df[df['provider'] == prov]

    # Build matrix: rows=countries, cols=servers
    matrix = np.full((len(COUNTRIES), len(SERVERS)), np.nan)
    for _, row in sub.iterrows():
        ci = COUNTRIES.index(row['country'])
        si = SERVERS.index(row['server'])
        matrix[ci, si] = row['median_gap_ms']

    im = ax.imshow(matrix, cmap=CMAP, vmin=VMIN, vmax=VMAX,
                   aspect='auto', origin='upper')

    # Cell numbers
    for ci in range(len(COUNTRIES)):
        for si in range(len(SERVERS)):
            v = matrix[ci, si]
            if not np.isnan(v):
                color = '#333333' if 100 < v < 400 else '#333333'
                ax.text(si, ci, f'{v:.0f}', ha='center', va='center',
                        fontsize=7.5, color=color)

    # Continent separators
    for sep in CONTINENT_SEPS:
        ax.axhline(sep, color='#bbbbbb', linewidth=0.5)

    # Title
    label = sub.iloc[0]['provider_label']
    arch = sub.iloc[0]['architecture']
    ax.set_title(f'{label}\n({arch})', fontsize=8, fontweight='bold', pad=4)

    # X-axis
    ax.set_xticks(range(len(SERVERS)))
    ax.set_xticklabels(SERVERS, fontsize=7)
    ax.tick_params(axis='x', length=0, pad=2)

    # Y-axis: only first panel
    if pi == 0:
        ax.set_yticks(range(len(COUNTRIES)))
        ax.set_yticklabels([COUNTRY_NAMES[c] for c in COUNTRIES], fontsize=7)
    else:
        ax.set_yticks([])

    ax.tick_params(axis='y', length=0)

    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)

# Colorbar
cax = fig.add_subplot(gs[0, -1])
cb = fig.colorbar(im, cax=cax)
cb.set_label('Median gap (ms)', fontsize=8)
cb.ax.tick_params(labelsize=7)

plt.savefig(OUT_EPS, format='eps', bbox_inches='tight', pad_inches=0.02)
plt.savefig(OUT_PDF, format='pdf', bbox_inches='tight', pad_inches=0.02)
print(f'Written {OUT_EPS} and {OUT_PDF}')
