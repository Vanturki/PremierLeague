# Premier League Data Analysis 🏴󠁧󠁢󠁥󠁮󠁧󠁿⚽

A data analysis project exploring Premier League **2024–25** statistics — player
performance, team standings, and goal contributions. Built entirely with Python
and exported as a self-contained interactive HTML report, plus a `rich` terminal
dashboard.

## 📊 Project Overview

This project analyzes Premier League data to uncover insights about:
- Top goal scorers and assist leaders
- Best attacking and defensive teams
- Win/Draw/Loss breakdown per team
- Overall goal contributions per player

## 📁 Project Structure

| Path | Description |
|------|-------------|
| `pl_utils.py` | Shared module: paths, color palette, data loaders, chart helpers |
| `analyze_players.py` | Player charts → `output/top10_*.png` |
| `analyze_teams.py` | Team charts → `output/teams_*.png` |
| `build_report.py` | Assembles the final `output/pl_analysis_report.html` |
| `pl_dashboard.py` | Animated `rich` terminal dashboard |
| `Premier League.ipynb` | Exploratory analysis notebook |
| `data/` | Source CSVs (FBref-style, bundled so the repo runs on a fresh clone) |
| `output/` | Generated charts + HTML report |

## 📈 Sample Visualizations

- Top 10 Goals Scored / Assists / Goal Contributions (G+A)
- Top 5 Teams by Goals Scored
- Top 5 Best Defense Teams
- Win/Draw/Loss Breakdown (all 20 teams)

## 🛠️ Tools & Technologies

- **Language:** Python
- **Libraries:** Pandas, NumPy, Matplotlib, Rich
- **Output:** Self-contained HTML report + terminal dashboard
- **Version Control:** Git & GitHub

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/Vanturki/PremierLeague.git
cd PremierLeague

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate the charts (writes to output/)
python analyze_players.py
python analyze_teams.py

# 4. Build the HTML report (needs the 6 charts above first)
python build_report.py
# → open output/pl_analysis_report.html

# 5. (Optional) Run the terminal dashboard
python pl_dashboard.py
```

## 👤 Author
Turki Alotaibi
github.com/Vanturki
