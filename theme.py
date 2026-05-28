"""
theme.py — Palette, helpers et utilitaires partagés
=====================================================
Importer dans chaque scène :
    from theme import *
"""

from manim import *
import numpy as np
from pathlib import Path

# ============================================================
# PALETTE Hi! PARIS
# ============================================================
BG        = "#004178"
RED       = "#FF0049"
CYAN      = "#14B8FF"
GOLD      = "#FFD166"
GREEN     = "#06D6A0"
PURPLE    = "#A855F7"
WHITE_TXT = "#F4F6FA"
GREY      = "#EFEFEF"
DARK_BOX  = "#002B52"
FONT      = "Nunito"
FONT_TITLE = "Montserrat"   # titres (section_title, headers)
MONO      = "DejaVu Sans Mono"

# ============================================================
# CONFIG GLOBALE
# ============================================================
config.background_color = BG
np.random.seed(42)

ASSETS = Path(__file__).parent / "assets"


# ============================================================
# HELPERS TEXTE
# ============================================================

def T(s, **kw):
    """Text wrapper — force DejaVu Sans partout."""
    kw.setdefault("font", FONT)
    return Text(s, **kw)


def TM(s, **kw):
    """Monospace text — code / SSML."""
    kw.setdefault("font", MONO)
    return Text(s, **kw)


def section_title(txt: str, font_size: int = 42) -> VGroup:
    bar = Rectangle(
        width=0.10, height=0.70,
        fill_color=RED, fill_opacity=1, stroke_width=0,
    )
    label = Text(txt, font=FONT_TITLE, font_size=font_size,
                 color=WHITE_TXT, weight=BOLD)
    return VGroup(bar, label).arrange(RIGHT, buff=0.22, aligned_edge=LEFT)


def kpi_card(value: str, label: str, color=RED, w=3.0, h=1.6) -> VGroup:
    """Carte KPI avec valeur en gros et label en petit."""
    bg = RoundedRectangle(
        corner_radius=0.14, width=w, height=h,
        fill_color=DARK_BOX, fill_opacity=1,
        stroke_color=color, stroke_width=2,
    )
    val_txt = T(value, font_size=38, color=color, weight=BOLD)
    lbl_txt = T(label, font_size=18, color=GREY)
    content = VGroup(val_txt, lbl_txt).arrange(DOWN, buff=0.12)
    content.move_to(bg)
    return VGroup(bg, content)


def rounded_box(txt_lines: list, color=CYAN, w=3.5, h=2.0,
                title: str = None, title_size=26, body_size=20) -> VGroup:
    """Boîte arrondie générique."""
    bg = RoundedRectangle(
        corner_radius=0.18, width=w, height=h,
        fill_color=DARK_BOX, fill_opacity=1,
        stroke_color=color, stroke_width=2.5,
    )
    items = []
    if title:
        items.append(T(title, font_size=title_size, color=color, weight=BOLD))
    for line in txt_lines:
        items.append(T(line, font_size=body_size, color=WHITE_TXT))
    content = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    content.move_to(bg)
    return VGroup(bg, content)


# ============================================================
# HELPERS SIGNAL
# ============================================================

def sine_wave(amplitude=0.6, freq=2.0, phase=0.0,
              x_start=-6.5, x_end=6.5, n=500,
              color=CYAN, sw=3.0) -> VMobject:
    """Sinusoïde comme VMobject (dessin instantané)."""
    xs = np.linspace(x_start, x_end, n)
    ys = amplitude * np.sin(2 * np.pi * freq * (xs - x_start) / (x_end - x_start) + phase)
    pts = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
    path = VMobject(stroke_color=color, stroke_width=sw)
    path.set_points_smoothly(pts)
    return path


def speech_signal_func(t: float) -> float:
    """Signal de parole synthétique réaliste (fondamentale + harmoniques + enveloppe)."""
    f0 = 160
    env = np.exp(-2.5 * t) * (1 + 0.4 * np.sin(2 * np.pi * 2.5 * t))
    return env * (
        0.55 * np.sin(2 * np.pi * f0 * t)
        + 0.28 * np.sin(2 * np.pi * 2 * f0 * t)
        + 0.14 * np.sin(2 * np.pi * 3 * f0 * t)
        + 0.07 * np.sin(2 * np.pi * 4 * f0 * t)
        + 0.04 * np.sin(2 * np.pi * 5 * f0 * t)
    )


def f0_curve(t: float) -> float:
    """Contour F0 réaliste — montée interrogative française."""
    if t < 0.03 or t > 0.97:
        return 140
    base = 155 + 75 * np.sin(np.pi * t * 0.9)
    jitter = 5 * np.sin(41 * t) + 3 * np.sin(17 * t)
    return base + jitter


# ============================================================
# HELPERS ANIMATION
# ============================================================

def glow_flash(obj, color=RED, n=12, radius=0.35, length=0.20) -> Flash:
    return Flash(obj, flash_radius=radius, line_length=length,
                 color=color, num_lines=n)


def load_img(stem: str) -> ImageMobject:
    for ext in (".png", ".jpg", ".jpeg"):
        p = ASSETS / f"{stem}{ext}"
        if p.exists():
            return ImageMobject(str(p))
    raise FileNotFoundError(f"Image '{stem}' not found in assets/")


def axes_xy(x_range, y_range, x_len=9.0, y_len=3.0) -> Axes:
    return Axes(
        x_range=x_range, y_range=y_range,
        x_length=x_len, y_length=y_len,
        axis_config={"color": GREY, "stroke_width": 1.5},
        tips=False,
    )
