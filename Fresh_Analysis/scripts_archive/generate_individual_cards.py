import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\individual_player_eda'
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    'figure.dpi': 150, 'savefig.dpi': 150, 'savefig.bbox': 'tight',
    'font.size': 10, 'axes.titlesize': 12, 'axes.labelsize': 10,
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

def render_batter_cards(players, filename, title):
    fig, axes = plt.subplots(len(players), 3, figsize=(18, len(players)*2.6))
    
    for i, p in enumerate(players):
        # Subplot 1: Scorecard / Header Info
        ax_info = axes[i, 0]
        ax_info.axis('off')
        
        info_text = (
            f"#{p['rank']}  {p['name'].upper()}\n"
            f"Status: {p['team']} | Rating: {p['rating']:.2f}\n"
            f"──────────────────────────────────────────\n"
            f"• HP Strike Rate : {p['hp_sr']:.1f} (Norm: {p['norm_sr']:.1f} | Δ: +{p['uplift']:.1f})\n"
            f"• HP Average     : {p['hp_avg']:.1f} | Balls: {p['balls']} b\n"
            f"• Dot Ball %     : {p['dot_pct']:.1f}% | Net bRAA: +{p['braa']:.1f}\n"
            f"• Positive Match : {p['pos_pct']:.1f}%"
        )
        ax_info.text(0.05, 0.5, info_text, va='center', fontsize=10.5, family='monospace',
                     fontweight='bold', color='white',
                     bbox=dict(boxstyle='round,pad=0.6', facecolor='#161B22', edgecolor=GOLD if p['rank']<=3 else CYAN, linewidth=1.5))
        
        # Subplot 2: Pace vs Spin Matchup
        ax_craft = axes[i, 1]
        craft_y = [1, 0]
        craft_vals = [p['vs_pace'], p['vs_spin']]
        bars = ax_craft.barh(craft_y, craft_vals, height=0.45, color=['#388BFD', '#2EA043'], edgecolor='#30363D')
        ax_craft.set_yticks(craft_y)
        ax_craft.set_yticklabels(['vs. Pace', 'vs. Spin'], fontsize=9, fontweight='bold')
        ax_craft.set_xlim(0, 225)
        ax_craft.set_title(f"Craft Matchup Split (Δ: {p['vs_pace'] - p['vs_spin']:+.1f} SR)", fontsize=10, fontweight='bold', color=CYAN)
        ax_craft.grid(axis='x', alpha=0.25)
        for b in bars:
            w = b.get_width()
            ax_craft.text(w + 3, b.get_y() + b.get_height()/2, f"{w:.1f}", va='center', fontsize=9, fontweight='bold', color='white')
            
        # Subplot 3: Scenario Value Decomposition (bRAA)
        ax_scen = axes[i, 2]
        scen_y = [2, 1, 0]
        scen_vals = [p['chase_braa'], p['death_braa'], p['coll_braa']]
        scen_labels = ['2nd Chase', '1st Death', 'Collapse']
        colors_scen = [CYAN, MAGENTA, ORANGE]
        
        bars_s = ax_scen.barh(scen_y, scen_vals, height=0.45, color=colors_scen, edgecolor='#30363D')
        ax_scen.set_yticks(scen_y)
        ax_scen.set_yticklabels(scen_labels, fontsize=9, fontweight='bold')
        ax_scen.axvline(0, color='white', linewidth=0.8, linestyle='--')
        ax_scen.set_xlim(-60, 200)
        ax_scen.set_title(f"Scenario Value Decomposition (Total bRAA: +{p['braa']:.0f})", fontsize=10, fontweight='bold', color=GOLD)
        ax_scen.grid(axis='x', alpha=0.25)
        for b in bars_s:
            w = b.get_width()
            offset = 4 if w >= 0 else -18
            ax_scen.text(w + offset, b.get_y() + b.get_height()/2, f"{w:+.0f}", va='center', fontsize=8.5, fontweight='bold', color='white')

    plt.suptitle(title, fontsize=14, fontweight='bold', color='white', y=1.005)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, filename))
    plt.close()
    print(f"Saved {filename}")

def render_bowler_cards(players, filename, title):
    fig, axes = plt.subplots(len(players), 3, figsize=(18, len(players)*2.6))
    
    for i, p in enumerate(players):
        # Subplot 1: Scorecard / Header Info
        ax_info = axes[i, 0]
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
                     fontweight='bold', color='white',
                     bbox=dict(boxstyle='round,pad=0.6', facecolor='#161B22', edgecolor=GOLD if p['rank']<=3 else CYAN, linewidth=1.5))
        
        # Subplot 2: Phase Dominance Breakdown (wRSA)
        ax_phase = axes[i, 1]
        phase_y = [2, 1, 0]
        phase_vals = [p['pp_wrsa'], p['mid_wrsa'], p['death_wrsa']]
        phase_labels = ['Powerplay', 'Middle', 'Death']
        colors_phase = [ORANGE, CYAN, RED]
        
        bars = ax_phase.barh(phase_y, phase_vals, height=0.45, color=colors_phase, edgecolor='#30363D')
        ax_phase.set_yticks(phase_y)
        ax_phase.set_yticklabels(phase_labels, fontsize=9, fontweight='bold')
        ax_phase.axvline(0, color='white', linewidth=0.8, linestyle='--')
        ax_phase.set_xlim(-25, 220)
        ax_phase.set_title(f"Phase Runs Saved wRSA (Total: +{p['wrsa']:.0f})", fontsize=10, fontweight='bold', color=CYAN)
        ax_phase.grid(axis='x', alpha=0.25)
        for b in bars:
            w = b.get_width()
            offset = 4 if w >= 0 else -18
            ax_phase.text(w + offset, b.get_y() + b.get_height()/2, f"{w:+.0f}", va='center', fontsize=8.5, fontweight='bold', color='white')
            
        # Subplot 3: Choke Index & Boundary Resistance
        ax_choke = axes[i, 2]
        choke_y = [1, 0]
        choke_vals = [p['dot_pct'], p['bdry_pct']]
        bars_c = ax_choke.barh(choke_y, choke_vals, height=0.45, color=[GREEN, RED], edgecolor='#30363D')
        ax_choke.set_yticks(choke_y)
        ax_choke.set_yticklabels(['Dot Ball %', 'Bdry Conc %'], fontsize=9, fontweight='bold')
        ax_choke.set_xlim(0, 55)
        ax_choke.set_title(f"Choke Ratio: {p['dot_pct']:.1f}% Dots vs {p['bdry_pct']:.1f}% Bdry", fontsize=10, fontweight='bold', color=GREEN)
        ax_choke.grid(axis='x', alpha=0.25)
        for b in bars_c:
            w = b.get_width()
            ax_choke.text(w + 1.2, b.get_y() + b.get_height()/2, f"{w:.1f}%", va='center', fontsize=9, fontweight='bold', color='white')

    plt.suptitle(title, fontsize=14, fontweight='bold', color='white', y=1.005)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, filename))
    plt.close()
    print(f"Saved {filename}")

# Generate all 4 visual card dashboards
render_batter_cards(batters_all[:5], 'card_batters_rank_1_to_5.png', 'TOP 10 BATTERS UNDER PRESSURE: FORENSIC EDA CARDS (RANK 1 TO 5)')
render_batter_cards(batters_all[5:], 'card_batters_rank_6_to_10.png', 'TOP 10 BATTERS UNDER PRESSURE: FORENSIC EDA CARDS (RANK 6 TO 10)')
render_bowler_cards(bowlers_all[:5], 'card_bowlers_rank_1_to_5.png', 'TOP 10 BOWLERS UNDER PRESSURE: FORENSIC EDA CARDS (RANK 1 TO 5)')
render_bowler_cards(bowlers_all[5:], 'card_bowlers_rank_6_to_10.png', 'TOP 10 BOWLERS UNDER PRESSURE: FORENSIC EDA CARDS (RANK 6 TO 10)')

print("ALL 4 INDIVIDUAL PLAYER FORENSIC CARDS GENERATED SUCCESSFULLY!")
