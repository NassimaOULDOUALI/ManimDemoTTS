"""
s03_tts.py — Scène 3 : TTS moderne & problème expressivité (~40s)
=================================================================
v2 (branche vivatech_v2) :
  - Slide 3 redessinée : cartes "problèmes SSML" sans overflow
    → titre + description en DOWN (pas RIGHT), padding explicite,
      rescale automatique si le texte dépasse la largeur utile

Contraintes Manim v0.20.1 :
  - Pas de stroke_opacity= → .set_stroke(opacity=...)
  - Pas d'aligned_edge=None dans .animate
  - Barres via UpdateFromAlphaFunc
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *


# ─────────────────────────────────────────────────────────────────────────────
# HELPER : carte "problème" propre
# ─────────────────────────────────────────────────────────────────────────────
def problem_card(
    title_str: str,
    desc_str: str,
    color,
    card_w: float = 7.8,
    card_h: float = 0.92,
    title_fs: int = 21,
    desc_fs: int = 17,
) -> VGroup:
    """
    Carte horizontale avec positionnement absolu.
    Layout : [sep | TITRE_ZONE | DESC_ZONE]
    Les deux zones ont des x fixes — aucun arrange entre elles.
    """
    # Zones absolues (en coordonnées locales, origine = centre du bg)
    sep_x_local    = -card_w / 2 + 0.28          # bord gauche + padding
    title_x_local  = sep_x_local + 0.06 + 0.18   # après sep + gap
    title_max_w    = 2.10                          # largeur max titre
    desc_x_local   = sep_x_local + 0.06 + title_max_w + 0.45  # après titre + gap
    desc_max_w     = card_w / 2 - 0.20            # reste jusqu'au bord droit

    bg = RoundedRectangle(
        corner_radius=0.14,
        width=card_w,
        height=card_h,
        fill_color=DARK_BOX,
        fill_opacity=1,
        stroke_color=color,
        stroke_width=1.8,
    )
    # Placer bg à l'origine pour travailler en coordonnées locales
    bg.move_to(ORIGIN)

    # Séparateur vertical
    sep = Rectangle(
        width=0.05, height=card_h * 0.55,
        fill_color=color, fill_opacity=0.75, stroke_width=0,
    )
    sep.move_to(np.array([sep_x_local, 0, 0]))

    # Titre — rescalé si trop large
    head = T(title_str, font_size=title_fs, color=color, weight=BOLD)
    if head.width > title_max_w:
        head.scale(title_max_w / head.width)
    # Ancré à gauche de la zone titre
    head.move_to(np.array([title_x_local + head.width / 2, 0, 0]))

    # Description — rescalée si trop large
    desc = T(desc_str, font_size=desc_fs, color=GREY)
    if desc.width > desc_max_w:
        desc.scale(desc_max_w / desc.width)
    # Ancré à gauche de la zone desc
    desc.move_to(np.array([desc_x_local + desc.width / 2, 0, 0]))

    return VGroup(bg, sep, head, desc)


# =============================================================================
# SCÈNE
# =============================================================================

class SceneTTS(Scene):
    def construct(self):

        # ══════════════════════════════════════════════════════════════
        # TITRE
        # ══════════════════════════════════════════════════════════════
        title = section_title("Modern TTS & The Expressivity Problem") \
            .to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # ══════════════════════════════════════════════════════════════
        # SLIDE 1 : Pipeline TTS simplifié
        # ══════════════════════════════════════════════════════════════
        subtitle = T("How a TTS system works", font_size=26, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.32)
        self.play(FadeIn(subtitle), run_time=0.5)

        stages = [
            ("Text\nInput",     WHITE_TXT, "\"Bonjour !\""),
            ("Text\nAnalysis",  CYAN,      "G2P · NLP"),
            ("Acoustic\nModel", CYAN,      "Pitch · Duration"),
            ("Vocoder",         GREEN,     "Waveform"),
            ("Audio\nOutput",   GOLD,      "🔊"),
        ]

        boxes = VGroup()
        for label, color, sub in stages:
            bg = RoundedRectangle(
                corner_radius=0.14, width=2.0, height=1.4,
                fill_color=DARK_BOX, fill_opacity=1,
                stroke_color=color, stroke_width=2,
            )
            head = T(label, font_size=19, color=color, weight=BOLD)
            sub_t = T(sub, font_size=15, color=GREY)
            content = VGroup(head, sub_t).arrange(DOWN, buff=0.10)
            content.move_to(bg)
            boxes.add(VGroup(bg, content))

        arrows = VGroup()
        pipeline = VGroup()
        for i, box in enumerate(boxes):
            pipeline.add(box)
            if i < len(boxes) - 1:
                arr = Arrow(RIGHT * 0.05, RIGHT * 0.55,
                            color=GREY, stroke_width=3,
                            tip_length=0.20, buff=0)
                pipeline.add(arr)
                arrows.add(arr)

        pipeline.arrange(RIGHT, buff=0.0)
        pipeline.next_to(subtitle, DOWN, buff=0.55)
        pipeline.scale_to_fit_width(config.frame_width - 0.8)

        self.play(FadeIn(boxes[0], shift=RIGHT * 0.2), run_time=0.5)
        for i in range(len(boxes) - 1):
            self.play(
                GrowArrow(arrows[i]),
                FadeIn(boxes[i + 1], shift=RIGHT * 0.2),
                run_time=0.45,
            )

        self.wait(0.6)

        prob_rect = SurroundingRectangle(boxes[2], color=RED,
                                         stroke_width=3, buff=0.12)
        prob_lbl = T("⚠  Prosody is hardcoded here", font_size=20, color=RED)
        prob_lbl.next_to(boxes[2], DOWN, buff=0.55)

        self.play(Create(prob_rect), FadeIn(prob_lbl, shift=UP * 0.1), run_time=0.8)
        self.wait(2.5)

        self.play(
            FadeOut(VGroup(pipeline, arrows, prob_rect, prob_lbl, subtitle)),
            run_time=0.8,
        )

        # ══════════════════════════════════════════════════════════════
        # SLIDE 2 : Baromètre intelligibilité vs expressivité
        # ══════════════════════════════════════════════════════════════
        subtitle2 = T("Commercial TTS: great clarity, poor expressivity",
                      font_size=25, color=GREY)
        subtitle2.next_to(title, DOWN, buff=0.32)
        self.play(FadeIn(subtitle2), run_time=0.5)

        bar_w = 5.5

        def make_bar(label, fill_ratio, color, y_pos):
            lbl = T(label, font_size=22, color=WHITE_TXT)
            bg = Rectangle(width=bar_w, height=0.38,
                            fill_color=DARK_BOX, fill_opacity=1,
                            stroke_color=GREY, stroke_width=1)
            fg = Rectangle(width=bar_w * fill_ratio, height=0.38,
                            fill_color=color, fill_opacity=0.85,
                            stroke_width=0)
            fg.align_to(bg, LEFT)
            pct = T(f"{int(fill_ratio * 100)}%", font_size=20, color=color, weight=BOLD)
            pct.next_to(bg, RIGHT, buff=0.2)
            lbl.next_to(bg, LEFT, buff=0.25)
            bar_group = VGroup(bg, fg, lbl, pct)
            bar_group.shift(UP * y_pos)
            return bar_group, fg

        bar_intel, fg_intel = make_bar("Intelligibility", 0.92, GREEN, 0.5)
        bar_expr,  fg_expr  = make_bar("Expressivity",   0.28, RED, -0.5)

        bars = VGroup(bar_intel, bar_expr).shift(DOWN * 0.2)

        self.play(
            FadeIn(VGroup(bar_intel[0], bar_intel[2], bar_intel[3]),
                   VGroup(bar_expr[0], bar_expr[2], bar_expr[3])),
            run_time=0.6,
        )

        fg_intel_anim = fg_intel.copy().set_width(0.01).align_to(bar_intel[0], LEFT)
        fg_expr_anim  = fg_expr.copy().set_width(0.01).align_to(bar_expr[0], LEFT)
        self.add(fg_intel_anim, fg_expr_anim)

        self.play(
            fg_intel_anim.animate.set_width(bar_w * 0.92).align_to(bar_intel[0], LEFT),
            run_time=1.2, rate_func=smooth,
        )
        self.play(
            fg_expr_anim.animate.set_width(bar_w * 0.28).align_to(bar_expr[0], LEFT),
            run_time=1.0, rate_func=smooth,
        )
        self.wait(0.4)

        gap_arrow = DoubleArrow(
            bar_expr[0].get_right() + RIGHT * 0.05 + UP * 0.19,
            bar_intel[0].get_right() + RIGHT * 0.05 + UP * 0.19,
            color=GOLD, stroke_width=2.5, tip_length=0.18, buff=0,
        )
        gap_lbl = T("Gap to close!", font_size=20, color=GOLD, weight=BOLD)
        gap_lbl.next_to(gap_arrow, RIGHT, buff=0.2)
        self.play(Create(gap_arrow), FadeIn(gap_lbl), run_time=0.8)
        self.wait(2.5)

        self.play(
            FadeOut(VGroup(bars, fg_intel_anim, fg_expr_anim,
                           gap_arrow, gap_lbl, subtitle2)),
            run_time=0.8,
        )

        # ══════════════════════════════════════════════════════════════
        # SLIDE 3 : Problèmes LLM + SSML — cartes redessinées
        # ══════════════════════════════════════════════════════════════
        subtitle3 = T("Why is automated SSML hard?", font_size=26, color=GREY)
        subtitle3.next_to(title, DOWN, buff=0.32)
        self.play(FadeIn(subtitle3), run_time=0.5)

        problems = [
            ("Manual markup", "Does not scale to large corpora",              RED),
            ("LLM zero-shot", "Under-generates tags (Figure 3 paper)",        RED),
            ("LLM few-shot",  "Inconsistent — architecture-dependent",        RED),
            ("BiLSTM",        "Good for rate, weak on volume",                GOLD),
        ]

        prob_cards = VGroup(*[
            problem_card(
                title_str=p[0],
                desc_str=p[1],
                color=p[2],
                card_w=7.8,
                card_h=0.92,
                title_fs=21,
                desc_fs=17,
            )
            for p in problems
        ])

        prob_cards.arrange(DOWN, buff=0.22)
        prob_cards.next_to(subtitle3, DOWN, buff=0.50)

        # Fallback : rescale si ça dépasse le frame
        frame_w = config.frame_width - 0.6
        if prob_cards.width > frame_w:
            prob_cards.scale(frame_w / prob_cards.width)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=RIGHT * 0.2) for c in prob_cards],
                lag_ratio=0.28,
            ),
            run_time=1.6,
        )
        self.wait(3.5)

        self.play(
            FadeOut(VGroup(title, subtitle3, prob_cards)),
            run_time=1.0,
        )