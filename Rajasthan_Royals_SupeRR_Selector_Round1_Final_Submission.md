# Rajasthan Royals (RR) SupeRR Selector Season 2: Round 1 Submission
## Shaping RR's IPL 2027 Auction Strategy: Identifying the Most Reliable Players Under Pressure

**Author / Candidate:** Senior Performance & Quantitative Cricket Analyst  
**Target Franchise:** Rajasthan Royals (War Room Strategy Group)  
**Deliverable Type:** Complete Slide-by-Slide Submission Deck & Technical Dossier  
**Competition Round:** Round 1 – High-Pressure Reliability Analysis  

---

## SLIDE 1: Executive Overview & The Rajasthan Royals Strategic Imperative

### 1. The Context Heading into the IPL 2027 Mini-Auction (16 December 2026, Goa)
- **Total Franchise Purse:** ₹157.00 Crore
- **Rajasthan Royals Retained Players ($N=13$):** Yashasvi Jaiswal, Vaibhav Sooryavanshi, Riyan Parag, Dhruv Jurel, Ravindra Jadeja, Jofra Archer, Donovan Ferreira, Lhuan-dre Pretorius, Sushant Mishra, Brijesh Sharma, Yash Raj Punja, Mohammad Shami (trade-in), M. Siddharth (trade-in).
- **Remaining RR Auction Purse:** **₹27.05 Crore** (7th highest in the IPL).
- **Major Off-Season Voids Created:**
  1. **Sanju Samson (Traded to CSK):** Loss of long-time captain and dependable middle-overs spin anchor.
  2. **Shimron Hetmyer (Released):** Vacancy at #6/#7 death finisher.
  3. **Frontline Mystery Spinner:** Finger spin covered by Jadeja and Siddharth, but lacking an elite wrist-spin or mystery-spin containment option.
  4. **Death Bowling Co-Closer:** Jofra Archer requires an elite yorker-execution partner to secure overs 17–20.

### 2. The Core Strategic Objective
To mathematically analyze Rajasthan Royals' proprietary ball-by-ball performance database (**167,872 clean deliveries across 883 matches**), model situational leverage via a continuous cricket-grounded Pressure Index ($PI \in [0, 100]$), and assemble a prioritized **Auction Recruitment Portfolio** that maximizes win-probability under extreme match pressure while strictly respecting RR's **₹27.05 Crore budget constraint**.

---

## SLIDE 2: Data Cleaning, Audit & Boundary Conditions

### 1. Strict Eligibility Filters
To ensure zero wastage of franchise war-room capital, the raw dataset (**200,999 deliveries**) was filtered against four real-world governance boundaries:
- **Exclusion 1: 68 Pakistan-Associated Players Purged:** Filtered via `competition_team_player_mapping.csv` per IPL governing council tournament regulations.
- **Exclusion 2: 18 Confirmed IPL Retirees & Opt-Outs Purged:** Explicitly removed modern-era confirmed retirees (**MS Dhoni**, **Ravichandran Ashwin**, **Matthew Wade**, **Dinesh Karthik**, **Ambati Rayudu**, **Andre Russell**, **Alex Hales**, **David Willey**, **Dwayne Bravo**, **Kieron Pollard**, **Shikhar Dhawan**, **Wriddhiman Saha**) and tournament opt-outs (**Travis Head**, **Mitchell Starc**).
- **Exclusion 3: IPL 2027 Franchise Retentions Filtered:** Ingested the complete 17 November 2026 retention and release declarations across all 10 franchises (e.g. Suryakumar Yadav, Tilak Varma, Heinrich Klaasen, Rashid Khan, Jasprit Bumrah, and Glenn Phillips are retained by their respective teams and cannot be bid upon).
- **Audit Reconciliation:** Correctly decoded categorical `extras1_runs` codes and restricted credited bowler wickets strictly to legitimate dismissals (`Bowled`, `Caught`, `LBW`, `Stump`, `Hit Wicket`), eliminating false run-out attributions.

---

## SLIDE 3: Analytical Methodology — The Continuous Pressure Formulation

### 1. Why Arbitrary Over Slices Fail
Traditional cricket analytics arbitrarily labels overs 16–20 as "pressure." This is fundamentally flawed: the 18th over of a 60-run blowout carries negligible pressure, whereas the 4th over following an $8/3$ collapse carries immense win-probability swing.

### 2. Dual Situational Pressure Algorithm ($PI \in [0, 100]$)
We reconstructed the exact pre-delivery match state across all deliveries:

```
                            CONTINUOUS DUAL PRESSURE FORMULA
                                           │
         ┌─────────────────────────────────┴─────────────────────────────────┐
         ▼                                                                   ▼
BATTING PRESSURE INDEX (PI_Bat)                                     BOWLING PRESSURE INDEX (PI_Bowl)
• 1st Innings: Phase weight (PP=1.0, Mid=2.2,                       • 1st Innings: Phase danger + Current RR
  Death=3.8) + Cumulative wickets lost before ball +                  vs. dynamic tournament par + Opponent wickets.
  Dynamic tournament par score deficit.                             • 2nd Innings: Countdown progression + Required
• 2nd Innings: Required Run Rate acceleration                         run rate tension curve (vs 8.4 RPO) + Death
  (RRR / 8.0) + Wickets lost + Ball countdown.                        bonus + Blowout filter.
```

$$\text{PI}_{\text{Bat, 1st}} = \Big[12.0 \cdot W_{\text{phase}} + 6.5 \cdot \text{Wkts}_{\text{lost}} + 0.8 \cdot (\text{Par}_{\text{ball}} - \text{Score}_{\text{before}})\Big] \in [5, 95]$$

$$\text{PI}_{\text{Bat, 2nd}} = \Big[22.0 \cdot \Big(\frac{\text{RRR}}{8.0}\Big) + 5.5 \cdot \text{Wkts}_{\text{lost}} + 16.0 \cdot \Big(1.0 - \frac{\text{Balls}_{\text{rem}}}{\text{Balls}_{\text{tot}}}\Big)\Big] \in [5, 98]$$

$$\text{PI}_{\text{Bowl, 2nd}} = \Big[18.0 + 22.0 \cdot \Big(1.0 - \frac{\text{Balls}_{\text{rem}}}{\text{Balls}_{\text{tot}}}\Big) + 24.0 \cdot \Big(1.0 - \frac{|\text{Req}_{\text{RPB}} - 1.4|}{1.4}\Big) + 18.0_{\text{Death}} + 2.5 \cdot (\text{Wkts}_{\text{hand}} - 4)\Big]$$

### 3. High-Pressure Cutoff ($\text{PI} \ge 65$) & Bayesian Shrinkage
Deliveries with **$\text{PI} \ge 65$** isolate the critical **19.2% of batting deliveries (32,231 balls)** and **5.4% of bowling deliveries (9,133 balls)**. To eliminate small-sample noise, empirical Bayesian shrinkage anchors each player to global domain priors ($135.0$ SR for batters, $8.50$ Econ for bowlers):

$$\text{SR}_{\text{Shrunk}} = \frac{N_{\text{balls}}}{N_{\text{balls}} + 80} \cdot \text{SR}_{\text{HP}} + \frac{80}{N_{\text{balls}} + 80} \cdot 135.0$$

$$\text{Econ}_{\text{Shrunk}} = \frac{N_{\text{balls}}}{N_{\text{balls}} + 60} \cdot \text{Econ}_{\text{HP}} + \frac{60}{N_{\text{balls}} + 60} \cdot 8.50$$

---

## SLIDE 4: Methodological Validation — Global Benchmark Roster

To prove mathematical validity, the composite rating model was tested against the entire modern player universe:

| Global Rank | Top 10 Batters (Global Baseline) | Composite Rating | IPL 2027 Status | Top 10 Bowlers (Global Baseline) | Composite Rating | IPL 2027 Status |
| :---: | :--- | :---: | :---: | :--- | :---: | :---: |
| **1** | **Namboori Tilak Varma** | 81.54 | Retained (MI) | **Rashid Khan** | 90.48 | Retained (GT) |
| **2** | **Suryakumar Yadav** | 79.27 | Retained (MI) | **Maheesh Theekshana** | 73.81 | **AVAILABLE IN AUCTION** |
| **3** | **Naman Dhir** | 77.93 | Retained (MI) | **Mohsin Khan** | 73.69 | Retained (LSG) |
| **4** | **Marcus Stoinis** | 76.52 | Retained (PBKS) | **Harshal Patel** | 72.77 | Retained (GT Trade) |
| **5** | **Rovman Powell** | 74.77 | Retained (KKR) | **Avesh Khan** | 72.03 | **AVAILABLE IN AUCTION** |
| **6** | **Heinrich Klaasen** | 72.86 | Retained (SRH) | **Arshdeep Singh** | 71.53 | Retained (MI Trade) |
| **7** | **Sherfane Rutherford** | 72.56 | Retained (MI) | **Eshan Malinga** | 70.87 | Retained (SRH) |
| **8** | **Nicholas Pooran** | 72.28 | Retained (LSG) | **Mitchell Santner** | 69.26 | Retained (MI) |
| **9** | **Ayush Badoni** | 72.04 | Retained (LSG) | **Josh Hazlewood** | 68.40 | Retained (RCB) |
| **10** | **Azmatullah Omarzai** | 70.69 | **AVAILABLE IN AUCTION** | **Yuzvendra Chahal** | 65.26 | Retained (PBKS) |

*Conclusion:* The model accurately identifies the elite clutch players of modern T20 cricket. We now isolate the **Available Auction Targets**.

---

## SLIDE 5: Top Picks — Finalized Top 10 Available Batters (IPL 2027 Auction)

Filtering out all retained players yields the **definitive auction batting target board**:

| Rank | Player Name | Pressure Rating | HP Strike Rate | Career Base SR | Clutch Uplift ($\Delta\text{SR}$) | Recent 2Y HP SR (2025–26) | HP Balls Faced | Form Trajectory | Recommended Tactical Role for RR |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Azmatullah Omarzai** | **70.69** | **165.4** | 118.9 | **+46.5** | **178.6** | 295 | **Surging / Peak Form (▲▲)** | **#1 Target:** Seam-bowling #6/#7 engine (Curran trade void) |
| **2** | **Mohammad Nabi** | **67.31** | **158.7** | 114.6 | **+44.1** | **154.2** | 254 | **High-Floor Stable (■)** | **Tactical Matchup:** Spin-counter floater |
| **3** | **Sikandar Raza** | **66.89** | **170.0** | 127.1 | **+42.9** | **177.0** | 203 | **Progressive Growth (▲)** | **Clutch Accelerator:** 170+ HP SR with spin-bowling depth |
| **4** | **M Shahrukh Khan** | **66.66** | **181.8** | 136.9 | **+44.9** | **186.0** | 121 | **Progressive Growth (▲)** | **#1 Domestic Target:** Elite Indian pace-hitter death closer |
| **5** | **Dasun Shanaka** | **63.74** | **152.8** | 127.8 | **+25.0** | **148.1** | 299 | **High-Floor Stable (■)** | **Pace Finisher:** Experienced boundary clearer & seam cover |
| **6** | **Mark Adair** | **63.08** | **142.9** | 77.8 | **+65.1** | **165.9** | 259 | **Surging / Peak Form (▲▲)** | **Lower-Order Hitter:** Late boundary striker & swing |
| **7** | **George Dockrell** | **60.50** | **146.8** | 117.8 | **+29.0** | **141.8** | 269 | **High-Floor Stable (■)** | **Middle Anchor:** Left-hand spin stabilizer |
| **8** | **Daryl Mitchell** | **60.40** | **156.3** | 141.0 | **+15.3** | **189.4** | 245 | **Surging / Peak Form (▲▲)** | **Samson Cover:** Dominant subcontinent spin anchor (#3/#4) |
| **9** | **Nurul Hasan** | **59.56** | **159.2** | 101.3 | **+57.9** | **195.8** | 125 | **Surging / Peak Form (▲▲)** | **WK Reserve & Finisher:** Late-innings chase specialist |
| **10** | **Jaker Ali Anik** | **58.72** | **152.9** | 111.9 | **+41.0** | **123.9** | 187 | **Cooling Down (▼)** | **Depth Finisher:** Middle/death boundary striker |

---

## SLIDE 6: Top Picks — Finalized Top 10 Available Bowlers (IPL 2027 Auction)

Filtering out all retained players yields the **definitive auction bowling target board**:

| Rank | Player Name | Pressure Rating | High-Pressure Economy | Career Base Econ | Clutch $\Delta\text{Econ}$ | Recent 2Y HP Econ (2025–26) | HP Wicket SR | HP Wickets | Recommended Tactical Role for RR |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Maheesh Theekshana** | **73.81** | **7.29** | 7.67 | **-0.38** | **6.78** | 28.0 | 3 | **#1 Frontline Target:** Chokes runs under pressure; PP & Death spin |
| **2** | **Avesh Khan** | **72.03** | **9.68** | 9.48 | **+0.20** | **10.46** | **15.9** | **12** | **#1 Domestic Seamer:** Hard-length death bowler alongside Shami |
| **3** | **Wanindu Hasaranga** | **65.07** | **8.96** | 8.01 | +0.95 | **8.61** | **16.2** (7.7 in 2Y) | 5 | **Attacking Wrist Spin:** Middle-overs strike weapon (Chahal void) |
| **4** | **Ravi Bishnoi** | **64.05** | **9.69** | 8.32 | +1.37 | 12.50 | **13.0** | 9 | **Googly Specialist:** Wicket-taking threat on true tracks |
| **5** | **Matheesha Pathirana** | **61.88** | 10.14 | 8.22 | +1.92 | 16.55 | **11.3** | **14** | **Death Co-Closer:** Lethal sling yorkers paired with Jofra Archer |
| **6** | **Mustafizur Rahman** | **61.03** | **9.56** | 7.60 | +1.96 | **6.83** | **14.8** | 8 | **Cutter Specialist:** Re-engineered dip; Sawai Mansingh Stadium asset |
| **7** | **Dushmantha Chameera** | **58.80** | 10.05 | 8.74 | +1.31 | **10.59** | **12.3** | 6 | **Express Shock Bowler:** 145+ km/h middle-overs enforcer |
| **8** | **Alzarri Joseph** | **57.61** | 10.21 | 9.80 | +0.41 | 12.82 | **19.2** (7.3 in 2Y) | 4 | **Hit-the-Deck Seamer:** Heavy length execution |
| **9** | **Tushar Deshpande** | **54.17** | 11.14 | 9.70 | +1.44 | 11.66 | **10.9** | 9 | **Domestic Seamer:** Early swing bowler (viable buy-back) |
| **10** | **Richard Ngarava** | **47.28** | 10.14 | 8.48 | +2.51 | **10.62** | **21.8** | 4 | **Budget Left-Arm:** Low-cost tactical pace reserve |

---

## SLIDE 7: Two-Year Recency & Form Trajectory Deep-Dive (2025–2026 vs. 2022–2024)

### 1. The Peaking Assets (Bidding Priority)
- **Azmatullah Omarzai:** High-pressure strike rate surged by **+43.8 points** (from 134.8 to **178.6 HP SR** across 206 balls in 2025–2026). At 26 years old, he is entering his international peak.
- **Daryl Mitchell:** Recorded a massive **+50.7 point strike rate expansion** (from 138.8 to **189.4 HP SR** in 2025–2026), proving his evolution into an elite multi-phase power hitter.
- **Maheesh Theekshana:** Economy improved from 7.48 to a stifling **6.78 HP Economy (-0.69 RPO)** over the last 2 years. He is the most economical pressure spinner in world cricket.
- **Mustafizur Rahman:** Cutters and slower-ball variations underwent a dramatic resurgence, improving his HP economy by **-3.62 RPO** (from 10.45 down to **6.83 HP Econ**).

### 2. Tactical Traps & Risk Mitigations
- **Matheesha Pathirana:** Experienced economy inflation in 2025–2026 (16.55 across 29 balls) due to premeditated ramp shots. *Mitigation:* Deploy him with specialized third-man sweepers and pair him with Jofra Archer's length containment.
- **Jaker Ali Anik:** Experienced a drop from 181.1 to 123.9 HP SR in 2025–2026. *Mitigation:* Do not enter bidding wars; pivot domestic finishing capital to **M Shahrukh Khan**.

---

## SLIDE 8: How Each Player Strengthens the Rajasthan Royals Squad

```
┌──────────────────────────────────────┬───────────────────────────────┬────────────────────────────────────────────────────────┐
│ Tactical Problem / Off-Season Void   │ Primary Solution Player       │ Why This Player Strengthens RR                         │
├──────────────────────────────────────┼───────────────────────────────┼────────────────────────────────────────────────────────┤
│ 1. Death Finisher Vacancy            │ **M Shahrukh Khan**           │ • Direct domestic upgrade over Hetmyer                 │
│    (Shimron Hetmyer Released)        │ (Rating: 66.66 | 181.8 HP SR) │ • 186.0 HP SR in 2025–2026; domestic boundary hitter   │
├──────────────────────────────────────┼───────────────────────────────┼────────────────────────────────────────────────────────┤
│ 2. Middle-Overs Anchor Loss          │ **Daryl Mitchell**            │ • Spin dominator in subcontinent conditions            │
│    (Sanju Samson Traded to CSK)      │ (Rating: 60.40 | 189.4 HP SR) │ • Insulates Jaiswal & Parag; prevents batting collapses│
├──────────────────────────────────────┼───────────────────────────────┼────────────────────────────────────────────────────────┤
│ 3. Seam-Bowling All-Rounder Gap      │ **Azmatullah Omarzai**        │ • #1 Ranked Available Batter (70.69 Rating)            │
│    (Sam Curran Traded to LSG)        │ (Rating: 70.69 | 178.6 HP SR) │ • +46.5 clutch uplift; bowls 2–4 hard seam overs       │
├──────────────────────────────────────┼───────────────────────────────┼────────────────────────────────────────────────────────┤
│ 4. Frontline Mystery Spin Void       │ **Maheesh Theekshana**        │ • #1 Ranked Available Bowler (73.81 Rating)            │
│    (Chahal Released to PBKS)         │ (Rating: 73.81 | 6.78 HP Econ)│ • Sub-7.50 economy anywhere; bowls PP (1–6) & Death    │
├──────────────────────────────────────┼───────────────────────────────┼────────────────────────────────────────────────────────┤
│ 5. Death Yorker Partner for Archer   │ **Matheesha Pathirana**       │ • Extreme strike capability (11.3 balls/wkt)           │
│    (Innings 17–20 Closer)            │ (Rating: 61.88 | 14 HP Wkts)  │ • Lethal sling yorkers dismantle stumps in tight chases│
└──────────────────────────────────────┴───────────────────────────────┴────────────────────────────────────────────────────────┘
```

---

## SLIDE 9: Rajasthan Royals War Room Budget & Auction Allocation Plan

Allocating Rajasthan Royals' **₹27.05 Crore remaining purse** across a prioritized 10-player acquisition board:

```
┌────┬─────────────────────────┬───────────────┬─────────────────┬───────────────────┬──────────────────────────────────────────┐
│ No │ Player Name             │ Tactical Role │ Est. Bid Price  │ Walk-Away Ceiling │ Strategic Justification for RR           │
├────┼─────────────────────────┼───────────────┼─────────────────┼───────────────────┼──────────────────────────────────────────┤
│ 1  │ **Maheesh Theekshana**  │ Mystery Spin  │ ₹6.00 Cr        │ ₹7.50 Cr          │ #1 HP Bowler; sub-7.50 economy anywhere  │
│ 2  │ **Matheesha Pathirana** │ Death Closer  │ ₹7.00 Cr        │ ₹8.50 Cr          │ 11.3 HP Wkt SR; sling yorker co-closer   │
│ 3  │ **M Shahrukh Khan**     │ Indian Finisher│ ₹4.50 Cr       │ ₹5.50 Cr          │ 181.8 HP Strike Rate; pace hitter        │
│ 4  │ **Azmatullah Omarzai**  │ Seam All-Round│ ₹4.00 Cr        │ ₹5.00 Cr          │ #1 HP Batter (+46.5 uplift) + seam overs │
│ 5  │ **Daryl Mitchell**      │ Middle Anchor │ ₹2.50 Cr        │ ₹3.50 Cr          │ Spin dominator (Samson departure cover)  │
│ 6  │ **Avesh Khan**          │ Indian Seamer │ ₹1.50 Cr        │ ₹2.50 Cr          │ Hard-length death overs reserve          │
│ 7  │ **Wanindu Hasaranga**   │ Wrist Spin    │ ₹1.00 Cr        │ ₹2.00 Cr          │ Middle-phase wicket taker (Chahal void)  │
│ 8  │ **Nurul Hasan**         │ WK / Finisher │ ₹0.30 Cr        │ ₹0.60 Cr          │ 159.2 HP SR (+57.9 uplift); backup WK    │
│ 9  │ **Sikandar Raza**       │ Spin Floater  │ ₹0.15 Cr        │ ₹0.50 Cr          │ 170.0 HP Strike Rate; veteran value pick │
│ 10 │ **Richard Ngarava**     │ Left-Arm Seam │ ₹0.10 Cr        │ ₹0.30 Cr          │ Low-cost overseas seam backup            │
├────┴─────────────────────────┴───────────────┴─────────────────┴───────────────────┴──────────────────────────────────────────┤
│ TOTAL ESTIMATED COMMITMENT:                  │ ₹27.05 Cr       │                   │ 100% UTILIZATION OF REMAINING PURSE      │
└──────────────────────────────────────────────┴─────────────────┴───────────────────┴──────────────────────────────────────────┘
```

---

## SLIDE 10: Projected High-Pressure Match-Day Starting XI & Rotation

With these acquisitions, Rajasthan Royals field an elite, pressure-proof starting lineup:

```
╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║                      RAJASTHAN ROYALS PROJECTED HIGH-PRESSURE MATCH XI                        ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝
 1. Yashasvi Jaiswal (LHB)        ──> Explosive PP Aggressor (268.8 HP SR | Retained RR)
 2. Vaibhav Sooryavanshi (LHB)    ──> Dynamic Emerging Opener (Retained RR)
 3. Daryl Mitchell (RHB) ✈        ──> Anchor & Spin Counter (156.3 HP SR | AUCTION TARGET)
 4. Riyan Parag (RHB)             ──> Middle Enforcer & Spin Depth (166.4 HP SR | Retained RR)
 5. Dhruv Jurel (RHB / WK)        ──> Primary Finisher & Wicketkeeper (166.7 HP SR | Retained RR)
 6. M Shahrukh Khan (RHB)         ──> Indian Death Power Hitter (181.8 HP SR | AUCTION TARGET)
 7. Azmatullah Omarzai (RHB / RAM)✈──> Seam All-Rounder Engine (165.4 HP SR | AUCTION TARGET)
 8. Ravindra Jadeja (LHB / SLA)   ──> Finger Spin Controller (Retained RR)
 9. Maheesh Theekshana (OB) ✈     ──> Mystery Containment (7.29 HP Econ | AUCTION TARGET)
 10. Jofra Archer (RAF) ✈         ──> Express Pace Spearhead (Retained RR)
 11. Mohammad Shami (RAF)         ──> Powerplay Seam Spearhead (Trade-in RR)
 ───────────────────────────────────────────────────────────────────────────────────────────────
 IMPACT SUB / CLOSER:
 12. Matheesha Pathirana (RAF) ✈  ──> Sling Death Closer (11.3 HP Wkt SR | AUCTION TARGET)
     (Rotates with Daryl Mitchell / Azmatullah Omarzai based on 1st vs. 2nd innings conditions)
 ───────────────────────────────────────────────────────────────────────────────────────────────
```

---

## SLIDE 11: Artifact & Verification Index

All quantitative models, registries, and visuals are fully reproducible and available locally:

- **Auction Target Top 10 Visual:** [`scratch_deepdive_top10_auction_pool.png`](file:///c:/Users/Asus-2025/Downloads/RR/final_pressure_charts_white_bg/scratch_deepdive_top10_auction_pool.png)
- **Recent 2-Year Deep-Dive Visual:** [`recent_2y_pressure_deepdive.png`](file:///c:/Users/Asus-2025/Downloads/RR/final_pressure_charts_white_bg/recent_2y_pressure_deepdive.png)
- **Pressure Component Breakdown Visual:** [`pressure_deepdive_component_breakdown.png`](file:///c:/Users/Asus-2025/Downloads/RR/final_pressure_charts_white_bg/pressure_deepdive_component_breakdown.png)
- **Global Benchmark Top 10 Visual:** [`scratch_deepdive_top10_global.png`](file:///c:/Users/Asus-2025/Downloads/RR/final_pressure_charts_white_bg/scratch_deepdive_top10_global.png)
- **Available Batters CSV Register:** [`scratch_top10_available_batters_auction.csv`](file:///c:/Users/Asus-2025/Downloads/RR/Fresh_Analysis/scratch_top10_available_batters_auction.csv)
- **Available Bowlers CSV Register:** [`scratch_top10_available_bowlers_auction.csv`](file:///c:/Users/Asus-2025/Downloads/RR/Fresh_Analysis/scratch_top10_available_bowlers_auction.csv)
- **Batters 2-Year Performance CSV:** [`top10_batters_recent_2y_performance.csv`](file:///c:/Users/Asus-2025/Downloads/RR/Fresh_Analysis/top10_batters_recent_2y_performance.csv)
- **Bowlers 2-Year Performance CSV:** [`top10_bowlers_recent_2y_performance.csv`](file:///c:/Users/Asus-2025/Downloads/RR/Fresh_Analysis/top10_bowlers_recent_2y_performance.csv)
- **Master Jupyter Notebook Pipeline:** [`RR_SupeRR_Selector_Complete_Cricket_EDA_and_Pressure_Analysis.ipynb`](file:///c:/Users/Asus-2025/Downloads/RR/RR_SupeRR_Selector_Complete_Cricket_EDA_and_Pressure_Analysis.ipynb)
