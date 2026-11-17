"""
Complete Player-by-Player Exploratory Data Analysis (EDA) & Comparative Analysis Pipeline
Analyzes EVERY batter (N=794) and EVERY bowler (N=587) in the clean dataset (excluding Pakistan & Retired).
Calculates career metrics, phase splits (PP, Middle, Death), innings splits, pressure metrics,
tactical archetypes, and percentile rankings across all players.
Generates comprehensive comparative matrices, CSV registers, and publication-ready white-background figures.
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
print(f"Clean deliveries: {len(df):,}")

# Pre-Delivery Match State & Deliveries
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

df = df.merge(matches[['match_id', 'comp_id', 'first_inn_balls', 'second_inn_balls', 'revised_target']], on='match_id', how='left')
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

# Retained Roster Map
retained_roster = {
    'ruturaj gaikwad', 'sanju samson', 'kartik sharma', 'shivam dube', 'noor ahmad',
    'liam livingstone', 'rahul chahar', 'anshul kamboj', 'jack edwards', 'dewald brevis',
    'gurjapneet singh', 'akeal hosein', 'jamie overton', 'spencer johnson', 'sarfaraz khan',
    'ayush mhatre', 'urvil patel', 'arshdeep singh', 'ashwani kumar', 'corbin bosch',
    'jasprit bumrah', 'mitchell santner', 'naman dhir', 'quinton de kock', 'raghu sharma',
    'raj angad bawa', 'rohit sharma', 'ryan rickelton', 'shardul thakur', 'sherfane rutherford',
    'suryakumar yadav', 'tilak varma', 'will jacks', 'angkrish raghuvanshi', 'anukul roy',
    'cameron green', 'finn allen', 'harshit rana', 'kartik tyagi', 'manish pandey',
    'prashant solanki', 'ramandeep singh', 'rinku singh', 'rovman powell', 'sarthak ranjan',
    'saurabh dubey', 'sunil narine', 'tim seifert', 'vaibhav arora', 'varun chakravarthy',
    'abhishek sharma', 'pat cummins', 'heinrich klaasen', 'ishan kishan', 'nitish kumar reddy', 'nitish reddy',
    'aniket verma', 'shivang kumar', 'harsh dubey', 'eshan malinga', 'brydon carse',
    'praful hinge', 'sakib hussain', 'salil arora', 't natarajan', 'khaleel ahmed', 'nathan ellis',
    'kl rahul', 'axar patel', 'david miller', 'tristan stubbs', 'sameer rizvi',
    'ashutosh sharma', 'prithvi shaw', 'rishabh pant', 'zeeshan ansari', 'mukesh kumar',
    'lungi ngidi', 'vipraj nigam', 'madhav tiwari', 'kyle jamieson', 'nicholas pooran',
    'mitchell marsh', 'aiden markram', 'ayush badoni', 'abdul samad', 'mayank yadav',
    'mohsin khan', 'prince yadav', 'digvesh rathi', 'arjun tendulkar', 'himmat singh',
    'kuldeep yadav', 'sam curran', 'yashasvi jaiswal', 'vaibhav sooryavanshi', 'riyan parag',
    'dhruv jurel', 'ravindra jadeja', 'jofra archer', 'donovan ferreira', 'lhuan-dre pretorius',
    'sushant mishra', 'brijesh sharma', 'yash raj punja', 'mohammad shami', 'm. siddharth', 'manimaran siddharth',
    'shreyas iyer', 'prabhsimran singh', 'shashank singh', 'marcus stoinis', 'marco jansen',
    'yuzvendra chahal', 'hardik pandya', 'virat kohli', 'rajat patidar', 'phil salt',
    'tim david', 'venkatesh iyer', 'devdutt padikkal', 'jitesh sharma', 'bhuvneshwar kumar',
    'josh hazlewood', 'krunal pandya', 'romario shepherd', 'jacob duffy', 'suyash sharma', 'rasikh salam',
    'shubman gill', 'sai sudharsan', 'jos buttler', 'rashid khan', 'kagiso rabada',
    'mohammed siraj', 'prasidh krishna', 'washington sundar', 'rahul tewatia', 'sai kishore',
    'jason holder', 'arshad khan', 'gurnoor brar', 'harshal patel', 'glenn phillips',
    'gerald coetzee', 'nishant sindhu', 'manav suthar', 'anuj rawat'
}

def is_retained(name):
    c = str(name).strip().lower()
    for r in retained_roster:
        if r in c or c in r:
            return True
    return False

# -----------------------------------------------------------------------------
# 2. Comprehensive Batting EDA on Each Batter (N=794)
# -----------------------------------------------------------------------------
print("2. Computing Comprehensive Batting EDA across all batters...")

bat_tot = df.groupby(['striker_id', 'striker_name']).agg(
    matches=('match_id', 'nunique'),
    innings=('match_id', lambda x: len(x.unique())),
    balls_faced=('balls_faced', 'sum'),
    runs=('runs', 'sum'),
    dismissals=('is_striker_dismissed', 'sum'),
    fours=('is_four', 'sum'),
    sixes=('is_six', 'sum'),
    dots=('is_batter_dot', 'sum'),
    singles=('runs', lambda x: (x == 1).sum()),
    doubles=('runs', lambda x: (x == 2).sum()),
).reset_index()

# Phase splits for Batters
bat_phase = df.groupby(['striker_id', 'phase']).agg(
    phase_balls=('balls_faced', 'sum'),
    phase_runs=('runs', 'sum'),
    phase_dismissals=('is_striker_dismissed', 'sum'),
    phase_boundaries=('runs', lambda x: (x >= 4).sum()),
    phase_dots=('is_batter_dot', 'sum')
).unstack().fillna(0)

bat_phase.columns = [f"{col[1].lower()}_{col[0]}" for col in bat_phase.columns]
bat_phase = bat_phase.reset_index()

# Innings splits for Batters
bat_inn = df.groupby(['striker_id', 'innings']).agg(
    inn_balls=('balls_faced', 'sum'),
    inn_runs=('runs', 'sum'),
    inn_dismissals=('is_striker_dismissed', 'sum')
).unstack().fillna(0)
bat_inn.columns = [f"inn{col[1]}_{col[0]}" for col in bat_inn.columns]
bat_inn = bat_inn.reset_index()

# Pressure Batting
bat_hp = df[df['is_hp_bat']].groupby('striker_id').agg(
    hp_balls=('balls_faced', 'sum'),
    hp_runs=('runs', 'sum'),
    hp_dismissals=('is_striker_dismissed', 'sum'),
    hp_fours=('is_four', 'sum'),
    hp_sixes=('is_six', 'sum'),
    hp_dots=('is_batter_dot', 'sum')
).reset_index()

bat_base = df[~df['is_hp_bat']].groupby('striker_id').agg(
    base_balls=('balls_faced', 'sum'),
    base_runs=('runs', 'sum'),
    base_dismissals=('is_striker_dismissed', 'sum')
).reset_index()

# Merge all Batting EDA components
bat_eda = bat_tot.merge(bat_phase, on='striker_id', how='left')
bat_eda = bat_eda.merge(bat_inn, on='striker_id', how='left')
bat_eda = bat_eda.merge(bat_hp, on='striker_id', how='left').fillna(0)
bat_eda = bat_eda.merge(bat_base, on='striker_id', how='left').fillna(0)

# Derived Core Batting Metrics
bat_eda['batting_avg'] = (bat_eda['runs'] / np.maximum(1, bat_eda['dismissals'])).round(2)
bat_eda['strike_rate'] = ((bat_eda['runs'] / np.maximum(1, bat_eda['balls_faced'])) * 100.0).round(2)
bat_eda['dot_pct'] = ((bat_eda['dots'] / np.maximum(1, bat_eda['balls_faced'])) * 100.0).round(1)
bat_eda['boundary_pct'] = (((bat_eda['fours'] + bat_eda['sixes']) / np.maximum(1, bat_eda['balls_faced'])) * 100.0).round(1)
bat_eda['boundary_run_pct'] = ((((bat_eda['fours'] * 4) + (bat_eda['sixes'] * 6)) / np.maximum(1, bat_eda['runs'])) * 100.0).round(1)

# Phase Derived
bat_eda['pp_strike_rate'] = ((bat_eda['powerplay_phase_runs'] / np.maximum(1, bat_eda['powerplay_phase_balls'])) * 100.0).round(1)
bat_eda['pp_avg'] = (bat_eda['powerplay_phase_runs'] / np.maximum(1, bat_eda['powerplay_phase_dismissals'])).round(1)
bat_eda['mid_strike_rate'] = ((bat_eda['middle_phase_runs'] / np.maximum(1, bat_eda['middle_phase_balls'])) * 100.0).round(1)
bat_eda['mid_avg'] = (bat_eda['middle_phase_runs'] / np.maximum(1, bat_eda['middle_phase_dismissals'])).round(1)
bat_eda['death_strike_rate'] = ((bat_eda['death_phase_runs'] / np.maximum(1, bat_eda['death_phase_balls'])) * 100.0).round(1)
bat_eda['death_avg'] = (bat_eda['death_phase_runs'] / np.maximum(1, bat_eda['death_phase_dismissals'])).round(1)

# Pressure Derived
bat_eda['hp_strike_rate'] = ((bat_eda['hp_runs'] / np.maximum(1, bat_eda['hp_balls'])) * 100.0).round(1)
bat_eda['base_strike_rate'] = ((bat_eda['base_runs'] / np.maximum(1, bat_eda['base_balls'])) * 100.0).round(1)
bat_eda['delta_strike_rate'] = (bat_eda['hp_strike_rate'] - bat_eda['base_strike_rate']).round(1)
bat_eda['hp_avg'] = (bat_eda['hp_runs'] / np.maximum(1, bat_eda['hp_dismissals'])).round(1)
bat_eda['hp_dot_pct'] = ((bat_eda['hp_dots'] / np.maximum(1, bat_eda['hp_balls'])) * 100.0).round(1)
bat_eda['hp_boundary_pct'] = (((bat_eda['hp_fours'] + bat_eda['hp_sixes']) / np.maximum(1, bat_eda['hp_balls'])) * 100.0).round(1)

# Shrunk SR & Composite Pressure Rating
def norm(s): return (s - s.min()) / (s.max() - s.min() + 1e-6)
bat_eda['sr_shrunk'] = (bat_eda['hp_balls'] / (bat_eda['hp_balls'] + 80)) * bat_eda['hp_strike_rate'] + (80 / (bat_eda['hp_balls'] + 80)) * 135.0

# Pressure Composite Rating (for all batters with >= 100 HP balls)
bat_eda['pressure_rating'] = np.where(
    bat_eda['hp_balls'] >= 100,
    (0.40 * norm(bat_eda['sr_shrunk']) + 0.25 * norm(bat_eda['delta_strike_rate']) + 0.20 * norm(bat_eda['hp_boundary_pct']) + 0.15 * norm(np.log(np.maximum(1, bat_eda['hp_balls'])))) * 100.0,
    np.nan
).round(2)

# Batter Archetype Classification
def classify_batter(row):
    if row['balls_faced'] < 60:
        return "Emerging / Low Sample"
    if row['death_phase_balls'] >= 45 and row['death_strike_rate'] >= 170.0:
        return "Elite Death Finisher"
    if row['powerplay_phase_balls'] >= 90 and row['pp_strike_rate'] >= 140.0:
        return "Powerplay Aggressor"
    if row['middle_phase_balls'] >= 100 and row['dot_pct'] < 33.0 and row['batting_avg'] >= 32.0:
        return "Middle Phase Anchor"
    if row['strike_rate'] >= 150.0 and row['boundary_pct'] >= 18.0:
        return "High-Impact Power Striker"
    if row['batting_avg'] >= 35.0 and row['strike_rate'] < 135.0:
        return "Classical Accumulator"
    return "Balanced Core Batter"

bat_eda['batter_archetype'] = bat_eda.apply(classify_batter, axis=1)
bat_eda['is_retained'] = bat_eda['striker_name'].apply(is_retained)

# Percentiles across qualified batters (>= 100 balls)
qual_b = bat_eda['balls_faced'] >= 100
bat_eda['sr_percentile'] = np.where(qual_b, (bat_eda['strike_rate'].rank(pct=True) * 100).round(1), np.nan)
bat_eda['avg_percentile'] = np.where(qual_b, (bat_eda['batting_avg'].rank(pct=True) * 100).round(1), np.nan)
bat_eda['boundary_percentile'] = np.where(qual_b, (bat_eda['boundary_pct'].rank(pct=True) * 100).round(1), np.nan)
bat_eda['hp_sr_percentile'] = np.where(bat_eda['hp_balls'] >= 100, (bat_eda['hp_strike_rate'].rank(pct=True) * 100).round(1), np.nan)

# -----------------------------------------------------------------------------
# 3. Comprehensive Bowling EDA on Each Bowler (N=587)
# -----------------------------------------------------------------------------
print("3. Computing Comprehensive Bowling EDA across all bowlers...")

bowl_tot = df.groupby(['bowler_id', 'bowler_name']).agg(
    matches=('match_id', 'nunique'),
    innings=('match_id', lambda x: len(x.unique())),
    legal_balls=('is_legal', 'sum'),
    runs_conceded=('bowler_runs', 'sum'),
    wickets=('is_bowler_wkt', 'sum'),
    dots=('is_bowler_dot', 'sum'),
    fours=('is_four', 'sum'),
    sixes=('is_six', 'sum'),
    wides=('extras_type', lambda x: (x == 'wide').sum()),
    noballs=('extras_type', lambda x: (x == 'Overstep').sum())
).reset_index()

# Phase splits for Bowlers
bowl_phase = df.groupby(['bowler_id', 'phase']).agg(
    phase_balls=('is_legal', 'sum'),
    phase_runs=('bowler_runs', 'sum'),
    phase_wickets=('is_bowler_wkt', 'sum'),
    phase_dots=('is_bowler_dot', 'sum'),
    phase_boundaries=('bowler_runs', lambda x: (x >= 4).sum())
).unstack().fillna(0)
bowl_phase.columns = [f"{col[1].lower()}_{col[0]}" for col in bowl_phase.columns]
bowl_phase = bowl_phase.reset_index()

# Innings splits for Bowlers
bowl_inn = df.groupby(['bowler_id', 'innings']).agg(
    inn_balls=('is_legal', 'sum'),
    inn_runs=('bowler_runs', 'sum'),
    inn_wickets=('is_bowler_wkt', 'sum')
).unstack().fillna(0)
bowl_inn.columns = [f"inn{col[1]}_{col[0]}" for col in bowl_inn.columns]
bowl_inn = bowl_inn.reset_index()

# Pressure Bowling
bowl_hp = df[df['is_hp_bowl']].groupby('bowler_id').agg(
    hp_balls=('is_legal', 'sum'),
    hp_runs=('bowler_runs', 'sum'),
    hp_wkts=('is_bowler_wkt', 'sum'),
    hp_dots=('is_bowler_dot', 'sum'),
    hp_fours=('is_four', 'sum'),
    hp_sixes=('is_six', 'sum')
).reset_index()

bowl_base = df[~df['is_hp_bowl']].groupby('bowler_id').agg(
    base_balls=('is_legal', 'sum'),
    base_runs=('bowler_runs', 'sum'),
    base_wkts=('is_bowler_wkt', 'sum')
).reset_index()

# Merge all Bowling EDA components
bowl_eda = bowl_tot.merge(bowl_phase, on='bowler_id', how='left')
bowl_eda = bowl_eda.merge(bowl_inn, on='bowler_id', how='left')
bowl_eda = bowl_eda.merge(bowl_hp, on='bowler_id', how='left').fillna(0)
bowl_eda = bowl_eda.merge(bowl_base, on='bowler_id', how='left').fillna(0)

# Derived Core Bowling Metrics
bowl_eda['overs'] = (bowl_eda['legal_balls'] / 6.0).round(1)
bowl_eda['economy_rate'] = (bowl_eda['runs_conceded'] / np.maximum(1, bowl_eda['legal_balls'] / 6.0)).round(2)
bowl_eda['bowling_avg'] = (bowl_eda['runs_conceded'] / np.maximum(1, bowl_eda['wickets'])).round(2)
bowl_eda['wicket_strike_rate'] = (bowl_eda['legal_balls'] / np.maximum(1, bowl_eda['wickets'])).round(1)
bowl_eda['dot_pct'] = ((bowl_eda['dots'] / np.maximum(1, bowl_eda['legal_balls'])) * 100.0).round(1)
bowl_eda['boundary_conceded_pct'] = (((bowl_eda['fours'] + bowl_eda['sixes']) / np.maximum(1, bowl_eda['legal_balls'])) * 100.0).round(1)

# Phase Derived
bowl_eda['pp_economy'] = (bowl_eda['powerplay_phase_runs'] / np.maximum(1, bowl_eda['powerplay_phase_balls'] / 6.0)).round(2)
bowl_eda['pp_wkt_sr'] = (bowl_eda['powerplay_phase_balls'] / np.maximum(1, bowl_eda['powerplay_phase_wickets'])).round(1)
bowl_eda['mid_economy'] = (bowl_eda['middle_phase_runs'] / np.maximum(1, bowl_eda['middle_phase_balls'] / 6.0)).round(2)
bowl_eda['mid_wkt_sr'] = (bowl_eda['middle_phase_balls'] / np.maximum(1, bowl_eda['middle_phase_wickets'])).round(1)
bowl_eda['death_economy'] = (bowl_eda['death_phase_runs'] / np.maximum(1, bowl_eda['death_phase_balls'] / 6.0)).round(2)
bowl_eda['death_wkt_sr'] = (bowl_eda['death_phase_balls'] / np.maximum(1, bowl_eda['death_phase_wickets'])).round(1)

# Pressure Derived
bowl_eda['hp_econ'] = (bowl_eda['hp_runs'] / np.maximum(1, bowl_eda['hp_balls'] / 6.0)).round(2)
bowl_eda['base_econ'] = (bowl_eda['base_runs'] / np.maximum(1, bowl_eda['base_balls'] / 6.0)).round(2)
bowl_eda['delta_econ'] = (bowl_eda['hp_econ'] - bowl_eda['base_econ']).round(2)
bowl_eda['hp_sr'] = (bowl_eda['hp_balls'] / np.maximum(1, bowl_eda['hp_wkts'])).round(1)
bowl_eda['hp_dot_pct'] = ((bowl_eda['hp_dots'] / np.maximum(1, bowl_eda['hp_balls'])) * 100.0).round(1)
bowl_eda['hp_bdry_pct'] = (((bowl_eda['hp_fours'] + bowl_eda['hp_sixes']) / np.maximum(1, bowl_eda['hp_balls'])) * 100.0).round(1)

# Shrunk Economy & Composite Pressure Rating
bowl_eda['econ_shrunk'] = (bowl_eda['hp_balls'] / (bowl_eda['hp_balls'] + 60)) * bowl_eda['hp_econ'] + (60 / (bowl_eda['hp_balls'] + 60)) * 8.50

bowl_eda['pressure_rating'] = np.where(
    bowl_eda['hp_balls'] >= 60,
    (0.40 * norm(14.0 - bowl_eda['econ_shrunk']) + 0.25 * norm(-bowl_eda['delta_econ']) + 0.20 * norm(36.0 - bowl_eda['hp_sr'].clip(0, 36)) + 0.15 * norm(np.log(np.maximum(1, bowl_eda['hp_balls'])))) * 100.0,
    np.nan
).round(2)

# Bowler Archetype Classification
def classify_bowler(row):
    if row['legal_balls'] < 60:
        return "Emerging / Low Sample"
    if row['death_phase_balls'] >= 40 and row['death_economy'] <= 9.6:
        return "Elite Death Closer"
    if row['powerplay_phase_balls'] >= 60 and row['pp_wkt_sr'] <= 20.0 and row['pp_economy'] <= 7.8:
        return "Powerplay Strike Seamer"
    if row['middle_phase_balls'] >= 80 and row['mid_economy'] <= 7.4:
        return "Middle Run Restrictor"
    if row['wicket_strike_rate'] <= 16.0 and row['economy_rate'] <= 8.5:
        return "All-Phase Wicket Hunter"
    if row['economy_rate'] <= 7.8 and row['wicket_strike_rate'] > 20.0:
        return "Workhorse Containment"
    if row['economy_rate'] > 9.5 and row['wicket_strike_rate'] <= 18.0:
        return "Attacking / High Variance"
    return "Balanced Core Bowler"

bowl_eda['bowler_archetype'] = bowl_eda.apply(classify_bowler, axis=1)
bowl_eda['is_retained'] = bowl_eda['bowler_name'].apply(is_retained)

# Percentiles across qualified bowlers (>= 60 balls)
qual_w = bowl_eda['legal_balls'] >= 60
bowl_eda['econ_percentile'] = np.where(qual_w, ((-bowl_eda['economy_rate']).rank(pct=True) * 100).round(1), np.nan)
bowl_eda['wkt_sr_percentile'] = np.where(qual_w, ((-bowl_eda['wicket_strike_rate']).rank(pct=True) * 100).round(1), np.nan)
bowl_eda['dot_percentile'] = np.where(qual_w, (bowl_eda['dot_pct'].rank(pct=True) * 100).round(1), np.nan)
bowl_eda['hp_econ_percentile'] = np.where(bowl_eda['hp_balls'] >= 60, ((-bowl_eda['hp_econ']).rank(pct=True) * 100).round(1), np.nan)

# Export Full Player EDA CSVs
bat_eda_path = os.path.join(OUTPUT_DIR, "player_eda_batting_complete.csv")
bowl_eda_path = os.path.join(OUTPUT_DIR, "player_eda_bowling_complete.csv")
bat_eda.to_csv(bat_eda_path, index=False)
bowl_eda.to_csv(bowl_eda_path, index=False)
print(f"Exported complete Batting EDA ({len(bat_eda)} players) -> {bat_eda_path}")
print(f"Exported complete Bowling EDA ({len(bowl_eda)} players) -> {bowl_eda_path}")

# -----------------------------------------------------------------------------
# 4. Cross-Player Comparative Analysis Visualizations (Pure White #FFFFFF)
# -----------------------------------------------------------------------------
print("4. Generating publication-ready white background comparative charts...")

RR_PINK = "#E73895"
RR_BLUE = "#001D48"
RR_GOLD = "#C59B27"
RR_TEAL = "#0288D1"
RR_DARK = "#212121"

# FIG 1: Batter Comparative Quadrant (Baseline SR vs High-Pressure SR)
fig, ax = plt.subplots(figsize=(13, 9), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Filter qualified batters (>= 80 HP balls)
q_bat = bat_eda[bat_eda['hp_balls'] >= 80].copy()

# Scatter points: Retained vs Available
retained_mask = q_bat['is_retained']
ax.scatter(q_bat[retained_mask]['base_strike_rate'], q_bat[retained_mask]['hp_strike_rate'], color=RR_BLUE, alpha=0.65, s=q_bat[retained_mask]['hp_balls']*0.6, edgecolors='#000000', linewidth=0.5, label='Retained by Franchise')
ax.scatter(q_bat[~retained_mask]['base_strike_rate'], q_bat[~retained_mask]['hp_strike_rate'], color=RR_PINK, alpha=0.85, s=q_bat[~retained_mask]['hp_balls']*0.8, edgecolors='#000000', linewidth=0.8, label='Available in Auction (RR Targets)')

# Equality Line (y = x)
lims = [100, 200]
ax.plot(lims, lims, linestyle='--', color='#999999', alpha=0.8, label='Zero Clutch Uplift (HP SR = Base SR)')

# Quadrant Dividers (Median values)
med_base = q_bat['base_strike_rate'].median()
med_hp = q_bat['hp_strike_rate'].median()
ax.axvline(med_base, linestyle=':', color='#BBBBBB', alpha=0.7)
ax.axhline(med_hp, linestyle=':', color='#BBBBBB', alpha=0.7)

# Annotate Key Benchmark Players
key_batters = [
    'Suryakumar Yadav', 'Namboori Tilak Varma', 'Heinrich Klaasen', 'Nicholas Pooran',
    'Azmatullah Omarzai', 'Sikandar Raza', 'Mohammad Nabi', 'M Shahrukh Khan',
    'Glenn Phillips', 'Dasun Shanaka', 'Riyan Parag', 'Dhruv Jurel', 'Yashasvi Jaiswal'
]

for name in key_batters:
    row = q_bat[q_bat['striker_name'].str.lower() == name.lower()]
    if len(row) > 0:
        r = row.iloc[0]
        color = RR_PINK if not r['is_retained'] else RR_BLUE
        ax.annotate(
            r['striker_name'],
            (r['base_strike_rate'], r['hp_strike_rate']),
            xytext=(6, 4), textcoords='offset points',
            fontsize=9.5, fontweight='bold', color=color,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#FFFFFF', edgecolor=color, alpha=0.85)
        )

ax.set_title("Cross-Player Batting Comparison: Baseline Strike Rate vs High-Pressure Strike Rate\nBubble size proportional to High-Pressure Balls Faced | Upper Left = Elite Clutch Elevators", fontsize=13, fontweight='bold', color=RR_BLUE, pad=15)
ax.set_xlabel("Career Baseline Strike Rate (Low & Medium Pressure)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax.set_ylabel("High-Pressure Strike Rate (PI ≥ 65)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax.set_xlim(105, 195)
ax.set_ylim(105, 205)
ax.grid(True, linestyle='--', alpha=0.4, color='#DDDDDD')
ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CCCCCC', loc='lower right', fontsize=10)

plt.tight_layout()
fig1_path = os.path.join(CHARTS_DIR, "player_comparative_batting_clutch_scatter.png")
plt.savefig(fig1_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
plt.close()
print(f"Saved: {fig1_path}")

# FIG 2: Bowler Comparative Quadrant (Baseline Economy vs High-Pressure Economy)
fig, ax = plt.subplots(figsize=(13, 9), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Filter qualified bowlers (>= 50 HP balls)
q_bowl = bowl_eda[bowl_eda['hp_balls'] >= 50].copy()

retained_w_mask = q_bowl['is_retained']
ax.scatter(q_bowl[retained_w_mask]['base_econ'], q_bowl[retained_w_mask]['hp_econ'], color=RR_BLUE, alpha=0.65, s=q_bowl[retained_w_mask]['hp_balls']*0.9, edgecolors='#000000', linewidth=0.5, label='Retained by Franchise')
ax.scatter(q_bowl[~retained_w_mask]['base_econ'], q_bowl[~retained_w_mask]['hp_econ'], color=RR_TEAL, alpha=0.85, s=q_bowl[~retained_w_mask]['hp_balls']*1.1, edgecolors='#000000', linewidth=0.8, label='Available in Auction (RR Targets)')

# Equality Line (y = x)
lims_w = [6.0, 13.0]
ax.plot(lims_w, lims_w, linestyle='--', color='#999999', alpha=0.8, label='Zero Deterioration (HP Econ = Base Econ)')

key_bowlers = [
    'Rashid Khan', 'Maheesh Theekshana', 'Mohsin Khan', 'Avesh Khan', 'Wanindu Hasaranga',
    'Ravi Bishnoi', 'Matheesha Pathirana', 'Mustafizur Rahman', 'Jofra Archer', 'Mohammad Shami',
    'Jasprit Bumrah', 'Arshdeep Singh', 'Yuzvendra Chahal'
]

for name in key_bowlers:
    row = q_bowl[q_bowl['bowler_name'].str.lower() == name.lower()]
    if len(row) > 0:
        r = row.iloc[0]
        color = RR_TEAL if not r['is_retained'] else RR_BLUE
        ax.annotate(
            r['bowler_name'],
            (r['base_econ'], r['hp_econ']),
            xytext=(6, 4), textcoords='offset points',
            fontsize=9.5, fontweight='bold', color=color,
            bbox=dict(boxstyle="round,pad=0.2", facecolor='#FFFFFF', edgecolor=color, alpha=0.85)
        )

ax.set_title("Cross-Player Bowling Comparison: Baseline Economy vs High-Pressure Economy\nBubble size proportional to HP Deliveries | Lower Left = Elite Pressure Restrictors (Sub-8.00 Econ)", fontsize=13, fontweight='bold', color=RR_BLUE, pad=15)
ax.set_xlabel("Career Baseline Economy Rate (Low & Medium Pressure)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax.set_ylabel("High-Pressure Economy Rate (PI ≥ 65)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax.set_xlim(6.5, 11.5)
ax.set_ylim(6.5, 12.5)
ax.grid(True, linestyle='--', alpha=0.4, color='#DDDDDD')
ax.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CCCCCC', loc='lower right', fontsize=10)

plt.tight_layout()
fig2_path = os.path.join(CHARTS_DIR, "player_comparative_bowling_clutch_scatter.png")
plt.savefig(fig2_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
plt.close()
print(f"Saved: {fig2_path}")

# FIG 3: Head-to-Head Multi-Metric Comparison Matrix for Key Batters
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), facecolor='#FFFFFF')

target_batters = ['Suryakumar Yadav', 'Heinrich Klaasen', 'Azmatullah Omarzai', 'Sikandar Raza', 'M Shahrukh Khan', 'Dasun Shanaka', 'Riyan Parag', 'Dhruv Jurel']
sub_bat = bat_eda[bat_eda['striker_name'].isin(target_batters)].copy()
sub_bat = sub_bat.set_index('striker_name').reindex(target_batters).dropna()

# Subplot 1: Phase Strike Rate Progression (PP vs Middle vs Death)
x = np.arange(len(sub_bat))
w = 0.25
ax1.bar(x - w, sub_bat['pp_strike_rate'], width=w, color='#0288D1', edgecolor='#333333', linewidth=0.6, label='Powerplay SR (1-6)')
ax1.bar(x, sub_bat['mid_strike_rate'], width=w, color='#F57C00', edgecolor='#333333', linewidth=0.6, label='Middle Overs SR (7-15)')
ax1.bar(x + w, sub_bat['death_strike_rate'], width=w, color='#D32F2F', edgecolor='#333333', linewidth=0.6, label='Death Overs SR (16-20)')
ax1.set_facecolor('#FFFFFF')
ax1.set_title("Phase Strike Rate Breakdown Across Key Peers & RR Targets\nEvaluating Acceleration Profiles Across Game Stages", fontsize=12, fontweight='bold', color=RR_BLUE, pad=12)
ax1.set_ylabel("Strike Rate", fontsize=11, fontweight='bold', color=RR_BLUE)
ax1.set_xticks(x)
ax1.set_xticklabels(sub_bat.index, rotation=30, ha='right', fontsize=9.5, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.4, color='#CCCCCC')
ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CCCCCC', loc='upper left')

# Subplot 2: Boundary % vs Dot Ball % Efficiency
ax2.scatter(sub_bat['dot_pct'], sub_bat['boundary_pct'], color=RR_PINK, s=150, edgecolors=RR_BLUE, linewidth=1.5)
for idx, name in enumerate(sub_bat.index):
    ax2.annotate(name, (sub_bat['dot_pct'].iloc[idx], sub_bat['boundary_pct'].iloc[idx]), xytext=(6, 4), textcoords='offset points', fontsize=9.5, fontweight='bold', color=RR_BLUE)
ax2.set_facecolor('#FFFFFF')
ax2.set_title("Boundary Rate (%) vs Dot Ball Rate (%)\nTop Right / Lower Dot = Optimal Scoring Efficiency", fontsize=12, fontweight='bold', color=RR_BLUE, pad=12)
ax2.set_xlabel("Career Dot Ball % (Lower is Better)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax2.set_ylabel("Career Boundary % (Higher is Better)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax2.grid(True, linestyle='--', alpha=0.4, color='#CCCCCC')

plt.tight_layout(pad=3.0)
fig3_path = os.path.join(CHARTS_DIR, "player_comparative_batters_head_to_head.png")
plt.savefig(fig3_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
plt.close()
print(f"Saved: {fig3_path}")

# FIG 4: Head-to-Head Multi-Metric Comparison Matrix for Key Bowlers
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), facecolor='#FFFFFF')

target_bowlers = ['Rashid Khan', 'Maheesh Theekshana', 'Mohsin Khan', 'Avesh Khan', 'Wanindu Hasaranga', 'Matheesha Pathirana', 'Jofra Archer', 'Mohammad Shami']
sub_bowl = bowl_eda[bowl_eda['bowler_name'].isin(target_bowlers)].copy()
sub_bowl = sub_bowl.set_index('bowler_name').reindex(target_bowlers).dropna()

# Subplot 1: Phase Economy Progression (PP vs Middle vs Death)
x = np.arange(len(sub_bowl))
w = 0.25
ax1.bar(x - w, sub_bowl['pp_economy'], width=w, color='#388E3C', edgecolor='#333333', linewidth=0.6, label='Powerplay Econ')
ax1.bar(x, sub_bowl['mid_economy'], width=w, color='#1976D2', edgecolor='#333333', linewidth=0.6, label='Middle Overs Econ')
ax1.bar(x + w, sub_bowl['death_economy'], width=w, color='#C2185B', edgecolor='#333333', linewidth=0.6, label='Death Overs Econ')
ax1.set_facecolor('#FFFFFF')
ax1.set_title("Phase Economy Rate Comparison Across Frontline Peers & Targets\nSub-10.0 Death Economy Defines Elite Closer Capability", fontsize=12, fontweight='bold', color=RR_BLUE, pad=12)
ax1.set_ylabel("Economy Rate", fontsize=11, fontweight='bold', color=RR_BLUE)
ax1.set_xticks(x)
ax1.set_xticklabels(sub_bowl.index, rotation=30, ha='right', fontsize=9.5, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.4, color='#CCCCCC')
ax1.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#CCCCCC', loc='upper left')

# Subplot 2: High-Pressure Economy vs High-Pressure Wicket Strike Rate
ax2.scatter(sub_bowl['hp_sr'], sub_bowl['hp_econ'], color=RR_BLUE, s=150, edgecolors=RR_TEAL, linewidth=1.5)
for idx, name in enumerate(sub_bowl.index):
    ax2.annotate(name, (sub_bowl['hp_sr'].iloc[idx], sub_bowl['hp_econ'].iloc[idx]), xytext=(6, 4), textcoords='offset points', fontsize=9.5, fontweight='bold', color=RR_BLUE)
ax2.set_facecolor('#FFFFFF')
ax2.set_title("High-Pressure Economy vs High-Pressure Wicket Strike Rate\nLower Left = Lethal Strike Capability & Run Suppression", fontsize=12, fontweight='bold', color=RR_BLUE, pad=12)
ax2.set_xlabel("High-Pressure Balls per Wicket (Lower is More Lethal)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax2.set_ylabel("High-Pressure Economy Rate (Lower is Tighter)", fontsize=11, fontweight='bold', color=RR_BLUE)
ax2.grid(True, linestyle='--', alpha=0.4, color='#CCCCCC')

plt.tight_layout(pad=3.0)
fig4_path = os.path.join(CHARTS_DIR, "player_comparative_bowlers_head_to_head.png")
plt.savefig(fig4_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
plt.close()
print(f"Saved: {fig4_path}")

# FIG 5: Tactical Archetype Distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7), facecolor='#FFFFFF')

bat_arch = bat_eda[bat_eda['balls_faced'] >= 60]['batter_archetype'].value_counts()
ax1.barh(bat_arch.index[::-1], bat_arch.values[::-1], color=RR_PINK, edgecolor=RR_BLUE, height=0.6)
ax1.set_facecolor('#FFFFFF')
ax1.set_title("Distribution of Batter Tactical Archetypes (Qualified Pool)\nCategorizing Career Roles Across Modern T20 Play", fontsize=12, fontweight='bold', color=RR_BLUE, pad=12)
ax1.set_xlabel("Player Count", fontsize=11, fontweight='bold', color=RR_BLUE)
for i, v in enumerate(bat_arch.values[::-1]):
    ax1.text(v + 1, i, str(v), va='center', fontweight='bold', color=RR_BLUE)

bowl_arch = bowl_eda[bowl_eda['legal_balls'] >= 60]['bowler_archetype'].value_counts()
ax2.barh(bowl_arch.index[::-1], bowl_arch.values[::-1], color=RR_BLUE, edgecolor=RR_PINK, height=0.6)
ax2.set_facecolor('#FFFFFF')
ax2.set_title("Distribution of Bowler Tactical Archetypes (Qualified Pool)\nCategorizing Bowling Roles Across Modern T20 Play", fontsize=12, fontweight='bold', color=RR_BLUE, pad=12)
ax2.set_xlabel("Player Count", fontsize=11, fontweight='bold', color=RR_BLUE)
for i, v in enumerate(bowl_arch.values[::-1]):
    ax2.text(v + 1, i, str(v), va='center', fontweight='bold', color=RR_BLUE)

plt.tight_layout(pad=3.0)
fig5_path = os.path.join(CHARTS_DIR, "player_archetype_distribution_summary.png")
plt.savefig(fig5_path, dpi=300, facecolor='#FFFFFF', edgecolor='none')
plt.close()
print(f"Saved: {fig5_path}")

# Mirror all newly generated charts to artifacts
import shutil
for fname in [
    "player_comparative_batting_clutch_scatter.png",
    "player_comparative_bowling_clutch_scatter.png",
    "player_comparative_batters_head_to_head.png",
    "player_comparative_bowlers_head_to_head.png",
    "player_archetype_distribution_summary.png"
]:
    src = os.path.join(CHARTS_DIR, fname)
    dst = os.path.join(ARTIFACT_DIR, fname)
    shutil.copy2(src, dst)
    print(f"Mirrored chart to artifact: {dst}")

print("\nSUCCESS: All player-level EDA metrics, archetype classifications, and comparative charts generated!")
