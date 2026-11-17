"""
Recent 2-Year Performance Deep-Dive (2025-2026 vs 2022-2024)
Analyzes the Top 10 Batters and Top 10 Bowlers across modern seasons.
Tracks form progression, strike rate uplift evolution, economy suppression trends,
and high-pressure reliability over the last past two years.
"""

import os, sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = r"c:\Users\Asus-2025\Downloads\RR"
DATASET_DIR = os.path.join(BASE_DIR, "Dataset")
OUTPUT_DIR = os.path.join(BASE_DIR, "Fresh_Analysis")
CHARTS_DIR = os.path.join(BASE_DIR, "final_pressure_charts_white_bg")
ARTIFACT_DIR = r"C:\Users\Asus-2025\.gemini\antigravity\brain\4fe6158e-0e76-450a-898e-f6d09dd602e6"

for d in [OUTPUT_DIR, CHARTS_DIR]:
    os.makedirs(d, exist_ok=True)

print("1. Loading raw datasets...")
bbb = pd.read_csv(os.path.join(DATASET_DIR, "ball_by_ball.csv"))
matches = pd.read_csv(os.path.join(DATASET_DIR, "matches.csv"))
comps = pd.read_csv(os.path.join(DATASET_DIR, "competitions.csv"))
ctpm = pd.read_csv(os.path.join(DATASET_DIR, "competition_team_player_mapping.csv"))

# Exclusions
pak_pids = set(ctpm[ctpm['team_name'].str.contains('Pakistan', case=False, na=False)]['player_id'].unique())
ret_df = pd.read_csv(os.path.join(BASE_DIR, "retired_ipl_players.csv"))
ret_names_set = set(ret_df['Player'].dropna().str.strip().str.lower().unique())
newly_confirmed_retirees = {
    'ravichandran ashwin', 'r ashwin', 'ashwin', 'mahendra singh dhoni', 'ms dhoni', 'm s dhoni', 'dhoni',
    'dinesh karthik', 'd karthik', 'ambati rayudu', 'a rayudu', 'matthew wade', 'm wade',
    'andre russell', 'a russell', 'alex hales', 'a hales', 'david willey', 'd willey',
    'dwayne bravo', 'dj bravo', 'kieron pollard', 'k pollard', 'shikhar dhawan', 's dhawan',
    'wriddhiman saha', 'w saha', 'travis head', 't head', 'mitchell starc', 'm starc'
}
all_retirees = ret_names_set | newly_confirmed_retirees
all_player_names = set(bbb['striker_name'].dropna().unique()) | set(bbb['bowler_name'].dropna().unique())
ret_matched = {n for n in all_player_names if n.strip().lower() in all_retirees}
ret_pids = set(bbb[bbb['striker_name'].isin(ret_matched)]['striker_id'].unique()) | set(bbb[bbb['bowler_name'].isin(ret_matched)]['bowler_id'].unique())
total_excl = pak_pids | ret_pids

df = bbb[~bbb['striker_id'].isin(total_excl) & ~bbb['bowler_id'].isin(total_excl)].copy()
df = df.merge(matches[['match_id', 'match_date', 'first_inn_revised_overs', 'second_inn_revised_overs', 'revised_target']], on='match_id', how='left')
df['year'] = pd.to_datetime(df['match_date']).dt.year
df['period'] = np.where(df['year'] >= 2025, '2025-2026', '2022-2024')

# Match state reconstruction
matches['first_inn_balls'] = np.where(matches['first_inn_revised_overs'].notnull() & (matches['first_inn_revised_overs'] > 0), matches['first_inn_revised_overs'], 120).astype(int)
matches['second_inn_balls'] = np.where(matches['second_inn_revised_overs'].notnull() & (matches['second_inn_revised_overs'] > 0), matches['second_inn_revised_overs'], matches['first_inn_balls']).astype(int)

is_wide = (df['extras_type'] == 'wide')
is_overstep = (df['extras_type'] == 'Overstep')
is_bye_lb = df['extras_type'].isin(['byes', 'legbyes'])
is_penalty = (df['extras_type'] == 'Penalty')

df['ball_runs'] = df['runs'] + (is_wide | is_overstep | is_bye_lb).astype(int) + df['extras_2_runs'].fillna(0) + (is_penalty.astype(int) * 5)
df['bowler_runs'] = df['runs'] + (is_wide | is_overstep).astype(int) + df['extras_2_runs'].fillna(0)
df['is_legal'] = (~(is_wide | is_overstep)).astype(int)
df['balls_faced'] = (~is_wide).astype(int)
df['is_batter_dot'] = ((df['runs'] == 0) & (~is_wide)).astype(int)
df['is_bowler_dot'] = ((df['bowler_runs'] == 0) & (df['is_legal'] == 1)).astype(int)
df['is_striker_dismissed'] = (df['is_wicket'] == 1) & (df['dismissed_player_id'] == df['striker_id'])
bowler_wkts = ['Bowled', 'Caught', 'LBW', 'Stump', 'Hit Wicket']
df['is_bowler_wkt'] = (df['is_wicket'] == 1) & (df['dismissal_type'].isin(bowler_wkts))

df = df.sort_values(['match_id', 'innings', 'overid', 'over_ball_num']).copy()
df['cum_runs'] = df.groupby(['match_id', 'innings'])['ball_runs'].cumsum()
df['cum_wkts'] = df.groupby(['match_id', 'innings'])['is_wicket'].cumsum()
df['cum_legal'] = df.groupby(['match_id', 'innings'])['is_legal'].cumsum()

df['score_before'] = df['cum_runs'] - df['ball_runs']
df['wkts_before'] = df['cum_wkts'] - df['is_wicket']
df['legal_balls_bowled'] = df['cum_legal'] - df['is_legal']

df = df.merge(matches[['match_id', 'comp_id', 'first_inn_balls', 'second_inn_balls']], on='match_id', how='left')
df['total_legal_balls'] = np.where(df['innings'] == 1, df['first_inn_balls'], df['second_inn_balls'])
df['balls_remaining'] = np.maximum(0, df['total_legal_balls'] - df['legal_balls_bowled'])
df['overs_remaining'] = df['balls_remaining'] / 6.0

inn1_tot = df[df['innings'] == 1].groupby('match_id')['ball_runs'].sum().rename('inn1_score')
df = df.merge(inn1_tot, on='match_id', how='left')
df['effective_target'] = np.where(df['innings'] == 2, np.where(df['revised_target'].notnull() & (df['revised_target'] > 0), df['revised_target'], df['inn1_score'] + 1), np.nan)
df['runs_needed'] = np.where(df['innings'] == 2, np.maximum(0, df['effective_target'] - df['score_before']), np.nan)
df['rrr'] = np.where((df['innings'] == 2) & (df['balls_remaining'] > 0), df['runs_needed'] / np.maximum(0.1, df['overs_remaining']), np.nan)
df['rrr_clipped'] = df['rrr'].clip(0, 36.0)

comp_avg = df[df['innings'] == 1].groupby('comp_id')['ball_runs'].sum() / np.maximum(1, df[df['innings'] == 1].groupby('comp_id')['match_id'].nunique())
df['comp_par_base'] = df['comp_id'].map(comp_avg).fillna(165.0)
df['par_total'] = df['comp_par_base'] * (df['total_legal_balls'] / 120.0)
df['par_at_ball'] = df['par_total'] * (df['legal_balls_bowled'] / np.maximum(1, df['total_legal_balls']))
df['par_deficit'] = df['par_at_ball'] - df['score_before']

def get_phase(o):
    if o <= 6: return 'Powerplay'
    elif o <= 15: return 'Middle'
    else: return 'Death'
df['phase'] = df['overid'].apply(get_phase)

# Pressure Index
phase_w_bat = df['phase'].map({'Powerplay': 1.0, 'Middle': 2.2, 'Death': 3.8})
pi_bat_1st = (12.0 * phase_w_bat + 6.5 * df['wkts_before'] + np.clip(0.8 * df['par_deficit'], -15, 25)).clip(5, 95)
pi_bat_2nd = (22.0 * (df['rrr_clipped'] / 8.0) + 5.5 * df['wkts_before'] + 16.0 * (1.0 - df['balls_remaining'] / df['total_legal_balls'])).clip(5, 98)
df['pressure_index_bat'] = np.where(df['innings'] == 1, pi_bat_1st, pi_bat_2nd).round(1)

opp_wkts_in_hand = (10 - df['wkts_before']).clip(1, 10)
phase_w_bowl = df['phase'].map({'Powerplay': 1.2, 'Middle': 0.9, 'Death': 2.2})
cur_rr = np.where(df['legal_balls_bowled'] > 0, df['score_before'] / (df['legal_balls_bowled'] / 6.0), df['par_total'] / 20.0)
delta_rr = np.clip(cur_rr - (df['par_total'] / 20.0), -4.0, 5.0)
pi_bowl_1st = (15.0 + 12.0 * phase_w_bowl + 4.0 * delta_rr + 2.5 * (opp_wkts_in_hand - 5)).clip(10, 95)

req_run_per_ball = np.where(df['balls_remaining'] > 0, df['runs_needed'] / df['balls_remaining'], 0.0)
tension = np.maximum(0, 1.0 - np.abs(req_run_per_ball - 1.4) / 1.4)
progression = 1.0 - (df['balls_remaining'] / df['total_legal_balls'])
death_bowl_bonus = np.where(df['phase'] == 'Death', 18.0, 0.0)
is_blowout = (req_run_per_ball > 3.0) & (opp_wkts_in_hand <= 3)

pi_bowl_2nd = np.where(is_blowout, 15.0, (18.0 + 22.0 * progression + 24.0 * tension + death_bowl_bonus + 2.5 * (opp_wkts_in_hand - 4)).clip(10, 98))
df['pressure_index_bowl'] = np.where(df['innings'] == 1, pi_bowl_1st, pi_bowl_2nd).round(1)

df['is_hp_bat'] = df['pressure_index_bat'] >= 65
df['is_hp_bowl'] = df['pressure_index_bowl'] >= 65

# Load Target Lists
ab = pd.read_csv(os.path.join(OUTPUT_DIR, "scratch_top10_available_batters_auction.csv"))
aw = pd.read_csv(os.path.join(OUTPUT_DIR, "scratch_top10_available_bowlers_auction.csv"))

target_batters = ab['player_name'].tolist()
target_bowlers = aw['player_name'].tolist()

print("\n--- 2. Computing 2-Year Split Metrics for Batters ---")
bat_records = []

for name in target_batters:
    p_df = df[df['striker_name'].str.lower() == name.lower()]
    
    # 2025-2026
    r2_all = p_df[p_df['year'].isin([2025, 2026])]
    r2_hp = r2_all[r2_all['is_hp_bat']]
    r2_base = r2_all[~r2_all['is_hp_bat']]
    
    # 2022-2024
    e_all = p_df[p_df['year'].isin([2022, 2023, 2024])]
    e_hp = e_all[e_all['is_hp_bat']]
    e_base = e_all[~e_all['is_hp_bat']]
    
    # Year-by-year
    y25 = p_df[p_df['year'] == 2025]
    y26 = p_df[p_df['year'] == 2026]
    
    # Compute metrics
    r2_balls = r2_all['balls_faced'].sum()
    r2_runs = r2_all['runs'].sum()
    r2_sr = (r2_runs / np.maximum(1, r2_balls)) * 100.0 if r2_balls > 0 else np.nan
    
    r2_hp_balls = r2_hp['balls_faced'].sum()
    r2_hp_runs = r2_hp['runs'].sum()
    r2_hp_sr = (r2_hp_runs / np.maximum(1, r2_hp_balls)) * 100.0 if r2_hp_balls > 0 else np.nan
    r2_base_sr = (r2_base['runs'].sum() / np.maximum(1, r2_base['balls_faced'].sum())) * 100.0 if r2_base['balls_faced'].sum() > 0 else np.nan
    r2_uplift = (r2_hp_sr - r2_base_sr) if (not np.isnan(r2_hp_sr) and not np.isnan(r2_base_sr)) else np.nan
    r2_hp_avg = (r2_hp_runs / np.maximum(1, r2_hp['is_striker_dismissed'].sum())) if r2_hp_balls > 0 else np.nan
    r2_bdry_pct = ((r2_hp['is_four'].sum() + r2_hp['is_six'].sum()) / np.maximum(1, r2_hp_balls)) * 100.0 if r2_hp_balls > 0 else np.nan
    r2_dot_pct = (r2_hp['is_batter_dot'].sum() / np.maximum(1, r2_hp_balls)) * 100.0 if r2_hp_balls > 0 else np.nan
    
    # Early metrics
    e_hp_balls = e_hp['balls_faced'].sum()
    e_hp_sr = (e_hp['runs'].sum() / np.maximum(1, e_hp_balls)) * 100.0 if e_hp_balls > 0 else np.nan
    e_base_sr = (e_base['runs'].sum() / np.maximum(1, e_base['balls_faced'].sum())) * 100.0 if e_base['balls_faced'].sum() > 0 else np.nan
    e_uplift = (e_hp_sr - e_base_sr) if (not np.isnan(e_hp_sr) and not np.isnan(e_base_sr)) else np.nan
    
    # 2-Year Trend
    delta_trend = (r2_hp_sr - e_hp_sr) if (not np.isnan(r2_hp_sr) and not np.isnan(e_hp_sr)) else np.nan
    
    if np.isnan(delta_trend):
        trajectory = "Emerging Modern Asset"
    elif delta_trend >= 15.0:
        trajectory = "Surging / Peak Form (▲▲)"
    elif delta_trend >= 0.0:
        trajectory = "Progressive Growth (▲)"
    elif delta_trend >= -15.0:
        trajectory = "High-Floor Stable (■)"
    else:
        trajectory = "Cooling Down (▼)"
        
    bat_records.append({
        'player_name': name,
        'r2_matches': r2_all['match_id'].nunique(),
        'r2_total_balls': r2_balls,
        'r2_total_runs': r2_runs,
        'r2_overall_sr': round(r2_sr, 1) if not np.isnan(r2_sr) else np.nan,
        'r2_hp_balls': r2_hp_balls,
        'r2_hp_runs': r2_hp_runs,
        'r2_hp_sr': round(r2_hp_sr, 1) if not np.isnan(r2_hp_sr) else np.nan,
        'r2_clutch_uplift': round(r2_uplift, 1) if not np.isnan(r2_uplift) else np.nan,
        'r2_hp_avg': round(r2_hp_avg, 1) if not np.isnan(r2_hp_avg) else np.nan,
        'r2_hp_boundary_pct': round(r2_bdry_pct, 1) if not np.isnan(r2_bdry_pct) else np.nan,
        'r2_hp_dot_pct': round(r2_dot_pct, 1) if not np.isnan(r2_dot_pct) else np.nan,
        'early_hp_sr': round(e_hp_sr, 1) if not np.isnan(e_hp_sr) else np.nan,
        'delta_trend_hp_sr': round(delta_trend, 1) if not np.isnan(delta_trend) else np.nan,
        'form_trajectory': trajectory
    })

bat_2y = pd.DataFrame(bat_records)
bat_2y_path = os.path.join(OUTPUT_DIR, "top10_batters_recent_2y_performance.csv")
bat_2y.to_csv(bat_2y_path, index=False)
print(f"Exported Batters 2Y Performance -> {bat_2y_path}")

print("\n--- 3. Computing 2-Year Split Metrics for Bowlers ---")
bowl_records = []

for name in target_bowlers:
    p_df = df[df['bowler_name'].str.lower() == name.lower()]
    
    r2_all = p_df[p_df['year'].isin([2025, 2026])]
    r2_hp = r2_all[r2_all['is_hp_bowl']]
    r2_base = r2_all[~r2_all['is_hp_bowl']]
    
    e_all = p_df[p_df['year'].isin([2022, 2023, 2024])]
    e_hp = e_all[e_all['is_hp_bowl']]
    e_base = e_all[~e_all['is_hp_bowl']]
    
    # 2025-2026 metrics
    r2_balls = r2_all['is_legal'].sum()
    r2_runs = r2_all['bowler_runs'].sum()
    r2_wkts = r2_all['is_bowler_wkt'].sum()
    r2_econ = (r2_runs / np.maximum(1, r2_balls / 6.0)) if r2_balls > 0 else np.nan
    r2_wkt_sr = (r2_balls / np.maximum(1, r2_wkts)) if r2_wkts > 0 else np.nan
    
    r2_hp_balls = r2_hp['is_legal'].sum()
    r2_hp_runs = r2_hp['bowler_runs'].sum()
    r2_hp_wkts = r2_hp['is_bowler_wkt'].sum()
    r2_hp_econ = (r2_hp_runs / np.maximum(1, r2_hp_balls / 6.0)) if r2_hp_balls > 0 else np.nan
    r2_base_econ = (r2_base['bowler_runs'].sum() / np.maximum(1, r2_base['is_legal'].sum() / 6.0)) if r2_base['is_legal'].sum() > 0 else np.nan
    r2_suppr = (r2_hp_econ - r2_base_econ) if (not np.isnan(r2_hp_econ) and not np.isnan(r2_base_econ)) else np.nan
    r2_hp_wkt_sr = (r2_hp_balls / np.maximum(1, r2_hp_wkts)) if r2_hp_wkts > 0 else np.nan
    r2_dot_pct = (r2_hp['is_bowler_dot'].sum() / np.maximum(1, r2_hp_balls)) * 100.0 if r2_hp_balls > 0 else np.nan
    r2_bdry_pct = (((r2_hp['is_four'].sum() + r2_hp['is_six'].sum()) / np.maximum(1, r2_hp_balls)) * 100.0) if r2_hp_balls > 0 else np.nan
    
    # Early metrics
    e_hp_balls = e_hp['is_legal'].sum()
    e_hp_econ = (e_hp['bowler_runs'].sum() / np.maximum(1, e_hp_balls / 6.0)) if e_hp_balls > 0 else np.nan
    e_hp_wkts = e_hp['is_bowler_wkt'].sum()
    e_hp_wkt_sr = (e_hp_balls / np.maximum(1, e_hp_wkts)) if e_hp_wkts > 0 else np.nan
    
    # 2-Year Trend: Economy improvement (negative delta is good)
    delta_econ_trend = (r2_hp_econ - e_hp_econ) if (not np.isnan(r2_hp_econ) and not np.isnan(e_hp_econ)) else np.nan
    
    if np.isnan(delta_econ_trend):
        trajectory = "Emerging Modern Bowler"
    elif delta_econ_trend <= -0.80:
        trajectory = "Sharpening Containment (▲▲)"
    elif delta_econ_trend <= 0.20:
        trajectory = "Solid Control (▲)"
    elif delta_econ_trend <= 1.20:
        trajectory = "Consistent Workhorse (■)"
    else:
        trajectory = "Conceding Leakage (▼)"
        
    bowl_records.append({
        'player_name': name,
        'r2_matches': r2_all['match_id'].nunique(),
        'r2_total_balls': r2_balls,
        'r2_total_wkts': r2_wkts,
        'r2_overall_econ': round(r2_econ, 2) if not np.isnan(r2_econ) else np.nan,
        'r2_hp_balls': r2_hp_balls,
        'r2_hp_wkts': r2_hp_wkts,
        'r2_hp_econ': round(r2_hp_econ, 2) if not np.isnan(r2_hp_econ) else np.nan,
        'r2_delta_econ': round(r2_suppr, 2) if not np.isnan(r2_suppr) else np.nan,
        'r2_hp_wkt_sr': round(r2_hp_wkt_sr, 1) if not np.isnan(r2_hp_wkt_sr) else np.nan,
        'r2_hp_dot_pct': round(r2_dot_pct, 1) if not np.isnan(r2_dot_pct) else np.nan,
        'early_hp_econ': round(e_hp_econ, 2) if not np.isnan(e_hp_econ) else np.nan,
        'delta_trend_hp_econ': round(delta_econ_trend, 2) if not np.isnan(delta_econ_trend) else np.nan,
        'form_trajectory': trajectory
    })

bowl_2y = pd.DataFrame(bowl_records)
bowl_2y_path = os.path.join(OUTPUT_DIR, "top10_bowlers_recent_2y_performance.csv")
bowl_2y.to_csv(bowl_2y_path, index=False)
print(f"Exported Bowlers 2Y Performance -> {bowl_2y_path}")

# -----------------------------------------------------------------------------
# 4. Generate Publication-Quality White Background Visualizations (#FFFFFF)
# -----------------------------------------------------------------------------
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14), facecolor='#FFFFFF')

RR_PINK = '#E73895'
RR_BLUE = '#001D48'
RR_TEAL = '#0288D1'
RR_GOLD = '#C59B27'

# Plot 1: Batters 2Y (2025-2026) High-Pressure SR vs Early Cycle (2022-2024)
xb = np.arange(len(bat_2y))
w = 0.35
ax1.bar(xb - w/2, bat_2y['r2_hp_sr'].fillna(0), width=w, color=RR_PINK, edgecolor=RR_BLUE, label='Recent 2 Years (2025-2026) HP SR')
ax1.bar(xb + w/2, bat_2y['early_hp_sr'].fillna(0), width=w, color='#90A4AE', edgecolor='#37474F', label='Early Cycle (2022-2024) HP SR')
ax1.set_facecolor('#FFFFFF')
ax1.set_title('Top 10 Available Batters: High-Pressure Strike Rate Evolution\nComparing 2025-2026 Form vs 2022-2024 Baseline', fontsize=12, fontweight='bold', color=RR_BLUE, pad=12)
ax1.set_ylabel('High-Pressure Strike Rate', fontsize=11, fontweight='bold', color=RR_BLUE)
ax1.set_xticks(xb)
ax1.set_xticklabels(bat_2y['player_name'], rotation=30, ha='right', fontsize=9.5, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.4, color='#CCCCCC')
ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CCCCCC')

for i in range(len(bat_2y)):
    val = bat_2y['r2_hp_sr'].iloc[i]
    if not np.isnan(val) and val > 0:
        ax1.text(i - w/2, val + 2, f"{val:.1f}", ha='center', fontsize=9, fontweight='bold', color=RR_BLUE)

# Plot 2: Batters 2-Year Clutch Uplift vs High-Pressure Average
valid_bat = bat_2y.dropna(subset=['r2_clutch_uplift', 'r2_hp_avg']).copy()
ax2.scatter(valid_bat['r2_clutch_uplift'], valid_bat['r2_hp_avg'], color=RR_PINK, s=valid_bat['r2_hp_balls']*2.0, edgecolors=RR_BLUE, linewidth=1.5)
ax2.set_facecolor('#FFFFFF')
ax2.set_title('Top Available Batters: Recent 2-Year Clutch Uplift vs HP Average (2025-2026)\nBubble size proportional to 2025-2026 HP Balls Faced | Top-Right is Elite', fontsize=12, fontweight='bold', color=RR_BLUE, pad=12)
ax2.set_xlabel('Recent 2-Year Clutch Uplift (ΔSR = HP SR - Base SR)', fontsize=11, fontweight='bold', color=RR_BLUE)
ax2.set_ylabel('Recent 2-Year High-Pressure Batting Average', fontsize=11, fontweight='bold', color=RR_BLUE)
ax2.grid(True, linestyle='--', alpha=0.4, color='#CCCCCC')

for idx, r in valid_bat.iterrows():
    ax2.annotate(r['player_name'], (r['r2_clutch_uplift'], r['r2_hp_avg']), xytext=(5, 3), textcoords='offset points', fontsize=9.5, fontweight='bold', color=RR_BLUE)

# Plot 3: Bowlers 2Y (2025-2026) High-Pressure Economy vs Early Cycle (2022-2024)
xbow = np.arange(len(bowl_2y))
ax3.bar(xbow - w/2, bowl_2y['r2_hp_econ'].fillna(0), width=w, color=RR_BLUE, edgecolor=RR_PINK, label='Recent 2 Years (2025-2026) HP Econ')
ax3.bar(xbow + w/2, bowl_2y['early_hp_econ'].fillna(0), width=w, color='#78909C', edgecolor='#263238', label='Early Cycle (2022-2024) HP Econ')
ax3.set_facecolor('#FFFFFF')
ax3.set_title('Top 10 Available Bowlers: High-Pressure Economy Evolution\nComparing 2025-2026 Containment vs 2022-2024 Baseline (Lower is Better)', fontsize=12, fontweight='bold', color=RR_BLUE, pad=12)
ax3.set_ylabel('High-Pressure Economy Rate', fontsize=11, fontweight='bold', color=RR_BLUE)
ax3.set_xticks(xbow)
ax3.set_xticklabels(bowl_2y['player_name'], rotation=30, ha='right', fontsize=9.5, fontweight='bold')
ax3.grid(axis='y', linestyle='--', alpha=0.4, color='#CCCCCC')
ax3.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CCCCCC')

for i in range(len(bowl_2y)):
    val = bowl_2y['r2_hp_econ'].iloc[i]
    if not np.isnan(val) and val > 0:
        ax3.text(i - w/2, val + 0.2, f"{val:.2f}", ha='center', fontsize=9, fontweight='bold', color=RR_BLUE)

# Plot 4: Bowlers 2-Year HP Economy vs HP Wickets Taken (2025-2026)
valid_bowl = bowl_2y.dropna(subset=['r2_hp_econ', 'r2_hp_wkts']).copy()
ax4.scatter(valid_bowl['r2_hp_wkts'], valid_bowl['r2_hp_econ'], color=RR_TEAL, s=valid_bowl['r2_hp_balls']*2.0, edgecolors=RR_BLUE, linewidth=1.5)
ax4.set_facecolor('#FFFFFF')
ax4.set_title('Top Available Bowlers: Recent 2-Year HP Wickets vs HP Economy (2025-2026)\nBubble size proportional to 2025-2026 HP Balls Bowled | Bottom-Right is Elite', fontsize=12, fontweight='bold', color=RR_BLUE, pad=12)
ax4.set_xlabel('Recent 2-Year High-Pressure Wickets Taken (2025-2026)', fontsize=11, fontweight='bold', color=RR_BLUE)
ax4.set_ylabel('Recent 2-Year High-Pressure Economy Rate (Lower is Better)', fontsize=11, fontweight='bold', color=RR_BLUE)
ax4.grid(True, linestyle='--', alpha=0.4, color='#CCCCCC')

for idx, r in valid_bowl.iterrows():
    ax4.annotate(r['player_name'], (r['r2_hp_wkts'], r['r2_hp_econ']), xytext=(5, 3), textcoords='offset points', fontsize=9.5, fontweight='bold', color=RR_BLUE)

plt.tight_layout(pad=3.0)
fig_path = os.path.join(CHARTS_DIR, "recent_2y_pressure_deepdive.png")
plt.savefig(fig_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
plt.close()

import shutil
shutil.copy2(fig_path, os.path.join(ARTIFACT_DIR, "recent_2y_pressure_deepdive.png"))
print(f"Saved: {fig_path}")
print("\nSUCCESS: 2-Year deepdive metrics and visualization generated flawlessly!")
