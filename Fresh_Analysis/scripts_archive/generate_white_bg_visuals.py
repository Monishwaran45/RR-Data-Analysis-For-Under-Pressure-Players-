import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Paths
DIR_CARDS = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\individual_player_eda'
DIR_DEEPDIVE = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\deepdive_comparison_charts'
DIR_COMP = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\comparison_charts'
DIR_METHOD = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\methodology_eda_charts'

for d in [DIR_CARDS, DIR_DEEPDIVE, DIR_COMP, DIR_METHOD]:
    os.makedirs(d, exist_ok=True)

# PRISTINE WHITE BACKGROUND THEME
plt.rcParams.update({
    'figure.dpi': 150, 'savefig.dpi': 150, 'savefig.bbox': 'tight',
    'font.size': 10, 'axes.titlesize': 12, 'axes.labelsize': 11,
    'figure.facecolor': '#FFFFFF', 'axes.facecolor': '#FFFFFF',
    'text.color': '#111827', 'axes.labelcolor': '#111827',
    'xtick.color': '#374151', 'ytick.color': '#374151',
    'axes.edgecolor': '#D1D5DB', 'grid.color': '#E5E7EB',
})

# Crisp professional colors
NAVY = '#1E3A8A'
BLUE = '#2563EB'
LIGHT_BLUE = '#60A5FA'
TEAL = '#0D9488'
GREEN = '#16A34A'
RED = '#DC2626'
AMBER = '#D97706'
PURPLE = '#7C3AED'
DARK = '#1F2937'

# Data
batters_all = [
    {'rank': 1, 'name': 'Tim David', 'team': 'Available Pool', 'rating': 47.12, 'hp_sr': 194.6, 'norm_sr': 161.8, 'uplift': 32.8, 'hp_avg': 42.7, 'braa': 449.2, 'vs_pace': 207.5, 'vs_spin': 145.5, 'chase_braa': 130, 'death_braa': 180, 'coll_braa': 140, 'pos_pct': 70.5, 'dot_pct': 31.0, 'balls': 592},
    {'rank': 2, 'name': 'Shashank Singh', 'team': 'PBKS Retained', 'rating': 32.36, 'hp_sr': 170.9, 'norm_sr': 152.0, 'uplift': 18.9, 'hp_avg': 48.7, 'braa': 165.8, 'vs_pace': 178.3, 'vs_spin': 156.2, 'chase_braa': 75, 'death_braa': 100, 'coll_braa': -10, 'pos_pct': 71.4, 'dot_pct': 29.5, 'balls': 285},
    {'rank': 3, 'name': 'Rinku Singh', 'team': 'KKR Retained', 'rating': 31.84, 'hp_sr': 172.2, 'norm_sr': 133.8, 'uplift': 38.3, 'hp_avg': 38.9, 'braa': 313.9, 'vs_pace': 184.8, 'vs_spin': 132.2, 'chase_braa': 125, 'death_braa': 130, 'coll_braa': 60, 'pos_pct': 65.6, 'dot_pct': 30.9, 'balls': 632},
    {'rank': 4, 'name': 'Rishabh Pant', 'team': 'LSG Retained', 'rating': 31.17, 'hp_sr': 183.7, 'norm_sr': 133.1, 'uplift': 50.6, 'hp_avg': 34.6, 'braa': 142.7, 'vs_pace': 201.1, 'vs_spin': 130.0, 'chase_braa': 38, 'death_braa': 115, 'coll_braa': 15, 'pos_pct': 68.8, 'dot_pct': 31.9, 'balls': 245},
    {'rank': 5, 'name': 'Tristan Stubbs', 'team': 'DC Retained', 'rating': 30.24, 'hp_sr': 171.5, 'norm_sr': 130.2, 'uplift': 41.3, 'hp_avg': 42.1, 'braa': 250.6, 'vs_pace': 172.0, 'vs_spin': 170.1, 'chase_braa': 160, 'death_braa': 130, 'coll_braa': -40, 'pos_pct': 63.3, 'dot_pct': 24.3, 'balls': 516},
    {'rank': 6, 'name': 'Tilak Varma', 'team': 'MI Retained', 'rating': 26.27, 'hp_sr': 164.4, 'norm_sr': 135.7, 'uplift': 28.7, 'hp_avg': 40.5, 'braa': 275.8, 'vs_pace': 174.3, 'vs_spin': 132.0, 'chase_braa': 132, 'death_braa': 125, 'coll_braa': 20, 'pos_pct': 66.7, 'dot_pct': 28.6, 'balls': 640},
    {'rank': 7, 'name': 'Marcus Stoinis', 'team': 'Available Pool', 'rating': 23.45, 'hp_sr': 175.3, 'norm_sr': 143.9, 'uplift': 31.5, 'hp_avg': 30.7, 'braa': 158.8, 'vs_pace': 188.4, 'vs_spin': 133.7, 'chase_braa': 45, 'death_braa': 85, 'coll_braa': 30, 'pos_pct': 60.9, 'dot_pct': 29.9, 'balls': 385},
    {'rank': 8, 'name': 'Suryakumar Yadav', 'team': 'MI Retained', 'rating': 21.62, 'hp_sr': 192.1, 'norm_sr': 162.0, 'uplift': 30.2, 'hp_avg': 32.6, 'braa': 195.3, 'vs_pace': 203.4, 'vs_spin': 163.5, 'chase_braa': 40, 'death_braa': 140, 'coll_braa': 15, 'pos_pct': 62.5, 'dot_pct': 28.0, 'balls': 407},
    {'rank': 9, 'name': 'Rovman Powell', 'team': 'Available Pool', 'rating': 20.39, 'hp_sr': 157.4, 'norm_sr': 138.6, 'uplift': 18.8, 'hp_avg': 27.2, 'braa': 224.4, 'vs_pace': 173.4, 'vs_spin': 128.6, 'chase_braa': 142, 'death_braa': 60, 'coll_braa': 25, 'pos_pct': 50.7, 'dot_pct': 34.0, 'balls': 674},
    {'rank': 10, 'name': 'Dasun Shanaka', 'team': 'Available Pool', 'rating': 18.60, 'hp_sr': 157.0, 'norm_sr': 121.2, 'uplift': 35.8, 'hp_avg': 23.3, 'braa': 104.0, 'vs_pace': 168.7, 'vs_spin': 130.5, 'chase_braa': 90, 'death_braa': 25, 'coll_braa': -12, 'pos_pct': 53.3, 'dot_pct': 33.6, 'balls': 386},
]

bowlers_all = [
    {'rank': 1, 'name': 'Jasprit Bumrah', 'team': 'MI Retained', 'rating': 28.39, 'hp_econ': 7.08, 'norm_econ': 7.22, 'delta_econ': -0.14, 'wkt_sr': 13.05, 'wkts': 39, 'wrsa': 247.1, 'pp_wrsa': 20, 'mid_wrsa': 25, 'death_wrsa': 202, 'pos_pct': 64.9, 'dot_pct': 38.8, 'bdry_pct': 12.8, 'balls': 509},
    {'rank': 2, 'name': 'Matheesha Pathirana', 'team': 'CSK Retained', 'rating': 26.37, 'hp_econ': 8.35, 'norm_econ': 8.83, 'delta_econ': -0.48, 'wkt_sr': 10.27, 'wkts': 44, 'wrsa': 205.9, 'pp_wrsa': 12, 'mid_wrsa': 20, 'death_wrsa': 174, 'pos_pct': 71.8, 'dot_pct': 39.0, 'bdry_pct': 15.0, 'balls': 452},
    {'rank': 3, 'name': 'Wanindu Hasaranga', 'team': 'Available Pool', 'rating': 22.47, 'hp_econ': 7.64, 'norm_econ': 8.00, 'delta_econ': -0.36, 'wkt_sr': 10.07, 'wkts': 45, 'wrsa': 185.9, 'pp_wrsa': 8, 'mid_wrsa': 75, 'death_wrsa': 103, 'pos_pct': 56.5, 'dot_pct': 42.4, 'bdry_pct': 13.6, 'balls': 453},
    {'rank': 4, 'name': 'Yuzvendra Chahal', 'team': 'Available Pool', 'rating': 22.26, 'hp_econ': 8.57, 'norm_econ': 8.61, 'delta_econ': -0.04, 'wkt_sr': 12.03, 'wkts': 39, 'wrsa': 182.3, 'pp_wrsa': 45, 'mid_wrsa': 72, 'death_wrsa': 65, 'pos_pct': 50.9, 'dot_pct': 33.5, 'bdry_pct': 14.7, 'balls': 469},
    {'rank': 5, 'name': 'Kuldeep Yadav', 'team': 'DC Retained', 'rating': 20.54, 'hp_econ': 7.46, 'norm_econ': 8.16, 'delta_econ': -0.70, 'wkt_sr': 10.61, 'wkts': 38, 'wrsa': 162.3, 'pp_wrsa': 0, 'mid_wrsa': 92, 'death_wrsa': 70, 'pos_pct': 55.6, 'dot_pct': 39.4, 'bdry_pct': 12.5, 'balls': 403},
    {'rank': 6, 'name': 'Sam Curran', 'team': 'Available Pool', 'rating': 17.50, 'hp_econ': 10.67, 'norm_econ': 9.28, 'delta_econ': 1.39, 'wkt_sr': 13.17, 'wkts': 24, 'wrsa': 83.8, 'pp_wrsa': -12, 'mid_wrsa': 0, 'death_wrsa': 96, 'pos_pct': 38.3, 'dot_pct': 26.6, 'bdry_pct': 22.5, 'balls': 316},
    {'rank': 7, 'name': 'Sunil Narine', 'team': 'KKR Retained', 'rating': 17.12, 'hp_econ': 6.27, 'norm_econ': 7.01, 'delta_econ': -0.74, 'wkt_sr': 15.09, 'wkts': 22, 'wrsa': 115.5, 'pp_wrsa': 8, 'mid_wrsa': 28, 'death_wrsa': 80, 'pos_pct': 68.8, 'dot_pct': 42.5, 'bdry_pct': 9.6, 'balls': 332},
    {'rank': 8, 'name': 'Rashid Khan', 'team': 'GT Retained', 'rating': 15.48, 'hp_econ': 7.28, 'norm_econ': 7.45, 'delta_econ': -0.17, 'wkt_sr': 12.55, 'wkts': 56, 'wrsa': 187.7, 'pp_wrsa': -2, 'mid_wrsa': 20, 'death_wrsa': 170, 'pos_pct': 60.8, 'dot_pct': 39.2, 'bdry_pct': 12.2, 'balls': 703},
    {'rank': 9, 'name': 'Arshdeep Singh', 'team': 'PBKS Retained', 'rating': 14.88, 'hp_econ': 9.22, 'norm_econ': 9.06, 'delta_econ': 0.16, 'wkt_sr': 11.15, 'wkts': 75, 'wrsa': 166.7, 'pp_wrsa': -4, 'mid_wrsa': 42, 'death_wrsa': 128, 'pos_pct': 55.5, 'dot_pct': 36.3, 'bdry_pct': 19.7, 'balls': 836},
    {'rank': 10, 'name': 'Taskin Ahmed', 'team': 'Available Pool', 'rating': 12.68, 'hp_econ': 8.40, 'norm_econ': 7.76, 'delta_econ': 0.64, 'wkt_sr': 11.92, 'wkts': 26, 'wrsa': 94.8, 'pp_wrsa': 18, 'mid_wrsa': 82, 'death_wrsa': -5, 'pos_pct': 56.8, 'dot_pct': 41.9, 'bdry_pct': 16.8, 'balls': 310},
]

# Helper for pure numpy KDE
def kde_np(data, x_grid, bw=None):
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

# ─────────────────────────────────────────────────────────────────────────────
# PART 1: INDIVIDUAL FORENSIC PLAYER CARDS (WHITE BACKGROUND)
# ─────────────────────────────────────────────────────────────────────────────
def render_batter_cards_white(players, filename, title):
    fig, axes = plt.subplots(len(players), 3, figsize=(18, len(players)*2.6))
    fig.patch.set_facecolor('#FFFFFF')
    
    for i, p in enumerate(players):
        # 1: Info box
        ax_info = axes[i, 0]
        ax_info.set_facecolor('#FFFFFF')
        ax_info.axis('off')
        
        info_text = (
            f"#{p['rank']}  {p['name'].upper()}\n"
            f"Status: {p['team']} | Rating: {p['rating']:.2f}\n"
            f"──────────────────────────────────────────\n"
            f"• HP Strike Rate : {p['hp_sr']:.1f} (Norm: {p['norm_sr']:.1f} | Δ: +{p['uplift']:.1f})\n"
            f"• HP Average     : {p['hp_avg']:.1f} | Volume: {p['balls']} b\n"
            f"• Dot Ball %     : {p['dot_pct']:.1f}% | Net bRAA: +{p['braa']:.1f}\n"
            f"• Positive Match : {p['pos_pct']:.1f}%"
        )
        ax_info.text(0.05, 0.5, info_text, va='center', fontsize=10.5, family='monospace',
                     fontweight='bold', color='#111827',
                     bbox=dict(boxstyle='round,pad=0.6', facecolor='#F9FAFB', edgecolor=AMBER if p['rank']<=3 else BLUE, linewidth=2))
        
        # 2: Craft matchup
        ax_craft = axes[i, 1]
        ax_craft.set_facecolor('#FFFFFF')
        craft_y = [1, 0]
        craft_vals = [p['vs_pace'], p['vs_spin']]
        bars = ax_craft.barh(craft_y, craft_vals, height=0.45, color=[BLUE, TEAL], edgecolor='#1E3A8A')
        ax_craft.set_yticks(craft_y)
        ax_craft.set_yticklabels(['vs. Pace', 'vs. Spin'], fontsize=9.5, fontweight='bold', color='#111827')
        ax_craft.set_xlim(0, 230)
        ax_craft.set_title(f"Craft Matchup Split (Δ: {p['vs_pace'] - p['vs_spin']:+.1f} SR)", fontsize=10, fontweight='bold', color=NAVY)
        ax_craft.grid(axis='x', color='#E5E7EB', linestyle='--')
        for b in bars:
            w = b.get_width()
            ax_craft.text(w + 3, b.get_y() + b.get_height()/2, f"{w:.1f}", va='center', fontsize=9, fontweight='bold', color='#111827')
            
        # 3: Scenario bRAA
        ax_scen = axes[i, 2]
        ax_scen.set_facecolor('#FFFFFF')
        scen_y = [2, 1, 0]
        scen_vals = [p['chase_braa'], p['death_braa'], p['coll_braa']]
        scen_labels = ['2nd Chase', '1st Death', 'Collapse']
        colors_scen = [NAVY, PURPLE, AMBER]
        
        bars_s = ax_scen.barh(scen_y, scen_vals, height=0.45, color=colors_scen, edgecolor='#374151')
        ax_scen.set_yticks(scen_y)
        ax_scen.set_yticklabels(scen_labels, fontsize=9.5, fontweight='bold', color='#111827')
        ax_scen.axvline(0, color='#111827', linewidth=1, linestyle='--')
        ax_scen.set_xlim(-60, 205)
        ax_scen.set_title(f"Scenario Value Decomposition (Total bRAA: +{p['braa']:.0f})", fontsize=10, fontweight='bold', color='#B45309')
        ax_scen.grid(axis='x', color='#E5E7EB', linestyle='--')
        for b in bars_s:
            w = b.get_width()
            offset = 4 if w >= 0 else -18
            ax_scen.text(w + offset, b.get_y() + b.get_height()/2, f"{w:+.0f}", va='center', fontsize=9, fontweight='bold', color='#111827')

    plt.suptitle(title, fontsize=14, fontweight='bold', color=DARK, y=1.005)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_CARDS, filename), facecolor='#FFFFFF')
    plt.close()
    print(f"Saved {filename}")

def render_bowler_cards_white(players, filename, title):
    fig, axes = plt.subplots(len(players), 3, figsize=(18, len(players)*2.6))
    fig.patch.set_facecolor('#FFFFFF')
    
    for i, p in enumerate(players):
        # 1: Info box
        ax_info = axes[i, 0]
        ax_info.set_facecolor('#FFFFFF')
        ax_info.axis('off')
        
        info_text = (
            f"#{p['rank']}  {p['name'].upper()}\n"
            f"Status: {p['team']} | Rating: {p['rating']:.2f}\n"
            f"──────────────────────────────────────────\n"
            f"• HP Economy     : {p['hp_econ']:.2f} (Norm: {p['norm_econ']:.2f} | Δ: {p['delta_econ']:+.2f})\n"
            f"• Wickets & SR   : {p['wkts']} w | {p['wkt_sr']:.1f} balls/wkt\n"
            f"• Choke Metrics  : Dot: {p['dot_pct']:.1f}% | Bdry Conc: {p['bdry_pct']:.1f}%\n"
            f"• Net HP wRSA    : +{p['wrsa']:.1f} | Pos Match: {p['pos_pct']:.1f}%"
        )
        ax_info.text(0.05, 0.5, info_text, va='center', fontsize=10.5, family='monospace',
                     fontweight='bold', color='#111827',
                     bbox=dict(boxstyle='round,pad=0.6', facecolor='#F9FAFB', edgecolor=AMBER if p['rank']<=3 else BLUE, linewidth=2))
        
        # 2: Phase runs saved
        ax_phase = axes[i, 1]
        ax_phase.set_facecolor('#FFFFFF')
        phase_y = [2, 1, 0]
        phase_vals = [p['pp_wrsa'], p['mid_wrsa'], p['death_wrsa']]
        phase_labels = ['Powerplay', 'Middle', 'Death']
        colors_phase = [AMBER, BLUE, RED]
        
        bars = ax_phase.barh(phase_y, phase_vals, height=0.45, color=colors_phase, edgecolor='#374151')
        ax_phase.set_yticks(phase_y)
        ax_phase.set_yticklabels(phase_labels, fontsize=9.5, fontweight='bold', color='#111827')
        ax_phase.axvline(0, color='#111827', linewidth=1, linestyle='--')
        ax_phase.set_xlim(-25, 230)
        ax_phase.set_title(f"Phase Runs Saved wRSA (Total: +{p['wrsa']:.0f})", fontsize=10, fontweight='bold', color=BLUE)
        ax_phase.grid(axis='x', color='#E5E7EB', linestyle='--')
        for b in bars:
            w = b.get_width()
            offset = 4 if w >= 0 else -18
            ax_phase.text(w + offset, b.get_y() + b.get_height()/2, f"{w:+.0f}", va='center', fontsize=9, fontweight='bold', color='#111827')
            
        # 3: Choke ratio
        ax_choke = axes[i, 2]
        ax_choke.set_facecolor('#FFFFFF')
        choke_y = [1, 0]
        choke_vals = [p['dot_pct'], p['bdry_pct']]
        bars_c = ax_choke.barh(choke_y, choke_vals, height=0.45, color=[GREEN, RED], edgecolor='#374151')
        ax_choke.set_yticks(choke_y)
        ax_choke.set_yticklabels(['Dot Ball %', 'Bdry Conc %'], fontsize=9.5, fontweight='bold', color='#111827')
        ax_choke.set_xlim(0, 55)
        ax_choke.set_title(f"Choke Ratio: {p['dot_pct']:.1f}% Dots vs {p['bdry_pct']:.1f}% Bdry", fontsize=10, fontweight='bold', color=GREEN)
        ax_choke.grid(axis='x', color='#E5E7EB', linestyle='--')
        for b in bars_c:
            w = b.get_width()
            ax_choke.text(w + 1.2, b.get_y() + b.get_height()/2, f"{w:.1f}%", va='center', fontsize=9, fontweight='bold', color='#111827')

    plt.suptitle(title, fontsize=14, fontweight='bold', color=DARK, y=1.005)
    plt.tight_layout()
    plt.savefig(os.path.join(DIR_CARDS, filename), facecolor='#FFFFFF')
    plt.close()
    print(f"Saved {filename}")

render_batter_cards_white(batters_all[:5], 'card_batters_rank_1_to_5.png', 'TOP 10 BATTERS UNDER PRESSURE: FORENSIC EDA CARDS (RANK 1 TO 5)')
render_batter_cards_white(batters_all[5:], 'card_batters_rank_6_to_10.png', 'TOP 10 BATTERS UNDER PRESSURE: FORENSIC EDA CARDS (RANK 6 TO 10)')
render_bowler_cards_white(bowlers_all[:5], 'card_bowlers_rank_1_to_5.png', 'TOP 10 BOWLERS UNDER PRESSURE: FORENSIC EDA CARDS (RANK 1 TO 5)')
render_bowler_cards_white(bowlers_all[5:], 'card_bowlers_rank_6_to_10.png', 'TOP 10 BOWLERS UNDER PRESSURE: FORENSIC EDA CARDS (RANK 6 TO 10)')

# ─────────────────────────────────────────────────────────────────────────────
# PART 2: DATASET MACRO DEEP-DIVE COMPARISONS (WHITE BACKGROUND)
# ─────────────────────────────────────────────────────────────────────────────
df_bat = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\eda_all_eligible_batters_complete.csv')
df_bowl = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\eda_all_eligible_bowlers_complete.csv')

# VIZ 1: Batters density distributions
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor('#FFFFFF')
for ax in axes: ax.set_facecolor('#FFFFFF')

bat_active = df_bat[df_bat['hp_balls'] >= 15].copy()
sr_vals = bat_active['hp_strike_rate'].dropna().values
dot_vals = bat_active['hp_dot_pct'].dropna().values

n, bins, patches = axes[0].hist(sr_vals, bins=40, density=True, color='#F3F4F6', edgecolor='#D1D5DB')
x_sr = np.linspace(50, 240, 300)
kde_sr_vals = kde_np(sr_vals, x_sr)
axes[0].plot(x_sr, kde_sr_vals, color=BLUE, linewidth=2.5, label='Dataset Density (815 Batters)')
median_sr = np.median(sr_vals)
axes[0].axvline(median_sr, color='#6B7280', linestyle='--', linewidth=1.5, label=f'Dataset Median: {median_sr:.1f} SR')
axes[0].axvline(149.4, color=PURPLE, linestyle=':', linewidth=1.5, label='Qualified Median: 149.4 SR')

top_batters_simple = [
    ('Tim David', 194.59, AMBER), ('Shashank Singh', 170.88, BLUE), ('Rinku Singh', 172.15, GREEN),
    ('Rishabh Pant', 183.67, RED), ('Tristan Stubbs', 171.51, PURPLE), ('Tilak Varma', 164.38, TEAL),
    ('Marcus Stoinis', 175.32, NAVY), ('Suryakumar Yadav', 192.14, AMBER), ('Rovman Powell', 157.42, '#9333EA'),
    ('Dasun Shanaka', 156.99, '#059669')
]

for name, val, c in top_batters_simple:
    y_val = get_kde_val(val, x_sr, kde_sr_vals)
    axes[0].scatter(val, y_val, color=c, s=75, zorder=5, edgecolor='#111827')

axes[0].annotate('Tim David (194.6)', (194.59, get_kde_val(194.59, x_sr, kde_sr_vals)), xytext=(10, 20), textcoords='offset points',
                 fontsize=9, fontweight='bold', color=AMBER, arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.5))
axes[0].annotate('Suryakumar (192.1)', (192.14, get_kde_val(192.14, x_sr, kde_sr_vals)), xytext=(-80, 35), textcoords='offset points',
                 fontsize=9, fontweight='bold', color=NAVY, arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.5))
axes[0].annotate('Rishabh Pant (183.7)', (183.67, get_kde_val(183.67, x_sr, kde_sr_vals)), xytext=(10, 30), textcoords='offset points',
                 fontsize=9, fontweight='bold', color=RED, arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))

axes[0].set_xlabel('High-Pressure Strike Rate (SR)', fontsize=11, fontweight='bold')
axes[0].set_ylabel('Probability Density', fontsize=11, fontweight='bold')
axes[0].set_title('HIGH-PRESSURE STRIKE RATE: TOP 10 vs ENTIRE DATASET\nAll Top 10 Batters reside in the 86th to 99th percentile', fontsize=12, fontweight='bold', color=NAVY)
axes[0].grid(color='#E5E7EB', linestyle='--')
axes[0].legend(loc='upper right', fontsize=8.5)

# Dot%
n2, bins2, patches2 = axes[1].hist(dot_vals, bins=40, density=True, color='#F3F4F6', edgecolor='#D1D5DB')
x_dot = np.linspace(10, 70, 300)
kde_dot_vals = kde_np(dot_vals, x_dot)
axes[1].plot(x_dot, kde_dot_vals, color=RED, linewidth=2.5, label='Dataset Density (815 Batters)')
median_dot = np.median(dot_vals)
axes[1].axvline(median_dot, color='#6B7280', linestyle='--', linewidth=1.5, label=f'Dataset Median: {median_dot:.1f}% Dots')

top_dots = [('Tristan Stubbs', 24.3, PURPLE), ('Tilak Varma', 28.6, TEAL), ('Suryakumar', 28.0, NAVY), ('Shashank', 29.5, BLUE)]
for name, val, c in top_dots:
    axes[1].scatter(val, get_kde_val(val, x_dot, kde_dot_vals), color=c, s=75, zorder=5, edgecolor='#111827')

axes[1].annotate('Tristan Stubbs\n(24.3% Dots | #1 in Cricket)', (24.3, get_kde_val(24.3, x_dot, kde_dot_vals)), xytext=(-70, 30), textcoords='offset points',
                 fontsize=9, fontweight='bold', color=PURPLE, arrowprops=dict(arrowstyle='->', color=PURPLE, lw=1.5))

axes[1].set_xlabel('High-Pressure Dot Ball Percentage (%) [Lower = Better]', fontsize=11, fontweight='bold')
axes[1].set_ylabel('Probability Density', fontsize=11, fontweight='bold')
axes[1].set_title('DOT BALL SUPPRESSION: TOP 10 vs ENTIRE DATASET\nTop 10 Batters eliminate ball wastage (24% to 34% vs 39.2% median)', fontsize=12, fontweight='bold', color=RED)
axes[1].grid(color='#E5E7EB', linestyle='--')
axes[1].legend(loc='upper right', fontsize=8.5)

plt.suptitle('DATASET-WIDE BENCHMARK: BATTERS POPULATION DISTRIBUTION', fontsize=14, fontweight='bold', color=DARK, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(DIR_DEEPDIVE, 'viz1_batters_dataset_distribution_and_top10.png'), facecolor='#FFFFFF')
plt.close()
print("Saved viz1_batters_dataset_distribution_and_top10.png")

# VIZ 2: Bowlers density distributions
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor('#FFFFFF')
for ax in axes: ax.set_facecolor('#FFFFFF')

bowl_active = df_bowl[df_bowl['hp_balls'] >= 15].copy()
econ_vals = bowl_active['hp_econ'].dropna().values
econ_vals = econ_vals[(econ_vals >= 4.0) & (econ_vals <= 16.0)]
wkt_vals = bowl_active['hp_sr'].dropna().values
wkt_vals = wkt_vals[(wkt_vals >= 5.0) & (wkt_vals <= 45.0)]

n, bins, patches = axes[0].hist(econ_vals, bins=40, density=True, color='#F3F4F6', edgecolor='#D1D5DB')
x_econ = np.linspace(4.5, 15.5, 300)
kde_econ_vals = kde_np(econ_vals, x_econ)
axes[0].plot(x_econ, kde_econ_vals, color=BLUE, linewidth=2.5, label='Dataset Density (601 Bowlers)')
median_econ = np.median(econ_vals)
axes[0].axvline(median_econ, color='#6B7280', linestyle='--', linewidth=1.5, label=f'Dataset Median: {median_econ:.2f} RPO')

top_bowlers_simple = [
    ('Sunil Narine', 6.27, TEAL), ('Jasprit Bumrah', 7.08, AMBER), ('Rashid Khan', 7.28, NAVY),
    ('Kuldeep Yadav', 7.46, PURPLE), ('Wanindu Hasaranga', 7.64, GREEN), ('Matheesha Pathirana', 8.35, BLUE),
    ('Taskin Ahmed', 8.40, '#059669'), ('Yuzvendra Chahal', 8.57, RED), ('Arshdeep Singh', 9.22, '#9333EA'),
    ('Sam Curran', 10.67, '#DC2626')
]

for name, val, c in top_bowlers_simple:
    y_val = get_kde_val(val, x_econ, kde_econ_vals) if (val >= 4.5 and val <= 15.5) else 0.02
    axes[0].scatter(val, y_val, color=c, s=75, zorder=5, edgecolor='#111827')

axes[0].annotate('Sunil Narine (6.27)', (6.27, get_kde_val(6.27, x_econ, kde_econ_vals)), xytext=(-70, 30), textcoords='offset points',
                 fontsize=9, fontweight='bold', color=TEAL, arrowprops=dict(arrowstyle='->', color=TEAL, lw=1.5))
axes[0].annotate('Jasprit Bumrah (7.08)', (7.08, get_kde_val(7.08, x_econ, kde_econ_vals)), xytext=(-70, 45), textcoords='offset points',
                 fontsize=9, fontweight='bold', color=AMBER, arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.5))
axes[0].annotate('Sam Curran (10.67)\n[Defends 12.5 Par]', (10.67, get_kde_val(10.67, x_econ, kde_econ_vals)), xytext=(10, 25), textcoords='offset points',
                 fontsize=8.5, fontweight='bold', color=RED, arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))

axes[0].set_xlabel('High-Pressure Economy Rate (RPO) [Lower = Better]', fontsize=11, fontweight='bold')
axes[0].set_ylabel('Probability Density', fontsize=11, fontweight='bold')
axes[0].set_title('HIGH-PRESSURE ECONOMY: TOP 10 vs ENTIRE DATASET\nChoke masters suppress scoring deep into the left tail', fontsize=12, fontweight='bold', color=BLUE)
axes[0].grid(color='#E5E7EB', linestyle='--')
axes[0].legend(loc='upper right', fontsize=8.5)

# Wkt SR
n2, bins2, patches2 = axes[1].hist(wkt_vals, bins=40, density=True, color='#F3F4F6', edgecolor='#D1D5DB')
x_wkt = np.linspace(6.0, 40.0, 300)
kde_wkt_vals = kde_np(wkt_vals, x_wkt)
axes[1].plot(x_wkt, kde_wkt_vals, color=GREEN, linewidth=2.5, label='Dataset Density (601 Bowlers)')
median_wkt = np.median(wkt_vals)
axes[1].axvline(median_wkt, color='#6B7280', linestyle='--', linewidth=1.5, label=f'Dataset Median: {median_wkt:.1f} balls/wkt')

for name, val, c in [('Hasaranga', 10.07, GREEN), ('Pathirana', 10.27, BLUE), ('Kuldeep', 10.61, PURPLE)]:
    axes[1].scatter(val, get_kde_val(val, x_wkt, kde_wkt_vals), color=c, s=75, zorder=5, edgecolor='#111827')

axes[1].annotate('Hasaranga (10.07)', (10.07, get_kde_val(10.07, x_wkt, kde_wkt_vals)), xytext=(-70, 35), textcoords='offset points',
                 fontsize=9, fontweight='bold', color=GREEN, arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
axes[1].annotate('Pathirana (10.27)', (10.27, get_kde_val(10.27, x_wkt, kde_wkt_vals)), xytext=(10, 25), textcoords='offset points',
                 fontsize=9, fontweight='bold', color=BLUE, arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.5))

axes[1].set_xlabel('High-Pressure Wicket Strike Rate (Balls / Wicket) [Lower = Faster Strike]', fontsize=11, fontweight='bold')
axes[1].set_ylabel('Probability Density', fontsize=11, fontweight='bold')
axes[1].set_title('WICKET-STRIKE VELOCITY: TOP 10 vs ENTIRE DATASET\nTop 10 take a wicket every 10 to 13 balls (vs 17.0 median)', fontsize=12, fontweight='bold', color=GREEN)
axes[1].grid(color='#E5E7EB', linestyle='--')
axes[1].legend(loc='upper right', fontsize=8.5)

plt.suptitle('DATASET-WIDE BENCHMARK: BOWLERS POPULATION DISTRIBUTION', fontsize=14, fontweight='bold', color=DARK, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(DIR_DEEPDIVE, 'viz1_bowlers_dataset_distribution_and_top10.png'), facecolor='#FFFFFF')
plt.close()
print("Saved viz1_bowlers_dataset_distribution_and_top10.png")

# VIZ 3: Macro Scatter Batters
fig, ax = plt.subplots(figsize=(13, 8))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

bg_bat = df_bat[df_bat['hp_balls'] >= 10].copy()
bg_sr = bg_bat['hp_strike_rate'].values
bg_braa = (bg_bat['hp_runs'] - bg_bat['hp_balls'] * 1.45) * 0.7

ax.scatter(bg_sr, bg_braa, color='#D1D5DB', alpha=0.55, s=35, label='Eligible Batters Cloud (815 Players)')

for p in batters_all:
    c = AMBER if p['rank'] == 1 else (PURPLE if p['rank'] in [3, 5, 6] else BLUE)
    ax.scatter(p['hp_sr'], p['braa'], s=p['balls']*0.9, color=c, alpha=0.85, edgecolor='#111827', linewidth=1.5, zorder=5)
    dx, dy = 4, 5
    if p['name'] == 'Tim David': dy = -16
    elif p['name'] == 'Rinku Singh': dy = 10
    elif p['name'] == 'Suryakumar Yadav': dy = -16
    elif p['name'] == 'Tristan Stubbs': dx = -90; dy = 10
    elif p['name'] == 'Tilak Varma': dx = -80; dy = -15
    elif p['name'] == 'Shashank Singh': dx = -90; dy = 5
    
    ax.annotate(f"{p['name']}\n({p['hp_sr']:.1f} SR | +{p['braa']:.0f} bRAA)",
                (p['hp_sr'], p['braa']),
                xytext=(dx, dy), textcoords='offset points',
                fontsize=9, fontweight='bold', color='#111827')

ax.axvline(128.4, color='#6B7280', linestyle='--', alpha=0.7, label='Dataset Median SR (128.4)')
ax.axhline(0, color=RED, linestyle=':', alpha=0.8, label='Breakeven Par Expectation (bRAA = 0)')

ax.set_xlabel('High-Pressure Strike Rate (P_t >= 0.50)', fontsize=12, fontweight='bold')
ax.set_ylabel('Net Context-Adjusted Runs Above Average (bRAA)', fontsize=12, fontweight='bold')
ax.set_title('BATTERS MACRO LANDSCAPE: ALL 815 PLAYERS vs TOP 10 UNDER PRESSURE\nBubble size represents high-pressure balls faced | Top-Right Quadrant = Elite Match Winners', fontsize=13, fontweight='bold', color=DARK, pad=15)
ax.set_xlim(80, 220)
ax.set_ylim(-120, 500)
ax.grid(color='#E5E7EB', linestyle='--')
ax.legend(loc='upper left', fontsize=9.5, framealpha=0.9)

plt.tight_layout()
plt.savefig(os.path.join(DIR_DEEPDIVE, 'viz3_batters_macro_landscape_braa_scatter.png'), facecolor='#FFFFFF')
plt.close()
print("Saved viz3_batters_macro_landscape_braa_scatter.png")

# VIZ 4: Macro Scatter Bowlers
fig, ax = plt.subplots(figsize=(13, 8))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

bg_bowl = df_bowl[df_bowl['hp_balls'] >= 10].copy()
bg_econ = bg_bowl['hp_econ'].values
bg_wrsa = (bg_bowl['hp_balls'] * 1.65 - bg_bowl['hp_runs']) * 0.65

ax.scatter(bg_econ, bg_wrsa, color='#D1D5DB', alpha=0.55, s=35, label='Eligible Bowlers Cloud (601 Players)')

for p in bowlers_all:
    c = AMBER if p['rank'] == 1 else (TEAL if p['rank'] in [2, 7] else BLUE)
    ax.scatter(p['hp_econ'], p['wrsa'], s=p['balls']*0.9, color=c, alpha=0.85, edgecolor='#111827', linewidth=1.5, zorder=5)
    dx, dy = 4, 5
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
                fontsize=9, fontweight='bold', color='#111827')

ax.invert_xaxis()
ax.axvline(9.82, color='#6B7280', linestyle='--', alpha=0.7, label='Dataset Median Econ (9.82 RPO)')
ax.axhline(0, color=RED, linestyle=':', alpha=0.8, label='Breakeven Par Expectation (wRSA = 0)')

ax.set_xlabel('High-Pressure Economy Rate (Inverted: Left to Right = Lower Economy / Better Choke)', fontsize=12, fontweight='bold')
ax.set_ylabel('Net Context-Adjusted Runs Saved (wRSA)', fontsize=12, fontweight='bold')
ax.set_title('BOWLERS MACRO LANDSCAPE: ALL 601 PLAYERS vs TOP 10 UNDER PRESSURE\nBubble size represents high-pressure balls bowled | Top-Right Quadrant = Elite Choke & Wickets', fontsize=13, fontweight='bold', color=DARK, pad=15)
ax.set_xlim(13.5, 5.0)
ax.set_ylim(-100, 300)
ax.grid(color='#E5E7EB', linestyle='--')
ax.legend(loc='upper left', fontsize=9.5, framealpha=0.9)

plt.tight_layout()
plt.savefig(os.path.join(DIR_DEEPDIVE, 'viz4_bowlers_macro_landscape_wrsa_scatter.png'), facecolor='#FFFFFF')
plt.close()
print("Saved viz4_bowlers_macro_landscape_wrsa_scatter.png")

# VIZ 5: Grouped bar benchmarks
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.patch.set_facecolor('#FFFFFF')
for ax in axes: ax.set_facecolor('#FFFFFF')

bat_metrics = ['HP Strike Rate\n(SR)', 'Dot Ball %\n(Lower=Better)', 'Boundary %\n(Higher=Better)']
median_bat = [128.4, 39.2, 14.8]
qual_bat = [149.4, 33.4, 18.8]
top10_bat_v = [176.8, 28.2, 26.4]

x = np.arange(len(bat_metrics))
w = 0.25

b1 = axes[0].bar(x - w, median_bat, width=w, color='#9CA3AF', label='Entire Dataset Median (815 Batters)', edgecolor='#374151')
b2 = axes[0].bar(x, qual_bat, width=w, color=PURPLE, label='Qualified Cohort Avg (124 Batters)', edgecolor='#374151')
b3 = axes[0].bar(x + w, top10_bat_v, width=w, color=AMBER, label='Final Top 10 Elite Avg', edgecolor='#374151')

axes[0].set_xticks(x)
axes[0].set_xticklabels(bat_metrics, fontsize=10, fontweight='bold', color='#111827')
axes[0].set_title('BATTING COHORT GAPS: MEDIAN vs QUALIFIED vs TOP 10', fontsize=12, fontweight='bold', color=NAVY)
axes[0].set_ylabel('Metric Value', fontsize=11, fontweight='bold')
axes[0].grid(axis='y', color='#E5E7EB', linestyle='--')
axes[0].legend(loc='upper right', fontsize=9)

for rect in b1 + b2 + b3:
    h = rect.get_height()
    axes[0].text(rect.get_x() + rect.get_width()/2., h + 2, f"{h:.1f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#111827')
axes[0].set_ylim(0, 205)

bowl_metrics = ['HP Economy\n(Lower=Better)', 'Wicket SR\n(Lower=Better)', 'Boundary Conc %\n(Lower=Better)']
median_bowl = [9.82, 17.0, 21.9]
qual_bowl = [10.29, 17.8, 21.9]
top10_bowl_v = [7.95, 11.9, 14.8]

b4 = axes[1].bar(x - w, median_bowl, width=w, color='#9CA3AF', label='Entire Dataset Median (601 Bowlers)', edgecolor='#374151')
b5 = axes[1].bar(x, qual_bowl, width=w, color=PURPLE, label='Qualified Cohort Avg (45 Bowlers)', edgecolor='#374151')
b6 = axes[1].bar(x + w, top10_bowl_v, width=w, color=BLUE, label='Final Top 10 Elite Avg', edgecolor='#374151')

axes[1].set_xticks(x)
axes[1].set_xticklabels(bowl_metrics, fontsize=10, fontweight='bold', color='#111827')
axes[1].set_title('BOWLING COHORT GAPS: MEDIAN vs QUALIFIED vs TOP 10', fontsize=12, fontweight='bold', color=BLUE)
axes[1].set_ylabel('Metric Value', fontsize=11, fontweight='bold')
axes[1].grid(axis='y', color='#E5E7EB', linestyle='--')
axes[1].legend(loc='upper right', fontsize=9)

for rect in b4 + b5 + b6:
    h = rect.get_height()
    axes[1].text(rect.get_x() + rect.get_width()/2., h + 0.3, f"{h:.1f}", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#111827')
axes[1].set_ylim(0, 26)

plt.suptitle('THE STATISTICAL GAP: HOW THE TOP 10 SEPARATE FROM THE CRICKET POPULATION', fontsize=14, fontweight='bold', color=DARK, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(DIR_DEEPDIVE, 'viz5_cohort_gap_benchmarks_grouped_bar.png'), facecolor='#FFFFFF')
plt.close()
print("Saved viz5_cohort_gap_benchmarks_grouped_bar.png")

# ─────────────────────────────────────────────────────────────────────────────
# PART 3: INTRA-TOP10 HEATMAPS (WHITE BACKGROUND)
# ─────────────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

bat_df = pd.DataFrame(batters_all)
metrics_bat = ['hp_sr', 'hp_avg', 'uplift', 'braa', 'pos_pct', 'dot_pct', 'rating']
cols_label = ['HP Strike Rate', 'HP Average', 'Clutch Uplift', 'Net HP bRAA', 'Positive Match %', 'Dot Ball % (Inv)', 'Pressure Rating']

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
ax.set_xticklabels(cols_label, fontsize=10, fontweight='bold', rotation=20, ha='right', color='#111827')
ax.set_yticks(range(10))
ax.set_yticklabels(bat_df['name'].values, fontsize=11, fontweight='bold', color='#111827')

for i in range(10):
    for j in range(len(metrics_bat)):
        val = data_bat[i, j]
        fmt = f"{val:.1f}" if j in [0, 1, 2, 4, 5, 6] else f"{val:.0f}"
        if j == 2: fmt = f"+{val:.1f}"
        if j == 3: fmt = f"+{val:.0f}"
        if j in [4, 5]: fmt = f"{val:.1f}%"
        color = 'black' if norm_bat[i, j] < 0.75 else 'white'
        ax.text(j, i, fmt, ha='center', va='center', fontsize=9, fontweight='bold', color=color)

ax.set_title('TOP 10 BATTERS: HEAD-TO-HEAD METRIC MATRIX (GREEN = COHORT LEADER)', fontsize=13, fontweight='bold', color=NAVY, pad=15)
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Relative Cohort Rank (1.0 = Best in Top 10)', color='#111827')
cbar.ax.yaxis.set_tick_params(color='#111827')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#111827')

plt.tight_layout()
plt.savefig(os.path.join(DIR_DEEPDIVE, 'intra_top10_batters_matrix.png'), facecolor='#FFFFFF')
plt.close()
print("Saved intra_top10_batters_matrix.png")

# Bowlers Heatmap
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')

bowl_df = pd.DataFrame(bowlers_all)
metrics_bowl = ['hp_econ', 'wkt_sr', 'wrsa', 'pos_pct', 'wkts', 'rating']
cols_bowl_label = ['HP Economy (Inv)', 'Wicket SR (Inv)', 'Net HP wRSA', 'Positive Match %', 'Total HP Wickets', 'Pressure Rating']

data_bowl = bowl_df[metrics_bowl].values.copy()
norm_bowl = np.zeros_like(data_bowl)
for j in range(data_bowl.shape[1]):
    col = data_bowl[:, j]
    rng = col.max() - col.min()
    if metrics_bowl[j] in ['hp_econ', 'wkt_sr']:
        norm_bowl[:, j] = (col.max() - col) / rng
    else:
        norm_bowl[:, j] = (col - col.min()) / rng

im2 = ax.imshow(norm_bowl, cmap='YlGn', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(len(cols_bowl_label)))
ax.set_xticklabels(cols_bowl_label, fontsize=10, fontweight='bold', rotation=20, ha='right', color='#111827')
ax.set_yticks(range(10))
ax.set_yticklabels(bowl_df['name'].values, fontsize=11, fontweight='bold', color='#111827')

for i in range(10):
    for j in range(len(metrics_bowl)):
        val = data_bowl[i, j]
        fmt = f"{val:.2f}" if j == 0 else (f"{val:.1f}" if j in [1, 5] else f"{val:.0f}")
        if j == 2: fmt = f"+{val:.0f}"
        if j == 3: fmt = f"{val:.1f}%"
        color = 'black' if norm_bowl[i, j] < 0.75 else 'white'
        ax.text(j, i, fmt, ha='center', va='center', fontsize=9, fontweight='bold', color=color)

ax.set_title('TOP 10 BOWLERS: HEAD-TO-HEAD METRIC MATRIX (GREEN = COHORT LEADER)', fontsize=13, fontweight='bold', color=NAVY, pad=15)
cbar2 = plt.colorbar(im2, ax=ax, shrink=0.8)
cbar2.set_label('Relative Cohort Rank (1.0 = Best in Top 10)', color='#111827')
cbar2.ax.yaxis.set_tick_params(color='#111827')
plt.setp(plt.getp(cbar2.ax.axes, 'yticklabels'), color='#111827')

plt.tight_layout()
plt.savefig(os.path.join(DIR_DEEPDIVE, 'intra_top10_bowlers_matrix.png'), facecolor='#FFFFFF')
plt.close()
print("Saved intra_top10_bowlers_matrix.png")

print("ALL WHITE-BACKGROUND VISUALIZATIONS GENERATED SUCCESSFULLY!")
