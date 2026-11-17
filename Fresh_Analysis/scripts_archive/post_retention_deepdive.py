import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# White theme configuration
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
    'font.family': 'sans-serif',
}
plt.rcParams.update(WHITE_THEME)

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

BASE_DIR = r'c:\Users\Asus-2025\Downloads\RR'
FRESH_DIR = os.path.join(BASE_DIR, 'Fresh_Analysis')
CHARTS_DIR = os.path.join(BASE_DIR, 'final_pressure_charts_white_bg')
RR_CHARTS = os.path.join(BASE_DIR, 'charts')

# 1. Complete Official Retained Lists across all 10 teams
retained_csk = ['Ruturaj Gaikwad', 'Sanju Samson', 'Kartik Sharma', 'Shivam Dube', 'Noor Ahmad', 'Liam Livingstone', 'Rahul Chahar', 'Anshul Kamboj', 'Jack Edwards', 'Dewald Brevis', 'Gurjapneet Singh', 'Akeal Hosein', 'Jamie Overton', 'Spencer Johnson', 'Sarfaraz Khan', 'Ayush Mhatre', 'Urvil Patel']
retained_mi = ['Arshdeep Singh', 'Ashwani Kumar', 'Corbin Bosch', 'Jasprit Bumrah', 'Mitchell Santner', 'Naman Dhir', 'Quinton de Kock', 'Raghu Sharma', 'Raj Angad Bawa', 'Rohit Sharma', 'Ryan Rickelton', 'Shardul Thakur', 'Sherfane Rutherford', 'Suryakumar Yadav', 'Tilak Varma', 'Will Jacks']
retained_kkr = ['Angkrish Raghuvanshi', 'Anukul Roy', 'Cameron Green', 'Finn Allen', 'Harshit Rana', 'Kartik Tyagi', 'Manish Pandey', 'Prashant Solanki', 'Ramandeep Singh', 'Rinku Singh', 'Rovman Powell', 'Sarthak Ranjan', 'Saurabh Dubey', 'Sunil Narine', 'Tim Seifert', 'Vaibhav Arora', 'Varun Chakravarthy']
retained_srh = ['Abhishek Sharma', 'Pat Cummins', 'Heinrich Klaasen', 'Ishan Kishan', 'Nitish Kumar Reddy', 'Aniket Verma', 'Shivang Kumar', 'Harsh Dubey', 'Eshan Malinga', 'Brydon Carse', 'Praful Hinge', 'Sakib Hussain', 'Salil Arora', 'T Natarajan', 'Khaleel Ahmed', 'Nathan Ellis']
retained_dc = ['KL Rahul', 'Axar Patel', 'David Miller', 'Tristan Stubbs', 'Sameer Rizvi', 'Ashutosh Sharma', 'Prithvi Shaw', 'Rishabh Pant', 'Zeeshan Ansari', 'Mukesh Kumar', 'Lungi Ngidi', 'Vipraj Nigam', 'Madhav Tiwari', 'Kyle Jamieson']
retained_lsg = ['Nicholas Pooran', 'Mitchell Marsh', 'Aiden Markram', 'Ayush Badoni', 'Abdul Samad', 'Mayank Yadav', 'Mohsin Khan', 'Prince Yadav', 'Digvesh Rathi', 'Arjun Tendulkar', 'Himmat Singh', 'Kuldeep Yadav', 'Sam Curran']
retained_rr = ['Yashasvi Jaiswal', 'Vaibhav Sooryavanshi', 'Riyan Parag', 'Dhruv Jurel', 'Ravindra Jadeja', 'Jofra Archer', 'Donovan Ferreira', 'Lhuan-dre Pretorius', 'Sushant Mishra', 'Brijesh Sharma', 'Yash Raj Punja', 'Mohammad Shami', 'M. Siddharth']
retained_pbks = ['Shreyas Iyer', 'Prabhsimran Singh', 'Shashank Singh', 'Marcus Stoinis', 'Marco Jansen', 'Yuzvendra Chahal', 'Hardik Pandya']
retained_rcb = ['Virat Kohli', 'Rajat Patidar', 'Phil Salt', 'Tim David', 'Venkatesh Iyer', 'Devdutt Padikkal', 'Jitesh Sharma', 'Bhuvneshwar Kumar', 'Josh Hazlewood', 'Krunal Pandya', 'Romario Shepherd', 'Jacob Duffy', 'Suyash Sharma', 'Rasikh Salam']
retained_gt = ['Shubman Gill', 'Sai Sudharsan', 'Jos Buttler', 'Rashid Khan', 'Kagiso Rabada', 'Mohammed Siraj', 'Prasidh Krishna', 'Washington Sundar', 'Rahul Tewatia', 'Sai Kishore', 'Jason Holder', 'Arshad Khan', 'Gurnoor Brar', 'Harshal Patel']

all_retained = set(retained_csk + retained_mi + retained_kkr + retained_srh + retained_dc + retained_lsg + retained_rr + retained_pbks + retained_rcb + retained_gt)

# Confirmed Retired or Opted Out in this release
retired_or_opted_out = {'ms dhoni', 'mahendra singh dhoni', 'travis head', 'mitchell starc', 'dinesh karthik'}

def is_retained(name):
    n = name.lower().strip()
    for r in all_retained:
        rl = r.lower().strip()
        if rl in n or n in rl:
            return True
        parts = rl.split()
        if len(parts) >= 2 and all(p in n for p in parts):
            return True
    return False

def is_retired_or_optout(name):
    n = name.lower().strip()
    return any(ro in n for ro in retired_or_opted_out)

df_bat = pd.read_csv(os.path.join(FRESH_DIR, 'top_batters_under_pressure.csv'))
df_bowl = pd.read_csv(os.path.join(FRESH_DIR, 'top_bowlers_under_pressure.csv'))

df_bat['retained'] = df_bat['striker_name'].apply(is_retained)
df_bat['retired_optout'] = df_bat['striker_name'].apply(is_retired_or_optout)

df_bowl['retained'] = df_bowl['bowler_name'].apply(is_retained)
df_bowl['retired_optout'] = df_bowl['bowler_name'].apply(is_retired_or_optout)

# Filter for Available Auction Cohorts
avail_bat = df_bat[~df_bat['retained'] & ~df_bat['retired_optout']].copy()
avail_bat = avail_bat.sort_values('composite_rating', ascending=False).reset_index(drop=True)
avail_bat['auction_rank'] = range(1, len(avail_bat) + 1)

avail_bowl = df_bowl[~df_bowl['retained'] & ~df_bowl['retired_optout']].copy()
avail_bowl = avail_bowl.sort_values('composite_rating', ascending=False).reset_index(drop=True)
avail_bowl['auction_rank'] = range(1, len(avail_bowl) + 1)

top10_avail_bat = avail_bat.head(10).copy()
top10_avail_bowl = avail_bowl.head(10).copy()

# Export CSVs
top10_avail_bat.to_csv(os.path.join(FRESH_DIR, 'top10_available_batters_auction_2027.csv'), index=False)
top10_avail_bowl.to_csv(os.path.join(FRESH_DIR, 'top10_available_bowlers_auction_2027.csv'), index=False)

print("Exported top10_available_batters_auction_2027.csv and top10_available_bowlers_auction_2027.csv")

# ─────────────────────────────────────────────────────────────────────────────
# VISUAL 1: Top 10 Available Batters Under Pressure (White Background)
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#FFFFFF')

b_names = top10_avail_bat['striker_name'].values
y_pos = np.arange(len(b_names))

# Left: Composite Pressure Rating
bars1 = axes[0].barh(y_pos, top10_avail_bat['composite_rating'].values, color=NAVY, edgecolor='#CBD5E1', height=0.65)
axes[0].set_yticks(y_pos)
axes[0].set_yticklabels(b_names, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[0].set_xlabel('Composite Pressure Rating', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_title('TOP 10 AVAILABLE BATTERS: COMPOSITE RATING\n(Unretained Auction Pool for IPL 2027)', fontsize=12, fontweight='bold', color=NAVY)
axes[0].invert_yaxis()
axes[0].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(top10_avail_bat['composite_rating'].values):
    axes[0].text(v + 1.0, i, f'{v:.1f}', va='center', fontsize=9, fontweight='bold', color=DARK_TEXT)
axes[0].set_xlim(0, max(top10_avail_bat['composite_rating']) + 12)

# Right: High-Pressure Strike Rate & Clutch Uplift
axes[1].barh(y_pos - 0.2, top10_avail_bat['hp_sr'].values, height=0.38, color=BLUE, label='High-Pressure SR', edgecolor='#CBD5E1')
axes[1].barh(y_pos + 0.2, top10_avail_bat['base_sr'].values, height=0.38, color=SLATE, label='Baseline SR', edgecolor='#CBD5E1', alpha=0.7)
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(b_names, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[1].set_xlabel('Strike Rate (Runs / 100 Balls)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_title('HP STRIKE RATE vs BASELINE & CLUTCH UPLIFT', fontsize=12, fontweight='bold', color=NAVY)
axes[1].invert_yaxis()
axes[1].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
axes[1].legend(loc='lower right', fontsize=9, facecolor='#F8FAFC', edgecolor='#CBD5E1')
for i, v in enumerate(top10_avail_bat['hp_sr'].values):
    u = top10_avail_bat['delta_sr'].values[i]
    axes[1].text(v + 2.0, i - 0.2, f'{v:.1f} (+{u:.1f})', va='center', fontsize=8, fontweight='bold', color=NAVY)

plt.suptitle('IPL 2027 AUCTION SHORTLIST: TOP 10 AVAILABLE BATTERS UNDER PRESSURE', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
p_v1 = os.path.join(CHARTS_DIR, 'post_retention_top10_available_batters.png')
plt.savefig(p_v1, facecolor='#FFFFFF')
plt.savefig(os.path.join(RR_CHARTS, 'post_retention_top10_available_batters.png'), facecolor='#FFFFFF')
plt.close()
print("Saved post_retention_top10_available_batters.png")

# ─────────────────────────────────────────────────────────────────────────────
# VISUAL 2: Top 10 Available Bowlers Under Pressure (White Background)
# ─────────────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor='#FFFFFF')

w_names = top10_avail_bowl['bowler_name'].values
y_pos_w = np.arange(len(w_names))

# Left: Composite Pressure Rating
bars2 = axes[0].barh(y_pos_w, top10_avail_bowl['composite_rating'].values, color=CYAN, edgecolor='#CBD5E1', height=0.65)
axes[0].set_yticks(y_pos_w)
axes[0].set_yticklabels(w_names, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[0].set_xlabel('Composite Pressure Rating', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[0].set_title('TOP 10 AVAILABLE BOWLERS: COMPOSITE RATING\n(Pathirana, Burger & Coetzee Lead the Market)', fontsize=12, fontweight='bold', color=NAVY)
axes[0].invert_yaxis()
axes[0].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(top10_avail_bowl['composite_rating'].values):
    axes[0].text(v + 1.0, i, f'{v:.1f}', va='center', fontsize=9, fontweight='bold', color=DARK_TEXT)
axes[0].set_xlim(0, max(top10_avail_bowl['composite_rating']) + 12)

# Right: High-Pressure Economy & Wicket Strike Rate
axes[1].barh(y_pos_w, top10_avail_bowl['hp_econ'].values, height=0.6, color=TEAL, edgecolor='#CBD5E1')
axes[1].set_yticks(y_pos_w)
axes[1].set_yticklabels(w_names, fontsize=10, fontweight='bold', color=DARK_TEXT)
axes[1].set_xlabel('High-Pressure Economy Rate (Lower = Better)', fontsize=11, fontweight='bold', color=DARK_TEXT)
axes[1].set_title('HIGH-PRESSURE ECONOMY & WICKET STRIKE RATE (Balls/Wkt)', fontsize=12, fontweight='bold', color=NAVY)
axes[1].invert_yaxis()
axes[1].grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)
for i, v in enumerate(top10_avail_bowl['hp_econ'].values):
    sr = top10_avail_bowl['hp_sr'].values[i]
    wkts = top10_avail_bowl['hp_wkts'].values[i]
    axes[1].text(v + 0.15, i, f'{v:.2f} rpo ({sr:.1f} b/w, {wkts}w)', va='center', fontsize=8.5, fontweight='bold', color=DARK_TEXT)
axes[1].set_xlim(0, max(top10_avail_bowl['hp_econ']) + 2.5)

plt.suptitle('IPL 2027 AUCTION SHORTLIST: TOP 10 AVAILABLE BOWLERS UNDER PRESSURE', fontsize=14, fontweight='bold', color=NAVY, y=1.02)
plt.tight_layout()
p_v2 = os.path.join(CHARTS_DIR, 'post_retention_top10_available_bowlers.png')
plt.savefig(p_v2, facecolor='#FFFFFF')
plt.savefig(os.path.join(RR_CHARTS, 'post_retention_top10_available_bowlers.png'), facecolor='#FFFFFF')
plt.close()
print("Saved post_retention_top10_available_bowlers.png")

# Mirror charts to artifacts
art_dir = r'C:\Users\Asus-2025\.gemini\antigravity\brain\4fe6158e-0e76-450a-898e-f6d09dd602e6'
import shutil
shutil.copy2(p_v1, os.path.join(art_dir, 'deepdive_comparison_charts', 'post_retention_top10_available_batters.png'))
shutil.copy2(p_v2, os.path.join(art_dir, 'deepdive_comparison_charts', 'post_retention_top10_available_bowlers.png'))
print("Mirrored charts to artifacts.")
