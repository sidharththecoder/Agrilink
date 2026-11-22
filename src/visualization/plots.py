"""Reusable matplotlib helpers. Notebooks may import these, or plot inline."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "reports" / "figures"


def save_figure(fig, name: str, dpi: int = 150) -> Path:
    """Save a figure under reports/figures/ and return the path."""
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    path = FIG_DIR / f"{name}.png"
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    return path


def bar_chart(series, title: str, xlabel: str, color: str = "#3B8F7B"):
    """Horizontal bar chart for a pandas Series (index = labels)."""
    fig, ax = plt.subplots(figsize=(9, 5))
    series.sort_values().plot(kind="barh", ax=ax, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    plt.tight_layout()
    return fig
