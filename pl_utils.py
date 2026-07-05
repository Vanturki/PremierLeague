"""
pl_utils.py — وحدة مشتركة لمشروع تحليل الدوري الإنجليزي الممتاز 2024-25
تجمع كل الأكواد المتكررة: المسارات، الألوان، تحميل البيانات، ودوال الرسم.
تستوردها بقية السكربتات بدل تكرار نفس الكود.
"""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # backend بدون واجهة رسومية — للحفظ المباشر كـ PNG
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

# ── المسارات (نسبية للمشروع، تعمل على أي جهاز) ──────────────────────────────────
PROJECT_DIR = Path(__file__).resolve().parent   # مجلد المشروع نفسه
DATA_DIR    = PROJECT_DIR / "data"              # ملفات CSV المصدر
OUTPUT_DIR  = PROJECT_DIR / "output"            # مخرجات: صور PNG + تقرير HTML
OUTPUT_DIR.mkdir(exist_ok=True)                 # ننشئ مجلد المخرجات إن لم يوجد

# ── الترميز (Windows يتعطل على العربية/الرموز بترميز cp1252) ─────────────────────
def setup_utf8_stdout():
    """يضبط مخرجات الطرفية على UTF-8 حتى لا تنهار على الشرطة الطويلة أو الرموز."""
    for stream in (sys.stdout, sys.stderr):
        # reconfigure متوفرة في Python 3.7+ — نحميها بـ try لأي حالة نادرة
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

# ── لوحة الألوان الموحّدة ────────────────────────────────────────────────────────
COLORS = {
    "goals":    "#E63946",   # أحمر — الأهداف
    "assists":  "#457B9D",   # أزرق — صناعة الأهداف
    "g_plus_a": "#2A9D8F",   # فيروزي — المساهمات (أهداف + صناعة)
    "draw":     "#E9C46A",   # ذهبي — التعادلات
    "loss":     "#E76F51",   # برتقالي — الخسائر
}
BG         = "#F8F9FA"       # خلفية الرسم
GRID_COLOR = "#DEE2E6"       # لون الشبكة
BAR_EDGE   = "white"         # حدود الأعمدة
SEASON     = "Premier League 2024-25 Season"   # نص الموسم أسفل كل رسم

# ── تحميل البيانات (تنظيف موحّد) ─────────────────────────────────────────────────
def load_players():
    """يحمّل إحصائيات اللاعبين وينظّفها: تحويل رقمي + استبعاد من لم يلعب أي مباراة."""
    df = pd.read_csv(DATA_DIR / "Squad_PlayerStats__stats_standard.csv")
    df["Goals"]         = pd.to_numeric(df["Performance_Gls"], errors="coerce").fillna(0)
    df["Assists"]       = pd.to_numeric(df["Performance_Ast"], errors="coerce").fillna(0)
    df["Contributions"] = df["Goals"] + df["Assists"]           # المساهمات G+A
    df = df[df["Playing Time_MP"] > 0].copy()                   # فقط من خاض مباريات
    return df

def load_teams():
    """يحمّل جدول ترتيب الفرق (النظرة العامة) ويحوّل الأعمدة الرقمية."""
    df = pd.read_csv(DATA_DIR / "overwiev__results2024-202591_overall.csv")
    for col in ["MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

# ── دوال الرسم المشتركة ──────────────────────────────────────────────────────────
def style_ax(ax, title, xlabel):
    """تنسيق موحّد لأي محور: عنوان، شبكة أفقية، إخفاء الحدود الزائدة."""
    ax.set_title(title, fontsize=15, fontweight="bold", pad=14)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel("")
    ax.tick_params(axis="both", labelsize=10)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))  # أرقام صحيحة فقط
    ax.set_facecolor(BG)
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.spines[["top", "right", "left"]].set_visible(False)

def add_bar_labels(ax, offset=0.3):
    """يكتب قيمة كل عمود أفقي عند نهايته."""
    for bar in ax.patches:
        w = bar.get_width()
        if w > 0:
            ax.text(w + offset, bar.get_y() + bar.get_height() / 2,
                    f"{int(w)}", va="center", ha="left", fontsize=9, color="#333")

def save_chart(fig, filename):
    """يحفظ الشكل في مجلد output/ ويطبع المسار."""
    path = OUTPUT_DIR / filename
    fig.text(0.13, 0.92, SEASON, fontsize=9, color="#777")   # نص الموسم
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")
