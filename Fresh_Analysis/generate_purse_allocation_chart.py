import os
os.environ['MPLCONFIGDIR'] = r'c:\Users\Asus-2025\Downloads\RR\Fresh_Analysis\mpl_cache'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_FILE = r'c:\Users\Asus-2025\Downloads\RR\final_pressure_charts_white_bg\rr_war_room_purse_allocation_matrix.png'

# 10 Audited Auction Targets
targets = [
    {'name': 'Matheesha Pathirana', 'role': 'Death Closer', 'type': 'Bowler', 'os': True, 'rating': 61.88, 'bid': 7.00, 'ceiling': 8.50, 'color': '#1E3A8A'},
    {'name': 'Maheesh Theekshana', 'role': 'Lead Mystery Spin', 'type': 'Bowler', 'os': True, 'rating': 73.81, 'bid': 6.00, 'ceiling': 7.50, 'color': '#0D9488'},
    {'name': 'M Shahrukh Khan', 'role': 'Indian Finisher', 'type': 'Batter', 'os': False, 'rating': 66.66, 'bid': 4.50, 'ceiling': 5.50, 'color': '#DC2626'},
    {'name': 'Azmatullah Omarzai', 'role': 'Pace All-Rounder', 'type': 'All-Rounder', 'os': True, 'rating': 70.69, 'bid': 4.00, 'ceiling': 5.00, 'color': '#D97706'},
    {'name': 'Daryl Mitchell', 'role': 'Middle Anchor', 'type': 'Batter', 'os': True, 'rating': 60.40, 'bid': 2.50, 'ceiling': 3.50, 'color': '#2563EB'},
    {'name': 'Avesh Khan', 'role': 'Indian Death Seam', 'type': 'Bowler', 'os': False, 'rating': 72.03, 'bid': 1.50, 'ceiling': 2.20, 'color': '#0284C7'},
    {'name': 'Wanindu Hasaranga', 'role': 'Wrist Spin Cover', 'type': 'Bowler', 'os': True, 'rating': 65.07, 'bid': 1.00, 'ceiling': 2.00, 'color': '#059669'},
    {'name': 'Nurul Hasan', 'role': 'Backup WK Finisher', 'type': 'Batter', 'os': True, 'rating': 59.56, 'bid': 0.30, 'ceiling': 0.60, 'color': '#7C3AED'},
    {'name': 'Sikandar Raza', 'role': 'Depth Spin All-Round', 'type': 'All-Rounder', 'os': True, 'rating': 66.89, 'bid': 0.15, 'ceiling': 0.50, 'color': '#EA580C'},
    {'name': 'Richard Ngarava', 'role': 'Left-Arm Angle Seam', 'type': 'Bowler', 'os': True, 'rating': 47.28, 'bid': 0.10, 'ceiling': 0.30, 'color': '#475569'},
]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7.5), gridspec_kw={'width_ratios': [1.15, 0.85]}, facecolor='#FFFFFF')

# ─────────────────────────────────────────────────────────────────────────────
# SUBPLOT 1: VALUE-TO-RATING SCATTER WITH PRICE ELASTICITY CEILINGS
# ─────────────────────────────────────────────────────────────────────────────
ax1.set_facecolor('#FFFFFF')

# Valuation Tiers shading
ax1.axhspan(3.8, 8.8, color='#EFF6FF', alpha=0.6, label='Tier 1: Core Foundation Buys (₹4.0 - ₹8.5 Cr)')
ax1.axhspan(0.8, 3.8, color='#F0FDF4', alpha=0.6, label='Tier 2: Tactical Value Steals (₹1.0 - ₹3.5 Cr)')
ax1.axhspan(0.0, 0.8, color='#FEF3C7', alpha=0.6, label='Tier 3: Asymmetric Bargains (< ₹1.0 Cr)')

for p in targets:
    x = p['rating']
    y = p['bid']
    ceil = p['ceiling']
    
    # Ceiling vertical line
    ax1.plot([x, x], [y, ceil], color='#94A3B8', linestyle='--', linewidth=1.5, zorder=2)
    ax1.scatter(x, ceil, color='#DC2626', marker='^', s=45, zorder=3)
    
    # Target bid bubble
    size = 180 + y * 40
    ax1.scatter(x, y, s=size, color=p['color'], edgecolor='#0F172A', linewidth=1.5, zorder=4)
    
    # Labels
    label_text = f"{p['name']} ({'[OS]' if p['os'] else '[IND]'})\n₹{y:.2f} Cr (Max: ₹{ceil:.2f} Cr)"
    
    # Specific label placement offsets to prevent overlaps
    y_off = 0.35
    x_off = 0.0
    if p['name'] == 'Matheesha Pathirana': y_off = 0.45; x_off = -1.5
    elif p['name'] == 'Maheesh Theekshana': y_off = 0.45; x_off = 0.5
    elif p['name'] == 'Avesh Khan': y_off = 0.35; x_off = 1.0
    elif p['name'] == 'Wanindu Hasaranga': y_off = -0.55; x_off = -1.2
    elif p['name'] == 'Sikandar Raza': y_off = 0.30; x_off = 1.2
    elif p['name'] == 'Nurul Hasan': y_off = -0.45; x_off = -0.8
    elif p['name'] == 'Richard Ngarava': y_off = 0.35; x_off = 0.0
    elif p['name'] == 'Daryl Mitchell': y_off = -0.65; x_off = 0.0
    elif p['name'] == 'Azmatullah Omarzai': y_off = -0.65; x_off = 0.8
    elif p['name'] == 'M Shahrukh Khan': y_off = 0.40; x_off = -1.0

    ax1.text(x + x_off, y + y_off, label_text, fontsize=9.5, fontweight='bold',
             ha='center', va='center', color='#0F172A',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFFFFF', edgecolor='#CBD5E1', alpha=0.95))

ax1.set_xlabel('Pressure Composite Rating (PI ≥ 65)', fontsize=12, fontweight='bold', color='#0F172A')
ax1.set_ylabel('Target Bid Allocation (₹ Crore)', fontsize=12, fontweight='bold', color='#0F172A')
ax1.set_title('A. Value-to-Rating Matrix & Hard Walk-Away Ceilings (▲)', fontsize=13, fontweight='bold', color='#0F172A')
ax1.set_xlim(44, 78)
ax1.set_ylim(-0.2, 9.5)
ax1.grid(color='#E2E8F0', linestyle='--', alpha=0.8)
ax1.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=9)

# ─────────────────────────────────────────────────────────────────────────────
# SUBPLOT 2: PURSE ALLOCATION STACKED BREAKDOWN & 100% UTILIZATION
# ─────────────────────────────────────────────────────────────────────────────
ax2.set_facecolor('#FFFFFF')

# Sort targets by bid
sorted_targets = sorted(targets, key=lambda x: x['bid'])
names = [f"{p['name']} ({'[OS]' if p['os'] else '[IND]'})" for p in sorted_targets]
bids = [p['bid'] for p in sorted_targets]
colors = [p['color'] for p in sorted_targets]

y_pos = range(len(names))
bars = ax2.barh(y_pos, bids, color=colors, edgecolor='#0F172A', linewidth=1.2, height=0.65)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(names, fontsize=10, fontweight='bold', color='#0F172A')
ax2.set_xlabel('Allocated Bid Price (₹ Crore)', fontsize=12, fontweight='bold', color='#0F172A')
ax2.set_title('B. Budget Distribution: Exact ₹27.05 Cr Purse Balance', fontsize=13, fontweight='bold', color='#0F172A')
ax2.set_xlim(0, 8.5)
ax2.grid(axis='x', color='#E2E8F0', linestyle='--', alpha=0.8)

for bar in bars:
    w = bar.get_width()
    pct = (w / 27.05) * 100
    ax2.text(w + 0.15, bar.get_y() + bar.get_height()/2, f"₹{w:.2f} Cr ({pct:.1f}%)",
             va='center', fontsize=9.5, fontweight='bold', color='#0F172A')

# Total Purse Banner
summary_box = (
    "RAJASTHAN ROYALS WAR ROOM PURSE AUDIT:\n"
    "• Initial Purse Balance: ₹27.05 Crore (7th in IPL)\n"
    "• Total Target Commitment: ₹27.05 Crore\n"
    "• Budget Efficiency: 100.0% Fully Optimized\n"
    "• Remaining Reserve: ₹0.00 Cr (Zero Wastage)\n"
    "• Overseas Cap: 6 Targets (Max 4 in Starting XI)"
)
ax2.text(0.97, 0.18, summary_box, transform=ax2.transAxes,
         fontsize=9.5, family='monospace', fontweight='bold', ha='right', va='center',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#F8FAFC', edgecolor='#0284C7', linewidth=1.8))

plt.suptitle("RAJASTHAN ROYALS IPL 2027 MINI-AUCTION: ₹27.05 CRORE WAR ROOM CAPITAL BLUEPRINT",
             fontsize=14.5, fontweight='bold', color='#0F172A', y=0.99)
plt.tight_layout()
plt.savefig(OUT_FILE, facecolor='#FFFFFF', dpi=200)
plt.close()

print(f"SUCCESS: Generated {OUT_FILE}")
