import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\comparison_charts'
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
BLUE = '#388BFD'

# ─────────────────────────────────────────────────────────────────────────────
# 1. BATTERS COMPARISON: EXISTING MASTER vs EXISTING FRESH vs GEMINI HYDROGEN
# ─────────────────────────────────────────────────────────────────────────────
# Key shared and top players across models
players_bat = [
    'Tim David', 'Tristan Stubbs', 'Rinku Singh', 'Suryakumar Yadav',
    'Marcus Stoinis', 'Naman Dhir', 'Shashank Singh', 'Tilak Varma',
    'Rishabh Pant', 'Jos Buttler', 'Rovman Powell'
]

# Ranks in Master (A), Fresh (B), Hydrogen (H) - using 15 if unranked
ranks_a = [2, 8, 9, 1, 7, 4, 15, 6, 12, 3, 10]
ranks_b = [25, 1, 3, 8, 4, 2, 6, 17, 9, 20, 35]
ranks_h = [1, 5, 3, 8, 7, 12, 2, 6, 4, 15, 9]

# Scores / Ratings
score_a = [79.11, 75.41, 74.56, 84.38, 75.85, 77.70, 68.20, 76.02, 69.40, 79.02, 73.78]
score_b = [62.43, 81.66, 75.76, 72.21, 74.44, 78.29, 73.10, 67.77, 71.70, 60.00, 59.52]
score_h = [47.12, 30.24, 31.84, 21.62, 23.45, 18.50, 32.36, 26.27, 31.17, 15.00, 20.39]

fig, ax = plt.subplots(figsize=(14, 8))
y = np.arange(len(players_bat))
height = 0.25

rects1 = ax.barh(y - height, [100 - r*4 for r in ranks_a], height, label='Existing Master Model (Rate & Delta)', color=CYAN, edgecolor='#30363D')
rects2 = ax.barh(y, [100 - r*4 for r in ranks_b], height, label='Existing Fresh Model (Death Crisis Focus)', color=MAGENTA, edgecolor='#30363D')
rects3 = ax.barh(y + height, [100 - r*4 for r in ranks_h], height, label='Gemini Hydrogen Model (bRAA Context Par)', color=GOLD, edgecolor='#30363D')

ax.set_yticks(y)
ax.set_yticklabels(players_bat, fontsize=11, fontweight='bold')
ax.invert_yaxis()
ax.set_xlabel('Comparative Rank Power (Higher = Closer to #1)', fontsize=12)
ax.set_title('TOP BATTERS UNDER PRESSURE: MODEL-BY-MODEL RANK CONVERGENCE\nExisting Master vs Existing Fresh vs Gemini Hydrogen Model', fontsize=14, fontweight='bold', color='white', pad=15)
ax.legend(loc='lower right', fontsize=10, framealpha=0.8)
ax.grid(axis='x', alpha=0.25)

# Annotate exact ranks
for i in range(len(players_bat)):
    ra = f"#{ranks_a[i]}" if ranks_a[i] <= 10 else ">10"
    rb = f"#{ranks_b[i]}" if ranks_b[i] <= 10 else ">10"
    rh = f"#{ranks_h[i]}" if ranks_h[i] <= 10 else ">10"
    ax.text(100 - ranks_a[i]*4 + 1.2, i - height, ra, va='center', fontsize=9, fontweight='bold', color=CYAN)
    ax.text(100 - ranks_b[i]*4 + 1.2, i, rb, va='center', fontsize=9, fontweight='bold', color=MAGENTA)
    ax.text(100 - ranks_h[i]*4 + 1.2, i + height, rh, va='center', fontsize=9, fontweight='bold', color=GOLD)

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'comp_batters_rank_comparison.png'))
plt.close()
print("Saved comp_batters_rank_comparison.png")


# ─────────────────────────────────────────────────────────────────────────────
# 2. BOWLERS COMPARISON: EXISTING MASTER vs EXISTING FRESH vs GEMINI HYDROGEN
# ─────────────────────────────────────────────────────────────────────────────
players_bowl = [
    'Jasprit Bumrah', 'Rashid Khan', 'Matheesha Pathirana', 'Varun Chakravarthy',
    'Mitchell Santner', 'Sam Curran', 'Arshdeep Singh', 'Kuldeep Yadav',
    'Nandre Burger', 'Yuzvendra Chahal', 'Maheesh Theekshana'
]

b_ranks_a = [31, 1, 18, 5, 9, 2, 4, 15, 12, 14, 3]
b_ranks_b = [25, 18, 3, 2, 6, 74, 41, 10, 1, 16, 13]
b_ranks_h = [1, 8, 2, 12, 14, 6, 9, 5, 15, 4, 11]

fig, ax = plt.subplots(figsize=(14, 8))
y = np.arange(len(players_bowl))

rects1 = ax.barh(y - height, [100 - r*3 for r in b_ranks_a], height, label='Existing Master Model (Rate & Context)', color=CYAN, edgecolor='#30363D')
rects2 = ax.barh(y, [100 - r*3 for r in b_ranks_b], height, label='Existing Fresh Model (Delta Econ & Choke)', color=MAGENTA, edgecolor='#30363D')
rects3 = ax.barh(y + height, [100 - r*3 for r in b_ranks_h], height, label='Gemini Hydrogen Model (wRSA Runs Saved)', color=GOLD, edgecolor='#30363D')

ax.set_yticks(y)
ax.set_yticklabels(players_bowl, fontsize=11, fontweight='bold')
ax.invert_yaxis()
ax.set_xlabel('Comparative Rank Power (Higher = Closer to #1)', fontsize=12)
ax.set_title('TOP BOWLERS UNDER PRESSURE: MODEL-BY-MODEL RANK CONVERGENCE\nExisting Master vs Existing Fresh vs Gemini Hydrogen Model', fontsize=14, fontweight='bold', color='white', pad=15)
ax.legend(loc='lower right', fontsize=10, framealpha=0.8)
ax.grid(axis='x', alpha=0.25)

for i in range(len(players_bowl)):
    ra = f"#{b_ranks_a[i]}" if b_ranks_a[i] <= 10 else ">10"
    rb = f"#{b_ranks_b[i]}" if b_ranks_b[i] <= 10 else ">10"
    rh = f"#{b_ranks_h[i]}" if b_ranks_h[i] <= 10 else ">10"
    ax.text(100 - b_ranks_a[i]*3 + 1.2, i - height, ra, va='center', fontsize=9, fontweight='bold', color=CYAN)
    ax.text(100 - b_ranks_b[i]*3 + 1.2, i, rb, va='center', fontsize=9, fontweight='bold', color=MAGENTA)
    ax.text(100 - b_ranks_h[i]*3 + 1.2, i + height, rh, va='center', fontsize=9, fontweight='bold', color=GOLD)

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'comp_bowlers_rank_comparison.png'))
plt.close()
print("Saved comp_bowlers_rank_comparison.png")


# ─────────────────────────────────────────────────────────────────────────────
# 3. METHODOLOGY ARCHITECTURE: DELIVERIES SPLIT & DYNAMIC WICKET VALUE
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Left: High-Pressure Deliveries Volume comparison
models = ['Gemini Hydrogen\n(Pt >= 0.50)', 'Existing Master\n(PI >= 65)', 'Existing Fresh\n(PI >= 65 Strict)']
hp_vols = [47199, 35412, 27903]
ord_vols = [153800, 165587, 144969]
pcts = [23.48, 17.62, 16.14]

x = np.arange(len(models))
b1 = axes[0].bar(x, hp_vols, color=RED, alpha=0.85, label='High-Pressure Deliveries', edgecolor='#30363D', width=0.55)
axes[0].set_xticks(x)
axes[0].set_xticklabels(models, fontsize=10, fontweight='bold')
axes[0].set_ylabel('High-Pressure Deliveries Count', fontsize=11)
axes[0].set_title('HIGH-PRESSURE REGIME SAMPLE SIZE COMPARISON', fontsize=12, fontweight='bold', color=GOLD)
axes[0].grid(axis='y', alpha=0.25)

for i, rect in enumerate(b1):
    h = rect.get_height()
    axes[0].text(rect.get_x() + rect.get_width()/2., h + 1000,
                 f"{h:,} balls\n({pcts[i]:.1f}%)",
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color='white')

axes[0].set_ylim(0, 56000)

# Right: Dynamic Wicket Value V_W(t) Decay Curve
balls_rem = np.linspace(120, 1, 120)
vw = 6.0 + 11.0 * (balls_rem / 120.0)
static_vw = [12.0] * 120

axes[1].plot(120 - balls_rem, vw, color=GOLD, linewidth=3, label='Hydrogen Dynamic Wicket Value V_W(t)')
axes[1].axhline(12.0, color=CYAN, linestyle='--', linewidth=2, label='Traditional Static Wicket Value (12 runs)')
axes[1].fill_between(120 - balls_rem, vw, 12.0, where=(vw >= 12.0), color=GOLD, alpha=0.15)
axes[1].fill_between(120 - balls_rem, vw, 12.0, where=(vw < 12.0), color=RED, alpha=0.15)

axes[1].set_xlabel('Innings Progression (Over 1 to Over 20)', fontsize=11)
axes[1].set_ylabel('Wicket Run-Value (Runs Cost)', fontsize=11)
axes[1].set_title('DYNAMIC WICKET RUN-VALUE DECAY CURVE (V_W)\nOver 1 dismissal costs 17.0 runs vs Over 20 cost of 6.1 runs', fontsize=12, fontweight='bold', color=CYAN)
axes[1].set_xticks([0, 36, 60, 90, 114, 120])
axes[1].set_xticklabels(['Over 1\n(16.9 r)', 'Over 6\n(PP End)', 'Over 10\n(11.5 r)', 'Over 15\n(8.8 r)', 'Over 19\n(6.6 r)', 'Over 20\n(6.1 r)'])
axes[1].grid(alpha=0.25)
axes[1].legend(loc='upper right', fontsize=9)

plt.suptitle('METHODOLOGY & REGIME CALIBRATION ARCHITECTURE', fontsize=14, fontweight='bold', color='white', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'comp_methodology_regime_split.png'))
plt.close()
print("Saved comp_methodology_regime_split.png")


# ─────────────────────────────────────────────────────────────────────────────
# 4. BATTERS SCATTER: NET bRAA vs HIGH-PRESSURE STRIKE RATE
# ─────────────────────────────────────────────────────────────────────────────
bat_names_scatter = ['Tim David', 'Shashank Singh', 'Rinku Singh', 'Rishabh Pant',
                     'Tristan Stubbs', 'Tilak Varma', 'Marcus Stoinis', 'Suryakumar Yadav',
                     'Rovman Powell', 'Dasun Shanaka', 'Jos Buttler', 'Naman Dhir']
hp_sr_scatter = [194.59, 170.88, 172.15, 183.67, 171.51, 164.38, 175.32, 192.14, 157.42, 156.99, 205.40, 202.80]
braa_scatter = [449.2, 165.8, 313.9, 142.7, 250.6, 275.8, 158.8, 195.3, 224.4, 104.0, 180.0, 155.0]
balls_scatter = [592, 285, 632, 245, 516, 640, 385, 407, 674, 386, 147, 142]
tiers = ['Triple Core', 'Dual Model', 'Triple Core', 'Dual Model', 'Triple Core', 'Triple Core', 'Triple Core', 'Triple Core', 'Dual Model', 'Dual Model', 'Master Specialist', 'Dual Model']

color_map = {'Triple Core': GOLD, 'Dual Model': CYAN, 'Master Specialist': MAGENTA}

fig, ax = plt.subplots(figsize=(12, 8))

for i, name in enumerate(bat_names_scatter):
    c = color_map[tiers[i]]
    s = balls_scatter[i] / 1.5
    ax.scatter(hp_sr_scatter[i], braa_scatter[i], s=s, color=c, alpha=0.8, edgecolor='white', linewidth=1.2, zorder=4)
    # Offset labels smartly
    dx, dy = 1.2, 8
    if name == 'Tim David':
        dy = -15
    elif name == 'Rinku Singh':
        dy = 12
    elif name == 'Suryakumar Yadav':
        dy = -15
    elif name == 'Naman Dhir':
        dy = -15
    ax.annotate(f"{name}\n({hp_sr_scatter[i]:.1f} SR | +{braa_scatter[i]:.0f} bRAA)",
                (hp_sr_scatter[i], braa_scatter[i]),
                xytext=(dx, dy), textcoords='offset points',
                fontsize=9, fontweight='bold', color=c)

# Reference benchmark lines
ax.axvline(170, color='#8B949E', linestyle=':', alpha=0.5, label='High-Pressure SR Benchmark (170)')
ax.axhline(200, color='#8B949E', linestyle=':', alpha=0.5, label='Elite +200 Net bRAA Benchmark')

ax.set_xlabel('High-Pressure Strike Rate (P_t >= 0.50 / PI >= 65)', fontsize=12)
ax.set_ylabel('Net Context-Adjusted Runs Above Average (bRAA)', fontsize=12)
ax.set_title('BATTERS CONSENSUS MATRIX: STRIKE RATE vs RUNS ABOVE AVERAGE (bRAA)\nBubble size proportional to high-pressure balls faced', fontsize=13, fontweight='bold', color='white', pad=15)

# Custom legend
from matplotlib.lines import Line2D
custom_lines = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=GOLD, markersize=10, label='Triple Consensus Core (Top in All Models)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=CYAN, markersize=10, label='Dual Model Leader (Top in 2 Models)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=MAGENTA, markersize=10, label='Rate Specialist (High SR, Lower Sample)'),
]
ax.legend(handles=custom_lines, loc='upper left', fontsize=9, framealpha=0.8)
ax.grid(alpha=0.25)

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'comp_batters_braa_vs_sr.png'))
plt.close()
print("Saved comp_batters_braa_vs_sr.png")


# ─────────────────────────────────────────────────────────────────────────────
# 5. BOWLERS SCATTER: NET wRSA vs HIGH-PRESSURE ECONOMY
# ─────────────────────────────────────────────────────────────────────────────
bowl_names_scatter = ['Jasprit Bumrah', 'Matheesha Pathirana', 'Wanindu Hasaranga',
                      'Yuzvendra Chahal', 'Kuldeep Yadav', 'Sam Curran',
                      'Sunil Narine', 'Rashid Khan', 'Arshdeep Singh', 'Taskin Ahmed',
                      'Varun Chakravarthy', 'Nandre Burger']
hp_econ_scatter = [7.08, 8.35, 7.64, 8.57, 7.46, 10.67, 6.27, 7.28, 9.22, 8.40, 6.52, 5.61]
wrsa_scatter = [247.1, 205.9, 185.9, 182.3, 162.3, 83.8, 115.5, 187.7, 166.7, 94.8, 140.0, 95.0]
bowl_balls_scatter = [509, 452, 453, 469, 403, 316, 332, 703, 836, 310, 208, 61]
bowl_tiers = ['Triple Core', 'Triple Core', 'Dual Model', 'Dual Model', 'Triple Core', 'Triple Core', 'Dual Model', 'Triple Core', 'Triple Core', 'Dual Model', 'Rate Choke Elite', 'Rate Choke Elite']

b_color_map = {'Triple Core': GOLD, 'Dual Model': CYAN, 'Rate Choke Elite': MAGENTA}

fig, ax = plt.subplots(figsize=(12, 8))

for i, name in enumerate(bowl_names_scatter):
    c = b_color_map[bowl_tiers[i]]
    s = bowl_balls_scatter[i] / 1.5
    ax.scatter(hp_econ_scatter[i], wrsa_scatter[i], s=s, color=c, alpha=0.8, edgecolor='white', linewidth=1.2, zorder=4)
    dx, dy = 1.2, 8
    if name == 'Jasprit Bumrah':
        dy = 12
    elif name == 'Matheesha Pathirana':
        dy = 10
    elif name == 'Rashid Khan':
        dy = -15
    elif name == 'Sam Curran':
        dy = -15
    ax.annotate(f"{name}\n({hp_econ_scatter[i]:.2f} Econ | +{wrsa_scatter[i]:.0f} wRSA)",
                (hp_econ_scatter[i], wrsa_scatter[i]),
                xytext=(dx, dy), textcoords='offset points',
                fontsize=9, fontweight='bold', color=c)

ax.invert_xaxis()  # Lower economy is better, so move lower economy to the right!
ax.set_xlabel('High-Pressure Economy Rate (Inverted: Left to Right = Lower Economy / Better Choke)', fontsize=12)
ax.set_ylabel('Net Context-Adjusted Runs Saved Above Average (wRSA)', fontsize=12)
ax.set_title('BOWLERS CONSENSUS MATRIX: CHOKE ECONOMY vs RUNS SAVED (wRSA)\nBubble size proportional to high-pressure balls bowled', fontsize=13, fontweight='bold', color='white', pad=15)

custom_lines_b = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=GOLD, markersize=10, label='Triple Consensus Core (Top in All Models)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=CYAN, markersize=10, label='Dual Model Leader (Top in 2 Models)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=MAGENTA, markersize=10, label='Pure Economy Stranglers (Low sample or lower wRSA)'),
]
ax.legend(handles=custom_lines_b, loc='upper right', fontsize=9, framealpha=0.8)
ax.grid(alpha=0.25)

plt.tight_layout()
plt.savefig(os.path.join(OUT, 'comp_bowlers_wrsa_vs_econ.png'))
plt.close()
print("Saved comp_bowlers_wrsa_vs_econ.png")

print("ALL 5 COMPARATIVE VISUALIZATIONS GENERATED SUCCESSFULLY!")
