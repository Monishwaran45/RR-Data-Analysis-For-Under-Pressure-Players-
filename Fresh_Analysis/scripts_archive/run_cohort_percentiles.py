import pandas as pd
df_bat = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\eda_all_eligible_batters_complete.csv')
df_bowl = pd.read_csv(r'c:\Users\Asus-2025\Downloads\RR\eda_all_eligible_bowlers_complete.csv')

bat_names = ['Tim David', 'Shashank Singh', 'Rinku Singh', 'Rishabh Pant', 'Tristan Stubbs', 'Namboori Tilak Varma', 'Marcus Stoinis', 'Suryakumar Yadav', 'Rovman Powell', 'Dasun Shanaka']
bowl_names = ['Jasprit Bumrah', 'Matheesha Pathirana', 'Wanindu Hasaranga', 'Yuzvendra Chahal', 'Kuldeep Yadav', 'Sam Curran', 'Sunil Narine', 'Rashid Khan', 'Arshdeep Singh', 'Taskin Ahmed']

print('=== TOP 10 BATTERS COHORT BENCHMARKS ===')
for name in bat_names:
    row = df_bat[df_bat['player_name'].str.contains(name.split()[-1], case=False, na=False)]
    if len(row) > 0:
        r = row.iloc[0]
        sr_pct = (df_bat['hp_strike_rate'] < r['hp_strike_rate']).mean() * 100
        bdry_pct = (df_bat['hp_boundary_pct'] < r['hp_boundary_pct']).mean() * 100
        dot_pct = (df_bat['hp_dot_pct'] > r['hp_dot_pct']).mean() * 100
        pname = r['player_name']
        sr = r['hp_strike_rate']
        avg = r['hp_avg']
        delta_sr = r['delta_strike_rate']
        balls = int(r['hp_balls'])
        bdry = r['hp_boundary_pct']
        dot = r['hp_dot_pct']
        print(f'{pname:<22}: HP SR={sr:>5.1f} ({sr_pct:>4.1f}%tile) | HP Avg={avg:>4.1f} | Delta SR={delta_sr:>+5.1f} | HP Balls={balls:>3} | Bdry%={bdry:>4.1f}% ({bdry_pct:>4.1f}%tile) | Dot%={dot:>4.1f}% ({dot_pct:>4.1f}%tile)')

print('\n=== TOP 10 BOWLERS COHORT BENCHMARKS ===')
for name in bowl_names:
    row = df_bowl[df_bowl['player_name'].str.contains(name.split()[-1], case=False, na=False)]
    if len(row) > 0:
        r = row.iloc[0]
        econ_pct = (df_bowl['hp_econ'] > r['hp_econ']).mean() * 100
        sr_pct = (df_bowl['hp_sr'] > r['hp_sr']).mean() * 100
        dot_pct = (df_bowl['hp_dot_pct'] < r['hp_dot_pct']).mean() * 100
        pname = r['player_name']
        ec = r['hp_econ']
        wkt_sr = r['hp_sr']
        balls = int(r['hp_balls'])
        dot = r['hp_dot_pct']
        bdry = r['hp_bdry_conceded_pct']
        print(f'{pname:<22}: HP Econ={ec:>5.2f} ({econ_pct:>4.1f}%tile) | Wkt SR={wkt_sr:>4.1f} ({sr_pct:>4.1f}%tile) | HP Balls={balls:>3} | Dot%={dot:>4.1f}% ({dot_pct:>4.1f}%tile) | Bdry Conc%={bdry:>4.1f}%')
