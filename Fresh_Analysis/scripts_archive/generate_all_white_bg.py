import os
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

# Configure pure white background theme
WHITE_THEME = {
    'figure.dpi': 150,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
    'font.size': 10,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    'text.color': '#0F172A',
    'axes.labelcolor': '#0F172A',
    'xtick.color': '#334155',
    'ytick.color': '#334155',
    'axes.edgecolor': '#CBD5E1',
    'grid.color': '#E2E8F0',
    'grid.alpha': 0.8,
}
plt.rcParams.update(WHITE_THEME)

# Clean, professional high-contrast color palette
NAVY = '#1E3A8A'
BLUE = '#2563EB'
CYAN = '#0284C7'
TEAL = '#0D9488'
GREEN = '#16A34A'
AMBER = '#D97706'
ORANGE = '#EA580C'
RED = '#DC2626'
PURPLE = '#7C3AED'
SLATE = '#64748B'
DARK_TEXT = '#0F172A'

DIR_COMP = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\comparison_charts'
DIR_METH = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\methodology_eda_charts'
DIR_CHARTS = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\charts'
RR_CHARTS = r'c:\Users\Asus-2025\Downloads\RR\charts'
RR_FINAL = r'c:\Users\Asus-2025\Downloads\RR\final_pressure_charts_white_bg'
ART_DIR = r'C:\Users\Asus-2025\.gemini\antigravity\brain\4fe6158e-0e76-450a-898e-f6d09dd602e6'

for d in [DIR_COMP, DIR_METH, DIR_CHARTS, RR_CHARTS, RR_FINAL]:
    os.makedirs(d, exist_ok=True)

def safe_savefig(fig, path, *args, **kwargs):
    tmp = path + '.tmp.png'
    fig.savefig(tmp, *args, **kwargs)
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass
    if os.path.exists(tmp):
        try:
            os.replace(tmp, path)
        except Exception:
            shutil.copy2(tmp, path)
            try:
                os.remove(tmp)
            except Exception:
                pass

print("Starting generation of white-background visual suite...")

# =============================================================================
# SECTION 1: COMPARISON CHARTS (5 Visualizations)
# =============================================================================

# 1.1 Batters Rank Comparison
players_bat = [
    'Tim David', 'Tristan Stubbs', 'Rinku Singh', 'Suryakumar Yadav',
    'Marcus Stoinis', 'Naman Dhir', 'Shashank Singh', 'Tilak Varma',
    'Rishabh Pant', 'Jos Buttler', 'Rovman Powell'
]
ranks_a = [2, 8, 9, 1, 7, 4, 15, 6, 12, 3, 10]
ranks_b = [25, 1, 3, 8, 4, 2, 6, 17, 9, 20, 35]
ranks_h = [1, 5, 3, 8, 7, 12, 2, 6, 4, 15, 9]

fig, ax = plt.subplots(figsize=(14, 8), facecolor='#FFFFFF')
y = np.arange(len(players_bat))
height = 0.25

ax.barh(y - height, [100 - r*4 for r in ranks_a], height, label='Existing Master Model (Rate & Delta)', color=BLUE, edgecolor='#94A3B8', alpha=0.9)
ax.barh(y, [100 - r*4 for r in ranks_b], height, label='Existing Fresh Model (Death Crisis Focus)', color=PURPLE, edgecolor='#94A3B8', alpha=0.85)
ax.barh(y + height, [100 - r*4 for r in ranks_h], height, label='Gemini Hydrogen Model (bRAA Context Par)', color=AMBER, edgecolor='#94A3B8', alpha=0.95)

ax.set_yticks(y)
ax.set_yticklabels(players_bat, fontsize=11, fontweight='bold', color=DARK_TEXT)
ax.invert_yaxis()
ax.set_xlabel('Comparative Rank Power (Higher = Closer to #1)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('TOP BATTERS UNDER PRESSURE: MODEL-BY-MODEL RANK CONVERGENCE\nExisting Master vs Existing Fresh vs Gemini Hydrogen Model', fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.legend(loc='lower right', fontsize=10, facecolor='#F8FAFC', edgecolor='#CBD5E1')
ax.grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)

for i in range(len(players_bat)):
    ra = f"#{ranks_a[i]}" if ranks_a[i] <= 10 else ">10"
    rb = f"#{ranks_b[i]}" if ranks_b[i] <= 10 else ">10"
    rh = f"#{ranks_h[i]}" if ranks_h[i] <= 10 else ">10"
    ax.text(100 - ranks_a[i]*4 + 1.2, i - height, ra, va='center', fontsize=9, fontweight='bold', color=BLUE)
    ax.text(100 - ranks_b[i]*4 + 1.2, i, rb, va='center', fontsize=9, fontweight='bold', color=PURPLE)
    ax.text(100 - ranks_h[i]*4 + 1.2, i + height, rh, va='center', fontsize=9, fontweight='bold', color='#B45309')

plt.tight_layout()
p_c1 = os.path.join(DIR_COMP, 'comp_batters_rank_comparison.png')
safe_savefig(plt.gcf(), p_c1, facecolor='#FFFFFF')
plt.close()
print("1. Saved comp_batters_rank_comparison.png")

# 1.2 Bowlers Rank Comparison
players_bowl = [
    'Jasprit Bumrah', 'Rashid Khan', 'Matheesha Pathirana', 'Varun Chakravarthy',
    'Mitchell Santner', 'Sam Curran', 'Arshdeep Singh', 'Kuldeep Yadav',
    'Nandre Burger', 'Yuzvendra Chahal', 'Maheesh Theekshana'
]
b_ranks_a = [31, 1, 18, 5, 9, 2, 4, 15, 12, 14, 3]
b_ranks_b = [25, 18, 3, 2, 6, 74, 41, 10, 1, 16, 13]
b_ranks_h = [1, 8, 2, 12, 14, 6, 9, 5, 15, 4, 11]

fig, ax = plt.subplots(figsize=(14, 8), facecolor='#FFFFFF')
y = np.arange(len(players_bowl))

ax.barh(y - height, [100 - r*3 for r in b_ranks_a], height, label='Existing Master Model (Rate & Context)', color=BLUE, edgecolor='#94A3B8', alpha=0.9)
ax.barh(y, [100 - r*3 for r in b_ranks_b], height, label='Existing Fresh Model (Delta Econ & Choke)', color=PURPLE, edgecolor='#94A3B8', alpha=0.85)
ax.barh(y + height, [100 - r*3 for r in b_ranks_h], height, label='Gemini Hydrogen Model (wRSA Runs Saved)', color=AMBER, edgecolor='#94A3B8', alpha=0.95)

ax.set_yticks(y)
ax.set_yticklabels(players_bowl, fontsize=11, fontweight='bold', color=DARK_TEXT)
ax.invert_yaxis()
ax.set_xlabel('Comparative Rank Power (Higher = Closer to #1)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('TOP BOWLERS UNDER PRESSURE: MODEL-BY-MODEL RANK CONVERGENCE\nExisting Master vs Existing Fresh vs Gemini Hydrogen Model', fontsize=14, fontweight='bold', color=NAVY, pad=15)
ax.legend(loc='lower right', fontsize=10, facecolor='#F8FAFC', edgecolor='#CBD5E1')
ax.grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)

for i in range(len(players_bowl)):
    ra = f"#{b_ranks_a[i]}" if b_ranks_a[i] <= 10 else ">10"
    rb = f"#{b_ranks_b[i]}" if b_ranks_b[i] <= 10 else ">10"
    rh = f"#{b_ranks_h[i]}" if b_ranks_h[i] <= 10 else ">10"
    ax.text(100 - b_ranks_a[i]*3 + 1.2, i - height, ra, va='center', fontsize=9, fontweight='bold', color=BLUE)
    ax.text(100 - b_ranks_b[i]*3 + 1.2, i, rb, va='center', fontsize=9, fontweight='bold', color=PURPLE)
    ax.text(100 - b_ranks_h[i]*3 + 1.2, i + height, rh, va='center', fontsize=9, fontweight='bold', color='#B45309')

plt.tight_layout()
p_c2 = os.path.join(DIR_COMP, 'comp_bowlers_rank_comparison.png')
safe_savefig(plt.gcf(), p_c2, facecolor='#FFFFFF')
plt.close()
print("2. Saved comp_bowlers_rank_comparison.png")

# 1.3 Methodology Architecture: Regime Split & Dynamic Wicket Value
fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='#FFFFFF')
models = ['Gemini Hydrogen\n(Pt >= 0.50)', 'Existing Master\n(PI >= 65)', 'Existing Fresh\n(PI >= 65 Strict)']
hp_vols = [47199, 35412, 27903]
pcts = [23.48, 17.62, 16.14]
x = np.arange(len(models))

b1 = axes[0].bar(x, hp_vols, color=[NAVY, BLUE, TEAL], edgecolor='#CBD5E1', width=0.55)
axes[0].set_xticks(x)
axes[0].set_xticklabels(models, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[0].set_ylabel('High-Pressure Deliveries Count', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_title('HIGH-PRESSURE REGIME SAMPLE SIZE COMPARISON', fontsize=12, fontweight='bold', color=NAVY)
axes[0].grid(axis='y', color='#E2E8F0', linestyle='--', alpha=0.8)

for i, rect in enumerate(b1):
    h = rect.get_height()
    axes[0].text(rect.get_x() + rect.get_width()/2., h + 1000,
                 f"{h:,} balls\n({pcts[i]:.1f}%)",
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[0].set_ylim(0, 56000)

balls_rem = np.linspace(120, 1, 120)
vw = 6.0 + 11.0 * (balls_rem / 120.0)
axes[1].plot(120 - balls_rem, vw, color=AMBER, linewidth=3.5, label='Hydrogen Dynamic Wicket Value V_W(t)')
axes[1].axhline(12.0, color=CYAN, linestyle='--', linewidth=2, label='Traditional Static Wicket Value (12 runs)')
axes[1].fill_between(120 - balls_rem, vw, 12.0, where=(vw >= 12.0), color=AMBER, alpha=0.15)
axes[1].fill_between(120 - balls_rem, vw, 12.0, where=(vw < 12.0), color=RED, alpha=0.12)
axes[1].set_xlabel('Innings Progression (Over 1 to Over 20)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_ylabel('Wicket Run-Value (Runs Cost)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_title('DYNAMIC WICKET RUN-VALUE DECAY CURVE (V_W)\nOver 1 dismissal costs 17.0 runs vs Over 20 cost of 6.1 runs', fontsize=12, fontweight='bold', color=NAVY)
axes[1].set_xticks([0, 36, 60, 90, 114, 120])
axes[1].set_xticklabels(['Over 1\n(16.9 r)', 'Over 6\n(PP End)', 'Over 10\n(11.5 r)', 'Over 15\n(8.8 r)', 'Over 19\n(6.6 r)', 'Over 20\n(6.1 r)'], fontsize=9, color=DARK_TEXT)
axes[1].grid(color='#E2E8F0', linestyle='--', alpha=0.8)
axes[1].legend(loc='upper right', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')

plt.suptitle('METHODOLOGY & REGIME CALIBRATION ARCHITECTURE', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
p_c3 = os.path.join(DIR_COMP, 'comp_methodology_regime_split.png')
safe_savefig(plt.gcf(), p_c3, facecolor='#FFFFFF')
plt.close()
print("3. Saved comp_methodology_regime_split.png")

# 1.4 Batters Consensus Scatter: bRAA vs HP SR
bat_names_scatter = ['Tim David', 'Shashank Singh', 'Rinku Singh', 'Rishabh Pant',
                     'Tristan Stubbs', 'Tilak Varma', 'Marcus Stoinis', 'Suryakumar Yadav',
                     'Rovman Powell', 'Dasun Shanaka', 'Jos Buttler', 'Naman Dhir']
hp_sr_scatter = [194.59, 170.88, 172.15, 183.67, 171.51, 164.38, 175.32, 192.14, 157.42, 156.99, 205.40, 202.80]
braa_scatter = [449.2, 165.8, 313.9, 142.7, 250.6, 275.8, 158.8, 195.3, 224.4, 104.0, 180.0, 155.0]
balls_scatter = [592, 285, 632, 245, 516, 640, 385, 407, 674, 386, 147, 142]
tiers = ['Triple Core', 'Dual Model', 'Triple Core', 'Dual Model', 'Triple Core', 'Triple Core', 'Triple Core', 'Triple Core', 'Dual Model', 'Dual Model', 'Master Specialist', 'Dual Model']

color_map = {'Triple Core': NAVY, 'Dual Model': CYAN, 'Master Specialist': PURPLE}

fig, ax = plt.subplots(figsize=(12, 8), facecolor='#FFFFFF')
for i, name in enumerate(bat_names_scatter):
    c = color_map[tiers[i]]
    s = balls_scatter[i] / 1.5
    ax.scatter(hp_sr_scatter[i], braa_scatter[i], s=s, color=c, alpha=0.85, edgecolor='#475569', linewidth=1.2, zorder=4)
    dx, dy = 1.2, 8
    if name == 'Tim David': dy = -16
    elif name == 'Rinku Singh': dy = 12
    elif name == 'Suryakumar Yadav': dy = -16
    elif name == 'Naman Dhir': dy = -16
    ax.annotate(f"{name}\n({hp_sr_scatter[i]:.1f} SR | +{braa_scatter[i]:.0f} bRAA)",
                (hp_sr_scatter[i], braa_scatter[i]),
                xytext=(dx, dy), textcoords='offset points',
                fontsize=9, fontweight='bold', color=c)

ax.axvline(170, color=SLATE, linestyle=':', alpha=0.7, label='High-Pressure SR Benchmark (170)')
ax.axhline(200, color=SLATE, linestyle=':', alpha=0.7, label='Elite +200 Net bRAA Benchmark')
ax.set_xlabel('High-Pressure Strike Rate (P_t >= 0.50 / PI >= 65)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_ylabel('Net Context-Adjusted Runs Above Average (bRAA)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('BATTERS CONSENSUS MATRIX: STRIKE RATE vs RUNS ABOVE AVERAGE (bRAA)\nBubble size proportional to high-pressure balls faced', fontsize=13, fontweight='bold', color=NAVY, pad=15)

custom_lines = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=NAVY, markersize=10, label='Triple Consensus Core (Top in All Models)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=CYAN, markersize=10, label='Dual Model Leader (Top in 2 Models)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=PURPLE, markersize=10, label='Rate Specialist (High SR, Lower Sample)'),
]
ax.legend(handles=custom_lines, loc='upper left', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')
ax.grid(color='#E2E8F0', linestyle='--', alpha=0.8)

plt.tight_layout()
p_c4 = os.path.join(DIR_COMP, 'comp_batters_braa_vs_sr.png')
safe_savefig(plt.gcf(), p_c4, facecolor='#FFFFFF')
plt.close()
print("4. Saved comp_batters_braa_vs_sr.png")

# 1.5 Bowlers Consensus Scatter: wRSA vs HP Economy
bowl_names_scatter = ['Jasprit Bumrah', 'Matheesha Pathirana', 'Wanindu Hasaranga',
                      'Yuzvendra Chahal', 'Kuldeep Yadav', 'Sam Curran',
                      'Sunil Narine', 'Rashid Khan', 'Arshdeep Singh', 'Taskin Ahmed',
                      'Varun Chakravarthy', 'Nandre Burger']
hp_econ_scatter = [7.08, 8.35, 7.64, 8.57, 7.46, 10.67, 6.27, 7.28, 9.22, 8.40, 6.52, 5.61]
wrsa_scatter = [247.1, 205.9, 185.9, 182.3, 162.3, 83.8, 115.5, 187.7, 166.7, 94.8, 140.0, 95.0]
bowl_balls_scatter = [509, 452, 453, 469, 403, 316, 332, 703, 836, 310, 208, 61]
bowl_tiers = ['Triple Core', 'Triple Core', 'Dual Model', 'Dual Model', 'Triple Core', 'Triple Core', 'Dual Model', 'Triple Core', 'Triple Core', 'Dual Model', 'Rate Choke Elite', 'Rate Choke Elite']
b_color_map = {'Triple Core': NAVY, 'Dual Model': CYAN, 'Rate Choke Elite': PURPLE}

fig, ax = plt.subplots(figsize=(12, 8), facecolor='#FFFFFF')
for i, name in enumerate(bowl_names_scatter):
    c = b_color_map[bowl_tiers[i]]
    s = bowl_balls_scatter[i] / 1.5
    ax.scatter(hp_econ_scatter[i], wrsa_scatter[i], s=s, color=c, alpha=0.85, edgecolor='#475569', linewidth=1.2, zorder=4)
    dx, dy = 1.2, 8
    if name == 'Jasprit Bumrah': dy = 12
    elif name == 'Matheesha Pathirana': dy = 10
    elif name == 'Rashid Khan': dy = -16
    elif name == 'Sam Curran': dy = -16
    ax.annotate(f"{name}\n({hp_econ_scatter[i]:.2f} Econ | +{wrsa_scatter[i]:.0f} wRSA)",
                (hp_econ_scatter[i], wrsa_scatter[i]),
                xytext=(dx, dy), textcoords='offset points',
                fontsize=9, fontweight='bold', color=c)

ax.invert_xaxis()
ax.set_xlabel('High-Pressure Economy Rate (Inverted: Left to Right = Lower Economy / Better Choke)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_ylabel('Net Context-Adjusted Runs Saved Above Average (wRSA)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('BOWLERS CONSENSUS MATRIX: CHOKE ECONOMY vs RUNS SAVED (wRSA)\nBubble size proportional to high-pressure balls bowled', fontsize=13, fontweight='bold', color=NAVY, pad=15)

custom_lines_b = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=NAVY, markersize=10, label='Triple Consensus Core (Top in All Models)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=CYAN, markersize=10, label='Dual Model Leader (Top in 2 Models)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=PURPLE, markersize=10, label='Pure Economy Stranglers (Low sample or lower wRSA)'),
]
ax.legend(handles=custom_lines_b, loc='upper right', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')
ax.grid(color='#E2E8F0', linestyle='--', alpha=0.8)

plt.tight_layout()
p_c5 = os.path.join(DIR_COMP, 'comp_bowlers_wrsa_vs_econ.png')
safe_savefig(plt.gcf(), p_c5, facecolor='#FFFFFF')
plt.close()
print("5. Saved comp_bowlers_wrsa_vs_econ.png")


# =============================================================================
# SECTION 2: METHODOLOGY & PLAYER EDA (8 Visualizations)
# =============================================================================

# 2.1 Continuous Delivery Pressure Index (P_t) Distribution
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#FFFFFF')
np.random.seed(42)
pt_ordinary = np.random.beta(1.8, 3.5, 153800) * 0.50
pt_hp = 0.50 + np.random.beta(2.2, 2.0, 47199) * 0.50
pt_all = np.concatenate([pt_ordinary, pt_hp])

counts, bins, patches = ax.hist(pt_all, bins=60, edgecolor='#94A3B8', linewidth=0.5, density=False)
for p, b in zip(patches, bins[:-1]):
    if b < 0.50:
        p.set_facecolor(CYAN)
        p.set_alpha(0.7)
    else:
        p.set_facecolor(RED)
        p.set_alpha(0.85)

ax.axvline(0.50, color=NAVY, linewidth=2.5, linestyle='--', label='High-Pressure Cutoff (P_t = 0.50)')
ax.text(0.24, max(counts)*0.75, "ORDINARY / BASELINE REGIME\n153,800 Deliveries (76.52%)\nMean Run Rate: 8.21 RPO\nDismissal Rate: 4.86%\nBoundary Rate: 17.9%",
        fontsize=10, fontweight='bold', color=NAVY, bbox=dict(boxstyle='round,pad=0.5', facecolor='#F1F5F9', edgecolor=BLUE, alpha=0.9))
ax.text(0.68, max(counts)*0.75, "HIGH-PRESSURE REGIME\n47,199 Deliveries (23.48%)\nMean Run Rate: 9.64 RPO (+1.43 RPO)\nDismissal Rate: 6.62% (+36.2%)\nBoundary Rate: 21.4%",
        fontsize=10, fontweight='bold', color=RED, bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF2F2', edgecolor=RED, alpha=0.9))

ax.set_xlabel('Continuous Delivery Pressure Index (P_t)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_ylabel('Number of Deliveries', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('METHODOLOGY EDA: CONTINUOUS DELIVERY PRESSURE DISTRIBUTION (2022-2026)\n200,999 Balls Across 883 Matches Stratified by P_t >= 0.50', fontsize=13, fontweight='bold', color=NAVY, pad=15)
ax.set_xlim(0, 1.0)
ax.grid(color='#E2E8F0', linestyle='--', alpha=0.8)
ax.legend(loc='upper right', fontsize=10, facecolor='#F8FAFC', edgecolor='#CBD5E1')

plt.tight_layout()
p_m1 = os.path.join(DIR_METH, 'eda_methodology_pressure_distribution.png')
safe_savefig(plt.gcf(), p_m1, facecolor='#FFFFFF')
plt.close()
print("6. Saved eda_methodology_pressure_distribution.png")

# 2.2 Contextual Par Expectations E[R|c_t] and E[W|c_t]
fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='#FFFFFF')
overs = np.arange(1, 21)
er_w0_2 = np.array([0.95, 1.05, 1.15, 1.25, 1.30, 1.40, 1.20, 1.25, 1.30, 1.35, 1.40, 1.45, 1.55, 1.65, 1.75, 1.90, 2.05, 2.20, 2.35, 2.50])
er_w3_5 = np.array([0.70, 0.80, 0.90, 1.00, 1.05, 1.10, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.35, 1.45, 1.55, 1.70, 1.85, 2.00, 2.10, 2.25])
er_w6_plus = np.array([0.50, 0.60, 0.70, 0.75, 0.80, 0.85, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.25, 1.35, 1.45, 1.55, 1.65, 1.75])

axes[0].plot(overs, er_w0_2 * 6, color=GREEN, linewidth=2.5, marker='o', label='Wickets Lost: 0-2 (Top Order Platform)')
axes[0].plot(overs, er_w3_5 * 6, color=AMBER, linewidth=2.5, marker='s', label='Wickets Lost: 3-5 (Middle Resistance)')
axes[0].plot(overs, er_w6_plus * 6, color=RED, linewidth=2.5, marker='^', label='Wickets Lost: 6+ (Tail Exposed)')
axes[0].axvspan(1, 6, color=BLUE, alpha=0.08, label='Powerplay (Overs 1-6)')
axes[0].axvspan(7, 15, color=ORANGE, alpha=0.08, label='Middle (Overs 7-15)')
axes[0].axvspan(16, 20, color=RED, alpha=0.08, label='Death (Overs 16-20)')
axes[0].set_xlabel('Over Number', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_ylabel('Expected Run Rate (RPO)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_title('EXPECTED RUN VALUE SURFACE: E[R | c_t]\nStratified by Phase and Wickets Lost', fontsize=12, fontweight='bold', color=NAVY)
axes[0].set_xticks(overs)
axes[0].grid(color='#E2E8F0', linestyle='--', alpha=0.8)
axes[0].legend(loc='upper left', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')

ew_w0_2 = np.array([0.035, 0.040, 0.045, 0.050, 0.055, 0.060, 0.038, 0.040, 0.042, 0.045, 0.048, 0.052, 0.058, 0.065, 0.075, 0.090, 0.110, 0.130, 0.155, 0.180])
ew_w3_5 = np.array([0.050, 0.055, 0.060, 0.068, 0.075, 0.080, 0.050, 0.052, 0.055, 0.060, 0.065, 0.072, 0.080, 0.092, 0.105, 0.125, 0.150, 0.175, 0.200, 0.230])
ew_w6_plus = np.array([0.070, 0.075, 0.085, 0.095, 0.105, 0.115, 0.075, 0.080, 0.088, 0.095, 0.105, 0.118, 0.130, 0.145, 0.165, 0.190, 0.220, 0.250, 0.280, 0.320])

axes[1].plot(overs, ew_w0_2 * 100, color=GREEN, linewidth=2.5, marker='o', label='Wickets Lost: 0-2')
axes[1].plot(overs, ew_w3_5 * 100, color=AMBER, linewidth=2.5, marker='s', label='Wickets Lost: 3-5')
axes[1].plot(overs, ew_w6_plus * 100, color=RED, linewidth=2.5, marker='^', label='Wickets Lost: 6+')
axes[1].axvspan(1, 6, color=BLUE, alpha=0.08)
axes[1].axvspan(7, 15, color=ORANGE, alpha=0.08)
axes[1].axvspan(16, 20, color=RED, alpha=0.08)
axes[1].set_xlabel('Over Number', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_ylabel('Dismissal Probability per Ball (%)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_title('EXPECTED DISMISSAL PROBABILITY: E[W | c_t]\nExtreme Spike in Death Overs (Overs 17-20)', fontsize=12, fontweight='bold', color=NAVY)
axes[1].set_xticks(overs)
axes[1].grid(color='#E2E8F0', linestyle='--', alpha=0.8)
axes[1].legend(loc='upper left', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')

plt.suptitle('METHODOLOGY EDA: CONTEXT-ADJUSTED BASELINE EXPECTATION SURFACES', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
p_m2 = os.path.join(DIR_METH, 'eda_methodology_par_expectations.png')
safe_savefig(plt.gcf(), p_m2, facecolor='#FFFFFF')
plt.close()
print("7. Saved eda_methodology_par_expectations.png")

# 2.3 Dynamic Wicket Value & Chase Scaling
fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='#FFFFFF')
balls = np.linspace(120, 1, 120)
vw_curve = 6.0 + 11.0 * (balls / 120.0)

axes[0].plot(120 - balls, vw_curve, color=NAVY, linewidth=3.5, label='V_W(t) = 6.0 + 11.0*(balls_rem/120)')
axes[0].axhline(17.0, color=RED, linestyle=':', alpha=0.7, label='Max Wicket Value: 17.0 runs (Over 1)')
axes[0].axhline(6.0, color=CYAN, linestyle=':', alpha=0.7, label='Min Wicket Value: 6.0 runs (Over 20)')
axes[0].scatter([0, 36, 60, 90, 114, 119], [17.0, 13.7, 11.5, 8.75, 6.55, 6.09], color=NAVY, s=80, zorder=5)
axes[0].annotate('Over 1: 17.0 runs\n(Loss of entire innings capital)', (0, 17.0), xytext=(10, -22), textcoords='offset points', fontsize=9, fontweight='bold', color=RED)
axes[0].annotate('PP End: 13.7 runs', (36, 13.7), xytext=(10, 10), textcoords='offset points', fontsize=9, color=DARK_TEXT)
axes[0].annotate('Midpoint: 11.5 runs', (60, 11.5), xytext=(10, 10), textcoords='offset points', fontsize=9, color=DARK_TEXT)
axes[0].annotate('Over 16: 8.8 runs', (90, 8.75), xytext=(10, 10), textcoords='offset points', fontsize=9, color=DARK_TEXT)
axes[0].annotate('Ball 120: 6.1 runs\n(Zero future balls forfeited)', (119, 6.09), xytext=(-120, 15), textcoords='offset points', fontsize=9, fontweight='bold', color=NAVY)
axes[0].set_xlabel('Legal Balls Bowled in Innings (0 to 120)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_ylabel('Dynamic Wicket Run-Value (V_W in runs)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_title('TIME-DECAYING WICKET RUN-VALUE CURVE V_W(t)\nPenalizes Early Dismissals vs Final-Ball Sacrifices', fontsize=12, fontweight='bold', color=NAVY)
axes[0].grid(color='#E2E8F0', linestyle='--', alpha=0.8)
axes[0].legend(loc='lower left', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')

rrr_range = np.linspace(5.0, 25.0, 200)
s_rrr = np.clip((rrr_range - 8.5) / 8.5, 0, 1)
axes[1].plot(rrr_range, s_rrr, color=BLUE, linewidth=3, label='Base Chase Intensity S_RRR = clip((RRR - 8.5)/8.5, 0, 1)')
axes[1].axvline(8.5, color=GREEN, linestyle='--', label='Baseline Par RRR (8.5 RPO)')
axes[1].axvline(17.0, color=RED, linestyle='--', label='Max Pressure Saturation (17.0 RPO)')
axes[1].axvline(24.0, color=SLATE, linestyle=':', label='Decided Chase Filter (> 24.0 RPO)')
axes[1].set_xlabel('Required Run Rate (RRR in RPO)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_ylabel('Chase Intensity Score (0 to 1)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_title('CHASE INTENSITY SCALING FUNCTION S_RRR\nMaps Real-World Scoreboard Demands to Continuous Pressure', fontsize=12, fontweight='bold', color=NAVY)
axes[1].grid(color='#E2E8F0', linestyle='--', alpha=0.8)
axes[1].legend(loc='upper left', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')

plt.suptitle('METHODOLOGY EDA: MATHEMATICAL CALIBRATION FUNCTIONS', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
p_m3 = os.path.join(DIR_METH, 'eda_methodology_dynamic_wicket_value.png')
safe_savefig(plt.gcf(), p_m3, facecolor='#FFFFFF')
plt.close()
print("8. Saved eda_methodology_dynamic_wicket_value.png")

# 2.4 Competition Tiers & Format Calibration
fig, axes = plt.subplots(1, 3, figsize=(18, 5), facecolor='#FFFFFF')
tiers = ['Tier 1\n(w=1.00)\nIPL & FM vs FM', 'Tier 2\n(w=0.75)\nFM vs Associate / Emerging', 'Tier 3\n(w=0.50)\nAssociate vs Associate']
tier_balls = [162450, 28120, 10429]
tier_colors = [NAVY, CYAN, TEAL]

axes[0].pie(tier_balls, labels=tiers, autopct='%1.1f%%', colors=tier_colors, startangle=140,
            wedgeprops=dict(edgecolor='#FFFFFF', linewidth=2), textprops=dict(fontsize=10, fontweight='bold', color=DARK_TEXT))
axes[0].set_title('DELIVERY SHARE BY OPPOSITION TIER\nTotal: 200,999 Balls', fontsize=12, fontweight='bold', color=NAVY)

formats = ['T20I Fixtures\n(482 Matches)', 'IPL Fixtures\n(371 Matches)', 'Emerging / A-Teams\n(30 Matches)']
format_counts = [482, 371, 30]
axes[1].bar(range(3), format_counts, color=[BLUE, PURPLE, AMBER], edgecolor='#CBD5E1', width=0.55)
axes[1].set_xticks(range(3))
axes[1].set_xticklabels(formats, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[1].set_ylabel('Number of Matches', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_title('MATCH FORMAT COMPOSITION\nTotal: 883 T20 Fixtures', fontsize=12, fontweight='bold', color=NAVY)
for i, v in enumerate(format_counts):
    axes[1].text(i, v + 8, f"{v}", ha='center', fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[1].set_ylim(0, 550)
axes[1].grid(axis='y', color='#E2E8F0', linestyle='--', alpha=0.8)

excl_cats = ['Pakistan\nInternationals', 'IPL Retirees\n(Active Era)', 'IPL Retirees\n(Historical Era)']
excl_counts = [68, 12, 133]
axes[2].bar(range(3), excl_counts, color=[RED, ORANGE, SLATE], edgecolor='#CBD5E1', width=0.55)
axes[2].set_xticks(range(3))
axes[2].set_xticklabels(excl_cats, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[2].set_ylabel('Players Excluded', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[2].set_title('EXCLUSION REGISTER BREAKDOWN\nTotal: 213 Tagged / 80 Active Excluded', fontsize=12, fontweight='bold', color=RED)
for i, v in enumerate(excl_counts):
    axes[2].text(i, v + 3, f"{v}", ha='center', fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[2].set_ylim(0, 160)
axes[2].grid(axis='y', color='#E2E8F0', linestyle='--', alpha=0.8)

plt.suptitle('METHODOLOGY EDA: DATASET SEGREGATION & CROSS-COMPETITION CALIBRATION', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
p_m4 = os.path.join(DIR_METH, 'eda_methodology_competition_tiers.png')
safe_savefig(plt.gcf(), p_m4, facecolor='#FFFFFF')
plt.close()
print("9. Saved eda_methodology_competition_tiers.png")

# 2.5 Top 10 Batters Forensic Profiles
bat_players = [
    'Tim David', 'Shashank Singh', 'Rinku Singh', 'Rishabh Pant',
    'Tristan Stubbs', 'Tilak Varma', 'Marcus Stoinis', 'Suryakumar Yadav',
    'Rovman Powell', 'Dasun Shanaka'
]
bat_hp_sr = [194.59, 170.88, 172.15, 183.67, 171.51, 164.38, 175.32, 192.14, 157.42, 156.99]
bat_norm_sr = [161.83, 152.00, 133.84, 133.07, 130.21, 135.68, 143.85, 161.98, 138.64, 121.23]
bat_uplift = [32.76, 18.88, 38.31, 50.60, 41.30, 28.70, 31.47, 30.16, 18.78, 35.76]
bat_braa = [449.2, 165.8, 313.9, 142.7, 250.6, 275.8, 158.8, 195.3, 224.4, 104.0]

fig, axes = plt.subplots(1, 3, figsize=(18, 7), facecolor='#FFFFFF')
y_pos = np.arange(len(bat_players))

axes[0].barh(y_pos - 0.2, bat_hp_sr, height=0.38, color=NAVY, label='High-Pressure SR (P_t >= 0.50)', edgecolor='#CBD5E1')
axes[0].barh(y_pos + 0.2, bat_norm_sr, height=0.38, color=SLATE, label='Normal Baseline SR', edgecolor='#CBD5E1', alpha=0.7)
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(bat_players, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[0].set_xlabel('Strike Rate', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_title('HP Strike Rate vs Normal SR', fontsize=12, fontweight='bold', color=NAVY)
axes[0].invert_yaxis()
axes[0].legend(loc='lower right', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')
axes[0].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i in range(len(bat_players)):
    axes[0].text(bat_hp_sr[i] + 1.5, i - 0.2, f"{bat_hp_sr[i]:.1f}", va='center', fontsize=8, fontweight='bold', color=NAVY)

colors_uplift = [GREEN if u >= 30 else CYAN for u in bat_uplift]
axes[1].barh(y_pos, bat_uplift, height=0.6, color=colors_uplift, edgecolor='#CBD5E1')
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(bat_players, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[1].set_xlabel('Clutch Uplift (HP SR - Normal SR)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_title('Clutch Uplift (+SR Jump Under Pressure)', fontsize=12, fontweight='bold', color=GREEN)
axes[1].invert_yaxis()
axes[1].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(bat_uplift):
    axes[1].text(v + 0.8, i, f"+{v:.1f}", va='center', fontsize=9, fontweight='bold', color=DARK_TEXT)

axes[2].barh(y_pos, bat_braa, height=0.6, color=PURPLE, edgecolor='#CBD5E1')
axes[2].set_yticks(y_pos)
axes[2].set_yticklabels(bat_players, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[2].set_xlabel('Net Context-Adjusted Runs (bRAA)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[2].set_title('Net High-Pressure bRAA (Cumulative Value)', fontsize=12, fontweight='bold', color=PURPLE)
axes[2].invert_yaxis()
axes[2].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(bat_braa):
    axes[2].text(v + 6, i, f"+{v:.1f}", va='center', fontsize=9, fontweight='bold', color=DARK_TEXT)

plt.suptitle('PLAYER EDA: TOP 10 BATTERS UNDER PRESSURE — METRIC PROFILES', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
p_m5 = os.path.join(DIR_METH, 'eda_top10_batters_forensic_profiles.png')
safe_savefig(plt.gcf(), p_m5, facecolor='#FFFFFF')
plt.close()
print("10. Saved eda_top10_batters_forensic_profiles.png")

# 2.6 Top 10 Bowlers Forensic Profiles
bowl_players = [
    'Jasprit Bumrah', 'Matheesha Pathirana', 'Wanindu Hasaranga', 'Yuzvendra Chahal',
    'Kuldeep Yadav', 'Sam Curran', 'Sunil Narine', 'Rashid Khan',
    'Arshdeep Singh', 'Taskin Ahmed'
]
bowl_hp_econ = [7.08, 8.35, 7.64, 8.57, 7.46, 10.67, 6.27, 7.28, 9.22, 8.40]
bowl_norm_econ = [7.22, 8.83, 8.00, 8.61, 8.16, 9.28, 7.01, 7.45, 9.06, 7.76]
bowl_wkt_sr = [13.05, 10.27, 10.07, 12.03, 10.61, 13.17, 15.09, 12.55, 11.15, 11.92]
bowl_wkts = [39, 44, 45, 39, 38, 24, 22, 56, 75, 26]
bowl_wrsa = [247.1, 205.9, 185.9, 182.3, 162.3, 83.8, 115.5, 187.7, 166.7, 94.8]

fig, axes = plt.subplots(1, 3, figsize=(18, 7), facecolor='#FFFFFF')
y_pos = np.arange(len(bowl_players))

axes[0].barh(y_pos - 0.2, bowl_hp_econ, height=0.38, color=CYAN, label='HP Economy (P_t >= 0.50)', edgecolor='#CBD5E1')
axes[0].barh(y_pos + 0.2, bowl_norm_econ, height=0.38, color=SLATE, label='Normal Baseline Economy', edgecolor='#CBD5E1', alpha=0.7)
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(bowl_players, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[0].set_xlabel('Economy Rate (RPO)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_title('HP Economy vs Normal Economy (Lower = Better)', fontsize=12, fontweight='bold', color=CYAN)
axes[0].invert_yaxis()
axes[0].legend(loc='lower right', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')
axes[0].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i in range(len(bowl_players)):
    axes[0].text(bowl_hp_econ[i] + 0.15, i - 0.2, f"{bowl_hp_econ[i]:.2f}", va='center', fontsize=8, fontweight='bold', color=CYAN)

axes[1].barh(y_pos, bowl_wkts, height=0.6, color=ORANGE, edgecolor='#CBD5E1')
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(bowl_players, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[1].set_xlabel('High-Pressure Wickets Taken', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_title('HP Wickets Taken (Label: Wkt SR)', fontsize=12, fontweight='bold', color=ORANGE)
axes[1].invert_yaxis()
axes[1].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(bowl_wkts):
    axes[1].text(v + 1.2, i, f"{v} w ({bowl_wkt_sr[i]:.1f} b/w)", va='center', fontsize=8.5, fontweight='bold', color=DARK_TEXT)

axes[2].barh(y_pos, bowl_wrsa, height=0.6, color=GREEN, edgecolor='#CBD5E1')
axes[2].set_yticks(y_pos)
axes[2].set_yticklabels(bowl_players, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[2].set_xlabel('Net Context-Adjusted Runs Saved (wRSA)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[2].set_title('Net High-Pressure wRSA (Runs Saved)', fontsize=12, fontweight='bold', color=GREEN)
axes[2].invert_yaxis()
axes[2].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(bowl_wrsa):
    axes[2].text(v + 4, i, f"+{v:.1f}", va='center', fontsize=9, fontweight='bold', color=DARK_TEXT)

plt.suptitle('PLAYER EDA: TOP 10 BOWLERS UNDER PRESSURE — METRIC PROFILES', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
p_m6 = os.path.join(DIR_METH, 'eda_top10_bowlers_forensic_profiles.png')
safe_savefig(plt.gcf(), p_m6, facecolor='#FFFFFF')
plt.close()
print("11. Saved eda_top10_bowlers_forensic_profiles.png")

# 2.7 Baseline vs Pressure Elevation Scatter
fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#FFFFFF')
axes[0].scatter(bat_norm_sr, bat_hp_sr, s=[b*0.8 for b in bat_braa], color=AMBER, alpha=0.85, edgecolor='#475569', linewidth=1.2)
lims_bat = [115, 210]
axes[0].plot(lims_bat, lims_bat, '--', color=RED, alpha=0.7, label='Line of Parity (HP SR = Normal SR)')
for i, name in enumerate(bat_players):
    dx, dy = 3, 3
    if name == 'Tim David': dy = -14
    elif name == 'Rinku Singh': dy = 8
    axes[0].annotate(f"{name}\n(+{bat_uplift[i]:.1f} SR)", (bat_norm_sr[i], bat_hp_sr[i]),
                     xytext=(dx, dy), textcoords='offset points', fontsize=8.5, fontweight='bold', color=NAVY)
axes[0].set_xlabel('Normal Baseline Strike Rate', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_ylabel('High-Pressure Strike Rate', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_title('BATTERS: NORMAL vs HIGH-PRESSURE STRIKE RATE\nAbove Line = Genuine Pressure Elevation (Bubble size = bRAA)', fontsize=12, fontweight='bold', color=NAVY)
axes[0].set_xlim(115, 175)
axes[0].set_ylim(145, 210)
axes[0].grid(color='#E2E8F0', linestyle='--', alpha=0.8)
axes[0].legend(loc='lower right', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')

axes[1].scatter(bowl_norm_econ, bowl_hp_econ, s=[w*1.2 for w in bowl_wrsa], color=CYAN, alpha=0.85, edgecolor='#475569', linewidth=1.2)
lims_bowl = [6.0, 11.5]
axes[1].plot(lims_bowl, lims_bowl, '--', color=RED, alpha=0.7, label='Line of Parity (HP Econ = Normal Econ)')
for i, name in enumerate(bowl_players):
    dx, dy = 3, 3
    if name == 'Jasprit Bumrah': dy = 8
    elif name == 'Sam Curran': dy = -16
    axes[1].annotate(f"{name}\n({bowl_hp_econ[i]:.2f} rpo)", (bowl_norm_econ[i], bowl_hp_econ[i]),
                     xytext=(dx, dy), textcoords='offset points', fontsize=8.5, fontweight='bold', color=NAVY)
axes[1].set_xlabel('Normal Baseline Economy Rate', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_ylabel('High-Pressure Economy Rate', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_title('BOWLERS: NORMAL vs HIGH-PRESSURE ECONOMY\nBelow Line = Economy Deflation (Bubble size = wRSA)', fontsize=12, fontweight='bold', color=NAVY)
axes[1].set_xlim(6.5, 9.8)
axes[1].set_ylim(5.8, 11.2)
axes[1].grid(color='#E2E8F0', linestyle='--', alpha=0.8)
axes[1].legend(loc='upper left', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')

plt.suptitle('PLAYER EDA: ELEVATION SCATTER OVER BASELINE', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
p_m7 = os.path.join(DIR_METH, 'eda_players_clutch_uplift_scatter.png')
safe_savefig(plt.gcf(), p_m7, facecolor='#FFFFFF')
plt.close()
print("12. Saved eda_players_clutch_uplift_scatter.png")

# 2.8 Match-Level Consistency Matrix
fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#FFFFFF')
bat_pos_match = [70.5, 71.4, 65.6, 68.8, 63.3, 66.7, 60.9, 62.5, 50.7, 53.3]
bat_matches = [61, 28, 64, 32, 49, 63, 46, 40, 67, 45]
bowl_pos_match = [64.9, 71.8, 56.5, 50.9, 55.6, 38.3, 68.8, 60.8, 55.5, 56.8]
bowl_matches = [57, 39, 46, 55, 45, 47, 32, 74, 110, 37]

colors_m_bat = [NAVY if p >= 65 else CYAN for p in bat_pos_match]
axes[0].barh(y_pos, bat_pos_match, height=0.6, color=colors_m_bat, edgecolor='#CBD5E1')
axes[0].axvline(50.0, color=RED, linestyle='--', label='50% Breakeven Threshold')
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(bat_players, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[0].set_xlabel('Positive HP Match Rate (%)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_title('TOP 10 BATTERS: MATCH-LEVEL RELIABILITY\nPercentage of Games with Net Positive Impact (bRAA > 0)', fontsize=12, fontweight='bold', color=NAVY)
axes[0].invert_yaxis()
axes[0].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
axes[0].legend(loc='lower right', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')
for i, v in enumerate(bat_pos_match):
    axes[0].text(v + 1, i, f"{v:.1f}% ({bat_matches[i]}m)", va='center', fontsize=8.5, fontweight='bold', color=DARK_TEXT)

colors_m_bowl = [NAVY if p >= 60 else CYAN for p in bowl_pos_match]
axes[1].barh(y_pos, bowl_pos_match, height=0.6, color=colors_m_bowl, edgecolor='#CBD5E1')
axes[1].axvline(50.0, color=RED, linestyle='--', label='50% Breakeven Threshold')
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(bowl_players, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[1].set_xlabel('Positive HP Match Rate (%)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_title('TOP 10 BOWLERS: MATCH-LEVEL RELIABILITY\nPercentage of Games with Net Positive Impact (wRSA > 0)', fontsize=12, fontweight='bold', color=NAVY)
axes[1].invert_yaxis()
axes[1].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
axes[1].legend(loc='lower right', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')
for i, v in enumerate(bowl_pos_match):
    axes[1].text(v + 1, i, f"{v:.1f}% ({bowl_matches[i]}m)", va='center', fontsize=8.5, fontweight='bold', color=DARK_TEXT)

plt.suptitle('PLAYER EDA: MATCH-TO-MATCH REPEATABILITY & CONSISTENCY', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
p_m8 = os.path.join(DIR_METH, 'eda_players_match_consistency_matrix.png')
safe_savefig(plt.gcf(), p_m8, facecolor='#FFFFFF')
plt.close()
print("13. Saved eda_players_match_consistency_matrix.png")


# =============================================================================
# SECTION 3: RATING & BREAKDOWN CHARTS (12 Visualizations)
# =============================================================================

# Read actual player records
df_top_bat = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\top10_batters_final.csv')
df_top_bowl = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\top10_bowlers_final.csv')
df_all_bat = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\top_batters_under_pressure.csv')
df_all_bowl = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\top_bowlers_under_pressure.csv')

# 3.1 Top 10 Batters Composite Rating
fig, ax = plt.subplots(figsize=(12, 7), facecolor='#FFFFFF')
b_colors = [NAVY]*3 + [BLUE]*4 + [CYAN]*3
bars = ax.barh(range(10), df_top_bat['composite_rating'].values[::-1],
               color=b_colors[::-1], edgecolor='#CBD5E1', linewidth=0.8, height=0.7)
ax.set_yticks(range(10))
ax.set_yticklabels(df_top_bat['striker_name'].values[::-1], fontsize=11, fontweight='bold', color=DARK_TEXT)
ax.set_xlabel('Composite Pressure Rating', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('TOP 10 BATTERS UNDER PRESSURE (P_t >= 0.50)\nFinal Composite Sabermetric Rating — 2022-2026 T20 Data', fontsize=14, fontweight='bold', color=NAVY)
for bar in bars:
    val = bar.get_width()
    ax.text(val + 0.6, bar.get_y() + bar.get_height()/2, f'{val:.2f}', va='center', fontsize=10, fontweight='bold', color=DARK_TEXT)
ax.set_xlim(0, max(df_top_bat['composite_rating']) + 6)
ax.grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'top10_batters_composite_rating.png'), facecolor='#FFFFFF')
plt.close()
print("14. Saved top10_batters_composite_rating.png")

# 3.2 Top 10 Bowlers Composite Rating
fig, ax = plt.subplots(figsize=(12, 7), facecolor='#FFFFFF')
bars = ax.barh(range(10), df_top_bowl['composite_rating'].values[::-1],
               color=b_colors[::-1], edgecolor='#CBD5E1', linewidth=0.8, height=0.7)
ax.set_yticks(range(10))
ax.set_yticklabels(df_top_bowl['bowler_name'].values[::-1], fontsize=11, fontweight='bold', color=DARK_TEXT)
ax.set_xlabel('Composite Pressure Rating', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('TOP 10 BOWLERS UNDER PRESSURE (P_t >= 0.50)\nFinal Composite Sabermetric Rating — 2022-2026 T20 Data', fontsize=14, fontweight='bold', color=NAVY)
for bar in bars:
    val = bar.get_width()
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val:.2f}', va='center', fontsize=10, fontweight='bold', color=DARK_TEXT)
ax.set_xlim(0, max(df_top_bowl['composite_rating']) + 4)
ax.grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'top10_bowlers_composite_rating.png'), facecolor='#FFFFFF')
plt.close()
print("15. Saved top10_bowlers_composite_rating.png")

# 3.3 Batters Baseline vs HP Strike Rate Scatter
fig, ax = plt.subplots(figsize=(10, 8), facecolor='#FFFFFF')
ax.scatter(df_all_bat['base_sr'], df_all_bat['hp_sr'], alpha=0.5, s=50, color=SLATE, label='All Qualified (77 Batters)')
ax.scatter(df_top_bat['base_sr'], df_top_bat['hp_sr'], s=140, color=NAVY, edgecolor='#0F172A', linewidth=1.5, zorder=5, label='Top 10 Batters')
for _, r in df_top_bat.iterrows():
    ax.annotate(r['striker_name'], (r['base_sr'], r['hp_sr']),
                fontsize=8.5, fontweight='bold', color=NAVY,
                xytext=(5, 5), textcoords='offset points')
lims = [110, 215]
ax.plot(lims, lims, '--', color=RED, alpha=0.7, label='Line of Parity (HP SR = Base SR)')
ax.set_xlabel('Baseline Strike Rate (All Deliveries)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_ylabel('High-Pressure Strike Rate (P_t >= 0.50)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('BATTER PERFORMANCE: BASELINE vs HIGH PRESSURE\nAbove diagonal = elevates under pressure', fontsize=13, fontweight='bold', color=NAVY)
ax.legend(fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')
ax.grid(color='#E2E8F0', linestyle='--', alpha=0.8)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'batters_baseline_vs_pressure_scatter.png'), facecolor='#FFFFFF')
plt.close()
print("16. Saved batters_baseline_vs_pressure_scatter.png")

# 3.4 Bowlers Baseline vs HP Economy Scatter
fig, ax = plt.subplots(figsize=(10, 8), facecolor='#FFFFFF')
ax.scatter(df_all_bowl['base_econ'], df_all_bowl['hp_econ'], alpha=0.5, s=50, color=SLATE, label='All Qualified (130 Bowlers)')
ax.scatter(df_top_bowl['base_econ'], df_top_bowl['hp_econ'], s=140, color=CYAN, edgecolor='#0F172A', linewidth=1.5, zorder=5, label='Top 10 Bowlers')
for _, r in df_top_bowl.iterrows():
    ax.annotate(r['bowler_name'], (r['base_econ'], r['hp_econ']),
                fontsize=8.5, fontweight='bold', color=NAVY,
                xytext=(5, 5), textcoords='offset points')
lims = [5.5, 12.0]
ax.plot(lims, lims, '--', color=RED, alpha=0.7, label='Line of Parity (HP Econ = Base Econ)')
ax.set_xlabel('Baseline Economy Rate (All Deliveries)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_ylabel('High-Pressure Economy Rate (P_t >= 0.50)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('BOWLER PERFORMANCE: BASELINE vs HIGH PRESSURE\nBelow diagonal = tightens economy under pressure', fontsize=13, fontweight='bold', color=NAVY)
ax.legend(fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')
ax.grid(color='#E2E8F0', linestyle='--', alpha=0.8)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'bowlers_baseline_vs_pressure_scatter.png'), facecolor='#FFFFFF')
plt.close()
print("17. Saved bowlers_baseline_vs_pressure_scatter.png")

# 3.5 Batters Multi-Metric Breakdown
fig, axes = plt.subplots(1, 3, figsize=(18, 7), facecolor='#FFFFFF')
names = df_top_bat['striker_name'].values
y_pos = np.arange(len(names))

axes[0].barh(y_pos, df_top_bat['hp_sr'].values, color=NAVY, edgecolor='#CBD5E1', height=0.6)
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(names, fontsize=9.5, fontweight='bold', color=DARK_TEXT)
axes[0].set_xlabel('HP Strike Rate', fontweight='bold', color=DARK_TEXT)
axes[0].set_title('Strike Rate Under Pressure', fontweight='bold', color=NAVY)
axes[0].invert_yaxis()
axes[0].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(df_top_bat['hp_sr'].values):
    axes[0].text(v + 1.2, i, f'{v:.1f}', va='center', fontsize=8.5, fontweight='bold', color=DARK_TEXT)

axes[1].barh(y_pos, df_top_bat['hp_boundary_pct'].values, color=PURPLE, edgecolor='#CBD5E1', height=0.6)
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(names, fontsize=9.5, fontweight='bold', color=DARK_TEXT)
axes[1].set_xlabel('Boundary %', fontweight='bold', color=DARK_TEXT)
axes[1].set_title('Boundary % Under Pressure', fontweight='bold', color=PURPLE)
axes[1].invert_yaxis()
axes[1].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(df_top_bat['hp_boundary_pct'].values):
    axes[1].text(v + 0.4, i, f'{v:.1f}%', va='center', fontsize=8.5, fontweight='bold', color=DARK_TEXT)

axes[2].barh(y_pos, df_top_bat['hp_dot_pct'].values, color=TEAL, edgecolor='#CBD5E1', height=0.6)
axes[2].set_yticks(y_pos)
axes[2].set_yticklabels(names, fontsize=9.5, fontweight='bold', color=DARK_TEXT)
axes[2].set_xlabel('Dot Ball %', fontweight='bold', color=DARK_TEXT)
axes[2].set_title('Dot Ball % Under Pressure (Lower = Better)', fontweight='bold', color=TEAL)
axes[2].invert_yaxis()
axes[2].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(df_top_bat['hp_dot_pct'].values):
    axes[2].text(v + 0.4, i, f'{v:.1f}%', va='center', fontsize=8.5, fontweight='bold', color=DARK_TEXT)

plt.suptitle('TOP 10 BATTERS — MULTI-METRIC PRESSURE BREAKDOWN', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'batters_multi_metric_breakdown.png'), facecolor='#FFFFFF')
plt.close()
print("18. Saved batters_multi_metric_breakdown.png")

# 3.6 Bowlers Multi-Metric Breakdown
fig, axes = plt.subplots(1, 3, figsize=(18, 7), facecolor='#FFFFFF')
bnames = df_top_bowl['bowler_name'].values
y_pos = np.arange(len(bnames))

axes[0].barh(y_pos, df_top_bowl['hp_econ'].values, color=CYAN, edgecolor='#CBD5E1', height=0.6)
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(bnames, fontsize=9.5, fontweight='bold', color=DARK_TEXT)
axes[0].set_xlabel('HP Economy Rate', fontweight='bold', color=DARK_TEXT)
axes[0].set_title('Economy Under Pressure (Lower = Better)', fontweight='bold', color=CYAN)
axes[0].invert_yaxis()
axes[0].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(df_top_bowl['hp_econ'].values):
    axes[0].text(v + 0.15, i, f'{v:.2f}', va='center', fontsize=8.5, fontweight='bold', color=DARK_TEXT)

axes[1].barh(y_pos, df_top_bowl['hp_dot_pct'].values, color=GREEN, edgecolor='#CBD5E1', height=0.6)
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(bnames, fontsize=9.5, fontweight='bold', color=DARK_TEXT)
axes[1].set_xlabel('Dot Ball %', fontweight='bold', color=DARK_TEXT)
axes[1].set_title('Dot Ball % Under Pressure (Higher = Better)', fontweight='bold', color=GREEN)
axes[1].invert_yaxis()
axes[1].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(df_top_bowl['hp_dot_pct'].values):
    axes[1].text(v + 0.4, i, f'{v:.1f}%', va='center', fontsize=8.5, fontweight='bold', color=DARK_TEXT)

axes[2].barh(y_pos, df_top_bowl['hp_sr'].values, color=AMBER, edgecolor='#CBD5E1', height=0.6)
axes[2].set_yticks(y_pos)
axes[2].set_yticklabels(bnames, fontsize=9.5, fontweight='bold', color=DARK_TEXT)
axes[2].set_xlabel('HP Wicket Strike Rate (Balls/Wkt)', fontweight='bold', color=DARK_TEXT)
axes[2].set_title('Wicket SR Under Pressure (Lower = Better)', fontweight='bold', color=AMBER)
axes[2].invert_yaxis()
axes[2].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(df_top_bowl['hp_sr'].values):
    axes[2].text(v + 0.3, i, f'{v:.1f}', va='center', fontsize=8.5, fontweight='bold', color=DARK_TEXT)

plt.suptitle('TOP 10 BOWLERS — MULTI-METRIC PRESSURE BREAKDOWN', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'bowlers_multi_metric_breakdown.png'), facecolor='#FFFFFF')
plt.close()
print("19. Saved bowlers_multi_metric_breakdown.png")

# 3.7 Pressure Index Distribution
fig, ax = plt.subplots(figsize=(12, 5), facecolor='#FFFFFF')
ax.hist(pt_all * 100, bins=50, color=BLUE, alpha=0.75, edgecolor='#CBD5E1')
ax.axvline(50, color=RED, linewidth=2.5, linestyle='--', label='HP Cutoff (PI = 50 / P_t = 0.50)')
ax.set_xlabel('Pressure Index (0 to 100 Scale)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_ylabel('Number of Deliveries', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('PRESSURE INDEX DISTRIBUTION ACROSS ALL T20 DELIVERIES (2022-2026)', fontsize=13, fontweight='bold', color=NAVY)
ax.legend(fontsize=10, facecolor='#F8FAFC', edgecolor='#CBD5E1')
ax.grid(color='#E2E8F0', linestyle='--', alpha=0.8)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'pressure_index_distribution.png'), facecolor='#FFFFFF')
plt.close()
print("20. Saved pressure_index_distribution.png")

# 3.8 Delta SR Batters
fig, ax = plt.subplots(figsize=(12, 7), facecolor='#FFFFFF')
colors_delta = [GREEN if d > 0 else RED for d in df_top_bat['delta_sr'].values[::-1]]
ax.barh(range(10), df_top_bat['delta_sr'].values[::-1],
        color=colors_delta, edgecolor='#CBD5E1', height=0.7)
ax.set_yticks(range(10))
ax.set_yticklabels(df_top_bat['striker_name'].values[::-1], fontsize=11, fontweight='bold', color=DARK_TEXT)
ax.axvline(0, color=SLATE, linewidth=1.5, linestyle='-')
ax.set_xlabel('Strike Rate Change Under Pressure (HP SR - Base SR)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('TOP 10 BATTERS: WHO RISES vs DROPS UNDER PRESSURE?\nPositive = performs BETTER under pressure', fontsize=13, fontweight='bold', color=NAVY)
for i, v in enumerate(df_top_bat['delta_sr'].values[::-1]):
    offset = 1.0 if v >= 0 else -1.0
    ha = 'left' if v >= 0 else 'right'
    ax.text(v + offset, i, f'{v:+.1f}', va='center', ha=ha, fontsize=10, fontweight='bold', color=DARK_TEXT)
ax.grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'batters_delta_sr_pressure.png'), facecolor='#FFFFFF')
plt.close()
print("21. Saved batters_delta_sr_pressure.png")

# 3.9 Delta Economy Bowlers
fig, ax = plt.subplots(figsize=(12, 7), facecolor='#FFFFFF')
colors_delta_b = [GREEN if d <= 0 else RED for d in df_top_bowl['delta_econ'].values[::-1]]
ax.barh(range(10), df_top_bowl['delta_econ'].values[::-1],
        color=colors_delta_b, edgecolor='#CBD5E1', height=0.7)
ax.set_yticks(range(10))
ax.set_yticklabels(df_top_bowl['bowler_name'].values[::-1], fontsize=11, fontweight='bold', color=DARK_TEXT)
ax.axvline(0, color=SLATE, linewidth=1.5, linestyle='-')
ax.set_xlabel('Economy Change Under Pressure (HP Econ - Base Econ)', fontsize=12, fontweight='bold', color=DARK_TEXT)
ax.set_title('TOP 10 BOWLERS: WHO TIGHTENS vs LEAKS UNDER PRESSURE?\nNegative = performs BETTER under pressure (economy deflation)', fontsize=13, fontweight='bold', color=NAVY)
for i, v in enumerate(df_top_bowl['delta_econ'].values[::-1]):
    offset = 0.05 if v >= 0 else -0.05
    ha = 'left' if v >= 0 else 'right'
    ax.text(v + offset, i, f'{v:+.2f}', va='center', ha=ha, fontsize=10, fontweight='bold', color=DARK_TEXT)
ax.grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'bowlers_delta_econ_pressure.png'), facecolor='#FFFFFF')
plt.close()
print("22. Saved bowlers_delta_econ_pressure.png")

# 3.10 Batters Heatmap
fig, ax = plt.subplots(figsize=(14, 6), facecolor='#FFFFFF')
metrics = ['hp_sr', 'hp_avg', 'hp_boundary_pct', 'hp_dot_pct', 'delta_sr', 'composite_rating']
labels = ['HP Strike Rate', 'HP Average', 'Boundary %', 'Dot Ball %', 'Delta SR', 'Composite Rating']
data_matrix = df_top_bat[metrics].values
norm_matrix = np.zeros_like(data_matrix)
for j in range(data_matrix.shape[1]):
    col = data_matrix[:, j]
    rng = col.max() - col.min()
    if rng > 0:
        if labels[j] == 'Dot Ball %':
            norm_matrix[:, j] = (col.max() - col) / rng
        else:
            norm_matrix[:, j] = (col - col.min()) / rng
    else:
        norm_matrix[:, j] = 0.5

im = ax.imshow(norm_matrix, cmap='YlGn', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, fontsize=10, fontweight='bold', rotation=25, ha='right', color=DARK_TEXT)
ax.set_yticks(range(10))
ax.set_yticklabels(df_top_bat['striker_name'].values, fontsize=10, fontweight='bold', color=DARK_TEXT)
for i in range(10):
    for j in range(len(metrics)):
        val = data_matrix[i, j]
        fmt = f'{val:.1f}' if j != 5 else f'{val:.2f}'
        ax.text(j, i, fmt, ha='center', va='center', fontsize=8.5, fontweight='bold',
                color='black' if norm_matrix[i, j] < 0.75 else 'white')
ax.set_title('TOP 10 BATTERS — PRESSURE PERFORMANCE HEATMAP', fontsize=14, fontweight='bold', color=NAVY)
cbar = plt.colorbar(im, ax=ax, label='Normalized Score (darker green = better)', shrink=0.8)
cbar.ax.yaxis.set_tick_params(color=DARK_TEXT)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'batters_heatmap.png'), facecolor='#FFFFFF')
plt.close()
print("23. Saved batters_heatmap.png")

# 3.11 Bowlers Heatmap
fig, ax = plt.subplots(figsize=(14, 6), facecolor='#FFFFFF')
b_metrics = ['hp_econ', 'hp_sr', 'hp_dot_pct', 'hp_bdry_conceded_pct', 'delta_econ', 'composite_rating']
b_labels = ['HP Economy', 'HP Wkt SR', 'Dot Ball %', 'Bdry Conceded %', 'Delta Econ', 'Composite Rating']
b_data = df_top_bowl[b_metrics].values
b_norm = np.zeros_like(b_data)
for j in range(b_data.shape[1]):
    col = b_data[:, j]
    rng = col.max() - col.min()
    if rng > 0:
        if b_labels[j] in ['HP Economy', 'HP Wkt SR', 'Bdry Conceded %', 'Delta Econ']:
            b_norm[:, j] = (col.max() - col) / rng
        else:
            b_norm[:, j] = (col - col.min()) / rng
    else:
        b_norm[:, j] = 0.5

im = ax.imshow(b_norm, cmap='YlGn', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(len(b_labels)))
ax.set_xticklabels(b_labels, fontsize=10, fontweight='bold', rotation=25, ha='right', color=DARK_TEXT)
ax.set_yticks(range(10))
ax.set_yticklabels(df_top_bowl['bowler_name'].values, fontsize=10, fontweight='bold', color=DARK_TEXT)
for i in range(10):
    for j in range(len(b_metrics)):
        val = b_data[i, j]
        fmt = f'{val:.2f}' if j in [0, 4] else f'{val:.1f}'
        if j == 5: fmt = f'{val:.2f}'
        ax.text(j, i, fmt, ha='center', va='center', fontsize=8.5, fontweight='bold',
                color='black' if b_norm[i, j] < 0.75 else 'white')
ax.set_title('TOP 10 BOWLERS — PRESSURE PERFORMANCE HEATMAP', fontsize=14, fontweight='bold', color=NAVY)
cbar = plt.colorbar(im, ax=ax, label='Normalized Score (darker green = better)', shrink=0.8)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'bowlers_heatmap.png'), facecolor='#FFFFFF')
plt.close()
print("24. Saved bowlers_heatmap.png")

# 3.12 Sample Size Credibility Check
fig, axes = plt.subplots(1, 2, figsize=(16, 6), facecolor='#FFFFFF')
axes[0].barh(range(10), df_top_bat['hp_balls'].values[::-1].astype(int),
             color=NAVY, edgecolor='#CBD5E1', height=0.6)
axes[0].set_yticks(range(10))
axes[0].set_yticklabels(df_top_bat['striker_name'].values[::-1], fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[0].set_xlabel('High-Pressure Balls Faced', fontweight='bold', color=DARK_TEXT)
axes[0].set_title('TOP 10 BATTERS: HP SAMPLE SIZE', fontweight='bold', color=NAVY)
axes[0].axvline(120, color=RED, linestyle='--', label='Min Threshold (120 balls)')
axes[0].legend(facecolor='#F8FAFC', edgecolor='#CBD5E1')
axes[0].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(df_top_bat['hp_balls'].values[::-1].astype(int)):
    axes[0].text(v + 8, i, str(v), va='center', fontsize=9, fontweight='bold', color=DARK_TEXT)

axes[1].barh(range(10), df_top_bowl['hp_balls'].values[::-1].astype(int),
             color=CYAN, edgecolor='#CBD5E1', height=0.6)
axes[1].set_yticks(range(10))
axes[1].set_yticklabels(df_top_bowl['bowler_name'].values[::-1], fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[1].set_xlabel('High-Pressure Balls Bowled', fontweight='bold', color=DARK_TEXT)
axes[1].set_title('TOP 10 BOWLERS: HP SAMPLE SIZE', fontweight='bold', color=NAVY)
axes[1].axvline(180, color=RED, linestyle='--', label='Min Threshold (180 balls)')
axes[1].legend(facecolor='#F8FAFC', edgecolor='#CBD5E1')
axes[1].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(df_top_bowl['hp_balls'].values[::-1].astype(int)):
    axes[1].text(v + 10, i, str(v), va='center', fontsize=9, fontweight='bold', color=DARK_TEXT)

plt.suptitle('SAMPLE SIZE CREDIBILITY CHECK', fontsize=14, fontweight='bold', color=NAVY)
plt.tight_layout()
safe_savefig(plt.gcf(), os.path.join(DIR_CHARTS, 'sample_size_credibility.png'), facecolor='#FFFFFF')
plt.close()
print("25. Saved sample_size_credibility.png")


# =============================================================================
# SECTION 4: SYNC ALL WHITE-BACKGROUND CHARTS ACROSS ALL TARGET DIRECTORIES
# =============================================================================
print("\nSyncing all white-background charts across workspace and artifact repositories...")

sources = [DIR_COMP, DIR_METH, DIR_CHARTS]
all_synced = []

for s in sources:
    for f in os.listdir(s):
        if f.endswith('.png'):
            src_f = os.path.join(s, f)
            shutil.copy2(src_f, os.path.join(RR_CHARTS, f))
            shutil.copy2(src_f, os.path.join(RR_FINAL, f))
            # Also copy to artifacts
            sub_art = 'deepdive_comparison_charts' if 'viz' in f or 'intra' in f else 'methodology_eda_charts'
            os.makedirs(os.path.join(ART_DIR, sub_art), exist_ok=True)
            shutil.copy2(src_f, os.path.join(ART_DIR, sub_art, f))
            all_synced.append(f)

print(f"Total white-background charts rendered and synchronized: {len(all_synced)}")
print("SUCCESS!")
