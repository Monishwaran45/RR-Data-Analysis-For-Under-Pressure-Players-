# -*- coding: utf-8 -*-
"""
Rajasthan Royals (RR) SupeRR Selector Season 2 - 5-Year Player Performance EDA (2022–2026)
Rigorous Longitudinal Sabermetric Pipeline.
Evaluates multi-season consistency, year-over-year trajectory, clutch evolution,
and volatility across all 5 seasons (2022, 2023, 2024, 2025, 2026).
"""

import os, sys
os.environ['MPLCONFIGDIR'] = r"c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\mpl_cache"
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)
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

# -----------------------------------------------------------------------------
# 1. Load Data
# -----------------------------------------------------------------------------
print("Loading datasets for 5-Year EDA...")
matches = pd.read_csv(os.path.join(DATASET_DIR, "matches.csv"))
matches['year'] = pd.to_datetime(matches['match_date']).dt.year

bbb = pd.read_csv(os.path.join(BASE_DIR, "Pressure_Tagged_Ball_By_Ball.csv"), low_memory=False)
bbb = bbb.merge(matches[['match_id', 'year']], on='match_id', how='left')
bbb['year'] = bbb['year'].fillna(bbb['season']).astype(int)

comps = pd.read_csv(os.path.join(DATASET_DIR, "competitions.csv"))
ctpm = pd.read_csv(os.path.join(DATASET_DIR, "competition_team_player_mapping.csv"))

# -----------------------------------------------------------------------------
# 2. Exclusions: 68 Pakistan Players + 18 Confirmed Retirees
# -----------------------------------------------------------------------------
pak_pids = set(ctpm[ctpm['team_name'].str.contains('Pakistan', case=False, na=False)]['player_id'].unique())
ret_df = pd.read_csv(os.path.join(BASE_DIR, "retired_ipl_players.csv"))
ret_names_set = set(ret_df['Player'].dropna().str.strip().str.lower().unique())

newly_confirmed_retirees = {
    'ravichandran ashwin', 'r ashwin', 'ashwin',
    'mahendra singh dhoni', 'ms dhoni', 'm s dhoni', 'dhoni',
    'dinesh karthik', 'd karthik',
    'ambati rayudu', 'a rayudu',
    'matthew wade', 'm wade',
    'andre russell', 'a russell',
    'alex hales', 'a hales',
    'david willey', 'd willey',
    'dwayne bravo', 'dj bravo',
    'kieron pollard', 'k pollard',
    'shikhar dhawan', 's dhawan',
    'wriddhiman saha', 'w saha',
    'travis head', 't head',
    'mitchell starc', 'm starc'
}
all_retirees = ret_names_set.union(newly_confirmed_retirees)

def is_retired(name):
    if not isinstance(name, str):
        return False
    clean = name.strip().lower()
    return clean in all_retirees

# Filter out ineligible
clean_bbb = bbb[
    (~bbb['striker_id'].isin(pak_pids)) &
    (~bbb['bowler_id'].isin(pak_pids))
].copy()

clean_bbb = clean_bbb[
    (~clean_bbb['striker_name'].apply(is_retired)) &
    (~clean_bbb['bowler_name'].apply(is_retired))
].copy()

print(f"Clean deliveries across 5 years (2022–2026): {len(clean_bbb):,}")
print("Deliveries by year:")
print(clean_bbb['year'].value_counts().sort_index())

# -----------------------------------------------------------------------------
# 3. High-Pressure Tagging (PI >= 65.0 or category HIGH)
# -----------------------------------------------------------------------------
clean_bbb['is_hp_bat'] = (clean_bbb['pressure_index_bat'] >= 65.0) | (clean_bbb['pressure_category_bat'] == 'HIGH')
clean_bbb['is_hp_bowl'] = (clean_bbb['pressure_index_bowl'] >= 65.0) | (clean_bbb['pressure_category_bowl'] == 'HIGH')

# -----------------------------------------------------------------------------
# 4. Year-by-Year Longitudinal Aggregations
# -----------------------------------------------------------------------------
print("Aggregating Year-by-Year Performance (2022–2026)...")

# Batters Yearly Aggregation
bat_records = []
years = [2022, 2023, 2024, 2025, 2026]

for yr in years:
    df_yr = clean_bbb[clean_bbb['year'] == yr]
    
    # Overall
    grouped = df_yr.groupby(['striker_id', 'striker_name']).agg(
        total_balls=('balls_faced', 'sum'),
        total_runs=('ball_runs', 'sum'),
        total_dismissals=('is_striker_dismissed', 'sum'),
        total_fours=('is_four', 'sum'),
        total_sixes=('is_six', 'sum'),
        total_dots=('is_batter_dot', 'sum'),
        matches=('match_id', 'nunique')
    ).reset_index()
    
    # HP
    df_hp = df_yr[df_yr['is_hp_bat']]
    grouped_hp = df_hp.groupby(['striker_id', 'striker_name']).agg(
        hp_balls=('balls_faced', 'sum'),
        hp_runs=('ball_runs', 'sum'),
        hp_dismissals=('is_striker_dismissed', 'sum'),
        hp_fours=('is_four', 'sum'),
        hp_sixes=('is_six', 'sum'),
        hp_dots=('is_batter_dot', 'sum')
    ).reset_index()
    
    merged = pd.merge(grouped, grouped_hp, on=['striker_id', 'striker_name'], how='left').fillna(0)
    merged['year'] = yr
    
    merged['overall_sr'] = np.where(merged['total_balls'] > 0, (merged['total_runs'] / merged['total_balls']) * 100, 0)
    merged['hp_sr'] = np.where(merged['hp_balls'] > 0, (merged['hp_runs'] / merged['hp_balls']) * 100, 0)
    merged['clutch_delta_sr'] = merged['hp_sr'] - merged['overall_sr']
    merged['hp_avg'] = np.where(merged['hp_dismissals'] > 0, merged['hp_runs'] / merged['hp_dismissals'], merged['hp_runs'])
    merged['hp_boundary_pct'] = np.where(merged['hp_balls'] > 0, ((merged['hp_fours'] + merged['hp_sixes']) / merged['hp_balls']) * 100, 0)
    merged['hp_dot_pct'] = np.where(merged['hp_balls'] > 0, (merged['hp_dots'] / merged['hp_balls']) * 100, 0)
    
    bat_records.append(merged)

bat_yearly_df = pd.concat(bat_records, ignore_index=True)

# Bowlers Yearly Aggregation
bowl_records = []
for yr in years:
    df_yr = clean_bbb[clean_bbb['year'] == yr]
    
    # Overall
    grouped = df_yr.groupby(['bowler_id', 'bowler_name']).agg(
        total_balls=('is_legal', 'sum'),
        total_runs=('bowler_runs', 'sum'),
        total_wkts=('is_bowler_wkt', 'sum'),
        total_dots=('is_bowler_dot', 'sum'),
        matches=('match_id', 'nunique')
    ).reset_index()
    
    # HP
    df_hp = df_yr[df_yr['is_hp_bowl']]
    grouped_hp = df_hp.groupby(['bowler_id', 'bowler_name']).agg(
        hp_balls=('is_legal', 'sum'),
        hp_runs=('bowler_runs', 'sum'),
        hp_wkts=('is_bowler_wkt', 'sum'),
        hp_dots=('is_bowler_dot', 'sum'),
        hp_fours=('is_four', 'sum'),
        hp_sixes=('is_six', 'sum')
    ).reset_index()
    
    merged = pd.merge(grouped, grouped_hp, on=['bowler_id', 'bowler_name'], how='left').fillna(0)
    merged['year'] = yr
    
    merged['overall_econ'] = np.where(merged['total_balls'] > 0, (merged['total_runs'] / merged['total_balls']) * 6, 0)
    merged['hp_econ'] = np.where(merged['hp_balls'] > 0, (merged['hp_runs'] / merged['hp_balls']) * 6, 0)
    merged['clutch_delta_econ'] = merged['hp_econ'] - merged['overall_econ']
    merged['hp_wkt_sr'] = np.where(merged['hp_wkts'] > 0, merged['hp_balls'] / merged['hp_wkts'], 999.0)
    merged['hp_dot_pct'] = np.where(merged['hp_balls'] > 0, (merged['hp_dots'] / merged['hp_balls']) * 100, 0)
    merged['hp_boundary_pct'] = np.where(merged['hp_balls'] > 0, ((merged['hp_fours'] + merged['hp_sixes']) / merged['hp_balls']) * 100, 0)
    
    bowl_records.append(merged)

bowl_yearly_df = pd.concat(bowl_records, ignore_index=True)

# Save longitudinal CSV registers
bat_yearly_df.to_csv(os.path.join(OUTPUT_DIR, "player_eda_5year_longitudinal_batting.csv"), index=False)
bowl_yearly_df.to_csv(os.path.join(OUTPUT_DIR, "player_eda_5year_longitudinal_bowling.csv"), index=False)
print("Saved yearly registers successfully!")

# -----------------------------------------------------------------------------
# 5. Focus Cohort: Top 10 Auction Pool Targets + Key Benchmarks
# -----------------------------------------------------------------------------
target_batters = [
    "Azmatullah Omarzai", "Mohammad Nabi", "Sikandar Raza", "M Shahrukh Khan",
    "Dasun Shanaka", "Mark Adair", "George Dockrell", "Daryl Mitchell",
    "Nurul Hasan", "Jaker Ali Anik"
]

target_bowlers = [
    "Maheesh Theekshana", "Avesh Khan", "Wanindu Hasaranga", "Ravi Bishnoi",
    "Matheesha Pathirana", "Mustafizur Rahman", "Dushmantha Chameera",
    "Alzarri Joseph", "Tushar Deshpande", "Richard Ngarava"
]

# Generate Summary Forensics Table for Target Batters
bat_summary_rows = []
for name in target_batters:
    p_df = bat_yearly_df[bat_yearly_df['striker_name'].str.contains(name, case=False, na=False)].sort_values('year')
    if len(p_df) == 0:
        continue
    
    cum_hp_balls = p_df['hp_balls'].sum()
    cum_hp_runs = p_df['hp_runs'].sum()
    career_hp_sr = (cum_hp_runs / cum_hp_balls * 100) if cum_hp_balls > 0 else 0
    
    # 2022-2024 vs 2025-2026
    early_df = p_df[p_df['year'].isin([2022, 2023, 2024])]
    late_df = p_df[p_df['year'].isin([2025, 2026])]
    
    early_sr = (early_df['hp_runs'].sum() / early_df['hp_balls'].sum() * 100) if early_df['hp_balls'].sum() > 0 else career_hp_sr
    late_sr = (late_df['hp_runs'].sum() / late_df['hp_balls'].sum() * 100) if late_df['hp_balls'].sum() > 0 else career_hp_sr
    
    # Yearly SR series
    sr_2022 = p_df[p_df['year'] == 2022]['hp_sr'].values[0] if len(p_df[p_df['year'] == 2022]) > 0 else 0
    sr_2023 = p_df[p_df['year'] == 2023]['hp_sr'].values[0] if len(p_df[p_df['year'] == 2023]) > 0 else 0
    sr_2024 = p_df[p_df['year'] == 2024]['hp_sr'].values[0] if len(p_df[p_df['year'] == 2024]) > 0 else 0
    sr_2025 = p_df[p_df['year'] == 2025]['hp_sr'].values[0] if len(p_df[p_df['year'] == 2025]) > 0 else 0
    sr_2026 = p_df[p_df['year'] == 2026]['hp_sr'].values[0] if len(p_df[p_df['year'] == 2026]) > 0 else 0
    
    active_srs = [s for s in [sr_2022, sr_2023, sr_2024, sr_2025, sr_2026] if s > 0]
    cv_sr = (np.std(active_srs) / np.mean(active_srs)) if len(active_srs) > 1 else 0.15
    trend = "Surging (▲▲)" if (late_sr - early_sr) > 10 else ("Progressive (▲)" if (late_sr - early_sr) > 0 else ("Cooling (▼)" if (late_sr - early_sr) < -10 else "Stable (■)"))
    
    bat_summary_rows.append({
        'Player': name,
        'Role': 'Batter',
        '5Y HP Balls': int(cum_hp_balls),
        '5Y Career HP SR': round(career_hp_sr, 1),
        'SR 2022': round(sr_2022, 1),
        'SR 2023': round(sr_2023, 1),
        'SR 2024': round(sr_2024, 1),
        'SR 2025': round(sr_2025, 1),
        'SR 2026': round(sr_2026, 1),
        'Early Era (22-24)': round(early_sr, 1),
        'Late Era (25-26)': round(late_sr, 1),
        'YoY Delta': round(late_sr - early_sr, 1),
        'Volatility (CV)': round(cv_sr, 2),
        'Trajectory': trend
    })

bat_summary_df = pd.DataFrame(bat_summary_rows)

# Generate Summary Forensics Table for Target Bowlers
bowl_summary_rows = []
for name in target_bowlers:
    p_df = bowl_yearly_df[bowl_yearly_df['bowler_name'].str.contains(name, case=False, na=False)].sort_values('year')
    if len(p_df) == 0:
        continue
    
    cum_hp_balls = p_df['hp_balls'].sum()
    cum_hp_runs = p_df['hp_runs'].sum()
    cum_hp_wkts = p_df['hp_wkts'].sum()
    career_hp_econ = (cum_hp_runs / cum_hp_balls * 6) if cum_hp_balls > 0 else 0
    career_hp_sr = (cum_hp_balls / cum_hp_wkts) if cum_hp_wkts > 0 else 999.0
    
    early_df = p_df[p_df['year'].isin([2022, 2023, 2024])]
    late_df = p_df[p_df['year'].isin([2025, 2026])]
    
    early_econ = (early_df['hp_runs'].sum() / early_df['hp_balls'].sum() * 6) if early_df['hp_balls'].sum() > 0 else career_hp_econ
    late_econ = (late_df['hp_runs'].sum() / late_df['hp_balls'].sum() * 6) if late_df['hp_balls'].sum() > 0 else career_hp_econ
    
    econ_2022 = p_df[p_df['year'] == 2022]['hp_econ'].values[0] if len(p_df[p_df['year'] == 2022]) > 0 else 0
    econ_2023 = p_df[p_df['year'] == 2023]['hp_econ'].values[0] if len(p_df[p_df['year'] == 2023]) > 0 else 0
    econ_2024 = p_df[p_df['year'] == 2024]['hp_econ'].values[0] if len(p_df[p_df['year'] == 2024]) > 0 else 0
    econ_2025 = p_df[p_df['year'] == 2025]['hp_econ'].values[0] if len(p_df[p_df['year'] == 2025]) > 0 else 0
    econ_2026 = p_df[p_df['year'] == 2026]['hp_econ'].values[0] if len(p_df[p_df['year'] == 2026]) > 0 else 0
    
    active_econs = [e for e in [econ_2022, econ_2023, econ_2024, econ_2025, econ_2026] if e > 0]
    cv_econ = (np.std(active_econs) / np.mean(active_econs)) if len(active_econs) > 1 else 0.15
    trend = "Peaking Choke (▲▲)" if (early_econ - late_econ) > 0.5 else ("Progressive (▲)" if (early_econ - late_econ) > 0 else ("Leaking (▼)" if (late_econ - early_econ) > 0.5 else "Stable (■)"))
    
    bowl_summary_rows.append({
        'Player': name,
        'Role': 'Bowler',
        '5Y HP Balls': int(cum_hp_balls),
        '5Y HP Wkts': int(cum_hp_wkts),
        '5Y Career HP Econ': round(career_hp_econ, 2),
        '5Y Wkt SR': round(career_hp_sr, 1),
        'Econ 2022': round(econ_2022, 2),
        'Econ 2023': round(econ_2023, 2),
        'Econ 2024': round(econ_2024, 2),
        'Econ 2025': round(econ_2025, 2),
        'Econ 2026': round(econ_2026, 2),
        'Early Era (22-24)': round(early_econ, 2),
        'Late Era (25-26)': round(late_econ, 2),
        'YoY Delta': round(late_econ - early_econ, 2),
        'Volatility (CV)': round(cv_econ, 2),
        'Trajectory': trend
    })

bowl_summary_df = pd.DataFrame(bowl_summary_rows)

summary_5y_combined = pd.concat([bat_summary_df, bowl_summary_df], ignore_index=True)
summary_5y_combined.to_csv(os.path.join(OUTPUT_DIR, "top10_5year_summary_eda.csv"), index=False)
print("Saved 5-Year summary CSV successfully!")

# -----------------------------------------------------------------------------
# 6. Generate 4 Publication-Grade 300 DPI Visual Charts
# -----------------------------------------------------------------------------
print("Generating 300 DPI 5-Year EDA Charts...")

# Chart 1: Batters 5-Year YoY Trajectory
fig, ax = plt.subplots(figsize=(12, 7), dpi=300, facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

palette = ['#C81D4E', '#141B2D', '#B45309', '#10B981', '#334155', '#6366F1', '#EC4899', '#8B5CF6', '#14B8A6', '#F59E0B']

for i, row in bat_summary_df.iterrows():
    srs = [row['SR 2022'], row['SR 2023'], row['SR 2024'], row['SR 2025'], row['SR 2026']]
    # Filter valid points
    pts = [(y, s) for y, s in zip(years, srs) if s > 0]
    if len(pts) >= 2:
        xs, ys = zip(*pts)
        lw = 2.8 if row['Player'] in ['Azmatullah Omarzai', 'M Shahrukh Khan', 'Daryl Mitchell'] else 1.6
        alpha = 1.0 if row['Player'] in ['Azmatullah Omarzai', 'M Shahrukh Khan', 'Daryl Mitchell'] else 0.7
        ax.plot(xs, ys, marker='o', markersize=6, linewidth=lw, alpha=alpha, label=f"{row['Player']} ({row['Trajectory']})", color=palette[i % len(palette)])

ax.axhline(138.4, color='#94A3B8', linestyle='--', linewidth=1.2, label='Global High-Pressure Prior SR (138.4)')
ax.set_title("Top 10 Available Batters: 5-Year High-Pressure Strike Rate Evolution (2022–2026)", fontsize=13, fontweight='bold', color='#141B2D', pad=15)
ax.set_xlabel("Tournament Season", fontsize=11, fontweight='bold', color='#141B2D')
ax.set_ylabel("High-Pressure Strike Rate (PI ≥ 65.0)", fontsize=11, fontweight='bold', color='#141B2D')
ax.set_xticks(years)
ax.grid(True, linestyle=':', alpha=0.5, color='#E2E8F0')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, fontsize=8.5)
plt.tight_layout()
chart1_path = os.path.join(CHARTS_DIR, "eda_5year_batters_trajectory.png")
fig.savefig(chart1_path, dpi=300)
plt.close(fig)

# Chart 2: Bowlers 5-Year YoY Trajectory
fig, ax = plt.subplots(figsize=(12, 7), dpi=300, facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

for i, row in bowl_summary_df.iterrows():
    econs = [row['Econ 2022'], row['Econ 2023'], row['Econ 2024'], row['Econ 2025'], row['Econ 2026']]
    pts = [(y, e) for y, e in zip(years, econs) if e > 0]
    if len(pts) >= 2:
        xs, ys = zip(*pts)
        lw = 2.8 if row['Player'] in ['Maheesh Theekshana', 'Matheesha Pathirana', 'Avesh Khan'] else 1.6
        alpha = 1.0 if row['Player'] in ['Maheesh Theekshana', 'Matheesha Pathirana', 'Avesh Khan'] else 0.7
        ax.plot(xs, ys, marker='s', markersize=6, linewidth=lw, alpha=alpha, label=f"{row['Player']} ({row['Trajectory']})", color=palette[i % len(palette)])

ax.axhline(8.92, color='#94A3B8', linestyle='--', linewidth=1.2, label='Global High-Pressure Prior Econ (8.92)')
ax.set_title("Top 10 Available Bowlers: 5-Year High-Pressure Economy Trajectory (2022–2026)", fontsize=13, fontweight='bold', color='#141B2D', pad=15)
ax.set_xlabel("Tournament Season", fontsize=11, fontweight='bold', color='#141B2D')
ax.set_ylabel("High-Pressure Economy Rate (PI ≥ 65.0 - Lower is Superior)", fontsize=11, fontweight='bold', color='#141B2D')
ax.set_xticks(years)
ax.grid(True, linestyle=':', alpha=0.5, color='#E2E8F0')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, fontsize=8.5)
plt.tight_layout()
chart2_path = os.path.join(CHARTS_DIR, "eda_5year_bowlers_trajectory.png")
fig.savefig(chart2_path, dpi=300)
plt.close(fig)

# Chart 3: Matrix Heatmap of 5 Seasons
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300, facecolor='#FFFFFF')
fig.suptitle("5-Season High-Pressure Heatmap Matrix (2022–2026)", fontsize=14, fontweight='bold', color='#141B2D', y=0.98)

# Batters Heatmap Data
bat_mat = []
bat_labels = []
for _, r in bat_summary_df.iterrows():
    bat_labels.append(r['Player'])
    bat_mat.append([r['SR 2022'], r['SR 2023'], r['SR 2024'], r['SR 2025'], r['SR 2026']])

im1 = ax1.imshow(bat_mat, cmap='YlOrRd', aspect='auto', vmin=120, vmax=200)
ax1.set_xticks(range(len(years)))
ax1.set_xticklabels(years, fontweight='bold')
ax1.set_yticks(range(len(bat_labels)))
ax1.set_yticklabels(bat_labels, fontweight='bold', fontsize=9)
ax1.set_title("Top Batters: High-Pressure Strike Rate Matrix", fontsize=11, fontweight='bold', color='#141B2D', pad=10)
for i in range(len(bat_labels)):
    for j in range(len(years)):
        val = bat_mat[i][j]
        txt = f"{val:.1f}" if val > 0 else "—"
        ax1.text(j, i, txt, ha='center', va='center', color='black' if val < 170 else 'white', fontsize=8.5, fontweight='bold')

# Bowlers Heatmap Data
bowl_mat = []
bowl_labels = []
for _, r in bowl_summary_df.iterrows():
    bowl_labels.append(r['Player'])
    bowl_mat.append([r['Econ 2022'], r['Econ 2023'], r['Econ 2024'], r['Econ 2025'], r['Econ 2026']])

im2 = ax2.imshow(bowl_mat, cmap='YlGnBu_r', aspect='auto', vmin=6.0, vmax=12.0)
ax2.set_xticks(range(len(years)))
ax2.set_xticklabels(years, fontweight='bold')
ax2.set_yticks(range(len(bowl_labels)))
ax2.set_yticklabels(bowl_labels, fontweight='bold', fontsize=9)
ax2.set_title("Top Bowlers: High-Pressure Economy Matrix", fontsize=11, fontweight='bold', color='#141B2D', pad=10)
for i in range(len(bowl_labels)):
    for j in range(len(years)):
        val = bowl_mat[i][j]
        txt = f"{val:.2f}" if val > 0 else "—"
        ax2.text(j, i, txt, ha='center', va='center', color='black' if val > 8.5 else 'white', fontsize=8.5, fontweight='bold')

plt.tight_layout()
chart3_path = os.path.join(CHARTS_DIR, "eda_5year_player_performance_heatmap.png")
fig.savefig(chart3_path, dpi=300)
plt.close(fig)

# Chart 4: 5-Year Volume vs Consistency Scatter
fig, ax = plt.subplots(figsize=(10, 6), dpi=300, facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Batters
ax.scatter(bat_summary_df['5Y HP Balls'], 1.0 - bat_summary_df['Volatility (CV)'], color='#C81D4E', s=120, edgecolors='#141B2D', linewidth=1.2, label='Top Batters', alpha=0.9)
for _, r in bat_summary_df.iterrows():
    ax.annotate(r['Player'].split()[-1], (r['5Y HP Balls'], 1.0 - r['Volatility (CV)']), textcoords="offset points", xytext=(0, 7), ha='center', fontsize=8.5, fontweight='bold', color='#141B2D')

# Bowlers
ax.scatter(bowl_summary_df['5Y HP Balls'], 1.0 - bowl_summary_df['Volatility (CV)'], color='#10B981', s=120, edgecolors='#141B2D', linewidth=1.2, label='Top Bowlers', alpha=0.9, marker='s')
for _, r in bowl_summary_df.iterrows():
    ax.annotate(r['Player'].split()[-1], (r['5Y HP Balls'], 1.0 - r['Volatility (CV)']), textcoords="offset points", xytext=(0, -12), ha='center', fontsize=8.5, fontweight='bold', color='#10B981')

ax.set_title("5-Year Experience Floor vs Longitudinal Consistency (2022–2026)", fontsize=13, fontweight='bold', color='#141B2D', pad=15)
ax.set_xlabel("5-Year Cumulative High-Pressure Deliveries (Sample Credibility)", fontsize=11, fontweight='bold', color='#141B2D')
ax.set_ylabel("Multi-Year Longitudinal Reliability Score (1 - Volatility CV)", fontsize=11, fontweight='bold', color='#141B2D')
ax.grid(True, linestyle=':', alpha=0.5, color='#E2E8F0')
ax.legend(frameon=True, fontsize=10, loc='lower right')
plt.tight_layout()
chart4_path = os.path.join(CHARTS_DIR, "eda_5year_consistency_vs_peak_scatter.png")
fig.savefig(chart4_path, dpi=300)
plt.close(fig)

# Sync to Artifact Directory
import shutil
for f in ["eda_5year_batters_trajectory.png", "eda_5year_bowlers_trajectory.png", "eda_5year_player_performance_heatmap.png", "eda_5year_consistency_vs_peak_scatter.png"]:
    src = os.path.join(CHARTS_DIR, f)
    dst = os.path.join(ARTIFACT_DIR, f)
    shutil.copyfile(src, dst)

print("All 4 charts generated, saved, and synced to artifact directory successfully!")
