# CLAUDE.md — PremierLeague

Guidance for Claude Code when working in this project.

## Identity & Language

Turki — data analyst learning AI and data engineering.

- Respond in Arabic; code comments in Arabic; technical terms stay in English
- Code must run immediately, formatted like VS Code (no sidebar line numbers)
- Data analysis follows: **Load → Clean → EDA → Visualize → Report**

## What this project is

Premier League **2024–25** analysis. Four Python scripts + a Jupyter notebook turn
FBref-style CSVs into 6 charts, a self-contained dark-theme HTML report, and a
`rich` terminal dashboard.

## Layout

| Path | Role |
|------|------|
| `data/` | Source CSVs (bundled — copied from `../datasets/PremierLeague/`). Read-only inputs. |
| `output/` | Generated: 6 PNGs + `pl_analysis_report.html`. Committed as the showcase. |
| `pl_utils.py` | **Shared module** — import from here; don't duplicate. |
| `analyze_players.py` / `analyze_teams.py` | Chart generators → `output/*.png` |
| `build_report.py` | Assembles `output/pl_analysis_report.html` |
| `pl_dashboard.py` | Standalone `rich` terminal dashboard (no file output) |
| `Premier League.ipynb` | Exploratory notebook (loads from `data/`) |

## Run order

```bash
python analyze_players.py     # → 3 player PNGs in output/
python analyze_teams.py       # → 3 team PNGs in output/
python build_report.py        # needs the 6 PNGs above → HTML
python pl_dashboard.py         # standalone; not part of the report pipeline
```

`build_report.py` reads the 6 PNGs from `output/`, so **always run the two
`analyze_*` scripts first** — it raises a clear error listing any missing charts.

## `pl_utils.py` — the shared module (reuse it)

Everything common lives here; refactor into it rather than copy-pasting:
- **Paths** — `PROJECT_DIR`, `DATA_DIR`, `OUTPUT_DIR` (all relative via `Path(__file__)`;
  `OUTPUT_DIR` auto-created). No absolute machine paths anywhere in this project.
- `setup_utf8_stdout()` — call first in every script; fixes Windows `cp1252`
  `UnicodeEncodeError` on Arabic / en-dash / emoji prints.
- `COLORS`, `BG`, `GRID_COLOR`, `SEASON` — the shared palette/labels.
- `load_players()` / `load_teams()` — cleaned DataFrames (numeric coercion,
  `Playing Time_MP > 0` filter). Use these instead of re-reading CSVs.
- `style_ax()`, `add_bar_labels()`, `save_chart()` — matplotlib helpers.
- `matplotlib.use("Agg")` is set here (headless PNG saving) — import order matters,
  so import `pl_utils` before `matplotlib.pyplot` in new scripts.

## Environment

- Windows 11, PowerShell 7. `python` resolves to the Microsoft Store build whose
  packages live in the **user site** — install with `pip install --user <pkg>`
  (`uv pip install --system` fails: Program Files is read-only).
- Dependencies: `pandas`, `numpy`, `matplotlib`, `rich` (see `requirements.txt`).

## Data gotchas

- Player CSV (`Squad_PlayerStats__stats_standard.csv`) has a junk trailing `Matches`
  column literally containing the string `"Matches"` — ignore it.
- `build_report.py` computes all "Key Numbers" stat cards **from the data**
  (top scorer, assister, G+A, most team goals, fewest conceded, champion). Never
  hardcode these — the old version did, and the report silently lied when data changed.
- The league-zone coloring (CL / EL / Conference / relegation) assumes exactly
  **20 teams sorted by points descending** (standard PL table). Revisit if the
  dataset shape changes.
- A full 38-game season: team-chart x-axis caps at 38 (not 42).

## Delivery

Own git remote: `github.com/Vanturki/PremierLeague`. Per workspace rules, branch
before changing, and open a PR instead of pushing to `main`.
