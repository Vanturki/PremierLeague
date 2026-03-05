import base64
import pandas as pd
from pathlib import Path

DESKTOP = Path(r"C:\Users\Turki\Desktop")
DATA    = Path(r"C:\Users\Turki\Downloads\archive (1)")

# ── Helpers ────────────────────────────────────────────────────────────────────
def img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def table_html(df, id_=""):
    rows = ""
    for _, r in df.iterrows():
        cells = "".join(f"<td>{v}</td>" for v in r)
        rows += f"<tr>{cells}</tr>\n"
    headers = "".join(f"<th>{c}</th>" for c in df.columns)
    return f'<table id="{id_}"><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>'

# ── Load data ──────────────────────────────────────────────────────────────────
players = pd.read_csv(DATA / "Squad_PlayerStats__stats_standard.csv")
players["Goals"]   = pd.to_numeric(players["Performance_Gls"], errors="coerce").fillna(0)
players["Assists"] = pd.to_numeric(players["Performance_Ast"], errors="coerce").fillna(0)
players["G+A"]     = players["Goals"] + players["Assists"]
players = players[players["Playing Time_MP"] > 0]

teams = pd.read_csv(DATA / "overwiev__results2024-202591_overall.csv")
for col in ["GF", "GA", "W", "D", "L", "Pts", "GD"]:
    teams[col] = pd.to_numeric(teams[col], errors="coerce")

# ── Build table data ───────────────────────────────────────────────────────────
top_goals   = players.nlargest(10, "Goals")[["Player","Squad","Goals"]].reset_index(drop=True)
top_goals.index += 1

top_assists = players.nlargest(10, "Assists")[["Player","Squad","Assists"]].reset_index(drop=True)
top_assists.index += 1

top_ga      = players.nlargest(10, "G+A")[["Player","Squad","Goals","Assists","G+A"]].reset_index(drop=True)
top_ga.index += 1

league_table = teams[["Squad","MP","W","D","L","GF","GA","GD","Pts"]].sort_values("Pts", ascending=False).reset_index(drop=True)
league_table.index += 1
league_table.insert(0, "#", league_table.index)

def df_to_html_rows(df):
    rows = ""
    for i, (_, r) in enumerate(df.iterrows()):
        medal = ""
        if i == 0: medal = " gold"
        elif i == 1: medal = " silver"
        elif i == 2: medal = " bronze"
        cells = "".join(f"<td>{v}</td>" for v in r)
        rows += f'<tr class="rank{medal}">{cells}</tr>\n'
    headers = "".join(f"<th>{c}</th>" for c in df.columns)
    return headers, rows

def league_rows(df):
    rows = ""
    for i, (_, r) in enumerate(df.iterrows()):
        cls = ""
        if i < 4:    cls = "cl"       # Champions League
        elif i < 6:  cls = "el"       # Europa League
        elif i < 7:  cls = "conf"     # Conference League
        elif i >= 17: cls = "rel"     # Relegation
        cells = "".join(f"<td>{v}</td>" for v in r)
        rows += f'<tr class="{cls}">{cells}</tr>\n'
    headers = "".join(f"<th>{c}</th>" for c in df.columns)
    return headers, rows

gh, gr = df_to_html_rows(top_goals.reset_index(drop=True))
ah, ar = df_to_html_rows(top_assists.reset_index(drop=True))
ch, cr = df_to_html_rows(top_ga.reset_index(drop=True))
lh, lr = league_rows(league_table)

# ── Encode charts ──────────────────────────────────────────────────────────────
charts = {k: img_b64(DESKTOP / k) for k in [
    "top10_goals.png",
    "top10_assists.png",
    "top10_goal_contributions.png",
    "teams_top5_goals_scored.png",
    "teams_top5_best_defense.png",
    "teams_wdl_breakdown.png",
]}

# ── HTML ───────────────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Premier League 2024-25 Analysis Report</title>
<style>
  /* ── Reset & Base ── */
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: #0d1117;
    color: #e6edf3;
    line-height: 1.6;
  }}

  /* ── Header ── */
  .hero {{
    background: linear-gradient(135deg, #38003c 0%, #00ff85 100%);
    padding: 60px 40px 50px;
    text-align: center;
    position: relative;
    overflow: hidden;
  }}
  .hero::before {{
    content: "";
    position: absolute; inset: 0;
    background: linear-gradient(135deg, #38003c 0%, #1a1a2e 60%, #00ff85 100%);
    opacity: 0.92;
  }}
  .hero-content {{ position: relative; z-index: 1; }}
  .hero-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(0,255,133,0.4);
    color: #00ff85;
    font-size: 0.75rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 20px;
    margin-bottom: 18px;
  }}
  .hero h1 {{
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 800;
    color: #fff;
    letter-spacing: -1px;
    margin-bottom: 10px;
  }}
  .hero p {{
    color: rgba(255,255,255,0.7);
    font-size: 1.05rem;
  }}

  /* ── Nav ── */
  nav {{
    background: #161b22;
    border-bottom: 1px solid #30363d;
    padding: 0 40px;
    display: flex;
    gap: 4px;
    position: sticky;
    top: 0;
    z-index: 100;
  }}
  nav a {{
    color: #8b949e;
    text-decoration: none;
    font-size: 0.9rem;
    padding: 14px 16px;
    border-bottom: 2px solid transparent;
    transition: color .2s, border-color .2s;
  }}
  nav a:hover {{ color: #e6edf3; border-color: #00ff85; }}

  /* ── Layout ── */
  .container {{ max-width: 1200px; margin: 0 auto; padding: 40px 24px; }}
  .section {{ margin-bottom: 64px; }}
  .section-header {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 28px;
    padding-bottom: 14px;
    border-bottom: 1px solid #21262d;
  }}
  .section-icon {{
    width: 42px; height: 42px;
    border-radius: 10px;
    display: grid; place-items: center;
    font-size: 1.2rem;
    flex-shrink: 0;
  }}
  .icon-red   {{ background: rgba(230,57,70,0.15);  color: #e63946; }}
  .icon-blue  {{ background: rgba(69,123,157,0.15); color: #457b9d; }}
  .icon-teal  {{ background: rgba(42,157,143,0.15); color: #2a9d8f; }}
  .icon-gold  {{ background: rgba(233,196,106,0.15);color: #e9c46a; }}
  .icon-green {{ background: rgba(0,255,133,0.15);  color: #00ff85; }}
  .section-header h2 {{
    font-size: 1.4rem;
    font-weight: 700;
    color: #e6edf3;
  }}
  .section-header p {{
    font-size: 0.85rem;
    color: #8b949e;
    margin-top: 2px;
  }}

  /* ── Cards ── */
  .card {{
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
  }}
  .card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
    gap: 24px;
  }}
  .chart-card {{
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 12px;
    overflow: hidden;
    transition: border-color .2s, transform .2s;
  }}
  .chart-card:hover {{
    border-color: #00ff85;
    transform: translateY(-2px);
  }}
  .chart-card img {{
    width: 100%;
    display: block;
  }}
  .chart-label {{
    padding: 12px 16px;
    font-size: 0.82rem;
    color: #8b949e;
    border-top: 1px solid #21262d;
    text-align: center;
  }}

  /* ── Tables ── */
  .table-wrap {{ overflow-x: auto; border-radius: 10px; border: 1px solid #21262d; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  thead tr {{ background: #0d1117; }}
  th {{
    padding: 12px 16px;
    text-align: left;
    font-size: 0.78rem;
    letter-spacing: .05em;
    text-transform: uppercase;
    color: #8b949e;
    font-weight: 600;
    white-space: nowrap;
  }}
  td {{ padding: 11px 16px; border-top: 1px solid #21262d; white-space: nowrap; }}
  tbody tr:hover {{ background: rgba(255,255,255,0.03); }}
  .gold   td:first-child {{ color: #ffd700; font-weight: 700; }}
  .silver td:first-child {{ color: #c0c0c0; font-weight: 700; }}
  .bronze td:first-child {{ color: #cd7f32; font-weight: 700; }}

  /* League table row colors */
  .cl   td:first-child {{ border-left: 3px solid #1d70b8; }}
  .el   td:first-child {{ border-left: 3px solid #e36414; }}
  .conf td:first-child {{ border-left: 3px solid #2a9d8f; }}
  .rel  td:first-child {{ border-left: 3px solid #e63946; }}

  /* ── Stat summary cards ── */
  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 28px;
  }}
  .stat-card {{
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
  }}
  .stat-card .val {{
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.1;
  }}
  .stat-card .lbl {{
    font-size: 0.78rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: .05em;
    margin-top: 4px;
  }}
  .stat-card .sub {{
    font-size: 0.82rem;
    color: #8b949e;
    margin-top: 2px;
  }}
  .c-red   {{ color: #e63946; }}
  .c-blue  {{ color: #457b9d; }}
  .c-teal  {{ color: #2a9d8f; }}
  .c-gold  {{ color: #e9c46a; }}
  .c-green {{ color: #00ff85; }}

  /* ── Legend ── */
  .legend {{
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    margin-bottom: 12px;
    font-size: 0.82rem;
    color: #8b949e;
  }}
  .legend span {{ display: flex; align-items: center; gap: 6px; }}
  .dot {{
    width: 10px; height: 10px;
    border-radius: 50%;
    display: inline-block;
  }}

  /* ── Footer ── */
  footer {{
    background: #161b22;
    border-top: 1px solid #21262d;
    text-align: center;
    padding: 28px;
    color: #8b949e;
    font-size: 0.82rem;
  }}
</style>
</head>
<body>

<!-- Hero -->
<div class="hero">
  <div class="hero-content">
    <div class="hero-badge">Data Analysis Report</div>
    <h1>Premier League 2024&ndash;25</h1>
    <p>Player &amp; Team Performance &mdash; Full Season Statistical Analysis</p>
  </div>
</div>

<!-- Nav -->
<nav>
  <a href="#players">Player Stats</a>
  <a href="#teams">Team Stats</a>
  <a href="#league-table">League Table</a>
</nav>

<div class="container">

  <!-- ════════════════════════════════════════════════════════
       SECTION 1 — KEY NUMBERS
  ═════════════════════════════════════════════════════════ -->
  <div class="section" id="overview">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="val c-red">29</div>
        <div class="lbl">Top Scorer Goals</div>
        <div class="sub">Mohamed Salah &middot; Liverpool</div>
      </div>
      <div class="stat-card">
        <div class="val c-blue">18</div>
        <div class="lbl">Top Assister</div>
        <div class="sub">Mohamed Salah &middot; Liverpool</div>
      </div>
      <div class="stat-card">
        <div class="val c-teal">47</div>
        <div class="lbl">Best G+A</div>
        <div class="sub">Mohamed Salah &middot; Liverpool</div>
      </div>
      <div class="stat-card">
        <div class="val c-gold">86</div>
        <div class="lbl">Most Goals (Team)</div>
        <div class="sub">Liverpool</div>
      </div>
      <div class="stat-card">
        <div class="val c-green">34</div>
        <div class="lbl">Fewest Conceded</div>
        <div class="sub">Arsenal</div>
      </div>
      <div class="stat-card">
        <div class="val c-red">84</div>
        <div class="lbl">Most Points</div>
        <div class="sub">Liverpool &mdash; Champions</div>
      </div>
    </div>
  </div>

  <!-- ════════════════════════════════════════════════════════
       SECTION 2 — PLAYER STATS
  ═════════════════════════════════════════════════════════ -->
  <div class="section" id="players">

    <div class="section-header">
      <div class="section-icon icon-red">&#9917;</div>
      <div>
        <h2>Player Statistics</h2>
        <p>Individual performance &mdash; goals, assists and combined contributions</p>
      </div>
    </div>

    <!-- Charts row -->
    <div class="card-grid" style="margin-bottom:28px;">
      <div class="chart-card">
        <img src="data:image/png;base64,{charts['top10_goals.png']}" alt="Top 10 Goals">
        <div class="chart-label">Top 10 Players by Goals Scored</div>
      </div>
      <div class="chart-card">
        <img src="data:image/png;base64,{charts['top10_assists.png']}" alt="Top 10 Assists">
        <div class="chart-label">Top 10 Players by Assists</div>
      </div>
    </div>
    <div class="chart-card" style="margin-bottom:28px;">
      <img src="data:image/png;base64,{charts['top10_goal_contributions.png']}" alt="Top 10 G+A">
      <div class="chart-label">Top 10 Players by Goal Contributions (Goals + Assists) &mdash; stacked by type</div>
    </div>

    <!-- Tables row -->
    <div class="card-grid">
      <div>
        <h3 style="margin-bottom:12px;font-size:1rem;color:#e6edf3;">&#127942; Top 10 Scorers</h3>
        <div class="table-wrap">
          <table>
            <thead><tr><th>#</th>{gh}</tr></thead>
            <tbody>{gr}</tbody>
          </table>
        </div>
      </div>
      <div>
        <h3 style="margin-bottom:12px;font-size:1rem;color:#e6edf3;">&#127942; Top 10 Assisters</h3>
        <div class="table-wrap">
          <table>
            <thead><tr><th>#</th>{ah}</tr></thead>
            <tbody>{ar}</tbody>
          </table>
        </div>
      </div>
    </div>

    <div style="margin-top:24px;">
      <h3 style="margin-bottom:12px;font-size:1rem;color:#e6edf3;">&#127942; Top 10 by Goal Contributions (G+A)</h3>
      <div class="table-wrap">
        <table>
          <thead><tr><th>#</th>{ch}</tr></thead>
          <tbody>{cr}</tbody>
        </table>
      </div>
    </div>

  </div>

  <!-- ════════════════════════════════════════════════════════
       SECTION 3 — TEAM STATS
  ═════════════════════════════════════════════════════════ -->
  <div class="section" id="teams">

    <div class="section-header">
      <div class="section-icon icon-teal">&#127960;</div>
      <div>
        <h2>Team Statistics</h2>
        <p>Attack, defense and results breakdown across all 20 clubs</p>
      </div>
    </div>

    <div class="card-grid" style="margin-bottom:24px;">
      <div class="chart-card">
        <img src="data:image/png;base64,{charts['teams_top5_goals_scored.png']}" alt="Top 5 Goals">
        <div class="chart-label">Top 5 Teams by Goals Scored</div>
      </div>
      <div class="chart-card">
        <img src="data:image/png;base64,{charts['teams_top5_best_defense.png']}" alt="Best Defense">
        <div class="chart-label">Top 5 Teams by Fewest Goals Conceded</div>
      </div>
    </div>

    <div class="chart-card" style="margin-bottom:24px;">
      <img src="data:image/png;base64,{charts['teams_wdl_breakdown.png']}" alt="W/D/L">
      <div class="chart-label">Win / Draw / Loss Breakdown &mdash; All 20 Teams</div>
    </div>

  </div>

  <!-- ════════════════════════════════════════════════════════
       SECTION 4 — FULL LEAGUE TABLE
  ═════════════════════════════════════════════════════════ -->
  <div class="section" id="league-table">

    <div class="section-header">
      <div class="section-icon icon-gold">&#128202;</div>
      <div>
        <h2>Full League Table</h2>
        <p>Final 2024&ndash;25 standings</p>
      </div>
    </div>

    <div class="legend">
      <span><span class="dot" style="background:#1d70b8;"></span> Champions League</span>
      <span><span class="dot" style="background:#e36414;"></span> Europa League</span>
      <span><span class="dot" style="background:#2a9d8f;"></span> Conference League</span>
      <span><span class="dot" style="background:#e63946;"></span> Relegation</span>
    </div>

    <div class="table-wrap">
      <table>
        <thead><tr>{lh}</tr></thead>
        <tbody>{lr}</tbody>
      </table>
    </div>

  </div>

</div><!-- /container -->

<footer>
  Premier League 2024&ndash;25 &middot; Data Analysis Report &middot; Generated with Python &amp; Matplotlib
</footer>

</body>
</html>"""

out = DESKTOP / "pl_analysis_report.html"
out.write_text(html, encoding="utf-8")
print(f"Report saved: {out}")
print(f"Size: {out.stat().st_size / 1024:.1f} KB")
