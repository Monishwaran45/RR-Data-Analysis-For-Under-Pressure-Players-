"""
==========================================================================
  RR SupeRR Selector Season 2 — Pressure Analysis Pipeline (Fresh Build)
  Excludes: Pakistan players (68) + Retired IPL players (12 in dataset)
  Output:  Top 10 Batters & Bowlers under pressure (PI >= 65)
==========================================================================
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings, os
warnings.filterwarnings('ignore')

OUT = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis'
DATA = r'c:\Users\Asus-2025\Downloads\RR\Dataset'
os.makedirs(os.path.join(OUT, 'charts'), exist_ok=True)

plt.rcParams.update({
    'figure.dpi': 150, 'savefig.dpi': 150, 'savefig.bbox': 'tight',
    'font.size': 10, 'axes.titlesize': 13, 'axes.labelsize': 11,
    'figure.facecolor': '#0D1117', 'axes.facecolor': '#161B22',
    'text.color': '#C9D1D9', 'axes.labelcolor': '#C9D1D9',
    'xtick.color': '#8B949E', 'ytick.color': '#8B949E',
    'axes.edgecolor': '#30363D', 'grid.color': '#21262D',
})

print("=" * 70)
print("  PHASE 1: DATA INGESTION")
print("=" * 70)

bbb = pd.read_csv(os.path.join(DATA, 'ball_by_ball.csv'))
matches = pd.read_csv(os.path.join(DATA, 'matches.csv'))
comps = pd.read_csv(os.path.join(DATA, 'competitions.csv'))
ctpm = pd.read_csv(os.path.join(DATA, 'competition_team_player_mapping.csv'))
teams = pd.read_csv(os.path.join(DATA, 'teams.csv'))
playing11 = pd.read_csv(os.path.join(DATA, 'playing_eleven.csv'))
retired = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\retired_ipl_players.csv')

print(f"  ball_by_ball     : {bbb.shape[0]:>10,} rows x {bbb.shape[1]} cols")
print(f"  matches          : {matches.shape[0]:>10,} rows")
print(f"  competitions     : {comps.shape[0]:>10,} rows")
print(f"  ctpm             : {ctpm.shape[0]:>10,} rows")
print(f"  teams            : {teams.shape[0]:>10,} rows")
print(f"  playing_eleven   : {playing11.shape[0]:>10,} rows")
print(f"  retired_players  : {retired.shape[0]:>10,} rows")

# ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  PHASE 2: EXCLUSION — PAKISTAN + RETIRED IPL PLAYERS")
print("=" * 70)

# 2a. Pakistan players (via CTPM: team_name contains 'Pakistan')
pak_players = ctpm[ctpm['team_name'].str.contains('Pakistan', case=False, na=False)]
pak_ids = set(pak_players['player_id'].unique())
pak_names = set(pak_players['player_name'].unique())
print(f"  Pakistan player IDs found: {len(pak_ids)}")

# 2b. Retired IPL players that exist in the dataset
all_bat_names = set(bbb['striker_name'].dropna().unique())
all_bowl_names = set(bbb['bowler_name'].dropna().unique())
all_dataset_names = all_bat_names | all_bowl_names
retired_names = set(retired['Player'].values)
retired_in_data = retired_names & all_dataset_names
print(f"  Retired IPL players in dataset: {len(retired_in_data)}")
for p in sorted(retired_in_data):
    print(f"    - {p}")

# 2c. Get retired player IDs from bbb
retired_bat_ids = set(bbb[bbb['striker_name'].isin(retired_in_data)]['striker_id'].unique())
retired_bowl_ids = set(bbb[bbb['bowler_name'].isin(retired_in_data)]['bowler_id'].unique())
retired_all_ids = retired_bat_ids | retired_bowl_ids

# 2d. Combined exclusion set
excluded_ids = pak_ids | retired_all_ids
excluded_names = pak_names | retired_in_data
print(f"\n  TOTAL EXCLUDED IDs: {len(excluded_ids)}")

# 2e. Filter ball_by_ball — remove rows where striker OR bowler is excluded
before = len(bbb)
bbb = bbb[~bbb['striker_id'].isin(excluded_ids) & ~bbb['bowler_id'].isin(excluded_ids)].copy()
after = len(bbb)
print(f"  Deliveries: {before:,} -> {after:,} (removed {before - after:,})")

# ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  PHASE 3: MATCH CONTEXT — BUILD PRESSURE INDEX")
print("=" * 70)

# Merge match info
bbb = bbb.merge(matches[['match_id', 'comp_id']], on='match_id', how='left')
bbb = bbb.merge(comps[['comp_id', 'match_format', 'season']], on='comp_id', how='left')

# Keep T20 formats only
bbb = bbb[bbb['match_format'].isin(['T20I', 'IPL', 'T20'])].copy()
print(f"  T20 deliveries after format filter: {len(bbb):,}")

# Build running match state per innings
bbb = bbb.sort_values(['match_id', 'innings', 'innings_ball_num']).copy()

# Calculate cumulative runs and wickets per innings
bbb['cum_runs'] = bbb.groupby(['match_id', 'innings'])['runs'].cumsum()
bbb['cum_wkts'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum()

# Total runs in innings (for 2nd innings target context)
inn_totals = bbb.groupby(['match_id', 'innings'])['runs'].sum().reset_index()
inn_totals.columns = ['match_id', 'innings', 'inn_total_runs']

# For 2nd innings, get 1st innings total as target
first_inn = inn_totals[inn_totals['innings'] == 1][['match_id', 'inn_total_runs']].copy()
first_inn.columns = ['match_id', 'first_inn_total']
bbb = bbb.merge(first_inn, on='match_id', how='left')

# Phase classification
def get_phase(over):
    if over <= 6:
        return 'Powerplay'
    elif over <= 15:
        return 'Middle'
    else:
        return 'Death'

bbb['phase'] = bbb['overid'].apply(get_phase)

# Balls remaining (out of 120 in a T20 innings)
bbb['balls_remaining'] = 120 - bbb['innings_ball_num']

# Required run rate (2nd innings)
bbb['target'] = bbb['first_inn_total'] + 1  # target = first_inn + 1
bbb['runs_needed'] = bbb['target'] - bbb['cum_runs']
bbb['overs_remaining'] = bbb['balls_remaining'] / 6.0
bbb['rrr'] = np.where(
    (bbb['innings'] == 2) & (bbb['overs_remaining'] > 0),
    bbb['runs_needed'] / bbb['overs_remaining'],
    0
)

# ── PRESSURE INDEX FORMULA ──
# Combines: over phase, wickets lost, run rate pressure, match stage
# Batting Pressure Index (per delivery):
#   Base: over_factor (higher in death) + wickets_factor + rrr_factor (2nd inn)
#   Normalized to 0-100 scale

def calc_pressure_index(row):
    """Calculate situational pressure index (0-100) for each delivery."""
    pi = 0.0
    over = row['overid']
    wkts = row['cum_wkts']
    inn = row['innings']
    balls_rem = row['balls_remaining']

    # 1. OVER PRESSURE (0-30): death overs are highest pressure
    if over >= 19:
        pi += 30
    elif over >= 17:
        pi += 25
    elif over >= 16:
        pi += 20
    elif over >= 11:
        pi += 10 + (over - 11) * 1.5
    elif over >= 7:
        pi += 5
    else:
        pi += 2  # powerplay — lower base pressure

    # 2. WICKETS PRESSURE (0-30): more wickets fallen = more pressure
    if wkts >= 7:
        pi += 30
    elif wkts >= 5:
        pi += 22
    elif wkts >= 4:
        pi += 17
    elif wkts >= 3:
        pi += 12
    elif wkts >= 2:
        pi += 7
    else:
        pi += 2

    # 3. RUN RATE PRESSURE — 2nd innings only (0-25)
    if inn == 2:
        rrr_val = row['rrr']
        if rrr_val > 15:
            pi += 25
        elif rrr_val > 12:
            pi += 22
        elif rrr_val > 10:
            pi += 18
        elif rrr_val > 8:
            pi += 12
        elif rrr_val > 6:
            pi += 6
        else:
            pi += 2
    else:
        # 1st innings: use scoring rate context
        current_rr = (row['cum_runs'] / max(row['innings_ball_num'], 1)) * 6
        if over >= 16 and current_rr < 7:
            pi += 12  # behind par
        elif over >= 16:
            pi += 8
        else:
            pi += 3

    # 4. MATCH STAGE INTENSITY (0-15): knockout/final = extra pressure
    # Use balls remaining as proxy
    if balls_rem <= 12:  # last 2 overs
        pi += 15
    elif balls_rem <= 30:  # last 5 overs
        pi += 10
    elif balls_rem <= 60:
        pi += 5
    else:
        pi += 1

    return min(pi, 100)

print("  Computing pressure index for every delivery...")
bbb['pressure_index'] = bbb.apply(calc_pressure_index, axis=1)

# Stats
print(f"  Pressure Index range: {bbb['pressure_index'].min():.1f} - {bbb['pressure_index'].max():.1f}")
print(f"  Mean PI: {bbb['pressure_index'].mean():.1f}, Median: {bbb['pressure_index'].median():.1f}")

hp_threshold = 65
bbb['is_high_pressure'] = bbb['pressure_index'] >= hp_threshold
hp_balls = bbb[bbb['is_high_pressure']].copy()
print(f"  High-pressure deliveries (PI >= {hp_threshold}): {len(hp_balls):,} ({100*len(hp_balls)/len(bbb):.1f}%)")

# ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  PHASE 4: BATTER PERFORMANCE UNDER PRESSURE")
print("=" * 70)

# === BASELINE (all deliveries) ===
base_bat = bbb.groupby(['striker_id', 'striker_name']).agg(
    base_runs=('runs', 'sum'),
    base_balls=('runs', 'count'),
    base_dismissals=('is_wicket', 'sum'),
    base_fours=('is_four', 'sum'),
    base_sixes=('is_six', 'sum'),
).reset_index()
base_bat['base_sr'] = (base_bat['base_runs'] / base_bat['base_balls'] * 100).round(1)
base_bat['base_avg'] = (base_bat['base_runs'] / base_bat['base_dismissals'].clip(lower=1)).round(1)

# === HIGH PRESSURE ===
hp_bat = hp_balls.groupby(['striker_id', 'striker_name']).agg(
    hp_runs=('runs', 'sum'),
    hp_balls=('runs', 'count'),
    hp_dismissals=('is_wicket', 'sum'),
    hp_fours=('is_four', 'sum'),
    hp_sixes=('is_six', 'sum'),
    hp_dots=('runs', lambda x: (x == 0).sum()),
).reset_index()
hp_bat['hp_sr'] = (hp_bat['hp_runs'] / hp_bat['hp_balls'] * 100).round(1)
hp_bat['hp_avg'] = (hp_bat['hp_runs'] / hp_bat['hp_dismissals'].clip(lower=1)).round(1)
hp_bat['hp_boundary_pct'] = (((hp_bat['hp_fours'] + hp_bat['hp_sixes']) / hp_bat['hp_balls']) * 100).round(1)
hp_bat['hp_dot_pct'] = ((hp_bat['hp_dots'] / hp_bat['hp_balls']) * 100).round(1)

# Merge
bat = hp_bat.merge(base_bat, on=['striker_id', 'striker_name'], how='left')
bat['delta_sr'] = (bat['hp_sr'] - bat['base_sr']).round(1)
bat['delta_avg'] = (bat['hp_avg'] - bat['base_avg']).round(1)

# Consistency: std dev of runs scored per match under HP
hp_match_bat = hp_balls.groupby(['striker_id', 'match_id']).agg(
    match_runs=('runs', 'sum')
).reset_index()
hp_bat_std = hp_match_bat.groupby('striker_id')['match_runs'].std().reset_index()
hp_bat_std.columns = ['striker_id', 'hp_score_std']
bat = bat.merge(hp_bat_std, on='striker_id', how='left')
bat['hp_score_std'] = bat['hp_score_std'].fillna(0)

# IQR for reliability
hp_bat_iqr = hp_match_bat.groupby('striker_id')['match_runs'].apply(
    lambda x: x.quantile(0.75) - x.quantile(0.25)
).reset_index()
hp_bat_iqr.columns = ['striker_id', 'hp_iqr']
bat = bat.merge(hp_bat_iqr, on='striker_id', how='left')

# Min qualification: 100 HP balls faced
MIN_BAT_BALLS = 100
bat_q = bat[bat['hp_balls'] >= MIN_BAT_BALLS].copy()
print(f"  Qualified batters (>= {MIN_BAT_BALLS} HP balls): {len(bat_q)}")

# Bayesian shrinkage for SR
league_sr = bat_q['hp_sr'].mean()
k_bat = 50  # shrinkage strength
bat_q['sr_shrunk'] = ((bat_q['hp_balls'] * bat_q['hp_sr'] + k_bat * league_sr) /
                       (bat_q['hp_balls'] + k_bat)).round(1)

# COMPOSITE RATING (batting)
# Weighted: shrunk SR (40%) + delta SR (15%) + HP avg (15%) + boundary% (10%)
#           + (100 - dot%) (10%) + consistency bonus (10%)
bat_q['consistency_score'] = (100 - bat_q['hp_score_std'].clip(upper=25) * 4).clip(lower=0)

sr_norm = (bat_q['sr_shrunk'] - bat_q['sr_shrunk'].min()) / (bat_q['sr_shrunk'].max() - bat_q['sr_shrunk'].min()) * 100
delta_norm = ((bat_q['delta_sr'] - bat_q['delta_sr'].min()) /
              (bat_q['delta_sr'].max() - bat_q['delta_sr'].min()) * 100)
avg_norm = ((bat_q['hp_avg'] - bat_q['hp_avg'].min()) /
            (bat_q['hp_avg'].max() - bat_q['hp_avg'].min()) * 100)
bdry_norm = ((bat_q['hp_boundary_pct'] - bat_q['hp_boundary_pct'].min()) /
             (bat_q['hp_boundary_pct'].max() - bat_q['hp_boundary_pct'].min()) * 100)
dot_norm = ((100 - bat_q['hp_dot_pct']) - (100 - bat_q['hp_dot_pct']).min()) / \
           ((100 - bat_q['hp_dot_pct']).max() - (100 - bat_q['hp_dot_pct']).min()) * 100
cons_norm = bat_q['consistency_score'] / bat_q['consistency_score'].max() * 100

bat_q['composite_rating'] = (
    sr_norm * 0.40 +
    delta_norm * 0.15 +
    avg_norm * 0.15 +
    bdry_norm * 0.10 +
    dot_norm * 0.10 +
    cons_norm * 0.10
).round(2)

bat_q = bat_q.sort_values('composite_rating', ascending=False).reset_index(drop=True)
bat_q['rank'] = range(1, len(bat_q) + 1)

print("\n  ======================== TOP 10 BATTERS UNDER PRESSURE ========================")
top10_bat = bat_q.head(10)
for _, r in top10_bat.iterrows():
    print(f"  #{int(r['rank']):>2} | {r['striker_name']:<22s} | Rating: {r['composite_rating']:>6.2f} | "
          f"HP SR: {r['hp_sr']:>6.1f} | HP Avg: {r['hp_avg']:>5.1f} | "
          f"Delta SR: {r['delta_sr']:>+6.1f} | HP Balls: {int(r['hp_balls']):>4d} | "
          f"Bdry%: {r['hp_boundary_pct']:>5.1f} | Dot%: {r['hp_dot_pct']:>5.1f}")

# ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  PHASE 5: BOWLER PERFORMANCE UNDER PRESSURE")
print("=" * 70)

# === BASELINE ===
base_bowl = bbb.groupby(['bowler_id', 'bowler_name']).agg(
    base_runs=('runs', 'sum'),
    base_balls=('runs', 'count'),
    base_wkts=('is_wicket', 'sum'),
).reset_index()
base_bowl['base_econ'] = (base_bowl['base_runs'] / (base_bowl['base_balls'] / 6)).round(2)

# === HIGH PRESSURE ===
hp_bowl = hp_balls.groupby(['bowler_id', 'bowler_name']).agg(
    hp_runs=('runs', 'sum'),
    hp_balls=('runs', 'count'),
    hp_wkts=('is_wicket', 'sum'),
    hp_dots=('runs', lambda x: (x == 0).sum()),
    hp_fours=('is_four', 'sum'),
    hp_sixes=('is_six', 'sum'),
).reset_index()
hp_bowl['hp_econ'] = (hp_bowl['hp_runs'] / (hp_bowl['hp_balls'] / 6)).round(2)
hp_bowl['hp_sr'] = (hp_bowl['hp_balls'] / hp_bowl['hp_wkts'].clip(lower=1)).round(1)
hp_bowl['hp_dot_pct'] = ((hp_bowl['hp_dots'] / hp_bowl['hp_balls']) * 100).round(1)
hp_bowl['hp_bdry_conceded_pct'] = (((hp_bowl['hp_fours'] + hp_bowl['hp_sixes']) / hp_bowl['hp_balls']) * 100).round(1)

# Merge
bowl = hp_bowl.merge(base_bowl, on=['bowler_id', 'bowler_name'], how='left')
bowl['delta_econ'] = (bowl['hp_econ'] - bowl['base_econ']).round(2)

# Consistency
hp_match_bowl = hp_balls.groupby(['bowler_id', 'match_id']).agg(
    match_runs=('runs', 'sum')
).reset_index()
hp_bowl_std = hp_match_bowl.groupby('bowler_id')['match_runs'].std().reset_index()
hp_bowl_std.columns = ['bowler_id', 'hp_runs_std']
bowl = bowl.merge(hp_bowl_std, on='bowler_id', how='left')
bowl['hp_runs_std'] = bowl['hp_runs_std'].fillna(0)

# Min qualification: 60 HP balls bowled
MIN_BOWL_BALLS = 60
bowl_q = bowl[bowl['hp_balls'] >= MIN_BOWL_BALLS].copy()
print(f"  Qualified bowlers (>= {MIN_BOWL_BALLS} HP balls): {len(bowl_q)}")

# Bayesian shrinkage for economy
league_econ = bowl_q['hp_econ'].mean()
k_bowl = 30
bowl_q['econ_shrunk'] = ((bowl_q['hp_balls'] * bowl_q['hp_econ'] + k_bowl * 6 * league_econ) /
                          (bowl_q['hp_balls'] + k_bowl * 6)).round(2)

# COMPOSITE RATING (bowling) — lower economy = better
# Inverted: (100 - econ_norm) * 40% + delta_econ_improvement (15%) + dot% (15%)
#           + wicket SR (10%) + (100 - bdry%) (10%) + consistency (10%)
bowl_q['consistency_score'] = (100 - bowl_q['hp_runs_std'].clip(upper=12) * 8).clip(lower=0)

econ_norm_inv = ((bowl_q['econ_shrunk'].max() - bowl_q['econ_shrunk']) /
                 (bowl_q['econ_shrunk'].max() - bowl_q['econ_shrunk'].min()) * 100)
delta_econ_norm = ((bowl_q['delta_econ'].max() - bowl_q['delta_econ']) /
                   (bowl_q['delta_econ'].max() - bowl_q['delta_econ'].min()) * 100)  # lower delta = better
sr_bowl_norm = ((bowl_q['hp_sr'].max() - bowl_q['hp_sr']) /
                (bowl_q['hp_sr'].max() - bowl_q['hp_sr'].min()) * 100)  # lower SR = more wkts
dot_bowl_norm = ((bowl_q['hp_dot_pct'] - bowl_q['hp_dot_pct'].min()) /
                 (bowl_q['hp_dot_pct'].max() - bowl_q['hp_dot_pct'].min()) * 100)
bdry_conc_norm = ((bowl_q['hp_bdry_conceded_pct'].max() - bowl_q['hp_bdry_conceded_pct']) /
                  (bowl_q['hp_bdry_conceded_pct'].max() - bowl_q['hp_bdry_conceded_pct'].min()) * 100)
cons_bowl_norm = bowl_q['consistency_score'] / bowl_q['consistency_score'].max() * 100

bowl_q['composite_rating'] = (
    econ_norm_inv * 0.40 +
    delta_econ_norm * 0.15 +
    dot_bowl_norm * 0.15 +
    sr_bowl_norm * 0.10 +
    bdry_conc_norm * 0.10 +
    cons_bowl_norm * 0.10
).round(2)

bowl_q = bowl_q.sort_values('composite_rating', ascending=False).reset_index(drop=True)
bowl_q['rank'] = range(1, len(bowl_q) + 1)

print("\n  ======================== TOP 10 BOWLERS UNDER PRESSURE ========================")
top10_bowl = bowl_q.head(10)
for _, r in top10_bowl.iterrows():
    print(f"  #{int(r['rank']):>2} | {r['bowler_name']:<22s} | Rating: {r['composite_rating']:>6.2f} | "
          f"HP Econ: {r['hp_econ']:>5.2f} | HP SR: {r['hp_sr']:>5.1f} | "
          f"Delta Econ: {r['delta_econ']:>+5.2f} | HP Balls: {int(r['hp_balls']):>4d} | "
          f"Dot%: {r['hp_dot_pct']:>5.1f} | Bdry%: {r['hp_bdry_conceded_pct']:>5.1f}")

# ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  PHASE 6: SAVE CSVs")
print("=" * 70)

bat_q.to_csv(os.path.join(OUT, 'top_batters_under_pressure.csv'), index=False)
bowl_q.to_csv(os.path.join(OUT, 'top_bowlers_under_pressure.csv'), index=False)
top10_bat.to_csv(os.path.join(OUT, 'top10_batters_final.csv'), index=False)
top10_bowl.to_csv(os.path.join(OUT, 'top10_bowlers_final.csv'), index=False)
print("  Saved: top_batters_under_pressure.csv")
print("  Saved: top_bowlers_under_pressure.csv")
print("  Saved: top10_batters_final.csv")
print("  Saved: top10_bowlers_final.csv")

# ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  PHASE 7: VISUALIZATIONS")
print("=" * 70)

GOLD = '#FFD700'
CYAN = '#58A6FF'
MAGENTA = '#F778A6'
GREEN = '#3FB950'
ORANGE = '#F0883E'
RED = '#F85149'
PURPLE = '#BC8CFF'
colors10 = ['#FFD700', '#58A6FF', '#F778A6', '#3FB950', '#F0883E',
            '#F85149', '#BC8CFF', '#79C0FF', '#D2A8FF', '#7EE787']

# ── CHART 1: Top 10 Batters — Composite Rating Bar ──
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(range(10), top10_bat['composite_rating'].values[::-1],
               color=colors10[::-1], edgecolor='#30363D', linewidth=0.8, height=0.7)
ax.set_yticks(range(10))
ax.set_yticklabels(top10_bat['striker_name'].values[::-1], fontsize=11, fontweight='bold')
ax.set_xlabel('Composite Pressure Rating', fontsize=12)
ax.set_title('TOP 10 BATTERS UNDER PRESSURE (PI >= 65)\nComposite Rating — 2022-2026 T20 Data', fontsize=14, fontweight='bold', color=GOLD)
for i, bar in enumerate(bars):
    val = bar.get_width()
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}', va='center', fontsize=10, fontweight='bold', color='white')
ax.set_xlim(0, max(top10_bat['composite_rating']) + 8)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'top10_batters_composite_rating.png'))
plt.close()
print("  Chart 1: top10_batters_composite_rating.png")

# ── CHART 2: Top 10 Bowlers — Composite Rating Bar ──
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(range(10), top10_bowl['composite_rating'].values[::-1],
               color=colors10[::-1], edgecolor='#30363D', linewidth=0.8, height=0.7)
ax.set_yticks(range(10))
ax.set_yticklabels(top10_bowl['bowler_name'].values[::-1], fontsize=11, fontweight='bold')
ax.set_xlabel('Composite Pressure Rating', fontsize=12)
ax.set_title('TOP 10 BOWLERS UNDER PRESSURE (PI >= 65)\nComposite Rating — 2022-2026 T20 Data', fontsize=14, fontweight='bold', color=CYAN)
for i, bar in enumerate(bars):
    val = bar.get_width()
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}', va='center', fontsize=10, fontweight='bold', color='white')
ax.set_xlim(0, max(top10_bowl['composite_rating']) + 8)
ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'top10_bowlers_composite_rating.png'))
plt.close()
print("  Chart 2: top10_bowlers_composite_rating.png")

# ── CHART 3: Batters HP SR vs Base SR (Scatter) ──
fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(bat_q['base_sr'], bat_q['hp_sr'], alpha=0.4, s=40, color='#8B949E', label='All qualified')
ax.scatter(top10_bat['base_sr'], top10_bat['hp_sr'], s=120, color=GOLD, edgecolor='white',
           linewidth=1.5, zorder=5, label='Top 10')
for _, r in top10_bat.iterrows():
    ax.annotate(r['striker_name'], (r['base_sr'], r['hp_sr']),
                fontsize=8, fontweight='bold', color=GOLD,
                xytext=(5, 5), textcoords='offset points')
# Reference line: HP SR = Base SR
lims = [min(ax.get_xlim()[0], ax.get_ylim()[0]), max(ax.get_xlim()[1], ax.get_ylim()[1])]
ax.plot(lims, lims, '--', color=RED, alpha=0.5, label='HP SR = Base SR')
ax.set_xlabel('Baseline Strike Rate (All Deliveries)', fontsize=12)
ax.set_ylabel('High-Pressure Strike Rate (PI >= 65)', fontsize=12)
ax.set_title('BATTER PERFORMANCE: BASELINE vs HIGH PRESSURE\nAbove diagonal = rises under pressure', fontsize=13, fontweight='bold', color=GOLD)
ax.legend(fontsize=9)
ax.grid(alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'batters_baseline_vs_pressure_scatter.png'))
plt.close()
print("  Chart 3: batters_baseline_vs_pressure_scatter.png")

# ── CHART 4: Bowlers HP Econ vs Base Econ (Scatter) ──
fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(bowl_q['base_econ'], bowl_q['hp_econ'], alpha=0.4, s=40, color='#8B949E', label='All qualified')
ax.scatter(top10_bowl['base_econ'], top10_bowl['hp_econ'], s=120, color=CYAN, edgecolor='white',
           linewidth=1.5, zorder=5, label='Top 10')
for _, r in top10_bowl.iterrows():
    ax.annotate(r['bowler_name'], (r['base_econ'], r['hp_econ']),
                fontsize=8, fontweight='bold', color=CYAN,
                xytext=(5, 5), textcoords='offset points')
lims = [min(ax.get_xlim()[0], ax.get_ylim()[0]), max(ax.get_xlim()[1], ax.get_ylim()[1])]
ax.plot(lims, lims, '--', color=RED, alpha=0.5, label='HP Econ = Base Econ')
ax.set_xlabel('Baseline Economy Rate (All Deliveries)', fontsize=12)
ax.set_ylabel('High-Pressure Economy Rate (PI >= 65)', fontsize=12)
ax.set_title('BOWLER PERFORMANCE: BASELINE vs HIGH PRESSURE\nBelow diagonal = improves under pressure', fontsize=13, fontweight='bold', color=CYAN)
ax.legend(fontsize=9)
ax.grid(alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'bowlers_baseline_vs_pressure_scatter.png'))
plt.close()
print("  Chart 4: bowlers_baseline_vs_pressure_scatter.png")

# ── CHART 5: Batters Multi-Metric Radar (Grouped Bar) ──
fig, axes = plt.subplots(1, 3, figsize=(18, 7))
names = top10_bat['striker_name'].values
y_pos = np.arange(len(names))

# 5a: HP Strike Rate
axes[0].barh(y_pos, top10_bat['hp_sr'].values, color=GOLD, edgecolor='#30363D', height=0.6)
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(names, fontsize=9, fontweight='bold')
axes[0].set_xlabel('HP Strike Rate')
axes[0].set_title('Strike Rate Under Pressure', fontweight='bold', color=GOLD)
axes[0].invert_yaxis()
for i, v in enumerate(top10_bat['hp_sr'].values):
    axes[0].text(v + 1, i, f'{v:.1f}', va='center', fontsize=8, color='white')

# 5b: Boundary %
axes[1].barh(y_pos, top10_bat['hp_boundary_pct'].values, color=MAGENTA, edgecolor='#30363D', height=0.6)
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(names, fontsize=9, fontweight='bold')
axes[1].set_xlabel('Boundary %')
axes[1].set_title('Boundary % Under Pressure', fontweight='bold', color=MAGENTA)
axes[1].invert_yaxis()
for i, v in enumerate(top10_bat['hp_boundary_pct'].values):
    axes[1].text(v + 0.3, i, f'{v:.1f}%', va='center', fontsize=8, color='white')

# 5c: Dot Ball %
axes[2].barh(y_pos, top10_bat['hp_dot_pct'].values, color=RED, edgecolor='#30363D', height=0.6)
axes[2].set_yticks(y_pos)
axes[2].set_yticklabels(names, fontsize=9, fontweight='bold')
axes[2].set_xlabel('Dot Ball %')
axes[2].set_title('Dot Ball % Under Pressure (lower = better)', fontweight='bold', color=RED)
axes[2].invert_yaxis()
for i, v in enumerate(top10_bat['hp_dot_pct'].values):
    axes[2].text(v + 0.3, i, f'{v:.1f}%', va='center', fontsize=8, color='white')

plt.suptitle('TOP 10 BATTERS — MULTI-METRIC PRESSURE BREAKDOWN', fontsize=15, fontweight='bold', color='white', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'batters_multi_metric_breakdown.png'))
plt.close()
print("  Chart 5: batters_multi_metric_breakdown.png")

# ── CHART 6: Bowlers Multi-Metric Breakdown ──
fig, axes = plt.subplots(1, 3, figsize=(18, 7))
bnames = top10_bowl['bowler_name'].values
y_pos = np.arange(len(bnames))

# 6a: HP Economy
axes[0].barh(y_pos, top10_bowl['hp_econ'].values, color=CYAN, edgecolor='#30363D', height=0.6)
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(bnames, fontsize=9, fontweight='bold')
axes[0].set_xlabel('HP Economy Rate')
axes[0].set_title('Economy Under Pressure (lower = better)', fontweight='bold', color=CYAN)
axes[0].invert_yaxis()
for i, v in enumerate(top10_bowl['hp_econ'].values):
    axes[0].text(v + 0.1, i, f'{v:.2f}', va='center', fontsize=8, color='white')

# 6b: Dot Ball %
axes[1].barh(y_pos, top10_bowl['hp_dot_pct'].values, color=GREEN, edgecolor='#30363D', height=0.6)
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(bnames, fontsize=9, fontweight='bold')
axes[1].set_xlabel('Dot Ball %')
axes[1].set_title('Dot Ball % Under Pressure (higher = better)', fontweight='bold', color=GREEN)
axes[1].invert_yaxis()
for i, v in enumerate(top10_bowl['hp_dot_pct'].values):
    axes[1].text(v + 0.3, i, f'{v:.1f}%', va='center', fontsize=8, color='white')

# 6c: Wicket SR
axes[2].barh(y_pos, top10_bowl['hp_sr'].values, color=PURPLE, edgecolor='#30363D', height=0.6)
axes[2].set_yticks(y_pos)
axes[2].set_yticklabels(bnames, fontsize=9, fontweight='bold')
axes[2].set_xlabel('HP Wicket Strike Rate (balls/wkt)')
axes[2].set_title('Wicket SR Under Pressure (lower = better)', fontweight='bold', color=PURPLE)
axes[2].invert_yaxis()
for i, v in enumerate(top10_bowl['hp_sr'].values):
    axes[2].text(v + 0.3, i, f'{v:.1f}', va='center', fontsize=8, color='white')

plt.suptitle('TOP 10 BOWLERS — MULTI-METRIC PRESSURE BREAKDOWN', fontsize=15, fontweight='bold', color='white', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'bowlers_multi_metric_breakdown.png'))
plt.close()
print("  Chart 6: bowlers_multi_metric_breakdown.png")

# ── CHART 7: Pressure Index Distribution ──
fig, ax = plt.subplots(figsize=(12, 5))
ax.hist(bbb['pressure_index'], bins=50, color=CYAN, alpha=0.7, edgecolor='#30363D')
ax.axvline(hp_threshold, color=RED, linewidth=2, linestyle='--', label=f'HP Threshold (PI = {hp_threshold})')
ax.set_xlabel('Pressure Index', fontsize=12)
ax.set_ylabel('Number of Deliveries', fontsize=12)
ax.set_title('PRESSURE INDEX DISTRIBUTION ACROSS ALL T20 DELIVERIES (2022-2026)', fontsize=13, fontweight='bold', color='white')
ax.legend(fontsize=10)
ax.grid(alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'pressure_index_distribution.png'))
plt.close()
print("  Chart 7: pressure_index_distribution.png")

# ── CHART 8: Delta SR (Batters) — who rises vs drops under pressure ──
fig, ax = plt.subplots(figsize=(12, 7))
colors_delta = [GREEN if d > 0 else RED for d in top10_bat['delta_sr'].values[::-1]]
ax.barh(range(10), top10_bat['delta_sr'].values[::-1],
        color=colors_delta, edgecolor='#30363D', height=0.7)
ax.set_yticks(range(10))
ax.set_yticklabels(top10_bat['striker_name'].values[::-1], fontsize=11, fontweight='bold')
ax.axvline(0, color='white', linewidth=1, linestyle='-')
ax.set_xlabel('Strike Rate Change Under Pressure (HP SR - Base SR)', fontsize=12)
ax.set_title('TOP 10 BATTERS: WHO RISES vs DROPS UNDER PRESSURE?\nPositive = performs BETTER under pressure', fontsize=13, fontweight='bold', color='white')
for i, v in enumerate(top10_bat['delta_sr'].values[::-1]):
    offset = 1 if v >= 0 else -1
    ha = 'left' if v >= 0 else 'right'
    ax.text(v + offset, i, f'{v:+.1f}', va='center', ha=ha, fontsize=10, fontweight='bold', color='white')
ax.grid(axis='x', alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'batters_delta_sr_pressure.png'))
plt.close()
print("  Chart 8: batters_delta_sr_pressure.png")

# ── CHART 9: Delta Economy (Bowlers) — who tightens vs leaks under pressure ──
fig, ax = plt.subplots(figsize=(12, 7))
colors_delta_b = [GREEN if d <= 0 else RED for d in top10_bowl['delta_econ'].values[::-1]]
ax.barh(range(10), top10_bowl['delta_econ'].values[::-1],
        color=colors_delta_b, edgecolor='#30363D', height=0.7)
ax.set_yticks(range(10))
ax.set_yticklabels(top10_bowl['bowler_name'].values[::-1], fontsize=11, fontweight='bold')
ax.axvline(0, color='white', linewidth=1, linestyle='-')
ax.set_xlabel('Economy Change Under Pressure (HP Econ - Base Econ)', fontsize=12)
ax.set_title('TOP 10 BOWLERS: WHO TIGHTENS vs LEAKS UNDER PRESSURE?\nNegative = performs BETTER under pressure', fontsize=13, fontweight='bold', color='white')
for i, v in enumerate(top10_bowl['delta_econ'].values[::-1]):
    offset = 0.05 if v >= 0 else -0.05
    ha = 'left' if v >= 0 else 'right'
    ax.text(v + offset, i, f'{v:+.2f}', va='center', ha=ha, fontsize=10, fontweight='bold', color='white')
ax.grid(axis='x', alpha=0.2)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'bowlers_delta_econ_pressure.png'))
plt.close()
print("  Chart 9: bowlers_delta_econ_pressure.png")

# ── CHART 10: Combined Summary Heatmap — Top 10 Batters ──
fig, ax = plt.subplots(figsize=(14, 6))
metrics = ['hp_sr', 'hp_avg', 'hp_boundary_pct', 'hp_dot_pct', 'delta_sr', 'composite_rating']
labels = ['HP Strike Rate', 'HP Average', 'Boundary %', 'Dot Ball %', 'Delta SR', 'Composite Rating']
data_matrix = top10_bat[metrics].values
# Normalize columns for heatmap
norm_matrix = np.zeros_like(data_matrix)
for j in range(data_matrix.shape[1]):
    col = data_matrix[:, j]
    rng = col.max() - col.min()
    if rng > 0:
        if labels[j] == 'Dot Ball %':  # lower is better
            norm_matrix[:, j] = (col.max() - col) / rng
        else:
            norm_matrix[:, j] = (col - col.min()) / rng
    else:
        norm_matrix[:, j] = 0.5

im = ax.imshow(norm_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, fontsize=10, fontweight='bold', rotation=25, ha='right')
ax.set_yticks(range(10))
ax.set_yticklabels(top10_bat['striker_name'].values, fontsize=10, fontweight='bold')
# Annotate with actual values
for i in range(10):
    for j in range(len(metrics)):
        val = data_matrix[i, j]
        fmt = f'{val:.1f}' if j != 5 else f'{val:.2f}'
        ax.text(j, i, fmt, ha='center', va='center', fontsize=8, fontweight='bold',
                color='black' if norm_matrix[i, j] > 0.4 else 'white')
ax.set_title('TOP 10 BATTERS — PRESSURE PERFORMANCE HEATMAP', fontsize=14, fontweight='bold', color=GOLD)
plt.colorbar(im, ax=ax, label='Normalized Score (green = better)', shrink=0.8)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'batters_heatmap.png'))
plt.close()
print("  Chart 10: batters_heatmap.png")

# ── CHART 11: Combined Summary Heatmap — Top 10 Bowlers ──
fig, ax = plt.subplots(figsize=(14, 6))
b_metrics = ['hp_econ', 'hp_sr', 'hp_dot_pct', 'hp_bdry_conceded_pct', 'delta_econ', 'composite_rating']
b_labels = ['HP Economy', 'HP Wkt SR', 'Dot Ball %', 'Bdry Conceded %', 'Delta Econ', 'Composite Rating']
b_data = top10_bowl[b_metrics].values
b_norm = np.zeros_like(b_data)
for j in range(b_data.shape[1]):
    col = b_data[:, j]
    rng = col.max() - col.min()
    if rng > 0:
        if b_labels[j] in ['HP Economy', 'HP Wkt SR', 'Bdry Conceded %', 'Delta Econ']:
            b_norm[:, j] = (col.max() - col) / rng  # lower = better
        else:
            b_norm[:, j] = (col - col.min()) / rng
    else:
        b_norm[:, j] = 0.5

im = ax.imshow(b_norm, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
ax.set_xticks(range(len(b_labels)))
ax.set_xticklabels(b_labels, fontsize=10, fontweight='bold', rotation=25, ha='right')
ax.set_yticks(range(10))
ax.set_yticklabels(top10_bowl['bowler_name'].values, fontsize=10, fontweight='bold')
for i in range(10):
    for j in range(len(b_metrics)):
        val = b_data[i, j]
        fmt = f'{val:.2f}' if j in [0, 4] else (f'{val:.1f}')
        if j == 5:
            fmt = f'{val:.2f}'
        ax.text(j, i, fmt, ha='center', va='center', fontsize=8, fontweight='bold',
                color='black' if b_norm[i, j] > 0.4 else 'white')
ax.set_title('TOP 10 BOWLERS — PRESSURE PERFORMANCE HEATMAP', fontsize=14, fontweight='bold', color=CYAN)
plt.colorbar(im, ax=ax, label='Normalized Score (green = better)', shrink=0.8)
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'bowlers_heatmap.png'))
plt.close()
print("  Chart 11: bowlers_heatmap.png")

# ── CHART 12: HP Balls Sample Size (Credibility Check) ──
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
# Batters
axes[0].barh(range(10), top10_bat['hp_balls'].values[::-1].astype(int),
             color=GOLD, edgecolor='#30363D', height=0.6)
axes[0].set_yticks(range(10))
axes[0].set_yticklabels(top10_bat['striker_name'].values[::-1], fontsize=10, fontweight='bold')
axes[0].set_xlabel('High-Pressure Balls Faced')
axes[0].set_title('TOP 10 BATTERS: HP SAMPLE SIZE', fontweight='bold', color=GOLD)
axes[0].axvline(MIN_BAT_BALLS, color=RED, linestyle='--', label=f'Min threshold ({MIN_BAT_BALLS})')
axes[0].legend()
for i, v in enumerate(top10_bat['hp_balls'].values[::-1].astype(int)):
    axes[0].text(v + 5, i, str(v), va='center', fontsize=9, color='white')

# Bowlers
axes[1].barh(range(10), top10_bowl['hp_balls'].values[::-1].astype(int),
             color=CYAN, edgecolor='#30363D', height=0.6)
axes[1].set_yticks(range(10))
axes[1].set_yticklabels(top10_bowl['bowler_name'].values[::-1], fontsize=10, fontweight='bold')
axes[1].set_xlabel('High-Pressure Balls Bowled')
axes[1].set_title('TOP 10 BOWLERS: HP SAMPLE SIZE', fontweight='bold', color=CYAN)
axes[1].axvline(MIN_BOWL_BALLS, color=RED, linestyle='--', label=f'Min threshold ({MIN_BOWL_BALLS})')
axes[1].legend()
for i, v in enumerate(top10_bowl['hp_balls'].values[::-1].astype(int)):
    axes[1].text(v + 3, i, str(v), va='center', fontsize=9, color='white')

plt.suptitle('SAMPLE SIZE CREDIBILITY CHECK', fontsize=14, fontweight='bold', color='white')
plt.tight_layout()
plt.savefig(os.path.join(OUT, 'charts', 'sample_size_credibility.png'))
plt.close()
print("  Chart 12: sample_size_credibility.png")

print("\n" + "=" * 70)
print("  PIPELINE COMPLETE")
print("=" * 70)
print(f"\n  Output directory: {OUT}")
print(f"  CSVs: 4 files")
print(f"  Charts: 12 high-res visualizations")
print("=" * 70)
