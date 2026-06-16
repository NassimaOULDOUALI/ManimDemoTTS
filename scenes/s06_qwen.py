"""
s06_qwen.py — Scène 6 : Architecture QwenA + QwenB (~50s)
==========================================================
v2 (branche vivatech_v2) — corrections layout :
  - Slide 1 : titre rescalé, val_labels positionnés depuis ax.c2p
  - Slide 2 : pipeline sur 3 lignes (input / QwenA / output),
              tokens rescalés pour tenir dans le frame
  - Slide 3 : blocs SSML côte-à-côte avec largeur fixe,
              MAE cards rescalées pour tenir dans le frame

Contraintes Manim v0.20.1 :
  - UpdateFromAlphaFunc pour les barres
  - Pas de stroke_opacity= → .set_stroke(opacity=...)
  - Pas d'aligned_edge=None dans .animate
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *


def token_box(text, color=WHITE_TXT, font_size=15, w=None):
    """Mini boîte token."""
    lbl = T(text, font_size=font_size, color=color)
    w = w or max(lbl.width + 0.22, 0.75)
    bg = RoundedRectangle(corner_radius=0.07, width=w, height=0.40,
                           fill_color=DARK_BOX, fill_opacity=1,
                           stroke_color=color, stroke_width=1.4)
    lbl.move_to(bg)
    return VGroup(bg, lbl)


class SceneQwen(Scene):
    def construct(self):

        FRAME_W = config.frame_width    # 14.22
        FRAME_H = config.frame_height   # 8.0

        # ══════════════════════════════════════════════════════════════
        # TITRE — rescalé pour tenir dans le frame
        # ══════════════════════════════════════════════════════════════
        title = section_title("Cascaded LLM Architecture: QwenA + QwenB") \
            .to_edge(UP, buff=0.45)
        if title.width > FRAME_W - 0.6:
            title.scale((FRAME_W - 0.6) / title.width)
        title.to_edge(UP, buff=0.45)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # ══════════════════════════════════════════════════════════════
        # SLIDE 1 : Sous-génération — barchart
        # ══════════════════════════════════════════════════════════════
        subtitle = T("Problem: LLMs under-generate SSML tags (all models, Figure 3)",
                     font_size=21, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.28)
        if subtitle.width > FRAME_W - 1.0:
            subtitle.scale((FRAME_W - 1.0) / subtitle.width)
        self.play(FadeIn(subtitle), run_time=0.5)

        ax_bar = Axes(
            x_range=[0, 8.0, 1], y_range=[0, 8.5, 2],
            x_length=7.5, y_length=3.2,
            axis_config={"color": GREY, "stroke_width": 1.5},
            x_axis_config={"include_ticks": False},
            tips=False,
        ).shift(DOWN * 0.5)

        y_label = T("<break> tags / segment", font_size=16, color=GREY).rotate(PI / 2)
        y_label.next_to(ax_bar, LEFT, buff=0.10)

        self.play(Create(ax_bar), FadeIn(y_label), run_time=0.7)

        bar_data = [
            ("Gold standard",   7.2, WHITE_TXT),
            ("Qwen3 32B (ZS)",  3.1, RED),
            ("Mistral 7B (ZS)", 2.4, RED),
            ("Our cascade",     7.1, GREEN),
        ]
        bar_xs = [1.3, 2.8, 4.3, 6.3]

        x_labels   = VGroup()
        all_bars   = VGroup()
        all_vlbls  = VGroup()

        for (name, val, col), bx in zip(bar_data, bar_xs):
            x_lbl = T(name, font_size=13, color=col)
            x_lbl.move_to(ax_bar.c2p(bx, 0) + DOWN * 0.45)
            x_labels.add(x_lbl)
        self.play(FadeIn(x_labels), run_time=0.4)

        for (name, val, col), bx in zip(bar_data, bar_xs):
            bar = Rectangle(width=0.80, height=0.001,
                            fill_color=col, fill_opacity=0.85, stroke_width=0)
            bottom_y = ax_bar.c2p(bx, 0)[1]
            top_y    = ax_bar.c2p(bx, val)[1]
            bar_x    = ax_bar.c2p(bx, 0)[0]

            def make_upd(by=bottom_y, ty=top_y, bxc=bar_x, c=col):
                def upd(mob, alpha):
                    h = max(0.001, (ty - by) * alpha)
                    mob.become(
                        Rectangle(width=0.80, height=h,
                                  fill_color=c, fill_opacity=0.85, stroke_width=0)
                        .move_to(np.array([bxc, by + h / 2, 0]))
                    )
                return upd

            bar.move_to(np.array([bar_x, bottom_y, 0]))
            self.add(bar)
            all_bars.add(bar)
            self.play(UpdateFromAlphaFunc(bar, make_upd(), run_time=0.65, rate_func=smooth))

            v_lbl = T(f"{val}", font_size=17, color=col, weight=BOLD)
            v_lbl.move_to(ax_bar.c2p(bx, val) + UP * 0.22)
            self.add(v_lbl)
            all_vlbls.add(v_lbl)

        equal_lbl = T("Our method ≈ Gold ✓", font_size=17, color=GREEN, weight=BOLD)
        equal_lbl.move_to(ax_bar.c2p(6.3, 7.1) + UP * 0.65 + RIGHT * 0.8)
        self.play(FadeIn(equal_lbl, shift=LEFT * 0.1), run_time=0.5)
        self.wait(2.0)

        self.play(
            FadeOut(VGroup(ax_bar, y_label, x_labels,
                           all_bars, all_vlbls, equal_lbl, subtitle)),
            run_time=0.7,
        )

        # ══════════════════════════════════════════════════════════════
        # SLIDE 2 : QwenA — layout vertical (3 lignes)
        #   ligne 1 : input tokens
        #   ligne 2 : flèche → QwenA → flèche
        #   ligne 3 : output tokens
        # ══════════════════════════════════════════════════════════════
        subtitle2 = T("Stage 1 — QwenA: Break Prediction (QLoRA, Qwen 2.5-7B)",
                      font_size=21, color=CYAN)
        subtitle2.next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(subtitle2), run_time=0.5)

        # ── Input tokens (ligne haute) ───────────────────────────────
        input_words = ["Bonjour,", "je", "m'appelle", "Bertrand", "Perier..."]
        input_tokens = VGroup(*[token_box(w, WHITE_TXT) for w in input_words])
        input_tokens.arrange(RIGHT, buff=0.10)
        max_tok_w = FRAME_W - 1.2
        if input_tokens.width > max_tok_w:
            input_tokens.scale(max_tok_w / input_tokens.width)
        input_tokens.move_to(UP * 1.8)

        lbl_in = T("Input text", font_size=16, color=GREY)
        lbl_in.next_to(input_tokens, UP, buff=0.12)

        self.play(FadeIn(lbl_in),
                  LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in input_tokens],
                              lag_ratio=0.10),
                  run_time=0.7)

        # ── QwenA block (centre) ─────────────────────────────────────
        qwen_a = RoundedRectangle(
            corner_radius=0.18, width=3.2, height=1.55,
            fill_color=DARK_BOX, fill_opacity=1,
            stroke_color=CYAN, stroke_width=3,
        )
        qwen_a_lbl = T("QwenA", font_size=24, color=CYAN, weight=BOLD)
        qwen_a_sub = T("QLoRA rank=8 α=16 · Frozen Qwen2.5-7B", font_size=13, color=GREY)
        if qwen_a_sub.width > 3.0:
            qwen_a_sub.scale(3.0 / qwen_a_sub.width)
        qwen_a_content = VGroup(qwen_a_lbl, qwen_a_sub).arrange(DOWN, buff=0.10)
        qwen_a_content.move_to(qwen_a)
        qwen_a_box = VGroup(qwen_a, qwen_a_content)
        qwen_a_box.move_to(ORIGIN + DOWN * 0.05)

        # Flèches verticales input→QwenA→output
        arr_down_in = Arrow(
            input_tokens.get_bottom() + DOWN * 0.05,
            qwen_a_box.get_top() + UP * 0.05,
            color=GREY, stroke_width=2.5, tip_length=0.18,
        )

        self.play(GrowArrow(arr_down_in), FadeIn(qwen_a_box), run_time=0.7)

        # Ghost tokens traversent QwenA
        ghost = input_tokens.copy()
        self.play(
            ghost.animate.move_to(qwen_a_box.get_center()).set_opacity(0).scale(0.4),
            run_time=0.5, rate_func=rush_into,
        )

        # ── Output tokens (ligne basse) ──────────────────────────────
        output_words  = ["Bonjour,", "<break>", "je", "m'appelle", "Bertrand", "Perier..."]
        output_colors = [WHITE_TXT, RED, WHITE_TXT, WHITE_TXT, WHITE_TXT, WHITE_TXT]
        output_tokens = VGroup(*[
            token_box(w, col) for w, col in zip(output_words, output_colors)
        ])
        output_tokens.arrange(RIGHT, buff=0.09)
        if output_tokens.width > max_tok_w:
            output_tokens.scale(max_tok_w / output_tokens.width)
        output_tokens.move_to(DOWN * 2.0)

        lbl_out = T("Break-tagged text", font_size=16, color=GREY)
        lbl_out.next_to(output_tokens, DOWN, buff=0.12)

        arr_down_out = Arrow(
            qwen_a_box.get_bottom() + DOWN * 0.05,
            output_tokens.get_top() + UP * 0.05,
            color=GREY, stroke_width=2.5, tip_length=0.18,
        )

        self.play(GrowArrow(arr_down_out), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in output_tokens],
                        lag_ratio=0.08),
            FadeIn(lbl_out),
            run_time=0.8,
        )

        # Flash <break>
        break_tok = output_tokens[1]
        self.play(glow_flash(break_tok, color=RED, n=10, radius=0.22), run_time=0.5)

        # F1 badge à droite du bloc QwenA
        f1_badge = kpi_card("99.24%", "F1 score\n(vs BERT 92.06%)", GREEN, w=2.2, h=1.25)
        f1_badge.next_to(qwen_a_box, RIGHT, buff=0.55)
        self.play(FadeIn(f1_badge, shift=LEFT * 0.2), run_time=0.6)
        self.wait(2.0)

        self.play(
            FadeOut(VGroup(input_tokens, lbl_in, arr_down_in,
                           qwen_a_box, ghost,
                           arr_down_out, output_tokens, lbl_out,
                           f1_badge, subtitle2)),
            run_time=0.7,
        )

        # ══════════════════════════════════════════════════════════════
        # SLIDE 3 : QwenB — layout horizontal strict, largeurs fixes
        # ══════════════════════════════════════════════════════════════
        subtitle3 = T("Stage 2 — QwenB: Prosodic Coefficient Prediction",
                      font_size=21, color=GOLD)
        subtitle3.next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(subtitle3), run_time=0.5)

        # Largeurs fixes pour garantir pas de chevauchement
        # Layout : [empty_block(4.2)] [qwen_b(2.8)] [full_block(4.2)]
        # Total = 11.2 + 2 buffs de 0.4 = 12.0 → tient dans 14.22
        block_w   = 4.0
        qwenb_w   = 2.8
        buf       = 0.45

        empty_ssml = TM(
            '<prosody rate="_%" pitch="_%" vol="%">\n'
            '  Bonjour,\n</prosody>\n'
            '<break time="_ms"/>',
            font_size=17, color=GREY,
        )
        full_ssml = TM(
            '<prosody rate="+5%" pitch="-7%" vol="-10%">\n'
            '  Bonjour,\n</prosody>\n'
            '<break time="500ms"/>',
            font_size=17, color=CYAN,
        )

        # Rescale si le texte dépasse block_w
        for mob in (empty_ssml, full_ssml):
            if mob.width > block_w - 0.30:
                mob.scale((block_w - 0.30) / mob.width)

        def ssml_box(ssml_mob, border_color, label_str, label_color):
            bg = RoundedRectangle(
                corner_radius=0.12, width=block_w, height=1.90,
                fill_color=DARK_BOX, fill_opacity=1,
                stroke_color=border_color, stroke_width=2,
            )
            ssml_mob.move_to(bg)
            lbl = T(label_str, font_size=15, color=label_color)
            lbl.next_to(bg, UP, buff=0.12)
            return VGroup(bg, ssml_mob), lbl

        empty_group, lbl_empty = ssml_box(
            empty_ssml, GREY,
            "Empty SSML skeleton (from QwenA)", GREY,
        )
        full_group, lbl_full = ssml_box(
            full_ssml, CYAN,
            "Full SSML (QwenB fills values)", CYAN,
        )

        # QwenB block
        qwen_b = RoundedRectangle(
            corner_radius=0.18, width=qwenb_w, height=1.55,
            fill_color=DARK_BOX, fill_opacity=1,
            stroke_color=GOLD, stroke_width=3,
        )
        qwen_b_lbl = T("QwenB", font_size=22, color=GOLD, weight=BOLD)
        qwen_b_sub = T("Regression on\nnumeric tokens", font_size=13, color=GREY)
        qwen_b_content = VGroup(qwen_b_lbl, qwen_b_sub).arrange(DOWN, buff=0.10)
        qwen_b_content.move_to(qwen_b)
        qwen_b_box = VGroup(qwen_b, qwen_b_content)

        # Positions absolues centrées
        total_w   = block_w + buf + qwenb_w + buf + block_w
        x_empty   = -total_w / 2 + block_w / 2
        x_qwenb   = x_empty + block_w / 2 + buf + qwenb_w / 2
        x_full    = x_qwenb + qwenb_w / 2 + buf + block_w / 2
        y_blocks  = DOWN * 0.20

        empty_group.move_to(np.array([x_empty, y_blocks[1], 0]))
        lbl_empty.next_to(empty_group, UP, buff=0.12)
        qwen_b_box.move_to(np.array([x_qwenb, y_blocks[1], 0]))
        full_group.move_to(np.array([x_full, y_blocks[1], 0]))
        lbl_full.next_to(full_group, UP, buff=0.12)

        arr_b_in  = Arrow(
            empty_group.get_right() + RIGHT * 0.05,
            qwen_b_box.get_left() - RIGHT * 0.05,
            color=GREY, stroke_width=2.5, tip_length=0.16,
        )
        arr_b_out = Arrow(
            qwen_b_box.get_right() + RIGHT * 0.05,
            full_group.get_left() - RIGHT * 0.05,
            color=GREY, stroke_width=2.5, tip_length=0.16,
        )

        self.play(FadeIn(lbl_empty), FadeIn(empty_group, shift=RIGHT * 0.12), run_time=0.6)
        self.play(GrowArrow(arr_b_in), FadeIn(qwen_b_box), run_time=0.6)
        self.play(GrowArrow(arr_b_out), run_time=0.4)
        self.play(FadeIn(lbl_full), FadeIn(full_group, shift=LEFT * 0.12), run_time=0.6)
        self.play(glow_flash(full_group, color=CYAN, n=12, radius=0.5), run_time=0.5)

        # MAE cards — 4 cartes sous le bloc central, rescalées pour tenir
        mae_cards = VGroup(
            kpi_card("0.97%",  "Pitch MAE",  CYAN,  w=2.0, h=1.15),
            kpi_card("1.09%",  "Volume MAE", GOLD,  w=2.0, h=1.15),
            kpi_card("1.10%",  "Rate MAE",   GREEN, w=2.0, h=1.15),
            kpi_card("132.9ms","Break MAE",  RED,   w=2.0, h=1.15),
        )
        mae_cards.arrange(RIGHT, buff=0.22)
        if mae_cards.width > FRAME_W - 0.8:
            mae_cards.scale((FRAME_W - 0.8) / mae_cards.width)
        mae_cards.next_to(empty_group, DOWN, buff=0.45)
        # Recentrer horizontalement
        mae_cards.move_to(np.array([0, mae_cards.get_center()[1], 0]))

        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.18) for c in mae_cards],
                        lag_ratio=0.16),
            run_time=1.0,
        )
        self.wait(3.5)

        self.play(
            FadeOut(VGroup(title, subtitle3,
                           empty_group, lbl_empty, arr_b_in,
                           qwen_b_box, arr_b_out,
                           full_group, lbl_full, mae_cards)),
            run_time=1.0,
        )