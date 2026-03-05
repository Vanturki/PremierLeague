import sys
import io
import time
import pandas as pd
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.text import Text
from rich.rule import Rule
from rich.align import Align
from rich import box
from rich.live import Live
from rich.layout import Layout
from rich.padding import Padding

# ── Force UTF-8 output on Windows ─────────────────────────────────────────────
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Setup ──────────────────────────────────────────────────────────────────────
console = Console(force_terminal=True, highlight=False)
DATA = Path(r"C:\Users\Turki\Downloads\archive (1)")

# ── Load Data ──────────────────────────────────────────────────────────────────
def load_data():
    players = pd.read_csv(DATA / "Squad_PlayerStats__stats_standard.csv")
    players["Goals"]   = pd.to_numeric(players["Performance_Gls"], errors="coerce").fillna(0).astype(int)
    players["Assists"] = pd.to_numeric(players["Performance_Ast"], errors="coerce").fillna(0).astype(int)
    players["G+A"]     = players["Goals"] + players["Assists"]
    players = players[players["Playing Time_MP"] > 0].copy()

    teams = pd.read_csv(DATA / "overwiev__results2024-202591_overall.csv")
    for col in ["GF", "GA", "W", "D", "L", "Pts", "GD", "MP"]:
        teams[col] = pd.to_numeric(teams[col], errors="coerce")

    return players, teams

# ── Medal helper ───────────────────────────────────────────────────────────────
def medal(rank):
    return {1: "[1]", 2: "[2]", 3: "[3]"}.get(rank, f"  {rank} ")

# ── Animate loading ────────────────────────────────────────────────────────────
def show_loading():
    datasets = [
        ("Squad_PlayerStats__stats_standard.csv",         "Player statistics"),
        ("overwiev__results2024-202591_overall.csv",       "League standings"),
        ("overwiev__stats_squads_standard_for.csv",        "Attack metrics"),
        ("overwiev__stats_squads_standard_against.csv",    "Defense metrics"),
    ]
    console.print()
    with Progress(
        SpinnerColumn(spinner_name="dots", style="bold green"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=36, style="green", complete_style="bright_green"),
        TextColumn("[bold white]{task.percentage:>3.0f}%"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Loading data files...", total=len(datasets))
        for fname, label in datasets:
            progress.update(task, description=f"[cyan]Loading[/cyan] [white]{label}[/white]")
            time.sleep(0.4)
            progress.advance(task)
    console.print()

# ── Hero banner ────────────────────────────────────────────────────────────────
def show_banner():
    banner = Text(justify="center")
    banner.append("\n  [*]  PREMIER LEAGUE 2024-25  [*]\n", style="bold white on #38003c")
    banner.append("   Interactive Terminal Dashboard   \n", style="bold #00ff85")
    console.print(Panel(banner, border_style="#38003c", padding=(0, 4)))
    console.print()

# ── Section rule ──────────────────────────────────────────────────────────────
def section(title, icon=""):
    console.print()
    console.print(Rule(f"[bold white] {icon}  {title} [/bold white]", style="#38003c"))
    console.print()

# ── Progress bar column (inline) ──────────────────────────────────────────────
def bar(value, max_value, width=20, color="green"):
    filled = int((value / max_value) * width) if max_value else 0
    bar_str = "#" * filled + "-" * (width - filled)
    return f"[{color}]{bar_str}[/{color}]"

# ══════════════════════════════════════════════════════════════════════════════
# TABLE 1 -- Top 10 Scorers
# ══════════════════════════════════════════════════════════════════════════════
def table_top_scorers(players):
    top = players.nlargest(10, "Goals").reset_index(drop=True)
    max_g = int(top["Goals"].max())

    t = Table(
        title="[bold white]Top 10 Goal Scorers[/bold white]",
        box=box.SIMPLE_HEAVY,
        border_style="#38003c",
        header_style="bold #00ff85",
        show_lines=False,
        min_width=72,
    )
    t.add_column("",      width=4,  justify="center")
    t.add_column("Player",          style="bold white",   min_width=22)
    t.add_column("Club",            style="dim white",    min_width=18)
    t.add_column("Goals", width=6,  justify="right", style="bold #e63946")
    t.add_column("Bar",             justify="left",  min_width=22)

    for i, row in top.iterrows():
        rank = i + 1
        g    = int(row["Goals"])
        color = "#e63946" if rank == 1 else ("#f4a261" if rank <= 3 else "red")
        t.add_row(
            medal(rank),
            str(row["Player"]),
            str(row["Squad"]),
            str(g),
            bar(g, max_g, width=20, color=color),
        )
    return t

# ══════════════════════════════════════════════════════════════════════════════
# TABLE 2 -- Top 10 Assisters
# ══════════════════════════════════════════════════════════════════════════════
def table_top_assists(players):
    top = players.nlargest(10, "Assists").reset_index(drop=True)
    max_a = int(top["Assists"].max())

    t = Table(
        title="[bold white]Top 10 Assisters[/bold white]",
        box=box.SIMPLE_HEAVY,
        border_style="#38003c",
        header_style="bold #00ff85",
        show_lines=False,
        min_width=72,
    )
    t.add_column("",       width=4,  justify="center")
    t.add_column("Player",           style="bold white",  min_width=22)
    t.add_column("Club",             style="dim white",   min_width=18)
    t.add_column("Ast",   width=5,   justify="right", style="bold #457b9d")
    t.add_column("Bar",              justify="left",  min_width=22)

    for i, row in top.iterrows():
        rank = i + 1
        a    = int(row["Assists"])
        color = "#457b9d" if rank == 1 else ("#74b4d4" if rank <= 3 else "blue")
        t.add_row(
            medal(rank),
            str(row["Player"]),
            str(row["Squad"]),
            str(a),
            bar(a, max_a, width=20, color=color),
        )
    return t

# ══════════════════════════════════════════════════════════════════════════════
# TABLE 3 -- Top 10 Goal Contributions
# ══════════════════════════════════════════════════════════════════════════════
def table_top_ga(players):
    top = players.nlargest(10, "G+A").reset_index(drop=True)
    max_ga = int(top["G+A"].max())

    t = Table(
        title="[bold white]Top 10 Goal Contributions (G+A)[/bold white]",
        box=box.SIMPLE_HEAVY,
        border_style="#38003c",
        header_style="bold #00ff85",
        show_lines=False,
        min_width=82,
    )
    t.add_column("",       width=4,  justify="center")
    t.add_column("Player",           style="bold white",  min_width=22)
    t.add_column("Club",             style="dim white",   min_width=18)
    t.add_column("Gls",  width=5,    justify="right", style="#e63946")
    t.add_column("Ast",  width=5,    justify="right", style="#457b9d")
    t.add_column("G+A",  width=5,    justify="right", style="bold #2a9d8f")
    t.add_column("Bar",              justify="left",  min_width=22)

    for i, row in top.iterrows():
        rank = i + 1
        ga   = int(row["G+A"])
        color = "#2a9d8f" if rank == 1 else ("bright_cyan" if rank <= 3 else "cyan")
        t.add_row(
            medal(rank),
            str(row["Player"]),
            str(row["Squad"]),
            str(int(row["Goals"])),
            str(int(row["Assists"])),
            str(ga),
            bar(ga, max_ga, width=20, color=color),
        )
    return t

# ══════════════════════════════════════════════════════════════════════════════
# TABLE 4 -- League Standings
# ══════════════════════════════════════════════════════════════════════════════
def table_standings(teams):
    t = Table(
        title="[bold white]League Standings[/bold white]",
        box=box.SIMPLE_HEAVY,
        border_style="#38003c",
        header_style="bold #00ff85",
        show_lines=False,
        min_width=88,
    )
    t.add_column("#",    width=4,  justify="center")
    t.add_column("Club",           style="bold white",  min_width=22)
    t.add_column("MP",   width=4,  justify="center", style="dim white")
    t.add_column("W",    width=4,  justify="center", style="bold #2a9d8f")
    t.add_column("D",    width=4,  justify="center", style="bold #e9c46a")
    t.add_column("L",    width=4,  justify="center", style="bold #e63946")
    t.add_column("GF",   width=5,  justify="center", style="#e63946")
    t.add_column("GA",   width=5,  justify="center", style="#457b9d")
    t.add_column("GD",   width=5,  justify="center")
    t.add_column("Pts",  width=5,  justify="center", style="bold #00ff85")
    t.add_column("Form", width=26, justify="left")

    standings = teams.sort_values("Pts", ascending=False).reset_index(drop=True)

    for i, row in standings.iterrows():
        pos  = i + 1
        gd   = int(row["GD"])
        gd_s = f"[green]+{gd}[/green]" if gd > 0 else (f"[red]{gd}[/red]" if gd < 0 else f"[dim]{gd}[/dim]")

        # Position color
        if pos <= 4:   pos_style = "bold #1d70b8"
        elif pos <= 6: pos_style = "bold #e36414"
        elif pos == 7: pos_style = "bold #2a9d8f"
        elif pos >= 18: pos_style = "bold #e63946"
        else:           pos_style = "dim white"

        # W/D/L progress bar
        w, d, l = int(row["W"]), int(row["D"]), int(row["L"])
        total   = w + d + l or 1
        ww = int((w / total) * 20)
        dw = int((d / total) * 20)
        lw = 20 - ww - dw
        form_bar = (
            f"[bold green]{'█' * ww}[/bold green]"
            f"[bold yellow]{'█' * dw}[/bold yellow]"
            f"[bold red]{'█' * lw}[/bold red]"
        )

        t.add_row(
            f"[{pos_style}]{pos}[/{pos_style}]",
            str(row["Squad"]),
            str(int(row["MP"])),
            str(w), str(d), str(l),
            str(int(row["GF"])),
            str(int(row["GA"])),
            gd_s,
            str(int(row["Pts"])),
            form_bar,
        )

        # Separator after CL / EL / CONF / mid / rel zones
        if pos in (4, 6, 7, 17):
            t.add_section()

    return t

# ══════════════════════════════════════════════════════════════════════════════
# TABLE 5 -- Best Attack & Best Defense (side by side)
# ══════════════════════════════════════════════════════════════════════════════
def table_attack_defense(teams):
    standings = teams.sort_values("Pts", ascending=False).reset_index(drop=True)

    # Attack -- top 5 by GF
    top_att = standings.nlargest(5, "GF").reset_index(drop=True)
    max_gf  = int(top_att["GF"].max())

    atk = Table(
        title="[bold white]Best Attack[/bold white]  [dim](Goals Scored)[/dim]",
        box=box.SIMPLE_HEAVY,
        border_style="red",
        header_style="bold #e63946",
        show_lines=False,
        min_width=46,
    )
    atk.add_column("",      width=4,  justify="center")
    atk.add_column("Club",            style="bold white", min_width=18)
    atk.add_column("GF",    width=5,  justify="right", style="bold #e63946")
    atk.add_column("Bar",             justify="left",  min_width=18)

    for i, row in top_att.iterrows():
        gf = int(row["GF"])
        atk.add_row(medal(i+1), str(row["Squad"]), str(gf),
                    bar(gf, max_gf, width=16, color="red"))

    # Defense -- top 5 by fewest GA
    top_def = standings.nsmallest(5, "GA").reset_index(drop=True)
    max_ga  = int(top_def["GA"].max())

    dfn = Table(
        title="[bold white]Best Defense[/bold white]  [dim](Goals Conceded)[/dim]",
        box=box.SIMPLE_HEAVY,
        border_style="blue",
        header_style="bold #457b9d",
        show_lines=False,
        min_width=46,
    )
    dfn.add_column("",      width=4,  justify="center")
    dfn.add_column("Club",            style="bold white", min_width=18)
    dfn.add_column("GA",    width=5,  justify="right", style="bold #457b9d")
    dfn.add_column("Bar",             justify="left",  min_width=18)

    for i, row in top_def.iterrows():
        ga = int(row["GA"])
        dfn.add_row(medal(i+1), str(row["Squad"]), str(ga),
                    bar(ga, max_ga, width=16, color="blue"))

    return atk, dfn

# ══════════════════════════════════════════════════════════════════════════════
# ANIMATED progress bars shown briefly at startup
# ══════════════════════════════════════════════════════════════════════════════
def show_stat_bars(players, teams):
    section("Season Highlights", "[#]")

    standings = teams.sort_values("Pts", ascending=False).reset_index(drop=True)
    top_scorer   = players.loc[players["Goals"].idxmax()]
    top_assister = players.loc[players["Assists"].idxmax()]
    top_ga_p     = players.loc[players["G+A"].idxmax()]
    best_team    = standings.iloc[0]
    arsenal_ga   = int(teams.loc[teams["Squad"] == "Arsenal", "GA"].values[0])

    stats = [
        ("[G]  Salah - Goals",       int(top_scorer["Goals"]),    38,  "#e63946"),
        ("[>]  Salah - Assists",      int(top_assister["Assists"]),38,  "#457b9d"),
        ("[!]  Salah - G+A",          int(top_ga_p["G+A"]),        76,  "#2a9d8f"),
        ("[T]  Liverpool - Points",   int(best_team["Pts"]),       114, "#00ff85"),
        ("[*]  Liverpool - Goals",    int(best_team["GF"]),        100, "#e9c46a"),
        ("[D]  Arsenal - Conceded",   arsenal_ga,                   60, "#74b4d4"),
    ]

    BAR_W = 36

    def render_table(step, total_steps):
        t = Table(box=None, show_header=False, padding=(0, 1))
        t.add_column("label", style="bold white",  min_width=28, no_wrap=True)
        t.add_column("bar",   min_width=BAR_W + 2, no_wrap=True)
        t.add_column("val",   style="bold white",  width=5, justify="right")
        for label, value, maximum, color in stats:
            current  = int(value * step / total_steps)
            filled   = int((current / maximum) * BAR_W)
            empty    = BAR_W - filled
            bar_text = Text()
            bar_text.append("#" * filled, style=color)
            bar_text.append("-" * empty,  style="dim white")
            t.add_row(label, bar_text, str(current))
        return t

    steps = 40
    with Live(render_table(0, steps), console=console,
              refresh_per_second=30, transient=False) as live:
        for step in range(1, steps + 1):
            live.update(render_table(step, steps))
            time.sleep(0.04)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    console.clear()
    show_banner()
    show_loading()

    players, teams = load_data()

    # ── Season highlight bars (animated) ──────────────────────────────────────
    show_stat_bars(players, teams)

    # ── Player tables ──────────────────────────────────────────────────────────
    section("Player Statistics", "[*]")
    console.print(Align.center(table_top_scorers(players)))
    console.print()
    console.print(Align.center(table_top_assists(players)))
    console.print()
    console.print(Align.center(table_top_ga(players)))

    # ── Attack / Defense side by side ─────────────────────────────────────────
    section("Team Attack & Defense", "[S]")
    atk, dfn = table_attack_defense(teams)
    console.print(Columns([Padding(atk, (0, 4)), Padding(dfn, (0, 4))], align="center"))

    # ── Full standings ─────────────────────────────────────────────────────────
    section("League Standings", "[T]")

    legend = Text(justify="center")
    legend.append("  *  ", style="bold #1d70b8")
    legend.append("Champions League   ", style="dim white")
    legend.append("*  ", style="bold #e36414")
    legend.append("Europa League   ", style="dim white")
    legend.append("*  ", style="bold #2a9d8f")
    legend.append("Conference League   ", style="dim white")
    legend.append("*  ", style="bold #e63946")
    legend.append("Relegation  ", style="dim white")
    console.print(legend)
    console.print()
    console.print(Align.center(table_standings(teams)))

    # ── Footer ─────────────────────────────────────────────────────────────────
    console.print()
    console.print(Rule(style="#38003c"))
    footer = Text("Premier League 2024-25  -  Data Analysis Dashboard  -  Powered by Rich", justify="center")
    console.print(footer, style="dim white")
    console.print()

if __name__ == "__main__":
    main()
