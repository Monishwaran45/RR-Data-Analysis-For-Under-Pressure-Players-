import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\deepdive_comparison_charts'
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    'figure.dpi': 150, 'savefig.dpi': 150, 'savefig.bbox': 'tight',
    'font.size': 10, 'axes.titlesize': 13, 'axes.labelsize': 11,
    'figure.facecolor': '#0D1117', 'axes.facecolor': '#161B22',
    'text.color': '#C9D1D9', 'axes.labelcolor': '#C9D1D9',
    'xtick.color': '#8B949E', 'ytick.color': '#8B949E',
    'axes.edgecolor': '#30363D', 'grid.color': '#21262D',
})

GOLD = '#FFD700'
CYAN = '#58A6FF'
MAGENTA = '#F778A6'
GREEN = '#3FB950'
ORANGE = '#F0883E'
RED = '#F85149'
PURPLE = '#BC8CFF'

# Top 10 Batters data
bat_df = pd.DataFrame([
    {'name': 'Tim David', 'hp_sr': 194.59, 'hp_avg': 42.67, 'uplift': 32.76, 'braa': 449.2, 'pos_pct': 70.5, 'dot_pct': 31.0, 'balls': 592, 'rating': 47.12},
    {'name': 'Shashank Singh', 'hp_sr': 170.88, 'hp_avg': 48.70, 'uplift': 18.88, 'braa': 165.8, 'pos_pct': 71.4, 'dot_pct': 29.5, 'balls': 285, 'rating': 32.36},
    {'name': 'Rinku Singh', 'hp_sr': 172.15, 'hp_avg': 38.86, 'uplift': 38.31, 'braa': 313.9, 'pos_pct': 65.6, 'dot_pct': 30.9, 'balls': 632, 'rating': 31.84},
    {'name': 'Rishabh Pant', 'hp_sr': 183.67, 'hp_avg': 34.62, 'uplift': 50.60, 'braa': 142.7, 'pos_pct': 68.8, 'dot_pct': 31.9, 'balls': 245, 'rating': 31.17},
    {'name': 'Tristan Stubbs', 'hp_sr': 171.51, 'hp_avg': 42.14, 'uplift': 41.30, 'braa': 250.6, 'pos_pct': 63.3, 'dot_pct': 24.3, 'balls': 516, 'rating': 30.24},
    {'name': 'Tilak Varma', 'hp_sr': 164.38, 'hp_avg': 40.46, 'uplift': 28.70, 'braa': 275.8, 'pos_pct': 66.7, 'dot_pct': 28.6, 'balls': 640, 'rating': 26.27},
    {'name': 'Marcus Stoinis', 'hp_sr': 175.32, 'hp_avg': 30.68, 'uplift': 31.47, 'braa': 158.8, 'pos_pct': 60.9, 'dot_pct': 29.9, 'balls': 385, 'rating': 23.45},
    {'name': 'Suryakumar Yadav', 'hp_sr': 192.14, 'hp_avg': 32.58, 'uplift': 30.16, 'braa': 195.3, 'pos_pct': 62.5, 'dot_pct': 28.0, 'balls': 407, 'rating': 21.62},
    {'name': 'Rovman Powell', 'hp_sr': 157.42, 'hp_avg': 27.21, 'uplift': 18.78, 'braa': 224.4, 'pos_pct': 50.7, 'dot_pct': 34.0, 'balls': 674, 'rating': 20.39},
    {'name': 'Dasun Shanaka', 'hp_sr': 156.99, 'hp_avg': 23.31, 'uplift': 35.76, 'braa': 104.0, 'pos_pct': 53.3, 'dot_pct': 33.6, 'balls': 386, 'rating': 18.60},
])

# Top 10 Bowlers data
bowl_df = pd.DataFrame([
    {'name': 'Jasprit Bumrah', 'hp_econ': 7.08, 'wkt_sr': 13.05, 'wrsa': 247.1, 'pos_pct': 64.9, 'wkts': 39, 'balls': 509, 'rating': 28.39},
    {'name': 'Matheesha Pathirana', 'hp_econ': 8.35, 'wkt_sr': 10.27, 'wrsa': 205.9, 'pos_pct': 71.8, 'wkts': 44, 'balls': 452, 'rating': 26.37},
    {'name': 'Wanindu Hasaranga', 'hp_econ': 7.64, 'wkt_sr': 10.07, 'wrsa': 185.9, 'pos_pct': 56.5, 'wkts': 45, 'balls': 453, 'rating': 22.47},
    {'name': 'Yuzvendra Chahal', 'hp_econ': 8.57, 'wkt_sr': 12.03, 'wrsa': 182.3, 'pos_pct': 50.9, 'wkts': 39, 'balls': 469, 'rating': 22.26},
    {'name': 'Kuldeep Yadav', 'hp_econ': 7.46, 'wkt_sr': 10.61, 'wrsa': 162.3, 'pos_pct': 55.6, 'wkts': 38, 'balls': 403, 'rating': 20.54},
    {'name': 'Sam Curran', 'hp_econ': 10.67, 'wkt_sr': 13.17, 'wrsa': 83.8, 'pos_pct': 38.3, 'wkts': 24, 'balls': 316, 'rating': 17.50},
    {'name': 'Sunil Narine', 'hp_econ': 6.27, 'wkt_sr': 15.09, 'wrsa': 115.5, 'pos_pct': 68.8, 'wkts': 22, 'balls': 332, 'rating': 17.12},
    {'name': 'Rashid Khan', 'hp_econ': 7.28, 'wkt_sr': 12.55, 'wrsa': 187.7, 'pos_pct': 60.8, 'wkts': 56, 'balls': 703, 'rating': 15.48},
    {'name': 'Arshdeep Singh', 'hp_econ': 9.22, 'wkt_sr': 11.15, 'wrsa': 166.7, 'pos_pct': 55.5, 'wkts': 75, 'balls': 836, 'rating': 14.88},
    {'name': 'Taskin Ahmed', 'hp_econ': 8.40, 'wkt_sr': 11.92, 'wrsa': 94.8, 'pos_pct': 56.8, 'wkts': 26, 'balls': 310, 'rating': 12.68},
])

# ── CHART 1: BATTERS HEAD-TO-HEAD MATRIX HEATMAP ──
fig, ax = plt.subplots(figsize=(14, 7))
metrics_bat = ['hp_sr', 'hp_avg', 'uplift', 'braa', 'pos_pct', 'dot_pct', 'rating']
cols_label = ['HP Strike Rate', 'HP Average', 'Clutch Uplift', 'Net HP bRAA', 'Positive Match %', 'Dot Ball % (Inv)', 'Pressure Rating']

# Normalize 0-1 (dot_pct inverted so lower is better)
data_bat = bat_df[metrics_bat].values.copy()
norm_bat = np.zeros_like(data_bat)
for j in range(data_bat.shape[1]):
    col = data_bat[:, j]
    rng = col.max() - col.min()
    if metrics_bat[j] == 'dot_pct':
        norm_bat[:, j] = (col.max() - col) / rng
    else:
        norm_bat[:, j] = (col - col.min()) / rng

im = ax.imshow(norm_bat, cmap='YlGn', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(len(cols_label)))
ax.set_xticklabels(cols_label, fontsize=10, fontweight='bold', rotation=20, ha='right')
ax.set_yticks(range(10))
ax.set_yticklabels(bat_df['name'].values, fontsize=11, fontweight='bold')

for i in range(10):
    for j in range(len(metrics_bat)):
        val = data_bat[i, j]
        fmt = f"{val:.1f}" if j in [0, 1, 2, 4, 5, 6] else f"{val:.0f}"
        if j == 2: fmt = f"+{val:.1f}"
        if j == 3: fmt = f"+{val:.0f}"
        if j in [4, 5]: fmt = f"{val:.1f}%"
        color = 'black' if norm_bat[i, j] > 0.45 else 'white'
        ax.text(j, i, fmt, ha='center', va='center', fontsize=9, fontweight='bold', color=color)

ax.set_title('TOP 10 BATTERS: HEAD-TO-HEAD METRIC MATRIX (GREEN = COHORT LEADER)', fontsize=13, fontweight='bold', color=GOLD, pad=15)
plt.colorbar(im, ax=ax, label='Relative Cohort Rank (1.0 = Best in Top 10)', shrink=0.8)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'intra_top10_batters_matrix.png'))
plt.close()
print("Saved intra_top10_batters_matrix.png")

# ── CHART 2: BOWLERS HEAD-TO-HEAD MATRIX HEATMAP ──
fig, ax = plt.subplots(figsize=(14, 7))
metrics_bowl = ['hp_econ', 'wkt_sr', 'wrsa', 'pos_pct', 'wkts', 'rating']
cols_bowl_label = ['HP Economy (Inv)', 'Wicket SR (Inv)', 'Net HP wRSA', 'Positive Match %', 'Total HP Wickets', 'Pressure Rating']

data_bowl = bowl_df[metrics_bowl].values.copy()
norm_bowl = np.zeros_like(data_bowl)
for j in range(data_bowl.shape[1]):
    col = data_bowl[:, j]
    rng = col.max() - col.min()
    if metrics_bowl[j] in ['hp_econ', 'wkt_sr']:
        norm_bowl[:, j] = (col.max() - col) / rng  # lower is better
    else:
        norm_bowl[:, j] = (col - col.min()) / rng

im2 = ax.imshow(norm_bowl, cmap='YlGn', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(len(cols_bowl_label)))
ax.set_xticklabels(cols_bowl_label, fontsize=10, fontweight='bold', rotation=20, ha='right')
ax.set_yticks(range(10))
ax.set_yticklabels(bowl_df['name'].values, fontsize=11, fontweight='bold')

for i in range(10):
    for j in range(len(metrics_bowl)):
        val = data_bowl[i, j]
        fmt = f"{val:.2f}" if j == 0 else (f"{val:.1f}" if j in [1, 5] else f"{val:.0f}")
        if j == 2: fmt = f"+{val:.0f}"
        if j == 3: fmt = f"{val:.1f}%"
        color = 'black' if norm_bowl[i, j] > 0.45 else 'white'
        ax.text(j, i, fmt, ha='center', va='center', fontsize=9, fontweight='bold', color=color)

ax.set_title('TOP 10 BOWLERS: HEAD-TO-HEAD METRIC MATRIX (GREEN = COHORT LEADER)', fontsize=13, fontweight='bold', color=CYAN, pad=15)
plt.colorbar(im2, ax=ax, label='Relative Cohort Rank (1.0 = Best in Top 10)', shrink=0.8)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'intra_top10_bowlers_matrix.png'))
plt.close()
print("Saved intra_top10_bowlers_matrix.png")

print("ALL INTRA-TOP10 VISUALIZATIONS GENERATED SUCCESSFULLY!")
