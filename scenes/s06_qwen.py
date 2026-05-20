"""
s06_qwen.py — Scène 6 : Architecture QwenA + QwenB (~50s)
==========================================================
Niveau : expert
Basé sur Figure 2 du papier + Section 4.4

Effets :
  - Tokens qui traversent QwenA (animation gauche→droite)
  - Placeholder SSML vide qui se remplit (QwenB)
  - Comparaison avant/après tags (under-generation LLM vs notre méthode)
  - QLoRA visualisation (paramètres gelés vs adaptés)
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *


def token_box(text, color=WHITE_TXT, font_size=16, w=None):
    """Mini boîte token."""
    lbl = T(text, font_size=font_size, color=color)
    w = w or max(lbl.width + 0.25, 0.9)
    bg = RoundedRectangle(corner_radius=0.08, width=w, height=0.44,
                           fill_color=DARK_BOX, fill_opacity=1,
                           stroke_color=color, stroke_width=1.5)
    lbl.move_to(bg)
    return VGroup(bg, lbl)


class SceneQwen(Scene):
    def construct(self):

        # ==============================================================
        # TITRE
        # ==============================================================
        title = section_title("Cascaded LLM Architecture: QwenA + QwenB") \
            .to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # ==============================================================
        # SLIDE 1 : Vue d'ensemble — pourquoi cascader ?
        # ==============================================================
        subtitle = T("Problem: LLMs under-generate SSML tags (all models, Figure 3)",
                     font_size=23, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.32)
        self.play(FadeIn(subtitle), run_time=0.5)

        # Visualisation sous-génération : Gold vs LLM
        bar_data = [
            ("Gold standard", 7.2, WHITE_TXT),
            ("Qwen3 32B (ZS)", 3.1, RED),
            ("Mistral 7B (ZS)", 2.4, RED),
            ("Our cascade",    7.1, GREEN),
        ]

        ax_bar = Axes(
            x_range=[0, 8.5, 1], y_range=[0, 4.5, 1],
            x_length=8.0, y_length=2.8,
            axis_config={"color": GREY, "stroke_width": 1.5},
            x_axis_config={"include_ticks": False},
            tips=False,
        ).shift(DOWN * 0.3)

        y_label = T("<break> tags / segment", font_size=18, color=GREY).rotate(PI / 2)
        y_label.next_to(ax_bar, LEFT, buff=0.12)

        self.play(Create(ax_bar), FadeIn(y_label), run_time=0.7)

        bar_xs = [1.5, 3.0, 4.5, 6.5]
        bars_grp  = VGroup()
        val_labels = VGroup()
        x_labels   = VGroup()

        for (name, val, col), bx in zip(bar_data, bar_xs):
            bar = Rectangle(width=0.85, height=0.001,
                            fill_color=col, fill_opacity=0.85, stroke_width=0)
            bars_grp.add(bar)

            v_lbl = T(f"{val}", font_size=18, color=col, weight=BOLD)
            val_labels.add(v_lbl)

            x_lbl = T(name, font_size=14, color=col)
            x_lbl.move_to(ax_bar.c2p(bx, -0.6))
            x_labels.add(x_lbl)

        self.play(FadeIn(x_labels), run_time=0.5)

        for bar, (_, val, col), v_lbl, bx in zip(bars_grp, bar_data, val_labels, bar_xs):
            bottom_y = ax_bar.c2p(bx, 0)[1]
            top_y    = ax_bar.c2p(bx, val)[1]
            bar_x    = ax_bar.c2p(bx, 0)[0]

            def make_updater(bx_=bx, by=bottom_y, ty=top_y, bxc=bar_x, c=col):
                def updater(mob, alpha):
                    h = max(0.001, (ty - by) * alpha)
                    mob.become(
                        Rectangle(width=0.85, height=h,
                                  fill_color=c, fill_opacity=0.85,
                                  stroke_width=0)
                        .move_to(np.array([bxc, by + h / 2, 0]))
                    )
                return updater

            bar.move_to(np.array([bar_x, bottom_y + 0.001, 0]))
            self.add(bar)
            self.play(
                UpdateFromAlphaFunc(bar, make_updater(), run_time=0.7, rate_func=smooth)
            )
            # Positionner le label au-dessus de la barre finale
            top_final = ax_bar.c2p(bx, val)[1]
            v_lbl.move_to(np.array([bar_x, top_final + 0.18, 0]))
            self.add(v_lbl)

        # Flèche "Our cascade = Gold"
        equal_lbl = T("Our method matches Gold ✓", font_size=18, color=GREEN, weight=BOLD)
        equal_lbl.to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        arr_eq = Arrow(equal_lbl.get_left() - RIGHT * 0.1,
                       val_labels[-1].get_right() + RIGHT * 0.05,
                       color=GREEN, stroke_width=2.5, tip_length=0.18)
        self.play(FadeIn(equal_lbl), GrowArrow(arr_eq), run_time=0.7)
        self.wait(2.0)

        self.play(
            FadeOut(VGroup(ax_bar, y_label, bars_grp, val_labels,
                           x_labels, equal_lbl, arr_eq, subtitle)),
            run_time=0.8,
        )

        # ==============================================================
        # SLIDE 2 : QwenA — Break prediction avec animation tokens
        # ==============================================================
        subtitle2 = T("Stage 1 — QwenA: Break Prediction (QLoRA, Qwen 2.5-7B)",
                      font_size=22, color=CYAN)
        subtitle2.next_to(title, DOWN, buff=0.32)
        self.play(FadeIn(subtitle2), run_time=0.5)

        # Input tokens
        input_words = ["Bonjour,", "je", "m'appelle", "Bertrand", "Perier..."]
        input_tokens = VGroup(*[token_box(w, WHITE_TXT) for w in input_words])
        input_tokens.arrange(RIGHT, buff=0.12)
        input_tokens.shift(LEFT * 3.5 + UP * 0.5)

        lbl_in = T("Input text", font_size=18, color=GREY)
        lbl_in.next_to(input_tokens, UP, buff=0.15)

        # QwenA block
        qwen_a = RoundedRectangle(
            corner_radius=0.20, width=3.0, height=1.8,
            fill_color=DARK_BOX, fill_opacity=1,
            stroke_color=CYAN, stroke_width=3,
        )
        qwen_a_lbl = T("QwenA", font_size=26, color=CYAN, weight=BOLD)
        qwen_a_sub = T("QLoRA rank=8 α=16\nFrozen Qwen2.5-7B", font_size=15, color=GREY)
        qwen_a_content = VGroup(qwen_a_lbl, qwen_a_sub).arrange(DOWN, buff=0.12)
        qwen_a_content.move_to(qwen_a)
        qwen_a_box = VGroup(qwen_a, qwen_a_content)
        qwen_a_box.shift(RIGHT * 0.2 + UP * 0.5)

        # Output tokens avec <break>
        output_words = ["Bonjour,", "<break>", "je", "m'appelle", "Bertrand", "Perier..."]
        output_colors = [WHITE_TXT, RED, WHITE_TXT, WHITE_TXT, WHITE_TXT, WHITE_TXT]
        output_tokens = VGroup(*[
            token_box(w, col)
            for w, col in zip(output_words, output_colors)
        ])
        output_tokens.arrange(RIGHT, buff=0.09)
        output_tokens.scale(0.88)
        output_tokens.shift(RIGHT * 3.8 + UP * 0.5)

        lbl_out = T("Break-tagged text", font_size=18, color=GREY)
        lbl_out.next_to(output_tokens, UP, buff=0.15)

        arr_a_in = Arrow(input_tokens.get_right() + RIGHT * 0.05,
                          qwen_a_box.get_left() - RIGHT * 0.05,
                          color=GREY, stroke_width=2.5, tip_length=0.18)
        arr_a_out = Arrow(qwen_a_box.get_right() + RIGHT * 0.05,
                           output_tokens.get_left() - RIGHT * 0.05,
                           color=GREY, stroke_width=2.5, tip_length=0.18)

        # F1 badge
        f1_badge = kpi_card("99.24%", "F1 score\n(vs BERT 92.06%)", GREEN, w=2.2, h=1.3)
        f1_badge.next_to(qwen_a_box, DOWN, buff=0.55)

        self.play(
            FadeIn(lbl_in),
            LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in input_tokens], lag_ratio=0.12),
            run_time=0.8,
        )
        self.play(GrowArrow(arr_a_in), FadeIn(qwen_a_box), run_time=0.7)

        # Tokens qui "traversent" QwenA — effet de processing
        ghost_tokens = input_tokens.copy()
        self.play(
            ghost_tokens.animate.move_to(qwen_a_box).set_opacity(0).scale(0.5),
            run_time=0.6, rate_func=rush_into,
        )

        self.play(GrowArrow(arr_a_out), run_time=0.4)
        self.play(
            LaggedStart(
                *[FadeIn(t, shift=RIGHT * 0.1) for t in output_tokens],
                lag_ratio=0.10,
            ),
            FadeIn(lbl_out),
            run_time=0.8,
        )

        # Flash sur le <break> token
        self.play(
            glow_flash(output_tokens[1], color=RED, n=10, radius=0.25),
            run_time=0.5,
        )
        self.play(FadeIn(f1_badge, shift=UP * 0.2), run_time=0.6)
        self.wait(2.0)

        self.play(
            FadeOut(VGroup(input_tokens, lbl_in, arr_a_in, qwen_a_box,
                           arr_a_out, output_tokens, lbl_out,
                           f1_badge, subtitle2, ghost_tokens)),
            run_time=0.8,
        )

        # ==============================================================
        # SLIDE 3 : QwenB — Prosodic regression
        # ==============================================================
        subtitle3 = T("Stage 2 — QwenB: Prosodic Coefficient Prediction",
                      font_size=22, color=GOLD)
        subtitle3.next_to(title, DOWN, buff=0.32)
        self.play(FadeIn(subtitle3), run_time=0.5)

        # Squelette SSML vide → plein
        empty_ssml = TM(
            '<prosody rate="_%" pitch="_%" volume="%">\n'
            '  Bonjour,\n</prosody>\n'
            '<break time="_ms"/>',
            font_size=20, color=GREY,
        )
        full_ssml = TM(
            '<prosody rate="+5%" pitch="-7%" volume="-10%">\n'
            '  Bonjour,\n</prosody>\n'
            '<break time="500ms"/>',
            font_size=20, color=CYAN,
        )

        lbl_empty = T("Empty SSML skeleton (from QwenA)", font_size=18, color=GREY)
        lbl_full = T("Full SSML (QwenB fills values)", font_size=18, color=CYAN)

        empty_bg = SurroundingRectangle(empty_ssml, color=DARK_BOX,
                                         fill_color=DARK_BOX, fill_opacity=0.9,
                                         buff=0.25, corner_radius=0.10)
        full_bg  = SurroundingRectangle(full_ssml,  color=CYAN,
                                         fill_color=DARK_BOX, fill_opacity=0.9,
                                         buff=0.25, corner_radius=0.10,
                                         stroke_width=2)

        empty_group = VGroup(empty_bg, empty_ssml)
        full_group  = VGroup(full_bg,  full_ssml)
        lbl_empty.next_to(empty_group, UP, buff=0.2)
        lbl_full.next_to(full_group,   UP, buff=0.2)

        empty_group.shift(LEFT * 3.2 + DOWN * 0.1)
        lbl_empty.shift(LEFT * 3.2)
        full_group.shift(RIGHT * 3.0 + DOWN * 0.1)
        lbl_full.shift(RIGHT * 3.0)

        # QwenB block central
        qwen_b = RoundedRectangle(
            corner_radius=0.20, width=2.6, height=1.6,
            fill_color=DARK_BOX, fill_opacity=1,
            stroke_color=GOLD, stroke_width=3,
        )
        qwen_b_lbl = T("QwenB", font_size=24, color=GOLD, weight=BOLD)
        qwen_b_sub = T("Regression on\nnumeric tokens", font_size=14, color=GREY)
        qwen_b_content = VGroup(qwen_b_lbl, qwen_b_sub).arrange(DOWN, buff=0.12)
        qwen_b_content.move_to(qwen_b)
        qwen_b_box = VGroup(qwen_b, qwen_b_content)
        qwen_b_box.shift(DOWN * 0.1)

        arr_b_in  = Arrow(empty_group.get_right() + RIGHT * 0.05,
                           qwen_b_box.get_left() - RIGHT * 0.05,
                           color=GREY, stroke_width=2.5, tip_length=0.18)
        arr_b_out = Arrow(qwen_b_box.get_right() + RIGHT * 0.05,
                           full_group.get_left() - RIGHT * 0.05,
                           color=GREY, stroke_width=2.5, tip_length=0.18)

        self.play(
            FadeIn(lbl_empty),
            FadeIn(empty_group, shift=RIGHT * 0.15),
            run_time=0.7,
        )
        self.play(GrowArrow(arr_b_in), FadeIn(qwen_b_box), run_time=0.6)
        self.play(GrowArrow(arr_b_out), run_time=0.4)
        self.play(
            FadeIn(lbl_full),
            FadeIn(full_group, shift=LEFT * 0.15),
            run_time=0.7,
        )
        self.play(glow_flash(full_group, color=CYAN, n=12, radius=0.5), run_time=0.6)

        # MAE badges en bas
        mae_cards = VGroup(
            kpi_card("0.97%", "Pitch MAE", CYAN, w=2.0, h=1.2),
            kpi_card("1.09%", "Volume MAE", GOLD, w=2.0, h=1.2),
            kpi_card("1.10%", "Rate MAE", GREEN, w=2.0, h=1.2),
            kpi_card("132.9ms", "Break MAE", RED, w=2.0, h=1.2),
        )
        mae_cards.arrange(RIGHT, buff=0.30)
        mae_cards.next_to(qwen_b_box, DOWN, buff=0.55)

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in mae_cards], lag_ratio=0.18),
            run_time=1.2,
        )
        self.wait(3.5)

        self.play(
            FadeOut(VGroup(title, subtitle3,
                           empty_group, lbl_empty, arr_b_in,
                           qwen_b_box, arr_b_out,
                           full_group, lbl_full, mae_cards)),
            run_time=1.0,
        )
