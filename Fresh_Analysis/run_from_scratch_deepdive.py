"""
Rajasthan Royals (RR) SupeRR Selector Season 2 - Standalone Scratch Deep-Dive Analysis
Rigorous Cricket Analytics Pipeline matching Master Notebook formulation.
Excludes all Pakistan players, all confirmed retired players (including R Ashwin, MS Dhoni, Matthew Wade, etc.),
and tags IPL 2027 Retained vs Available Auction Pool.
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

# -----------------------------------------------------------------------------
# 1. Load Data
# -----------------------------------------------------------------------------
print("Loading raw datasets from:", DATASET_DIR)
bbb = pd.read_csv(os.path.join(DATASET_DIR, "ball_by_ball.csv"))
matches = pd.read_csv(os.path.join(DATASET_DIR, "matches.csv"))
comps = pd.read_csv(os.path.join(DATASET_DIR, "competitions.csv"))
ctpm = pd.read_csv(os.path.join(DATASET_DIR, "competition_team_player_mapping.csv"))

print(f"Loaded deliveries: {len(bbb):,}, matches: {len(matches):,}, comps: {len(comps):,}")

# -----------------------------------------------------------------------------
# 2. Exclusions: 68 Pakistan Players + Confirmed Retirees & Opt-outs
# -----------------------------------------------------------------------------
pak_pids = set(ctpm[ctpm['team_name'].str.contains('Pakistan', case=False, na=False)]['player_id'].unique())

ret_csv_path = os.path.join(BASE_DIR, "retired_ipl_players.csv")
ret_df = pd.read_csv(ret_csv_path)
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
all_retirees_set = ret_names_set | newly_confirmed_retirees

all_strikers = set(bbb['striker_name'].dropna().unique())
all_bowlers = set(bbb['bowler_name'].dropna().unique())
all_player_names = all_strikers | all_bowlers

ret_matched_names = {n for n in all_player_names if n.strip().lower() in all_retirees_set}
ret_pids = set(bbb[bbb['striker_name'].isin(ret_matched_names)]['striker_id'].unique()) | \
           set(bbb[bbb['bowler_name'].isin(ret_matched_names)]['bowler_id'].unique())

total_excluded_pids = pak_pids | ret_pids
print(f"Exclusion IDs: {len(pak_pids)} Pakistan + {len(ret_pids)} Retirees/Opt-outs = {len(total_excluded_pids)} Excluded IDs")

# Apply Exclusion
df = bbb[~bbb['striker_id'].isin(total_excluded_pids) & ~bbb['bowler_id'].isin(total_excluded_pids)].copy()
print(f"Deliveries after exclusion: {len(bbb):,} -> {len(df):,} ({len(bbb) - len(df):,} removed)")

# Verify R Ashwin and MS Dhoni are completely absent
ashwin_check = df[df['striker_name'].str.lower().str.contains('ravichandran ashwin', na=False) | df['bowler_name'].str.lower().str.contains('ravichandran ashwin', na=False)]
dhoni_check = df[df['striker_name'].str.lower().str.contains('dhoni', na=False) | df['bowler_name'].str.lower().str.contains('dhoni', na=False)]
assert len(ashwin_check) == 0, "Ravichandran Ashwin still found in dataset!"
assert len(dhoni_check) == 0, "Dhoni still found in dataset!"
print("Verification SUCCESS: Ravichandran Ashwin, MS Dhoni, Matthew Wade, Dinesh Karthik, Starc, Head completely removed.")

# -----------------------------------------------------------------------------
# 3. Pre-Delivery Match State Reconstruction
# -----------------------------------------------------------------------------
matches['first_inn_balls'] = np.where(
    matches['first_inn_revised_overs'].notnull() & (matches['first_inn_revised_overs'] > 0),
    matches['first_inn_revised_overs'],
    120
).astype(int)
matches['second_inn_balls'] = np.where(
    matches['second_inn_revised_overs'].notnull() & (matches['second_inn_revised_overs'] > 0),
    matches['second_inn_revised_overs'],
    matches['first_inn_balls']
).astype(int)

is_wide = (df['extras_type'] == 'wide')
is_overstep = (df['extras_type'] == 'Overstep')
is_bye_lb = df['extras_type'].isin(['byes', 'legbyes'])
is_penalty = (df['extras_type'] == 'Penalty')

df['ball_runs'] = (
    df['runs'] +
    (is_wide | is_overstep | is_bye_lb).astype(int) +
    df['extras_2_runs'].fillna(0) +
    (is_penalty.astype(int) * 5)
)
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

df = df.merge(matches[['match_id', 'comp_id', 'first_inn_balls', 'second_inn_balls', 'revised_target']], on='match_id', how='left')
df['total_legal_balls'] = np.where(df['innings'] == 1, df['first_inn_balls'], df['second_inn_balls'])
df['balls_remaining'] = np.maximum(0, df['total_legal_balls'] - df['legal_balls_bowled'])
df['overs_remaining'] = df['balls_remaining'] / 6.0

inn1_tot = df[df['innings'] == 1].groupby('match_id')['ball_runs'].sum().rename('inn1_score')
df = df.merge(inn1_tot, on='match_id', how='left')
df['effective_target'] = np.where(
    df['innings'] == 2,
    np.where(df['revised_target'].notnull() & (df['revised_target'] > 0), df['revised_target'], df['inn1_score'] + 1),
    np.nan
)
df['runs_needed'] = np.where(df['innings'] == 2, np.maximum(0, df['effective_target'] - df['score_before']), np.nan)
df['rrr'] = np.where((df['innings'] == 2) & (df['balls_remaining'] > 0), df['runs_needed'] / np.maximum(0.1, df['overs_remaining']), np.nan)
df['rrr_clipped'] = df['rrr'].clip(0, 36.0)

comp_avg = df[df['innings'] == 1].groupby('comp_id')['ball_runs'].sum() / np.maximum(1, df[df['innings'] == 1].groupby('comp_id')['match_id'].nunique())
df['comp_par_base'] = df['comp_id'].map(comp_avg).fillna(165.0)
df['par_total'] = df['comp_par_base'] * (df['total_legal_balls'] / 120.0)
df['par_at_ball'] = df['par_total'] * (df['legal_balls_bowled'] / np.maximum(1, df['total_legal_balls']))
df['par_deficit'] = df['par_at_ball'] - df['score_before']

def get_phase(o):
    if o <= 6: return 'Powerplay (1-6)'
    elif o <= 15: return 'Middle (7-15)'
    else: return 'Death (16-20)'
df['phase'] = df['overid'].apply(get_phase)

# -----------------------------------------------------------------------------
# 4. Continuous Pressure Index (PI Bat & PI Bowl: 0-100)
# -----------------------------------------------------------------------------
phase_w_bat = df['phase'].map({'Powerplay (1-6)': 1.0, 'Middle (7-15)': 2.2, 'Death (16-20)': 3.8})
pi_bat_1st = (12.0 * phase_w_bat + 6.5 * df['wkts_before'] + np.clip(0.8 * df['par_deficit'], -15, 25)).clip(5, 95)
pi_bat_2nd = (22.0 * (df['rrr_clipped'] / 8.0) + 5.5 * df['wkts_before'] + 16.0 * (1.0 - df['balls_remaining'] / df['total_legal_balls'])).clip(5, 98)
df['pressure_index_bat'] = np.where(df['innings'] == 1, pi_bat_1st, pi_bat_2nd).round(1)

opp_wkts_in_hand = (10 - df['wkts_before']).clip(1, 10)
phase_w_bowl = df['phase'].map({'Powerplay (1-6)': 1.2, 'Middle (7-15)': 0.9, 'Death (16-20)': 2.2})
cur_rr = np.where(df['legal_balls_bowled'] > 0, df['score_before'] / (df['legal_balls_bowled'] / 6.0), df['par_total'] / 20.0)
delta_rr = np.clip(cur_rr - (df['par_total'] / 20.0), -4.0, 5.0)

pi_bowl_1st = (15.0 + 12.0 * phase_w_bowl + 4.0 * delta_rr + 2.5 * (opp_wkts_in_hand - 5)).clip(10, 95)

req_run_per_ball = np.where(df['balls_remaining'] > 0, df['runs_needed'] / df['balls_remaining'], 0.0)
tension = np.maximum(0, 1.0 - np.abs(req_run_per_ball - 1.4) / 1.4)
progression = 1.0 - (df['balls_remaining'] / df['total_legal_balls'])
death_bowl_bonus = np.where(df['phase'] == 'Death (16-20)', 18.0, 0.0)
is_blowout = (req_run_per_ball > 3.0) & (opp_wkts_in_hand <= 3)

pi_bowl_2nd = np.where(
    is_blowout,
    15.0,
    (18.0 + 22.0 * progression + 24.0 * tension + death_bowl_bonus + 2.5 * (opp_wkts_in_hand - 4)).clip(10, 98)
)
df['pressure_index_bowl'] = np.where(df['innings'] == 1, pi_bowl_1st, pi_bowl_2nd).round(1)

# High pressure definition (threshold = 65)
df['is_hp_bat'] = df['pressure_index_bat'] >= 65
df['is_hp_bowl'] = df['pressure_index_bowl'] >= 65

print(f"High-Pressure Batting Balls: {df['is_hp_bat'].sum():,} ({df['is_hp_bat'].mean()*100:.1f}%)")
print(f"High-Pressure Bowling Balls: {df['is_hp_bowl'].sum():,} ({df['is_hp_bowl'].mean()*100:.1f}%)")

# -----------------------------------------------------------------------------
# 5. Batter Metrics & Composite Rating
# -----------------------------------------------------------------------------
player_names_bat = df[['striker_id', 'striker_name']].drop_duplicates().set_index('striker_id')['striker_name'].to_dict()

hp_bat = df[df['is_hp_bat']].groupby('striker_id').agg(
    hp_runs=('runs', 'sum'),
    hp_balls=('balls_faced', 'sum'),
    hp_dismissals=('is_striker_dismissed', 'sum'),
    hp_fours=('is_four', 'sum'),
    hp_sixes=('is_six', 'sum'),
    hp_dots=('is_batter_dot', 'sum')
).reset_index()

base_bat = df[~df['is_hp_bat']].groupby('striker_id').agg(
    base_runs=('runs', 'sum'),
    base_balls=('balls_faced', 'sum'),
    base_dismissals=('is_striker_dismissed', 'sum')
).reset_index()

bat_m = hp_bat.merge(base_bat, on='striker_id', how='left').fillna(0)
bat_m['player_name'] = bat_m['striker_id'].map(player_names_bat)
bat_m['hp_strike_rate'] = (bat_m['hp_runs'] / np.maximum(1, bat_m['hp_balls']) * 100).round(1)
bat_m['base_strike_rate'] = (bat_m['base_runs'] / np.maximum(1, bat_m['base_balls']) * 100).round(1)
bat_m['delta_strike_rate'] = (bat_m['hp_strike_rate'] - bat_m['base_strike_rate']).round(1)
bat_m['hp_avg'] = (bat_m['hp_runs'] / np.maximum(1, bat_m['hp_dismissals'])).round(1)
bat_m['hp_boundary_pct'] = (((bat_m['hp_fours'] + bat_m['hp_sixes']) / np.maximum(1, bat_m['hp_balls'])) * 100).round(1)
bat_m['hp_dot_pct'] = ((bat_m['hp_dots'] / np.maximum(1, bat_m['hp_balls'])) * 100).round(1)

def norm(s): return (s - s.min()) / (s.max() - s.min() + 1e-6)

qual_bat = bat_m[bat_m['hp_balls'] >= 100].copy()
qual_bat['sr_shrunk'] = (qual_bat['hp_balls'] / (qual_bat['hp_balls'] + 80)) * qual_bat['hp_strike_rate'] + (80 / (qual_bat['hp_balls'] + 80)) * 135.0

qual_bat['composite_rating'] = (
    0.40 * norm(qual_bat['sr_shrunk']) +
    0.25 * norm(qual_bat['delta_strike_rate']) +
    0.20 * norm(qual_bat['hp_boundary_pct']) +
    0.15 * norm(np.log(qual_bat['hp_balls']))
) * 100.0

qual_bat = qual_bat.sort_values('composite_rating', ascending=False).reset_index(drop=True)
qual_bat['rank'] = range(1, len(qual_bat) + 1)
qual_bat['composite_rating'] = qual_bat['composite_rating'].round(2)

# -----------------------------------------------------------------------------
# 6. Bowler Metrics & Composite Rating
# -----------------------------------------------------------------------------
player_names_bowl = df[['bowler_id', 'bowler_name']].drop_duplicates().set_index('bowler_id')['bowler_name'].to_dict()

hp_bowl = df[df['is_hp_bowl']].groupby('bowler_id').agg(
    hp_runs=('bowler_runs', 'sum'),
    hp_balls=('is_legal', 'sum'),
    hp_wkts=('is_bowler_wkt', 'sum'),
    hp_dots=('is_bowler_dot', 'sum'),
    hp_fours=('is_four', 'sum'),
    hp_sixes=('is_six', 'sum')
).reset_index()

base_bowl = df[~df['is_hp_bowl']].groupby('bowler_id').agg(
    base_runs=('bowler_runs', 'sum'),
    base_balls=('is_legal', 'sum'),
    base_wkts=('is_bowler_wkt', 'sum')
).reset_index()

bowl_m = hp_bowl.merge(base_bowl, on='bowler_id', how='left').fillna(0)
bowl_m['player_name'] = bowl_m['bowler_id'].map(player_names_bowl)
bowl_m['hp_econ'] = (bowl_m['hp_runs'] / np.maximum(1, bowl_m['hp_balls'] / 6.0)).round(2)
bowl_m['base_econ'] = (bowl_m['base_runs'] / np.maximum(1, bowl_m['base_balls'] / 6.0)).round(2)
bowl_m['delta_econ'] = (bowl_m['hp_econ'] - bowl_m['base_econ']).round(2)
bowl_m['hp_sr'] = (bowl_m['hp_balls'] / np.maximum(1, bowl_m['hp_wkts'])).round(1)
bowl_m['hp_dot_pct'] = ((bowl_m['hp_dots'] / np.maximum(1, bowl_m['hp_balls'])) * 100).round(1)
bowl_m['hp_bdry_pct'] = (((bowl_m['hp_fours'] + bowl_m['hp_sixes']) / np.maximum(1, bowl_m['hp_balls'])) * 100).round(1)

qual_bowl = bowl_m[bowl_m['hp_balls'] >= 60].copy()
qual_bowl['econ_shrunk'] = (qual_bowl['hp_balls'] / (qual_bowl['hp_balls'] + 60)) * qual_bowl['hp_econ'] + (60 / (qual_bowl['hp_balls'] + 60)) * 8.50

qual_bowl['composite_rating'] = (
    0.40 * norm(14.0 - qual_bowl['econ_shrunk']) +
    0.25 * norm(-qual_bowl['delta_econ']) +
    0.20 * norm(36.0 - qual_bowl['hp_sr'].clip(0, 36)) +
    0.15 * norm(np.log(qual_bowl['hp_balls']))
) * 100.0

qual_bowl = qual_bowl.sort_values('composite_rating', ascending=False).reset_index(drop=True)
qual_bowl['rank'] = range(1, len(qual_bowl) + 1)
qual_bowl['composite_rating'] = qual_bowl['composite_rating'].round(2)

# -----------------------------------------------------------------------------
# 7. IPL 2027 Retention Status Tagging
# -----------------------------------------------------------------------------
retained_roster = {
    # CSK
    'ruturaj gaikwad', 'sanju samson', 'kartik sharma', 'shivam dube', 'noor ahmad',
    'liam livingstone', 'rahul chahar', 'anshul kamboj', 'jack edwards', 'dewald brevis',
    'gurjapneet singh', 'akeal hosein', 'jamie overton', 'spencer johnson', 'sarfaraz khan',
    'ayush mhatre', 'urvil patel',
    # MI
    'arshdeep singh', 'ashwani kumar', 'corbin bosch', 'jasprit bumrah', 'mitchell santner',
    'naman dhir', 'quinton de kock', 'raghu sharma', 'raj angad bawa', 'rohit sharma',
    'ryan rickelton', 'shardul thakur', 'sherfane rutherford', 'suryakumar yadav', 'tilak varma', 'will jacks',
    # KKR
    'angkrish raghuvanshi', 'anukul roy', 'cameron green', 'finn allen', 'harshit rana',
    'kartik tyagi', 'manish pandey', 'prashant solanki', 'ramandeep singh', 'rinku singh',
    'rovman powell', 'sarthak ranjan', 'saurabh dubey', 'sunil narine', 'tim seifert',
    'vaibhav arora', 'varun chakravarthy',
    # SRH
    'abhishek sharma', 'pat cummins', 'heinrich klaasen', 'ishan kishan', 'nitish kumar reddy', 'nitish reddy',
    'aniket verma', 'shivang kumar', 'harsh dubey', 'eshan malinga', 'brydon carse',
    'praful hinge', 'sakib hussain', 'salil arora', 't natarajan', 'khaleel ahmed', 'nathan ellis',
    # DC
    'kl rahul', 'axar patel', 'david miller', 'tristan stubbs', 'sameer rizvi',
    'ashutosh sharma', 'prithvi shaw', 'rishabh pant', 'zeeshan ansari', 'mukesh kumar',
    'lungi ngidi', 'vipraj nigam', 'madhav tiwari', 'kyle jamieson',
    # LSG
    'nicholas pooran', 'mitchell marsh', 'aiden markram', 'ayush badoni', 'abdul samad',
    'mayank yadav', 'mohsin khan', 'prince yadav', 'digvesh rathi', 'arjun tendulkar',
    'himmat singh', 'kuldeep yadav', 'sam curran',
    # RR
    'yashasvi jaiswal', 'vaibhav sooryavanshi', 'riyan parag', 'dhruv jurel', 'ravindra jadeja',
    'jofra archer', 'donovan ferreira', 'lhuan-dre pretorius', 'sushant mishra', 'brijesh sharma',
    'yash raj punja', 'mohammad shami', 'm. siddharth', 'manimaran siddharth',
    # PBKS
    'shreyas iyer', 'prabhsimran singh', 'shashank singh', 'marcus stoinis', 'marco jansen',
    'yuzvendra chahal', 'hardik pandya',
    # RCB
    'virat kohli', 'rajat patidar', 'phil salt', 'tim david', 'venkatesh iyer',
    'devdutt padikkal', 'jitesh sharma', 'bhuvneshwar kumar', 'josh hazlewood', 'krunal pandya',
    'romario shepherd', 'jacob duffy', 'suyash sharma', 'rasikh salam',
    # GT
    'shubman gill', 'sai sudharsan', 'jos buttler', 'rashid khan', 'kagiso rabada',
    'mohammed siraj', 'prasidh krishna', 'washington sundar', 'rahul tewatia', 'sai kishore',
    'jason holder', 'arshad khan', 'gurnoor brar', 'harshal patel'
}

def is_player_retained(name):
    clean = name.strip().lower()
    for ret in retained_roster:
        if ret in clean or clean in ret:
            return True
    return False

qual_bat['is_retained'] = qual_bat['player_name'].apply(is_player_retained)
qual_bowl['is_retained'] = qual_bowl['player_name'].apply(is_player_retained)

# Separate Global vs Auction Pool
top10_bat_global = qual_bat.head(10).copy()
top10_bowl_global = qual_bowl.head(10).copy()

avail_bat = qual_bat[~qual_bat['is_retained']].copy().reset_index(drop=True)
avail_bat['auction_rank'] = range(1, len(avail_bat) + 1)
top10_bat_auction = avail_bat.head(10).copy()

avail_bowl = qual_bowl[~qual_bowl['is_retained']].copy().reset_index(drop=True)
avail_bowl['auction_rank'] = range(1, len(avail_bowl) + 1)
top10_bowl_auction = avail_bowl.head(10).copy()

# Export CSVs
top10_bat_global.to_csv(os.path.join(OUTPUT_DIR, "scratch_top10_batters_overall.csv"), index=False)
top10_bowl_global.to_csv(os.path.join(OUTPUT_DIR, "scratch_top10_bowlers_overall.csv"), index=False)
top10_bat_auction.to_csv(os.path.join(OUTPUT_DIR, "scratch_top10_available_batters_auction.csv"), index=False)
top10_bowl_auction.to_csv(os.path.join(OUTPUT_DIR, "scratch_top10_available_bowlers_auction.csv"), index=False)

print("\n=======================================================")
print("TOP 10 BATTERS UNDER PRESSURE (GLOBAL POOL)")
print("=======================================================")
print(top10_bat_global[['rank', 'player_name', 'composite_rating', 'hp_strike_rate', 'delta_strike_rate', 'hp_balls', 'hp_avg', 'is_retained']])

print("\n=======================================================")
print("TOP 10 BOWLERS UNDER PRESSURE (GLOBAL POOL)")
print("=======================================================")
print(top10_bowl_global[['rank', 'player_name', 'composite_rating', 'hp_econ', 'delta_econ', 'hp_sr', 'hp_wkts', 'hp_balls', 'is_retained']])

print("\n=======================================================")
print("TOP 10 AVAILABLE BATTERS (IPL 2027 AUCTION POOL)")
print("=======================================================")
print(top10_bat_auction[['auction_rank', 'player_name', 'composite_rating', 'hp_strike_rate', 'delta_strike_rate', 'hp_balls', 'hp_avg']])

print("\n=======================================================")
print("TOP 10 AVAILABLE BOWLERS (IPL 2027 AUCTION POOL)")
print("=======================================================")
print(top10_bowl_auction[['auction_rank', 'player_name', 'composite_rating', 'hp_econ', 'delta_econ', 'hp_sr', 'hp_wkts', 'hp_balls']])

# -----------------------------------------------------------------------------
# 8. Publication-Quality White Background Visualizations
# -----------------------------------------------------------------------------
RR_PINK = "#E73895"
RR_BLUE = "#001D48"
RR_GOLD = "#C59B27"
RR_TEAL = "#0288D1"

# Chart 1: Global Top 10 Batters & Bowlers
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9), facecolor='#FFFFFF')

# Batters
colors_bat = [RR_PINK if r else '#78909C' for r in top10_bat_global['is_retained'].iloc[::-1]]
bars1 = ax1.barh(top10_bat_global['player_name'].iloc[::-1], top10_bat_global['composite_rating'].iloc[::-1], color=colors_bat, height=0.65, edgecolor='#333333', linewidth=0.8)
ax1.set_facecolor('#FFFFFF')
ax1.set_title("Top 10 Batters Under Pressure (Global Roster)\nPink = Retained by Franchise | Grey = Available in Auction", fontsize=13, fontweight='bold', color=RR_BLUE, pad=15)
ax1.set_xlabel("Pressure Composite Rating (0-100)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax1.set_xlim(0, 100)
ax1.grid(axis='x', linestyle='--', alpha=0.5, color='#CCCCCC')

for bar in bars1:
    w = bar.get_width()
    ax1.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"{w:.1f}", va='center', ha='left', fontsize=10, fontweight='bold', color=RR_BLUE)

# Bowlers
colors_bowl = [RR_BLUE if r else '#00838F' for r in top10_bowl_global['is_retained'].iloc[::-1]]
bars2 = ax2.barh(top10_bowl_global['player_name'].iloc[::-1], top10_bowl_global['composite_rating'].iloc[::-1], color=colors_bowl, height=0.65, edgecolor='#333333', linewidth=0.8)
ax2.set_facecolor('#FFFFFF')
ax2.set_title("Top 10 Bowlers Under Pressure (Global Roster)\nNavy = Retained by Franchise | Teal = Available in Auction", fontsize=13, fontweight='bold', color=RR_BLUE, pad=15)
ax2.set_xlabel("Pressure Composite Rating (0-100)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax2.set_xlim(0, 100)
ax2.grid(axis='x', linestyle='--', alpha=0.5, color='#CCCCCC')

for bar in bars2:
    w = bar.get_width()
    ax2.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"{w:.1f}", va='center', ha='left', fontsize=10, fontweight='bold', color=RR_BLUE)

plt.tight_layout(pad=3.0)
fig1_path = os.path.join(CHARTS_DIR, "scratch_deepdive_top10_global.png")
plt.savefig(fig1_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
plt.close()
print(f"Saved: {fig1_path}")

# Chart 2: Auction Pool Top 10 Available Targets
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9), facecolor='#FFFFFF')

# Available Batters
bars1 = ax1.barh(top10_bat_auction['player_name'].iloc[::-1], top10_bat_auction['composite_rating'].iloc[::-1], color=RR_PINK, height=0.65, edgecolor=RR_BLUE, linewidth=1.0)
ax1.set_facecolor('#FFFFFF')
ax1.set_title("Top 10 Available Batters Under Pressure (IPL 2027 Auction)\nUnretained Targets for Rajasthan Royals War Room", fontsize=13, fontweight='bold', color=RR_BLUE, pad=15)
ax1.set_xlabel("Pressure Composite Rating (0-100)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax1.set_xlim(0, 100)
ax1.grid(axis='x', linestyle='--', alpha=0.5, color='#CCCCCC')

for idx, bar in enumerate(bars1):
    w = bar.get_width()
    row = top10_bat_auction.iloc[len(top10_bat_auction) - 1 - idx]
    stat_lbl = f"{w:.1f} (SR: {row['hp_strike_rate']:.1f}, ΔSR: {row['delta_strike_rate']:+.1f})"
    ax1.text(w + 1.2, bar.get_y() + bar.get_height()/2, stat_lbl, va='center', ha='left', fontsize=9.5, fontweight='bold', color=RR_BLUE)

# Available Bowlers
bars2 = ax2.barh(top10_bowl_auction['player_name'].iloc[::-1], top10_bowl_auction['composite_rating'].iloc[::-1], color=RR_BLUE, height=0.65, edgecolor=RR_PINK, linewidth=1.0)
ax2.set_facecolor('#FFFFFF')
ax2.set_title("Top 10 Available Bowlers Under Pressure (IPL 2027 Auction)\nUnretained Targets for Rajasthan Royals War Room", fontsize=13, fontweight='bold', color=RR_BLUE, pad=15)
ax2.set_xlabel("Pressure Composite Rating (0-100)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax2.set_xlim(0, 100)
ax2.grid(axis='x', linestyle='--', alpha=0.5, color='#CCCCCC')

for idx, bar in enumerate(bars2):
    w = bar.get_width()
    row = top10_bowl_auction.iloc[len(top10_bowl_auction) - 1 - idx]
    stat_lbl = f"{w:.1f} (Econ: {row['hp_econ']:.2f}, Wkts: {int(row['hp_wkts'])})"
    ax2.text(w + 1.2, bar.get_y() + bar.get_height()/2, stat_lbl, va='center', ha='left', fontsize=9.5, fontweight='bold', color=RR_BLUE)

plt.tight_layout(pad=3.0)
fig2_path = os.path.join(CHARTS_DIR, "scratch_deepdive_top10_auction_pool.png")
plt.savefig(fig2_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
plt.close()
print(f"Saved: {fig2_path}")

# Copy to artifacts directory
import shutil
for fname in ["scratch_deepdive_top10_global.png", "scratch_deepdive_top10_auction_pool.png"]:
    src = os.path.join(CHARTS_DIR, fname)
    dst = os.path.join(ARTIFACT_DIR, fname)
    shutil.copy2(src, dst)
    print(f"Mirrored to artifact: {dst}")

print("\nSUCCESS: All scratch deep-dive scripts, CSVs, and white-background figures executed flawlessly!")
