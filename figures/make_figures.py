#!/usr/bin/env python3
"""Draft regeneration of the 3 remaining earlier figures from dataset.jsonl.
Outputs to scratchpad only (drafts for user approval; nothing in the paper
is touched). Region map inferred from RTT geometry and verified:
38.143=VA, 44.227=TK, 37.18=PA, 10.139=SP."""
import json, os, subprocess
from collections import defaultdict
import numpy as np

DS = '.'
S = '.'
REGION = {'172.31.38.143': 'VA', '172.31.44.227': 'TK',
          '172.31.37.18': 'PA', '172.31.10.139': 'SP'}
CORE7 = ['brightdata', 'soax', 'oxylabs', 'iproyal', 'netnut',
         'oxylabs_isp', 'oxylabs_mobile']
LABEL = {'brightdata': ('BrightData', 'Super-proxy'), 'soax': ('SOAX', 'Super-proxy'),
         'oxylabs': ('Oxylabs Resi', 'Super-proxy'), 'iproyal': ('IPRoyal', 'P2P'),
         'netnut': ('NetNut', 'ISP'), 'oxylabs_isp': ('Oxylabs ISP', 'ISP'),
         'oxylabs_mobile': ('Oxylabs Mob', 'Mobile')}
ALL9 = ['brightdata', 'brightdata_mobile', 'brightdata_isp', 'soax', 'oxylabs',
        'oxylabs_mobile', 'oxylabs_isp', 'iproyal', 'netnut']

rows = [json.loads(l) for l in open(DS)]
pos = [r for r in rows if r['label_class'] == 'resproxy']
core = [r for r in pos if r.get('src_pcap') == 'unified.pcap']
direct = [r for r in rows if r['label_class'] == 'direct']

# ---------- heatmap CSVs (gap + rtt) ----------
cells_g = defaultdict(list); cells_r = defaultdict(list)
for r in core:
    f, c, srv = r['label_family'], r.get('param_country'), REGION.get(r['server_ip'])
    if f in CORE7 and c and srv:
        if r.get('gap_ms') is not None: cells_g[(f, c, srv)].append(r['gap_ms'])
        if r.get('tcp_rtt_ms') is not None: cells_r[(f, c, srv)].append(r['tcp_rtt_ms'])

for name, cells in (('gap', cells_g), ('rtt', cells_r)):
    with open(f'{S}/heatmap_medians_{name}.csv', 'w') as w:
        w.write('provider,provider_label,architecture,country,server,median_gap_ms\n')
        n = 0
        for (f, c, srv), v in sorted(cells.items()):
            if len(v) >= 5:
                w.write(f'{f},{LABEL[f][0]},{LABEL[f][1]},{c},{srv},{np.median(v):.1f}\n')
                n += 1
    print(f'heatmap {name}: {n} cells')

# ---------- render heatmaps (layout copied from fig_heatmap_1row.py) ----------
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec

SERVERS = ['VA', 'TK', 'PA', 'SP']
COUNTRIES = ['us','ca','mx','gb','de','fr','ru','br','jp','sg','id','kr','in','au','za']
CNAMES = {'us':'United States','ca':'Canada','mx':'Mexico','gb':'United Kingdom',
          'de':'Germany','fr':'France','ru':'Russia','br':'Brazil','jp':'Japan',
          'sg':'Singapore','id':'Indonesia','kr':'South Korea','in':'India',
          'au':'Australia','za':'South Africa'}
SEPS = [2.5, 6.5, 7.5, 13.5]
CMAP = LinearSegmentedColormap.from_list('bwr_custom', [
    (0.0, '#2166ac'), (0.25, '#67a9cf'), (0.5, '#ffffff'),
    (0.75, '#ef8a62'), (1.0, '#b2182b')])

def render(csv, out, vmax, cbl):
    df = pd.read_csv(csv)
    fig = plt.figure(figsize=(14, 7))
    gs = gridspec.GridSpec(1, len(CORE7)+1, width_ratios=[1]*len(CORE7)+[0.05], wspace=0.08)
    for pi, prov in enumerate(CORE7):
        ax = fig.add_subplot(gs[0, pi]); sub = df[df['provider'] == prov]
        M = np.full((len(COUNTRIES), len(SERVERS)), np.nan)
        for _, row in sub.iterrows():
            if row['country'] in COUNTRIES:
                M[COUNTRIES.index(row['country']), SERVERS.index(row['server'])] = row['median_gap_ms']
        im = ax.imshow(M, cmap=CMAP, vmin=0, vmax=vmax, aspect='auto', origin='upper')
        for ci in range(len(COUNTRIES)):
            for si in range(len(SERVERS)):
                v = M[ci, si]
                if not np.isnan(v):
                    ax.text(si, ci, f'{v:.0f}', ha='center', va='center', fontsize=7.5, color='#333333')
        for sep in SEPS: ax.axhline(sep, color='#bbbbbb', linewidth=0.5)
        ax.set_title(f'{LABEL[prov][0]}\n({LABEL[prov][1]})', fontsize=8, fontweight='bold', pad=4)
        ax.set_xticks(range(len(SERVERS))); ax.set_xticklabels(SERVERS, fontsize=7)
        ax.tick_params(axis='x', length=0, pad=2)
        if pi == 0:
            ax.set_yticks(range(len(COUNTRIES)))
            ax.set_yticklabels([CNAMES[c] for c in COUNTRIES], fontsize=7)
        else:
            ax.set_yticks([])
        ax.tick_params(axis='y', length=0)
        for sp in ax.spines.values(): sp.set_visible(False)
    cax = fig.add_subplot(gs[0, -1]); cb = fig.colorbar(im, cax=cax)
    cb.set_label(cbl, fontsize=8); cb.ax.tick_params(labelsize=7)
    plt.savefig(out + '.pdf', format='pdf', bbox_inches='tight', pad_inches=0.02)
    plt.savefig(out + '.png', dpi=110, bbox_inches='tight', pad_inches=0.02)
    plt.close(fig); print('rendered', out)

render(f'{S}/heatmap_medians_gap.csv', f'{S}/draft_heatmap_gap', 500, 'Median gap (ms)')
render(f'{S}/heatmap_medians_rtt.csv', f'{S}/draft_heatmap_rtt', 400, 'Median TCP RTT (ms)')

# ---------- CDF .dat (per family + direct), downsampled ----------
os.makedirs('data', exist_ok=True)
def cdfdat(vals, path, cap=400):
    v = np.sort(np.asarray([x for x in vals if x is not None], float))
    idx = np.unique(np.linspace(0, len(v)-1, min(cap, len(v))).astype(int))
    with open(path, 'w') as w:
        w.write('# gap_ms cdf\n')
        for i in idx: w.write(f'{v[i]:.3f} {(i+1)/len(v):.5f}\n')
    return len(v)

ns = {}
ns['direct'] = cdfdat([r['gap_ms'] for r in direct], f'data/cdf_provider_direct.dat')
for f in ALL9:
    ns[f] = cdfdat([r['gap_ms'] for r in pos if r['label_family'] == f],
                   f'data/cdf_provider_{f}.dat')
print('CDF ns:', ns)
