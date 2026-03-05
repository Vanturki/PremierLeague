import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv(r"C:\Users\Turki\Downloads\archive (1)\Squad_PlayerStats__stats_standard.csv")

# Keep only numeric goal/assist columns and drop rows with no appearances
df["Goals"]        = pd.to_numeric(df["Performance_Gls"], errors="coerce").fillna(0)
df["Assists"]      = pd.to_numeric(df["Performance_Ast"], errors="coerce").fillna(0)
df["Contributions"] = df["Goals"] + df["Assists"]
df = df[df["Playing Time_MP"] > 0].copy()

# ── Shared style ───────────────────────────────────────────────────────────────
COLORS = {
    "goals":  "#E63946",   # red
    "assists": "#457B9D",  # blue
    "g_plus_a": "#2A9D8F", # teal
}
BAR_EDGE   = "white"
BACKGROUND = "#F8F9FA"
GRID_COLOR = "#DEE2E6"

def style_ax(ax, title, xlabel, color):
    ax.set_title(title, fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel("")
    ax.tick_params(axis="y", labelsize=10)
    ax.tick_params(axis="x", labelsize=10)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_facecolor(BACKGROUND)
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.spines[["top", "right", "left"]].set_visible(False)
    # value labels on bars
    for bar in ax.patches:
        w = bar.get_width()
        if w > 0:
            ax.text(
                w + 0.15, bar.get_y() + bar.get_height() / 2,
                f"{int(w)}", va="center", ha="left", fontsize=9, color="#333"
            )

def save_chart(top, value_col, title, xlabel, color, filename):
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BACKGROUND)

    top_sorted = top.sort_values(value_col)           # ascending so top is at top
    bars = ax.barh(
        top_sorted["Player"], top_sorted[value_col],
        color=color, edgecolor=BAR_EDGE, linewidth=0.6, zorder=3
    )
    style_ax(ax, title, xlabel, color)

    # Subtitle with season info
    fig.text(0.13, 0.92, "Premier League 2024–25 Season", fontsize=9, color="#777")

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    path = rf"C:\Users\Turki\Desktop\{filename}"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")

# ── Chart 1 — Top 10 by Goals ─────────────────────────────────────────────────
top_goals = df.nlargest(10, "Goals")[["Player", "Squad", "Goals"]]
save_chart(
    top_goals, "Goals",
    "Top 10 Players by Goals",
    "Goals",
    COLORS["goals"],
    "top10_goals.png"
)

# ── Chart 2 — Top 10 by Assists ───────────────────────────────────────────────
top_assists = df.nlargest(10, "Assists")[["Player", "Squad", "Assists"]]
save_chart(
    top_assists, "Assists",
    "Top 10 Players by Assists",
    "Assists",
    COLORS["assists"],
    "top10_assists.png"
)

# ── Chart 3 — Top 10 by Goal Contributions (G+A) ─────────────────────────────
top_ga = df.nlargest(10, "Contributions")[["Player", "Squad", "Goals", "Assists", "Contributions"]]

# Stacked bar for G+A so goals vs assists are visible
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BACKGROUND)
top_sorted = top_ga.sort_values("Contributions")

ax.barh(top_sorted["Player"], top_sorted["Goals"],
        color=COLORS["goals"],   edgecolor=BAR_EDGE, linewidth=0.6, zorder=3, label="Goals")
ax.barh(top_sorted["Player"], top_sorted["Assists"],
        left=top_sorted["Goals"],
        color=COLORS["assists"], edgecolor=BAR_EDGE, linewidth=0.6, zorder=3, label="Assists")

# value labels
for _, row in top_sorted.iterrows():
    ax.text(row["Contributions"] + 0.15,
            list(top_sorted["Player"]).index(row["Player"]),
            f"{int(row['Contributions'])}",
            va="center", ha="left", fontsize=9, color="#333")

ax.set_title("Top 10 Players by Goal Contributions (Goals + Assists)",
             fontsize=14, fontweight="bold", pad=14)
ax.set_xlabel("Goal Contributions (G+A)", fontsize=11)
ax.tick_params(axis="y", labelsize=10)
ax.tick_params(axis="x", labelsize=10)
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.set_facecolor(BACKGROUND)
ax.grid(axis="x", color=GRID_COLOR, linewidth=0.8, zorder=0)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.legend(loc="lower right", fontsize=10)
fig.text(0.13, 0.92, "Premier League 2024–25 Season", fontsize=9, color="#777")

plt.tight_layout(rect=[0, 0, 1, 0.95])
path = r"C:\Users\Turki\Desktop\top10_goal_contributions.png"
plt.savefig(path, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved: {path}")

# ── Quick summary printout ────────────────────────────────────────────────────
print("\n── Top 10 by Goals ──")
print(top_goals.to_string(index=False))
print("\n── Top 10 by Assists ──")
print(top_assists.to_string(index=False))
print("\n── Top 10 by G+A ──")
print(top_ga.to_string(index=False))
