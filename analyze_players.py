"""
analyze_players.py — رسوم إحصائيات اللاعبين (أفضل 10 في الأهداف، الصناعة، المساهمات).
المخرجات: 3 صور PNG في مجلد output/.
"""

import matplotlib.pyplot as plt

from pl_utils import (
    COLORS, BAR_EDGE, BG,
    load_players, style_ax, add_bar_labels, save_chart, setup_utf8_stdout,
)


def chart_single(df, value_col, title, xlabel, color, filename):
    """رسم عمودي أفقي لأفضل 10 لاعبين حسب عمود واحد (أهداف أو صناعة)."""
    top = df.nlargest(10, value_col)[["Player", "Squad", value_col]]
    top_sorted = top.sort_values(value_col)          # تصاعدي حتى يظهر الأعلى بالأعلى

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)
    ax.barh(top_sorted["Player"], top_sorted[value_col],
            color=color, edgecolor=BAR_EDGE, linewidth=0.6, zorder=3)
    style_ax(ax, title, xlabel)
    add_bar_labels(ax, offset=0.15)
    save_chart(fig, filename)
    return top


def chart_contributions(df):
    """رسم مكدّس للمساهمات: أهداف + صناعة لكل لاعب من أفضل 10."""
    top_ga = df.nlargest(10, "Contributions")[
        ["Player", "Squad", "Goals", "Assists", "Contributions"]
    ]
    top_sorted = top_ga.sort_values("Contributions")

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)

    # الطبقة الأولى: الأهداف — والثانية: الصناعة فوقها
    ax.barh(top_sorted["Player"], top_sorted["Goals"],
            color=COLORS["goals"], edgecolor=BAR_EDGE, linewidth=0.6, zorder=3, label="Goals")
    ax.barh(top_sorted["Player"], top_sorted["Assists"], left=top_sorted["Goals"],
            color=COLORS["assists"], edgecolor=BAR_EDGE, linewidth=0.6, zorder=3, label="Assists")

    # قيمة المجموع (G+A) عند نهاية كل عمود
    for i, (_, row) in enumerate(top_sorted.iterrows()):
        ax.text(row["Contributions"] + 0.15, i, f"{int(row['Contributions'])}",
                va="center", ha="left", fontsize=9, color="#333")

    style_ax(ax, "Top 10 Players by Goal Contributions (Goals + Assists)",
             "Goal Contributions (G+A)")
    ax.legend(loc="lower right", fontsize=10)
    save_chart(fig, "top10_goal_contributions.png")
    return top_ga


def main():
    setup_utf8_stdout()          # ضبط الترميز أولاً
    df = load_players()          # تحميل وتنظيف بيانات اللاعبين

    # ── الرسوم الثلاثة ──
    top_goals = chart_single(df, "Goals",
                             "Top 10 Players by Goals", "Goals",
                             COLORS["goals"], "top10_goals.png")
    top_assists = chart_single(df, "Assists",
                               "Top 10 Players by Assists", "Assists",
                               COLORS["assists"], "top10_assists.png")
    top_ga = chart_contributions(df)

    # ── ملخص نصّي سريع ──
    print("\n-- Top 10 by Goals --")
    print(top_goals.to_string(index=False))
    print("\n-- Top 10 by Assists --")
    print(top_assists.to_string(index=False))
    print("\n-- Top 10 by G+A --")
    print(top_ga.to_string(index=False))


if __name__ == "__main__":
    main()
