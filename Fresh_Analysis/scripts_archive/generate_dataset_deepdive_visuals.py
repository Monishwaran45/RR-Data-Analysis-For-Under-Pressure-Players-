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

def kde_np(data, x_grid, bw=None):
    """Pure numpy Gaussian Kernel Density Estimator without scipy."""
    data = np.asarray(data)
    n = len(data)
    if bw is None:
        bw = 1.06 * np.std(data) * (n ** (-1/5))
    bw = max(bw, 1e-4)
    diff = (x_grid[:, None] - data[None, :]) / bw
    dens = np.sum(np.exp(-0.5 * diff**2), axis=1) / (n * bw * np.sqrt(2 * np.pi))
    return dens

def get_kde_val(val, x_grid, dens):
    idx = np.argmin(np.abs(x_grid - val))
    return dens[idx]

# Load complete eligible player datasets
df_bat = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\eda_all_eligible_batters_complete.csv')
df_bowl = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\eda_all_eligible_bowlers_complete.csv')

# Top 10 Batters data
top_batters_data = [
    {'name': 'Tim David', 'hp_sr': 194.59, 'dot_pct': 31.0, 'braa': 449.2, 'hp_balls': 592, 'color': GOLD},
    {'name': 'Shashank Singh', 'hp_sr': 170.88, 'dot_pct': 29.5, 'braa': 165.8, 'hp_balls': 285, 'color': CYAN},
    {'name': 'Rinku Singh', 'hp_sr': 172.15, 'dot_pct': 30.9, 'braa': 313.9, 'hp_balls': 632, 'color': GREEN},
    {'name': 'Rishabh Pant', 'hp_sr': 183.67, 'dot_pct': 31.9, 'braa': 142.7, 'hp_balls': 245, 'color': ORANGE},
    {'name': 'Tristan Stubbs', 'hp_sr': 171.51, 'dot_pct': 24.3, 'braa': 250.6, 'hp_balls': 516, 'color': MAGENTA},
    {'name': 'Tilak Varma', 'hp_sr': 164.38, 'dot_pct': 28.6, 'braa': 275.8, 'hp_balls': 640, 'color': PURPLE},
    {'name': 'Marcus Stoinis', 'hp_sr': 175.32, 'dot_pct': 29.9, 'braa': 158.8, 'hp_balls': 385, 'color': '#79C0FF'},
    {'name': 'Suryakumar Yadav', 'hp_sr': 192.14, 'dot_pct': 28.0, 'braa': 195.3, 'hp_balls': 407, 'color': '#FFA657'},
    {'name': 'Rovman Powell', 'hp_sr': 157.42, 'dot_pct': 34.0, 'braa': 224.4, 'hp_balls': 674, 'color': '#D2A8FF'},
    {'name': 'Dasun Shanaka', 'hp_sr': 156.99, 'dot_pct': 33.6, 'braa': 104.0, 'hp_balls': 386, 'color': '#7EE787'},
]

# Top 10 Bowlers data
top_bowlers_data = [
    {'name': 'Jasprit Bumrah', 'hp_econ': 7.08, 'wkt_sr': 13.05, 'wrsa': 247.1, 'hp_balls': 509, 'color': GOLD},
    {'name': 'Matheesha Pathirana', 'hp_econ': 8.35, 'wkt_sr': 10.27, 'wrsa': 205.9, 'hp_balls': 452, 'color': CYAN},
    {'name': 'Wanindu Hasaranga', 'hp_econ': 7.64, 'wkt_sr': 10.07, 'wrsa': 185.9, 'hp_balls': 453, 'color': GREEN},
    {'name': 'Yuzvendra Chahal', 'hp_econ': 8.57, 'wkt_sr': 12.03, 'wrsa': 182.3, 'hp_balls': 469, 'color': ORANGE},
    {'name': 'Kuldeep Yadav', 'hp_econ': 7.46, 'wkt_sr': 10.61, 'wrsa': 162.3, 'hp_balls': 403, 'color': MAGENTA},
    {'name': 'Sam Curran', 'hp_econ': 10.67, 'wkt_sr': 13.17, 'wrsa': 83.8, 'hp_balls': 316, 'color': PURPLE},
    {'name': 'Sunil Narine', 'hp_econ': 6.27, 'wkt_sr': 15.09, 'wrsa': 115.5, 'hp_balls': 332, 'color': '#79C0FF'},
    {'name': 'Rashid Khan', 'hp_econ': 7.28, 'wkt_sr': 12.55, 'wrsa': 187.7, 'hp_balls': 703, 'color': '#FFA657'},
    {'name': 'Arshdeep Singh', 'hp_econ': 9.22, 'wkt_sr': 11.15, 'wrsa': 166.7, 'hp_balls': 836, 'color': '#D2A8FF'},
    {'name': 'Taskin Ahmed', 'hp_econ': 8.40, 'wkt_sr': 11.92, 'wrsa': 94.8, 'hp_balls': 310, 'color': '#7EE787'},
]

# ─────────────────────────────────────────────────────────────────────────────
# 1. BATTERS DATASET DISTRIBUTION & TOP 10 PINPOINT
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

bat_active = df_bat[df_bat['hp_balls'] >= 15].copy()
sr_vals = bat_active['hp_strike_rate'].dropna().values
dot_vals = bat_active['hp_dot_pct'].dropna().values

# Left: HP Strike Rate Distribution
n, bins, patches = axes[0].hist(sr_vals, bins=40, density=True, color='#21262D', edgecolor='#30363D', alpha=0.6)
x_sr = np.linspace(50, 240, 300)
kde_sr_vals = kde_np(sr_vals, x_sr)
axes[0].plot(x_sr, kde_sr_vals, color=CYAN, linewidth=2, label='Dataset Density (815 Batters)')

median_sr = np.median(sr_vals)
axes[0].axvline(median_sr, color='#8B949E', linestyle='--', linewidth=1.5, label=f'Dataset Median: {median_sr:.1f} SR')
axes[0].axvline(149.4, color=PURPLE, linestyle=':', linewidth=1.5, label='Qualified Median: 149.4 SR')

for p in top_batters_data:
    val = p['hp_sr']
    y_val = get_kde_val(val, x_sr, kde_sr_vals)
    axes[0].scatter(val, y_val, color=p['color'], s=70, zorder=5, edgecolor='white')

axes[0].annotate('Tim David (194.6)', (194.59, get_kde_val(194.59, x_sr, kde_sr_vals)), xytext=(10, 20), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color=GOLD, arrowprops=dict(arrowstyle='->', color=GOLD))
axes[0].annotate('Suryakumar (192.1)', (192.14, get_kde_val(192.14, x_sr, kde_sr_vals)), xytext=(-80, 35), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color='#FFA657', arrowprops=dict(arrowstyle='->', color='#FFA657'))
axes[0].annotate('Rishabh Pant (183.7)', (183.67, get_kde_val(183.67, x_sr, kde_sr_vals)), xytext=(10, 30), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color=ORANGE, arrowprops=dict(arrowstyle='->', color=ORANGE))

axes[0].set_xlabel('High-Pressure Strike Rate (SR)', fontsize=11)
axes[0].set_ylabel('Probability Density', fontsize=11)
axes[0].set_title('HIGH-PRESSURE STRIKE RATE: TOP 10 vs ENTIRE DATASET\nAll Top 10 Batters reside in the 86th to 99th percentile', fontsize=12, fontweight='bold', color=CYAN)
axes[0].grid(alpha=0.25)
axes[0].legend(loc='upper right', fontsize=8.5)

# Right: HP Dot Ball % Distribution
n2, bins2, patches2 = axes[1].hist(dot_vals, bins=40, density=True, color='#21262D', edgecolor='#30363D', alpha=0.6)
x_dot = np.linspace(10, 70, 300)
kde_dot_vals = kde_np(dot_vals, x_dot)
axes[1].plot(x_dot, kde_dot_vals, color=RED, linewidth=2, label='Dataset Density (815 Batters)')

median_dot = np.median(dot_vals)
axes[1].axvline(median_dot, color='#8B949E', linestyle='--', linewidth=1.5, label=f'Dataset Median: {median_dot:.1f}% Dots')

for p in top_batters_data:
    val = p['dot_pct']
    y_val = get_kde_val(val, x_dot, kde_dot_vals)
    axes[1].scatter(val, y_val, color=p['color'], s=70, zorder=5, edgecolor='white')

axes[1].annotate('Tristan Stubbs\n(24.3% Dots | #1 in Cricket)', (24.3, get_kde_val(24.3, x_dot, kde_dot_vals)), xytext=(-60, 30), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color=MAGENTA, arrowprops=dict(arrowstyle='->', color=MAGENTA))
axes[1].annotate('Tilak Varma (28.6%)', (28.6, get_kde_val(28.6, x_dot, kde_dot_vals)), xytext=(-70, 20), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color=PURPLE, arrowprops=dict(arrowstyle='->', color=PURPLE))

axes[1].set_xlabel('High-Pressure Dot Ball Percentage (%) [Lower = Better]', fontsize=11)
axes[1].set_ylabel('Probability Density', fontsize=11)
axes[1].set_title('DOT BALL SUPPRESSION: TOP 10 vs ENTIRE DATASET\nTop 10 Batters eliminate ball wastage (24% to 34% vs 39.2% median)', fontsize=12, fontweight='bold', color=MAGENTA)
axes[1].grid(alpha=0.25)
axes[1].legend(loc='upper right', fontsize=8.5)

plt.suptitle('DATASET-WIDE BENCHMARK: BATTERS POPULATION DISTRIBUTION', fontsize=14, fontweight='bold', color='white', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'viz1_batters_dataset_distribution_and_top10.png'))
plt.close()
print("Saved viz1_batters_dataset_distribution_and_top10.png")


# ─────────────────────────────────────────────────────────────────────────────
# 2. BOWLERS DATASET DISTRIBUTION & TOP 10 PINPOINT
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

bowl_active = df_bowl[df_bowl['hp_balls'] >= 15].copy()
econ_vals = bowl_active['hp_econ'].dropna().values
econ_vals = econ_vals[(econ_vals >= 4.0) & (econ_vals <= 16.0)]
wkt_vals = bowl_active['hp_sr'].dropna().values
wkt_vals = wkt_vals[(wkt_vals >= 5.0) & (wkt_vals <= 45.0)]

# Left: HP Economy Distribution
n, bins, patches = axes[0].hist(econ_vals, bins=40, density=True, color='#21262D', edgecolor='#30363D', alpha=0.6)
x_econ = np.linspace(4.5, 15.5, 300)
kde_econ_vals = kde_np(econ_vals, x_econ)
axes[0].plot(x_econ, kde_econ_vals, color=CYAN, linewidth=2, label='Dataset Density (601 Bowlers)')

median_econ = np.median(econ_vals)
axes[0].axvline(median_econ, color='#8B949E', linestyle='--', linewidth=1.5, label=f'Dataset Median: {median_econ:.2f} RPO')

for p in top_bowlers_data:
    val = p['hp_econ']
    y_val = get_kde_val(val, x_econ, kde_econ_vals) if (val >= 4.5 and val <= 15.5) else 0.02
    axes[0].scatter(val, y_val, color=p['color'], s=70, zorder=5, edgecolor='white')

axes[0].annotate('Sunil Narine (6.27)', (6.27, get_kde_val(6.27, x_econ, kde_econ_vals)), xytext=(-60, 30), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color='#79C0FF', arrowprops=dict(arrowstyle='->', color='#79C0FF'))
axes[0].annotate('Jasprit Bumrah (7.08)', (7.08, get_kde_val(7.08, x_econ, kde_econ_vals)), xytext=(-70, 45), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color=GOLD, arrowprops=dict(arrowstyle='->', color=GOLD))
axes[0].annotate('Rashid Khan (7.28)', (7.28, get_kde_val(7.28, x_econ, kde_econ_vals)), xytext=(10, 35), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color='#FFA657', arrowprops=dict(arrowstyle='->', color='#FFA657'))
axes[0].annotate('Sam Curran (10.67)\n[Defends 12.5 Par]', (10.67, get_kde_val(10.67, x_econ, kde_econ_vals)), xytext=(10, 25), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color=PURPLE, arrowprops=dict(arrowstyle='->', color=PURPLE))

axes[0].set_xlabel('High-Pressure Economy Rate (RPO) [Lower = Better]', fontsize=11)
axes[0].set_ylabel('Probability Density', fontsize=11)
axes[0].set_title('HIGH-PRESSURE ECONOMY: TOP 10 vs ENTIRE DATASET\nChoke masters suppress scoring deep into the left tail', fontsize=12, fontweight='bold', color=CYAN)
axes[0].grid(alpha=0.25)
axes[0].legend(loc='upper right', fontsize=8.5)

# Right: HP Wicket Strike Rate Distribution
n2, bins2, patches2 = axes[1].hist(wkt_vals, bins=40, density=True, color='#21262D', edgecolor='#30363D', alpha=0.6)
x_wkt = np.linspace(6.0, 40.0, 300)
kde_wkt_vals = kde_np(wkt_vals, x_wkt)
axes[1].plot(x_wkt, kde_wkt_vals, color=GREEN, linewidth=2, label='Dataset Density (601 Bowlers)')

median_wkt = np.median(wkt_vals)
axes[1].axvline(median_wkt, color='#8B949E', linestyle='--', linewidth=1.5, label=f'Dataset Median: {median_wkt:.1f} balls/wkt')

for p in top_bowlers_data:
    val = p['wkt_sr']
    y_val = get_kde_val(val, x_wkt, kde_wkt_vals) if (val >= 6.0 and val <= 40.0) else 0.02
    axes[1].scatter(val, y_val, color=p['color'], s=70, zorder=5, edgecolor='white')

axes[1].annotate('Hasaranga (10.07)', (10.07, get_kde_val(10.07, x_wkt, kde_wkt_vals)), xytext=(-70, 35), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color=GREEN, arrowprops=dict(arrowstyle='->', color=GREEN))
axes[1].annotate('Pathirana (10.27)', (10.27, get_kde_val(10.27, x_wkt, kde_wkt_vals)), xytext=(10, 25), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color=CYAN, arrowprops=dict(arrowstyle='->', color=CYAN))
axes[1].annotate('Kuldeep (10.61)', (10.61, get_kde_val(10.61, x_wkt, kde_wkt_vals)), xytext=(10, 40), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color=MAGENTA, arrowprops=dict(arrowstyle='->', color=MAGENTA))

axes[1].set_xlabel('High-Pressure Wicket Strike Rate (Balls / Wicket) [Lower = Faster Strike]', fontsize=11)
axes[1].set_ylabel('Probability Density', fontsize=11)
axes[1].set_title('WICKET-STRIKE VELOCITY: TOP 10 vs ENTIRE DATASET\nTop 10 take a wicket every 10 to 13 balls (vs 17.0 median)', fontsize=12, fontweight='bold', color=GREEN)
axes[1].grid(alpha=0.25)
axes[1].legend(loc='upper right', fontsize=8.5)

plt.suptitle('DATASET-WIDE BENCHMARK: BOWLERS POPULATION DISTRIBUTION', fontsize=14, fontweight='bold', color='white', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'viz1_bowlers_dataset_distribution_and_top10.png'))
plt.close()
print("Saved viz1_bowlers_dataset_distribution_and_top10.png")


# ─────────────────────────────────────────────────────────────────────────────
# 3. MACRO SCATTER: ALL 815 BATTERS vs TOP 10 (bRAA vs HP SR)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 8))

bg_bat = df_bat[df_bat['hp_balls'] >= 10].copy()
bg_sr = bg_bat['hp_strike_rate'].values
bg_braa = (bg_bat['hp_runs'] - bg_bat['hp_balls'] * 1.45) * 0.7

ax.scatter(bg_sr, bg_braa, color='#8B949E', alpha=0.25, s=30, label='Eligible Batters Cloud (815 Players)')

for p in top_batters_data:
    ax.scatter(p['hp_sr'], p['braa'], s=p['hp_balls']*0.9, color=p['color'], alpha=0.85,
               edgecolor='white', linewidth=1.5, zorder=5)
    
    dx, dy = 3, 5
    if p['name'] == 'Tim David': dy = -16
    elif p['name'] == 'Rinku Singh': dy = 10
    elif p['name'] == 'Suryakumar Yadav': dy = -16
    elif p['name'] == 'Tristan Stubbs': dx = -90; dy = 10
    elif p['name'] == 'Tilak Varma': dx = -80; dy = -15
    elif p['name'] == 'Shashank Singh': dx = -90; dy = 5
    
    ax.annotate(f"{p['name']}\n({p['hp_sr']:.1f} SR | +{p['braa']:.0f} bRAA)",
                (p['hp_sr'], p['braa']),
                xytext=(dx, dy), textcoords='offset points',
                fontsize=9, fontweight='bold', color=p['color'])

ax.axvline(128.4, color='#8B949E', linestyle='--', alpha=0.5, label='Dataset Median SR (128.4)')
ax.axhline(0, color=RED, linestyle=':', alpha=0.6, label='Breakeven Par Expectation (bRAA = 0)')

ax.set_xlabel('High-Pressure Strike Rate (P_t >= 0.50)', fontsize=12)
ax.set_ylabel('Net Context-Adjusted Runs Above Average (bRAA)', fontsize=12)
ax.set_title('BATTERS MACRO LANDSCAPE: ALL 815 PLAYERS vs TOP 10 UNDER PRESSURE\nBubble size represents high-pressure balls faced | Top-Right Quadrant = Elite Match Winners', fontsize=13, fontweight='bold', color='white', pad=15)
ax.set_xlim(80, 220)
ax.set_ylim(-120, 500)
ax.grid(alpha=0.25)
ax.legend(loc='upper left', fontsize=9.5, framealpha=0.8)

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'viz3_batters_macro_landscape_braa_scatter.png'))
plt.close()
print("Saved viz3_batters_macro_landscape_braa_scatter.png")


# ─────────────────────────────────────────────────────────────────────────────
# 4. MACRO SCATTER: ALL 601 BOWLERS vs TOP 10 (wRSA vs HP ECONOMY)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 8))

bg_bowl = df_bowl[df_bowl['hp_balls'] >= 10].copy()
bg_econ = bg_bowl['hp_econ'].values
bg_wrsa = (bg_bowl['hp_balls'] * 1.65 - bg_bowl['hp_runs']) * 0.65

ax.scatter(bg_econ, bg_wrsa, color='#8B949E', alpha=0.25, s=30, label='Eligible Bowlers Cloud (601 Players)')

for p in top_bowlers_data:
    ax.scatter(p['hp_econ'], p['wrsa'], s=p['hp_balls']*0.9, color=p['color'], alpha=0.85,
               edgecolor='white', linewidth=1.5, zorder=5)
    
    dx, dy = 3, 5
    if p['name'] == 'Jasprit Bumrah': dy = 12
    elif p['name'] == 'Matheesha Pathirana': dy = 10
    elif p['name'] == 'Rashid Khan': dy = -16
    elif p['name'] == 'Sam Curran': dy = -16
    elif p['name'] == 'Sunil Narine': dx = -80; dy = 10
    elif p['name'] == 'Kuldeep Yadav': dx = -80; dy = -15
    elif p['name'] == 'Wanindu Hasaranga': dx = -100; dy = 5
    
    ax.annotate(f"{p['name']}\n({p['hp_econ']:.2f} RPO | +{p['wrsa']:.0f} wRSA)",
                (p['hp_econ'], p['wrsa']),
                xytext=(dx, dy), textcoords='offset points',
                fontsize=9, fontweight='bold', color=p['color'])

ax.invert_xaxis()
ax.axvline(9.82, color='#8B949E', linestyle='--', alpha=0.5, label='Dataset Median Econ (9.82 RPO)')
ax.axhline(0, color=RED, linestyle=':', alpha=0.6, label='Breakeven Par Expectation (wRSA = 0)')

ax.set_xlabel('High-Pressure Economy Rate (Inverted: Left to Right = Lower Economy / Better Choke)', fontsize=12)
ax.set_ylabel('Net Context-Adjusted Runs Saved (wRSA)', fontsize=12)
ax.set_title('BOWLERS MACRO LANDSCAPE: ALL 601 PLAYERS vs TOP 10 UNDER PRESSURE\nBubble size represents high-pressure balls bowled | Top-Right Quadrant = Elite Choke & Wickets', fontsize=13, fontweight='bold', color='white', pad=15)
ax.set_xlim(13.5, 5.0)
ax.set_ylim(-100, 300)
ax.grid(alpha=0.25)
ax.legend(loc='upper left', fontsize=9.5, framealpha=0.8)

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'viz4_bowlers_macro_landscape_wrsa_scatter.png'))
plt.close()
print("Saved viz4_bowlers_macro_landscape_wrsa_scatter.png")


# ─────────────────────────────────────────────────────────────────────────────
# 5. COHORT GAP BENCHMARKS: DATASET MEDIAN vs QUALIFIED vs TOP 10
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

bat_metrics = ['HP Strike Rate\n(SR)', 'Dot Ball %\n(Lower=Better)', 'Boundary %\n(Higher=Better)']
median_bat = [128.4, 39.2, 14.8]
qual_bat = [149.4, 33.4, 18.8]
top10_bat = [176.8, 28.2, 26.4]

x = np.arange(len(bat_metrics))
w = 0.25

b1 = axes[0].bar(x - w, median_bat, width=w, color='#8B949E', label='Entire Dataset Median (815 Batters)', edgecolor='#30363D')
b2 = axes[0].bar(x, qual_bat, width=w, color=PURPLE, label='Qualified Cohort Avg (124 Batters)', edgecolor='#30363D')
b3 = axes[0].bar(x + w, top10_bat, width=w, color=GOLD, label='Final Top 10 Elite Avg', edgecolor='#30363D')

axes[0].set_xticks(x)
axes[0].set_xticklabels(bat_metrics, fontsize=10, fontweight='bold')
axes[0].set_title('BATTING COHORT GAPS: MEDIAN vs QUALIFIED vs TOP 10', fontsize=12, fontweight='bold', color=GOLD)
axes[0].set_ylabel('Metric Value', fontsize=11)
axes[0].grid(axis='y', alpha=0.25)
axes[0].legend(loc='upper right', fontsize=9)

for rect in b1 + b2 + b3:
    h = rect.get_height()
    axes[0].text(rect.get_x() + rect.get_width()/2., h + 2, f"{h:.1f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='white')
axes[0].set_ylim(0, 205)

bowl_metrics = ['HP Economy\n(Lower=Better)', 'Wicket SR\n(Lower=Better)', 'Boundary Conc %\n(Lower=Better)']
median_bowl = [9.82, 17.0, 21.9]
qual_bowl = [10.29, 17.8, 21.9]
top10_bowl = [7.95, 11.9, 14.8]

b4 = axes[1].bar(x - w, median_bowl, width=w, color='#8B949E', label='Entire Dataset Median (601 Bowlers)', edgecolor='#30363D')
b5 = axes[1].bar(x, qual_bowl, width=w, color=PURPLE, label='Qualified Cohort Avg (45 Bowlers)', edgecolor='#30363D')
b6 = axes[1].bar(x + w, top10_bowl, width=w, color=CYAN, label='Final Top 10 Elite Avg', edgecolor='#30363D')

axes[1].set_xticks(x)
axes[1].set_xticklabels(bowl_metrics, fontsize=10, fontweight='bold')
axes[1].set_title('BOWLING COHORT GAPS: MEDIAN vs QUALIFIED vs TOP 10', fontsize=12, fontweight='bold', color=CYAN)
axes[1].set_ylabel('Metric Value', fontsize=11)
axes[1].grid(axis='y', alpha=0.25)
axes[1].legend(loc='upper right', fontsize=9)

for rect in b4 + b5 + b6:
    h = rect.get_height()
    axes[1].text(rect.get_x() + rect.get_width()/2., h + 0.3, f"{h:.1f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='white')
axes[1].set_ylim(0, 26)

plt.suptitle('THE STATISTICAL GAP: HOW THE TOP 10 SEPARATE FROM THE CRICKET POPULATION', fontsize=14, fontweight='bold', color='white', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'viz5_cohort_gap_benchmarks_grouped_bar.png'))
plt.close()
print("Saved viz5_cohort_gap_benchmarks_grouped_bar.png")

print("ALL 5 DEEP-DIVE COMPARATIVE VISUALIZATIONS GENERATED SUCCESSFULLY (PURE NUMPY)!")
