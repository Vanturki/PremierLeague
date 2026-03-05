import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv(r"C:\Users\Turki\Downloads\archive (1)\overwiev__results2024-202591_overall.csv")
df["GF"] = pd.to_numeric(df["GF"], errors="coerce")
df["GA"] = pd.to_numeric(df["GA"], errors="coerce")
df["W"]  = pd.to_numeric(df["W"],  errors="coerce")
df["D"]  = pd.to_numeric(df["D"],  errors="coerce")
df["L"]  = pd.to_numeric(df["L"],  errors="coerce")

# ── Shared style ───────────────────────────────────────────────────────────────
BG       = "#F8F9FA"
GRID_COL = "#DEE2E6"
SEASON   = "Premier League 2024-25 Season"

def base_style(ax):
    ax.set_facecolor(BG)
    ax.grid(axis="x", color=GRID_COL, linewidth=0.8, zorder=0)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="both", labelsize=10)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

def add_bar_labels(ax, offset=0.3):
    for bar in ax.patches:
        w = bar.get_width()
        if w > 0:
            ax.text(w + offset, bar.get_y() + bar.get_height() / 2,
                    f"{int(w)}", va="center", ha="left", fontsize=10, color="#333")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 1 — Top 5 Teams by Goals Scored
# ══════════════════════════════════════════════════════════════════════════════
top_gf = df.nlargest(5, "GF").sort_values("GF")

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor(BG)

colors_gf = ["#E63946"] * 5
colors_gf[-1] = "#B5001B"   # darkest bar = highest value (top)

ax.barh(top_gf["Squad"], top_gf["GF"], color=colors_gf,
        edgecolor="white", linewidth=0.6, zorder=3)

base_style(ax)
add_bar_labels(ax, 0.5)
ax.set_xlabel("Goals Scored", fontsize=11)
ax.set_title("Top 5 Teams by Goals Scored", fontsize=15, fontweight="bold", pad=14)
fig.text(0.13, 0.93, SEASON, fontsize=9, color="#777")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(r"C:\Users\Turki\Desktop\teams_top5_goals_scored.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: teams_top5_goals_scored.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 2 — Top 5 Teams by Least Goals Conceded (Best Defense)
# ══════════════════════════════════════════════════════════════════════════════
best_def = df.nsmallest(5, "GA").sort_values("GA", ascending=False)  # ascending=False so best is at top

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor(BG)

colors_ga = ["#457B9D"] * 5
colors_ga[0] = "#1D4E6B"   # darkest = fewest conceded (top bar)

ax.barh(best_def["Squad"], best_def["GA"], color=colors_ga,
        edgecolor="white", linewidth=0.6, zorder=3)

base_style(ax)
add_bar_labels(ax, 0.3)
ax.set_xlabel("Goals Conceded", fontsize=11)
ax.set_title("Top 5 Teams by Best Defense\n(Fewest Goals Conceded)", fontsize=14, fontweight="bold", pad=14)
fig.text(0.13, 0.93, SEASON, fontsize=9, color="#777")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(r"C:\Users\Turki\Desktop\teams_top5_best_defense.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: teams_top5_best_defense.png")

# ══════════════════════════════════════════════════════════════════════════════
# Chart 3 — Win/Draw/Loss Breakdown for All Teams
# ══════════════════════════════════════════════════════════════════════════════
# Sort by wins descending so best team is at top
wdl = df[["Squad", "W", "D", "L"]].sort_values("W", ascending=True)

fig, ax = plt.subplots(figsize=(11, 9))
fig.patch.set_facecolor(BG)

y      = np.arange(len(wdl))
height = 0.6

# Stacked bars: W | D | L
bars_w = ax.barh(y, wdl["W"], height=height, color="#2A9D8F",
                 edgecolor="white", linewidth=0.5, zorder=3, label="Wins")
bars_d = ax.barh(y, wdl["D"], height=height, left=wdl["W"],
                 color="#E9C46A", edgecolor="white", linewidth=0.5, zorder=3, label="Draws")
bars_l = ax.barh(y, wdl["L"], height=height, left=wdl["W"] + wdl["D"],
                 color="#E76F51", edgecolor="white", linewidth=0.5, zorder=3, label="Losses")

# Inline labels inside segments (only if wide enough)
for i, (_, row) in enumerate(wdl.iterrows()):
    cx_w = row["W"] / 2
    cx_d = row["W"] + row["D"] / 2
    cx_l = row["W"] + row["D"] + row["L"] / 2
    for cx, val, tc in [(cx_w, row["W"], "white"),
                        (cx_d, row["D"], "#333"),
                        (cx_l, row["L"], "white")]:
        if val >= 3:
            ax.text(cx, i, str(int(val)), ha="center", va="center",
                    fontsize=9, fontweight="bold", color=tc, zorder=4)

ax.set_yticks(y)
ax.set_yticklabels(wdl["Squad"], fontsize=9)
ax.set_xlabel("Matches Played", fontsize=11)
ax.set_title("Win / Draw / Loss Breakdown — All Teams", fontsize=14, fontweight="bold", pad=14)
ax.set_xlim(0, 42)
ax.set_facecolor(BG)
ax.grid(axis="x", color=GRID_COL, linewidth=0.8, zorder=0)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.tick_params(axis="both", labelsize=9)
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
ax.legend(loc="lower right", fontsize=10, framealpha=0.8)
fig.text(0.13, 0.94, SEASON, fontsize=9, color="#777")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(r"C:\Users\Turki\Desktop\teams_wdl_breakdown.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: teams_wdl_breakdown.png")

# ── Quick summary ──────────────────────────────────────────────────────────────
print("\nTop 5 Goals Scored:")
print(df.nlargest(5, "GF")[["Squad","GF"]].to_string(index=False))
print("\nTop 5 Fewest Conceded:")
print(df.nsmallest(5, "GA")[["Squad","GA"]].to_string(index=False))
print("\nFull W/D/L table:")
print(df[["Squad","W","D","L"]].sort_values("W", ascending=False).to_string(index=False))
