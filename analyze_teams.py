"""
analyze_teams.py — رسوم إحصائيات الفرق (أفضل هجوم، أفضل دفاع، توزيع فوز/تعادل/خسارة).
المخرجات: 3 صور PNG في مجلد output/.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from pl_utils import (
    COLORS, GRID_COLOR, BG, SEASON,
    load_teams, style_ax, add_bar_labels, save_chart, setup_utf8_stdout,
)


def chart_goals_scored(df):
    """أفضل 5 فرق تسجيلاً للأهداف."""
    top_gf = df.nlargest(5, "GF").sort_values("GF")

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(BG)
    colors = ["#E63946"] * 5
    colors[-1] = "#B5001B"        # أغمق عمود = الأعلى تسجيلاً (بالأعلى)
    ax.barh(top_gf["Squad"], top_gf["GF"], color=colors,
            edgecolor="white", linewidth=0.6, zorder=3)
    style_ax(ax, "Top 5 Teams by Goals Scored", "Goals Scored")
    add_bar_labels(ax, offset=0.5)
    save_chart(fig, "teams_top5_goals_scored.png")


def chart_best_defense(df):
    """أفضل 5 فرق دفاعاً (الأقل استقبالاً للأهداف)."""
    best_def = df.nsmallest(5, "GA").sort_values("GA", ascending=False)  # الأفضل بالأعلى

    fig, ax = plt.subplots(figsize=(9, 5))
    fig.patch.set_facecolor(BG)
    colors = ["#457B9D"] * 5
    colors[0] = "#1D4E6B"         # أغمق = الأقل استقبالاً
    ax.barh(best_def["Squad"], best_def["GA"], color=colors,
            edgecolor="white", linewidth=0.6, zorder=3)
    style_ax(ax, "Top 5 Teams by Best Defense\n(Fewest Goals Conceded)", "Goals Conceded")
    add_bar_labels(ax, offset=0.3)
    save_chart(fig, "teams_top5_best_defense.png")


def chart_wdl(df):
    """توزيع الفوز/التعادل/الخسارة لكل الفرق العشرين (أعمدة مكدّسة)."""
    wdl = df[["Squad", "W", "D", "L"]].sort_values("W", ascending=True)  # الأفضل بالأعلى

    fig, ax = plt.subplots(figsize=(11, 9))
    fig.patch.set_facecolor(BG)
    y = np.arange(len(wdl))

    # أعمدة مكدّسة: فوز | تعادل | خسارة
    ax.barh(y, wdl["W"], height=0.6, color=COLORS["g_plus_a"],
            edgecolor="white", linewidth=0.5, zorder=3, label="Wins")
    ax.barh(y, wdl["D"], height=0.6, left=wdl["W"], color=COLORS["draw"],
            edgecolor="white", linewidth=0.5, zorder=3, label="Draws")
    ax.barh(y, wdl["L"], height=0.6, left=wdl["W"] + wdl["D"], color=COLORS["loss"],
            edgecolor="white", linewidth=0.5, zorder=3, label="Losses")

    # كتابة الأرقام داخل المقاطع الكبيرة فقط (>= 3)
    for i, (_, row) in enumerate(wdl.iterrows()):
        centers = [
            (row["W"] / 2, row["W"], "white"),
            (row["W"] + row["D"] / 2, row["D"], "#333"),
            (row["W"] + row["D"] + row["L"] / 2, row["L"], "white"),
        ]
        for cx, val, tc in centers:
            if val >= 3:
                ax.text(cx, i, str(int(val)), ha="center", va="center",
                        fontsize=9, fontweight="bold", color=tc, zorder=4)

    ax.set_yticks(y)
    ax.set_yticklabels(wdl["Squad"], fontsize=9)
    ax.set_xlabel("Matches Played", fontsize=11)
    ax.set_title("Win / Draw / Loss Breakdown — All Teams", fontsize=14, fontweight="bold", pad=14)
    ax.set_xlim(0, 38)            # موسم من 38 مباراة (كان 42 بالخطأ)
    ax.set_facecolor(BG)
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="both", labelsize=9)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.legend(loc="lower right", fontsize=10, framealpha=0.8)
    save_chart(fig, "teams_wdl_breakdown.png")


def main():
    setup_utf8_stdout()
    df = load_teams()

    chart_goals_scored(df)
    chart_best_defense(df)
    chart_wdl(df)

    # ── ملخص نصّي ──
    print("\nTop 5 Goals Scored:")
    print(df.nlargest(5, "GF")[["Squad", "GF"]].to_string(index=False))
    print("\nTop 5 Fewest Conceded:")
    print(df.nsmallest(5, "GA")[["Squad", "GA"]].to_string(index=False))
    print("\nFull W/D/L table:")
    print(df[["Squad", "W", "D", "L"]].sort_values("W", ascending=False).to_string(index=False))


if __name__ == "__main__":
    main()
