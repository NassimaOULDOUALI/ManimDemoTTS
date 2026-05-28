"""
s02_speech.py — Scène 2 : La parole humaine (~40s)
===================================================
v2 (branche vivatech_v2) :
  - Slide 3 redessinée : cartes KPI avec texte qui ne déborde pas
    → texte multi-lignes, font_size réduit, padding explicite,
      largeur/hauteur calculées pour contenir le contenu
  - Reste de la scène inchangé

Contraintes Manim v0.20.1 :
  - Pas de stroke_opacity= → .set_stroke(opacity=...)
  - Pas d'aligned_edge=None dans .animate
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *


# ─────────────────────────────────────────────────────────────────────────────
# HELPER : carte prosody propre, texte garanti dans le bg
# ─────────────────────────────────────────────────────────────────────────────
def prosody_card(
    title_str: str,
    line1_str: str,
    line2_str: str,
    color,
    card_w: float = 3.2,
    card_h: float = 2.15,
    pad: float = 0.22,          # padding intérieur horizontal
    title_fs: int = 22,
    body_fs: int = 16,
    sub_fs: int = 14,
) -> VGroup:
    """
    Carte prosody auto-dimensionnée.
    Le texte est wrappé manuellement et la hauteur de la carte
    s'adapte si le contenu dépasse card_h.
    """
    inner_w = card_w - 2 * pad   # largeur utile pour le texte

    # ── Textes ──────────────────────────────────────────────────────
    head = T(title_str, font_size=title_fs, color=color, weight=BOLD)
    l1   = T(line1_str, font_size=body_fs,  color=WHITE_TXT)
    l2   = T(line2_str, font_size=sub_fs,   color=GREY)

    # Forcer le texte à tenir dans inner_w
    for mob in (head, l1, l2):
        if mob.width > inner_w:
            mob.scale(inner_w / mob.width)

    content = VGroup(head, l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)

    # Hauteur effective = contenu + 2×padding vertical
    effective_h = max(card_h, content.height + 2 * pad)

    # ── Background ──────────────────────────────────────────────────
    bg = RoundedRectangle(
        corner_radius=0.16,
        width=card_w,
        height=effective_h,
        fill_color=DARK_BOX,
        fill_opacity=1,
        stroke_color=color,
        stroke_width=2.5,
    )

    # Centrer le contenu dans le bg (légèrement vers le haut pour équilibre optique)
    content.move_to(bg.get_center())

    return VGroup(bg, content)


# =============================================================================
# SCÈNE
# =============================================================================

class SceneSpeech(Scene):
    def construct(self):

        # ══════════════════════════════════════════════════════════════
        # TITRE
        # ══════════════════════════════════════════════════════════════
        title = section_title("The Human Voice").to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # ══════════════════════════════════════════════════════════════
        # SLIDE 1 : Harmoniques qui s'additionnent
        # ══════════════════════════════════════════════════════════════
        subtitle = T("Voice = fundamental frequency F₀ + harmonics",
                     font_size=26, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.32)
        self.play(FadeIn(subtitle), run_time=0.5)

        ax = axes_xy([0, 1, 0.25], [-1.3, 1.3, 0.5],
                     x_len=9.0, y_len=2.6).shift(DOWN * 0.2)
        x_lbl = T("Time", font_size=19, color=GREY).next_to(ax, DOWN, buff=0.12).to_edge(RIGHT, buff=1.0)
        y_lbl = T("Amplitude", font_size=19, color=GREY).next_to(ax, LEFT, buff=0.12).rotate(PI / 2)

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)

        harm_colors = [CYAN, GOLD, GREEN, RED]
        harm_coeffs = [(1, 0.55), (2, 0.28), (3, 0.14), (4, 0.07)]
        F0 = 200

        def cumulative(t, n_harmonics):
            return sum(
                c * np.sin(2 * np.pi * k * F0 * t)
                for k, c in harm_coeffs[:n_harmonics]
            )

        graphs = []
        for n in range(1, 5):
            col = harm_colors[n - 1]
            g = ax.plot(lambda t, n=n: cumulative(t, n),
                        x_range=[0, 1, 0.0005],
                        color=col, stroke_width=2.5)
            graphs.append(g)

        harm_labels = VGroup()
        for i, (col, (k, _)) in enumerate(zip(harm_colors, harm_coeffs)):
            lbl = T(f"+ harmonic {k}" if k > 1 else "Fundamental F₀",
                    font_size=18, color=col)
            harm_labels.add(lbl)
        harm_labels.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        harm_labels.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)

        current_graph = None
        for i, g in enumerate(graphs):
            if current_graph:
                self.play(
                    Transform(current_graph, g),
                    FadeIn(harm_labels[i], shift=LEFT * 0.1),
                    run_time=0.8,
                )
            else:
                self.play(
                    Create(g),
                    FadeIn(harm_labels[0], shift=LEFT * 0.1),
                    run_time=1.0,
                )
                current_graph = g

        self.wait(1.5)

        caption_harm = T("The richer the harmonics → the more expressive the voice",
                         font_size=21, color=GREY)
        caption_harm.next_to(ax, DOWN, buff=0.3)
        self.play(FadeIn(caption_harm), run_time=0.6)
        self.wait(2.0)

        self.play(
            FadeOut(VGroup(ax, current_graph, x_lbl, y_lbl,
                           harm_labels, caption_harm, subtitle)),
            run_time=0.8,
        )

        # ══════════════════════════════════════════════════════════════
        # SLIDE 2 : F0 naturelle vs synthétique
        # ══════════════════════════════════════════════════════════════
        subtitle2 = T("F₀ contour: Natural speech vs TTS", font_size=26, color=GREY)
        subtitle2.next_to(title, DOWN, buff=0.32)
        self.play(FadeIn(subtitle2), run_time=0.5)

        ax2 = axes_xy([0, 1, 0.25], [60, 300, 60],
                      x_len=9.0, y_len=3.2).shift(DOWN * 0.3)
        x2_lbl = T("Time (s)", font_size=19, color=GREY).next_to(ax2, DOWN, buff=0.12).to_edge(RIGHT, buff=1.0)
        y2_lbl = T("F₀ (Hz)", font_size=19, color=GREY).next_to(ax2, LEFT, buff=0.12).rotate(PI / 2)

        self.play(Create(ax2), FadeIn(x2_lbl), FadeIn(y2_lbl), run_time=0.7)

        f0_nat = ax2.plot(f0_curve, x_range=[0.03, 0.97, 0.004],
                          color=CYAN, stroke_width=3)

        def f0_synth(t):
            return 140 + 8 * np.sin(2 * np.pi * 0.8 * t)

        f0_syn = ax2.plot(f0_synth, x_range=[0, 1, 0.005],
                          color=RED, stroke_width=2.5)
        f0_syn.set_opacity(0.85)

        lbl_nat = T("Natural speech", font_size=21, color=CYAN, weight=BOLD)
        lbl_syn = T("Commercial TTS (baseline)", font_size=21, color=RED, weight=BOLD)
        lbl_nat.to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        lbl_syn.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.5)

        self.play(Create(f0_nat), FadeIn(lbl_nat), run_time=1.5)
        self.wait(0.4)
        self.play(Create(f0_syn), FadeIn(lbl_syn), run_time=1.2)
        self.wait(0.5)

        flat_zone = Rectangle(
            width=9.0, height=0.6,
            fill_color=RED, fill_opacity=0.10,
            stroke_color=RED, stroke_width=1.5,
        )
        flat_zone.set_stroke(opacity=0.5)
        flat_zone.move_to(ax2.c2p(0.5, 140))

        flat_label = T("⚠  Monotonous — no expressive variation",
                       font_size=20, color=RED)
        flat_label.next_to(flat_zone, DOWN, buff=0.15)

        self.play(FadeIn(flat_zone), run_time=0.6)
        self.play(FadeIn(flat_label, shift=UP * 0.1), run_time=0.5)
        self.wait(3.5)

        # ══════════════════════════════════════════════════════════════
        # SLIDE 3 : Les 4 paramètres prosodiques — cartes redessinées
        # ══════════════════════════════════════════════════════════════
        self.play(
            FadeOut(VGroup(ax2, f0_nat, f0_syn, x2_lbl, y2_lbl,
                           lbl_nat, lbl_syn, flat_zone, flat_label, subtitle2)),
            run_time=0.8,
        )

        subtitle3 = T("Prosody = 4 controllable parameters",
                      font_size=28, color=WHITE_TXT, weight=BOLD)
        subtitle3.next_to(title, DOWN, buff=0.38)
        self.play(FadeIn(subtitle3), run_time=0.5)

        # ── Données des 4 cartes ─────────────────────────────────────
        # line2 découpée en segments courts pour éviter le débordement
        params = [
            (
                "Pitch (F₀)", CYAN,
                "Perceived height\nof voice",
                "Intonation · questions\n· emphasis",
            ),
            (
                "Volume", GOLD,
                "Perceived intensity",
                "Prominence\n· emotional strength",
            ),
            (
                "Rate (Tempo)", GREEN,
                "Speed of\narticulation",
                "Urgency · clarity\n· rhythm",
            ),
            (
                "Breaks (Pauses)", RED,
                "Silences between\nphrases",
                "Structure\n· comprehension",
            ),
        ]

        # ── Construire les cartes ────────────────────────────────────
        cards = VGroup(*[
            prosody_card(
                title_str=p[0],
                line1_str=p[2],
                line2_str=p[3],
                color=p[1],
                card_w=3.1,
                card_h=2.20,
                pad=0.28,
                title_fs=22,
                body_fs=16,
                sub_fs=14,
            )
            for p in params
        ])

        # Espacement horizontal serré mais lisible
        cards.arrange(RIGHT, buff=0.22)
        # Centrer verticalement sous le subtitle
        cards.next_to(subtitle3, DOWN, buff=0.50)

        # Si les cartes dépassent le frame, rescaler l'ensemble
        frame_w = config.frame_width - 0.6
        if cards.width > frame_w:
            cards.scale(frame_w / cards.width)

        # ── Apparition en cascade ────────────────────────────────────
        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.22) for c in cards],
                lag_ratio=0.20,
            ),
            run_time=1.6,
        )

        # Pulse léger sur chaque carte (Indicate sur le bg uniquement)
        for card in cards:
            bg_mob = card[0]  # RoundedRectangle
            self.play(
                Indicate(bg_mob, scale_factor=1.04,
                         color=bg_mob.get_stroke_color()),
                run_time=0.30,
            )

        self.wait(3.0)

        self.play(
            FadeOut(VGroup(title, subtitle3, cards)),
            run_time=1.0,
        )