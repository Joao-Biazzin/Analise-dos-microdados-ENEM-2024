"""Estilo padrão dos gráficos do projeto.

Paleta e especificações seguem um sistema fixo (ordem categórica nunca ciclada,
sequencial = um matiz claro→escuro, divergente = azul↔vermelho com meio neutro).
Os PNGs são gerados em modo claro, com o fundo baked-in, para leitura estável
no README do GitHub.
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from . import config

# --- paleta (modo claro) ---
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"

# Ordem fixa: a sequência maximiza a separação para daltonismo — nunca reordenar
CATEGORICAL = [
    "#2a78d6",  # azul
    "#1baf7a",  # verde-água
    "#eda100",  # amarelo
    "#008300",  # verde
    "#4a3aa7",  # violeta
    "#e34948",  # vermelho
    "#e87ba4",  # magenta
    "#eb6834",  # laranja
]

BLUE = CATEGORICAL[0]
RED = CATEGORICAL[5]

_SEQ_BLUES = [
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
    "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b",
]
#: Sequencial (magnitude): um matiz, claro→escuro — mapas coropléticos, heatmaps
CMAP_SEQ = LinearSegmentedColormap.from_list("enem_blues", _SEQ_BLUES)

#: Divergente (polaridade): azul ↔ vermelho com meio neutro
CMAP_DIV = LinearSegmentedColormap.from_list(
    "enem_div", ["#0d366b", BLUE, "#f0efec", RED, "#7a1f1f"]
)


def setup() -> None:
    """Aplica o estilo padrão do projeto ao matplotlib/seaborn."""
    mpl.rcParams.update({
        "figure.facecolor": SURFACE,
        "figure.figsize": (9, 5),
        "figure.dpi": 110,
        "savefig.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "axes.edgecolor": BASELINE,
        "axes.labelcolor": INK_SECONDARY,
        "axes.titlecolor": INK,
        "axes.titlesize": 13,
        "axes.titleweight": "semibold",
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 1.0,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "text.color": INK,
        "font.family": ["Segoe UI", "DejaVu Sans", "sans-serif"],
        "axes.prop_cycle": mpl.cycler(color=CATEGORICAL),
        "lines.linewidth": 2.0,
        "lines.solid_joinstyle": "round",
        "lines.solid_capstyle": "round",
        "legend.frameon": False,
        "legend.fontsize": 9.5,
    })


def save_fig(fig: plt.Figure, name: str, figures_dir: Path | None = None) -> Path:
    """Salva a figura em reports/figures/<name>.png e devolve o caminho."""
    figures_dir = figures_dir or config.FIGURES_DIR
    figures_dir.mkdir(parents=True, exist_ok=True)
    path = figures_dir / f"{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    return path


def fmt_thousands(value: float, _pos=None) -> str:
    """Formata ticks com separador de milhar em padrão brasileiro (1.234.567)."""
    return f"{value:,.0f}".replace(",", ".")
