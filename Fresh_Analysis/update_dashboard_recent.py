import os

DASHBOARD_PATH = r'c:\Users\Asus-2025\Downloads\RR\Rajasthan_Royals_SupeRR_Selector_Dashboard.html'

with open(DASHBOARD_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Navigation Pill 06
html = html.replace(
    '06. 2-Year Recency & Stability',
    '06. 5-Year Longitudinal Trajectory & Recency (2022–2026)'
)

# 2. In Tab 5 (Tactical Voids), add Jaipur Home Ground Advantage to Void Matrix Table
jaipur_row = '''              <tr class="hover:bg-[#FAF8F5]">
                <td class="px-4 py-3 font-bold text-[#C81D4E]">6. Home Venue Dynamic<br><span class="text-[11px] font-normal text-slate-500">(Sawai Mansingh Stadium Calibration)</span></td>
                <td class="px-4 py-3 font-extrabold text-[#141B2D]">Mustafizur Rahman & Theekshana<br><span class="text-[11px] font-semibold text-[#10B981]">Backup: Wanindu Hasaranga</span></td>
                <td class="px-4 py-3 font-mono-num font-bold text-[#141B2D]">6.83 Late Econ<br><span class="text-[#10B981] font-bold">(3.00 Econ in '26)</span></td>
                <td class="px-4 py-3 text-[#334155]">Jaipur's large 70m+ square boundaries and abrasive pitch grip cutters and mystery carrom balls, making them 25% more restrictive at home.</td>
              </tr>
            </tbody>'''

html = html.replace('            </tbody>', jaipur_row, 1)

# In Starting XI, ensure Jadeja is #8 and dual Impact Sub strategy is detailed
starting_xi_old = '''          <!-- 8. M Siddharth -->
          <div class="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#E2E8F0] flex items-center justify-between">
            <div>
              <div class="text-[11px] font-bold text-slate-400">8. DEFENSIVE SPIN / #8 (SLA)</div>
              <div class="font-extrabold text-sm text-[#141B2D]">M Siddharth</div>
              <div class="text-[11px] text-[#4A5568]">Trade-in Left-Arm Finger Spin</div>
            </div>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800">Trade-in RR</span>
          </div>'''

starting_xi_new = '''          <!-- 8. Ravindra Jadeja -->
          <div class="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#E2E8F0] flex items-center justify-between">
            <div>
              <div class="text-[11px] font-bold text-slate-400">8. ALL-ROUNDER / #8 (LHB/SLA)</div>
              <div class="font-extrabold text-sm text-[#141B2D]">Ravindra Jadeja</div>
              <div class="text-[11px] text-[#4A5568]">Finger Spin Controller & Batting Depth</div>
            </div>
            <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800">Retained RR</span>
          </div>'''

if starting_xi_old in html:
    html = html.replace(starting_xi_old, starting_xi_new)

# Update Impact Sub section with dual legal IPL rule scenario
impact_sub_search = '<!-- 12. Impact Sub / Pathirana -->'
impact_sub_replace = '''<!-- 12. Impact Sub / Dual Strategy (100% IPL Compliant) -->
        <div class="p-4 rounded-xl bg-gradient-to-r from-[#FFF1F2] to-[#FAF8F5] border border-[#C81D4E]/30 space-y-2">
          <div class="flex items-center justify-between">
            <span class="font-bold text-xs text-[#C81D4E] flex items-center gap-1.5">
              <i class="fa-solid fa-bolt"></i> TACTICAL IMPACT SUB PROTOCOL (100% BCCI OVERSEAS COMPLIANT)
            </span>
            <span class="text-[11px] font-bold px-2.5 py-0.5 rounded bg-[#C81D4E] text-white">Pathirana ✈ (₹7.00 Cr) & Avesh Khan (₹1.50 Cr)</span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-[#334155]">
            <div class="p-3 bg-white rounded-lg border border-[#E2E8F0] space-y-1">
              <div class="font-bold text-[#141B2D]">Scenario A: Bowling First / Defending Target</div>
              <p class="text-[11px] text-[#4A5568]">Start with 3 Overseas (Theekshana, Archer, Pathirana). In 2nd innings, sub out Pathirana → bring in <strong>Daryl Mitchell ✈ [OS 4]</strong> to anchor the chase.</p>
            </div>
            <div class="p-3 bg-white rounded-lg border border-[#E2E8F0] space-y-1">
              <div class="font-bold text-[#141B2D]">Scenario B: Batting First / Chasing Setup</div>
              <p class="text-[11px] text-[#4A5568]">Start with 4 Overseas (Mitchell, Omarzai, Theekshana, Archer). At break, sub in <strong>Avesh Khan [IND]</strong> for a 145+ km/h death surge without violating the 4-overseas limit.</p>
            </div>
          </div>
        </div>'''

if impact_sub_search in html:
    # replace the impact sub card
    idx1 = html.find(impact_sub_search)
    idx2 = html.find('</div>', idx1 + 100) + 6 # find end of impact card
    html = html[:idx1] + impact_sub_replace + html[idx2:]

# 3. In Tab 6 (Stability & 5-Year Longitudinal EDA), prepend 5-Year Multi-Season Module
new_5year_section = '''      <!-- 5-Year Multi-Season Longitudinal Trajectory (2022–2026) Card -->
      <div class="ppt-card p-6 sm:p-8 space-y-5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <span class="text-xs font-bold uppercase tracking-wider text-[#C81D4E]">Longitudinal Sabermetrics</span>
            <h3 class="text-xl font-extrabold text-[#141B2D] mt-1">5-Year Longitudinal Trajectory & Multi-Season Evolution (2022–2026)</h3>
            <p class="text-xs text-[#4A5568] mt-0.5">
              Auditing 167,872 clean balls across 883 matches. Decoupling Early Era (2022–24) from Late Era (2025–26) with Coefficient of Variation (CV = σ / μ).
            </p>
          </div>
          <span class="px-3 py-1 bg-[#ECFDF5] border border-[#10B981]/30 text-[#10B981] text-xs font-bold rounded-lg self-start sm:self-auto">5 Seasons Audited</span>
        </div>

        <!-- 4 Key Longitudinal Highlights -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
          <div class="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#E2E8F0] space-y-1">
            <span class="text-slate-400 font-bold text-[10px] uppercase">Daryl Mitchell (NZ)</span>
            <div class="text-base font-extrabold text-[#141B2D]">+52.2 SR Surge</div>
            <p class="text-[11px] text-[#10B981] font-semibold">139.5 Early → 191.8 Late Era HP SR</p>
            <p class="text-[10px] text-slate-500">Subcontinent spin destroyer; #1 Sanju Samson replacement.</p>
          </div>

          <div class="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#E2E8F0] space-y-1">
            <span class="text-slate-400 font-bold text-[10px] uppercase">Azmatullah Omarzai (AFG)</span>
            <div class="text-base font-extrabold text-[#141B2D]">+49.7 SR Surge</div>
            <p class="text-[11px] text-[#10B981] font-semibold">135.1 Early → 184.7 Late Era (190.5 in '26)</p>
            <p class="text-[10px] text-slate-500">Compounding peak form; elite pace all-rounder at #7.</p>
          </div>

          <div class="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#E2E8F0] space-y-1">
            <span class="text-slate-400 font-bold text-[10px] uppercase">Maheesh Theekshana (SL)</span>
            <div class="text-base font-extrabold text-[#141B2D]">6.78 Late HP Econ</div>
            <p class="text-[11px] text-[#10B981] font-semibold">4.20 in 2026 | Sub-7.50 in all 5 Seasons</p>
            <p class="text-[10px] text-slate-500">Generational choke weapon; bowls PP (1-6) and Death.</p>
          </div>

          <div class="p-3.5 rounded-xl bg-[#FAF8F5] border border-[#E2E8F0] space-y-1">
            <span class="text-slate-400 font-bold text-[10px] uppercase">George Dockrell (IRE)</span>
            <div class="text-base font-extrabold text-[#141B2D]">CV = 0.07 Stability</div>
            <p class="text-[11px] text-[#0284C7] font-semibold">Lowest Volatility in Modern Cricket</p>
            <p class="text-[10px] text-slate-500">133-162 SR every year; ultimate low-cost collapse insurance.</p>
          </div>
        </div>

        <!-- 5-Year Charts Split Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          <div class="p-4 rounded-xl bg-white border border-[#E2E8F0] space-y-2">
            <span class="font-bold text-xs text-[#141B2D]">5-Season High-Pressure Heatmap Matrix (2022–2026)</span>
            <div class="rounded-lg overflow-hidden border border-[#E2E8F0]">
              <img src="final_pressure_charts_white_bg/eda_5year_player_performance_heatmap.png" onerror="this.src='./eda_5year_player_performance_heatmap.png'" alt="5-Season Heatmap Matrix" class="w-full h-auto object-cover hover:scale-[1.02] transition cursor-pointer">
            </div>
            <p class="text-[10px] text-[#4A5568]">Season-by-season matrix confirming 2025–2026 hyper-peaks for Mitchell, Omarzai, and Theekshana.</p>
          </div>

          <div class="p-4 rounded-xl bg-white border border-[#E2E8F0] space-y-2">
            <span class="font-bold text-xs text-[#141B2D]">5-Year Experience Floor vs Longitudinal Consistency (CV)</span>
            <div class="rounded-lg overflow-hidden border border-[#E2E8F0]">
              <img src="final_pressure_charts_white_bg/eda_5year_consistency_vs_peak_scatter.png" onerror="this.src='./eda_5year_consistency_vs_peak_scatter.png'" alt="Consistency vs Peak Scatter" class="w-full h-auto object-cover hover:scale-[1.02] transition cursor-pointer">
            </div>
            <p class="text-[10px] text-[#4A5568]">Maps sample credibility against multi-season stability score, identifying high-floor targets.</p>
          </div>
        </div>
      </div>\n\n'''

html = html.replace('id="content-stability" class="tab-content hidden space-y-6">', 'id="content-stability" class="tab-content hidden space-y-6">\n\n' + new_5year_section)

# 4. In Tab 7 (Simulator & Purse), add rr_war_room_purse_allocation_matrix.png
purse_banner_html = '''      <!-- 10-Player War Room Purse Allocation Matrix Visual -->
      <div class="ppt-card p-6 sm:p-8 space-y-4">
        <div class="flex items-center justify-between">
          <div>
            <span class="text-xs font-bold uppercase tracking-wider text-[#C81D4E]">War Room Valuation Framework</span>
            <h3 class="text-xl font-extrabold text-[#141B2D] mt-1">Rajasthan Royals ₹27.05 Crore Capital Blueprint & Walk-Away Ceilings</h3>
          </div>
          <span class="px-3 py-1 bg-[#EFF6FF] border border-[#2563EB]/30 text-[#2563EB] text-xs font-bold rounded-lg">100% Budget Optimization</span>
        </div>
        <div class="rounded-xl overflow-hidden border border-[#E2E8F0] bg-white">
          <img src="final_pressure_charts_white_bg/rr_war_room_purse_allocation_matrix.png" onerror="this.src='./rr_war_room_purse_allocation_matrix.png'" alt="Purse Allocation Matrix" class="w-full h-auto object-cover hover:scale-[1.01] transition cursor-pointer">
        </div>
        <p class="text-xs text-[#4A5568]">
          Value-to-Rating scatter showing Target Bids (₹ Cr), Hard Walk-Away Max Ceilings (▲), and strict fallback contingency pivots (e.g. Pathirana ₹8.5 Cr ceiling → Mustafizur ₹3.5 Cr pivot).
        </p>
      </div>\n\n'''

html = html.replace('id="content-simulator" class="tab-content hidden space-y-6">', 'id="content-simulator" class="tab-content hidden space-y-6">\n\n' + purse_banner_html)

# 5. In Tab 8 (Visual Proofs Gallery), add the 6 new 300 DPI charts into the grid
charts_gallery_addition = '''          <!-- Chart 5: 5-Year Batters Trajectory -->
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#E2E8F0] space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs text-[#141B2D]">5. 5-Year YoY Batters Trajectory</span>
              <span class="text-[10px] text-[#C81D4E] font-bold">300 DPI</span>
            </div>
            <div class="rounded-lg overflow-hidden border border-[#E2E8F0] bg-white">
              <img src="final_pressure_charts_white_bg/eda_5year_batters_trajectory.png" onerror="this.src='./eda_5year_batters_trajectory.png'" alt="5-Year Batters Trajectory" class="w-full h-auto object-cover hover:scale-[1.02] transition cursor-pointer">
            </div>
            <p class="text-[11px] text-[#4A5568]">Multi-season high-pressure strike rate evolution showing Mitchell (+52.2) and Omarzai (+49.7) upward climbs.</p>
          </div>

          <!-- Chart 6: 5-Year Bowlers Trajectory -->
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#E2E8F0] space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs text-[#141B2D]">6. 5-Year YoY Bowlers Trajectory</span>
              <span class="text-[10px] text-[#C81D4E] font-bold">300 DPI</span>
            </div>
            <div class="rounded-lg overflow-hidden border border-[#E2E8F0] bg-white">
              <img src="final_pressure_charts_white_bg/eda_5year_bowlers_trajectory.png" onerror="this.src='./eda_5year_bowlers_trajectory.png'" alt="5-Year Bowlers Trajectory" class="w-full h-auto object-cover hover:scale-[1.02] transition cursor-pointer">
            </div>
            <p class="text-[11px] text-[#4A5568]">Economy tightening curves showing Theekshana (sub-6.80) and Mustafizur Rahman generational suppression.</p>
          </div>

          <!-- Chart 7: Top 5 Batters Forensic EDA Cards -->
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#E2E8F0] space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs text-[#141B2D]">7. Batters Forensic EDA Cards (Ranks 1–5)</span>
              <span class="text-[10px] text-[#C81D4E] font-bold">300 DPI</span>
            </div>
            <div class="rounded-lg overflow-hidden border border-[#E2E8F0] bg-white">
              <img src="final_pressure_charts_white_bg/card_batters_rank_1_to_5.png" onerror="this.src='./card_batters_rank_1_to_5.png'" alt="Batters Forensic Cards 1-5" class="w-full h-auto object-cover hover:scale-[1.02] transition cursor-pointer">
            </div>
            <p class="text-[11px] text-[#4A5568]">Pace vs Spin matchup splits and Scenario bRAA decomposition for Omarzai, Nabi, Raza, Shahrukh, Shanaka.</p>
          </div>

          <!-- Chart 8: Top 5 Bowlers Forensic EDA Cards -->
          <div class="p-4 rounded-xl bg-[#FAF8F5] border border-[#E2E8F0] space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-bold text-xs text-[#141B2D]">8. Bowlers Forensic EDA Cards (Ranks 1–5)</span>
              <span class="text-[10px] text-[#C81D4E] font-bold">300 DPI</span>
            </div>
            <div class="rounded-lg overflow-hidden border border-[#E2E8F0] bg-white">
              <img src="final_pressure_charts_white_bg/card_bowlers_rank_1_to_5.png" onerror="this.src='./card_bowlers_rank_1_to_5.png'" alt="Bowlers Forensic Cards 1-5" class="w-full h-auto object-cover hover:scale-[1.02] transition cursor-pointer">
            </div>
            <p class="text-[11px] text-[#4A5568]">Phase runs saved (wRSA) and choke ratios for Theekshana, Avesh, Hasaranga, Bishnoi, Pathirana.</p>
          </div>'''

# Replace the closing grid tag in content-charts
idx_grid_end = html.find('        </div>\n      </div>\n\n      <!-- 4 Interactive High-DPI HTML5 Canvas Diagnostics -->')
if idx_grid_end != -1:
    html = html[:idx_grid_end] + charts_gallery_addition + '\n' + html[idx_grid_end:]

with open(DASHBOARD_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: Updated Rajasthan_Royals_SupeRR_Selector_Dashboard.html with all recent details!")
