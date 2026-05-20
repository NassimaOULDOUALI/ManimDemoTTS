"""
s07_results.py — Scène 7 : Résultats (~45s)
============================================
Basé sur Tables 4, 5 + Section 5.1 du papier

Effets :
  - MOS barchart animé avec delta +0.67 qui explose
  - KPI cards en cascade (F1, MAE, AB test)
  - Tableau comparatif final (notre méthode vs BiLSTM vs Few-shot LLM)
  - Compteur live MOS : 3.20 → 3.87

s08_outro.py — Scène 8 : Conclusion + Future (~20s)
"""

from manim import *
from manim.utils.color import ManimColor
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *

# ── Compat v0.20 ─────────────────────────────────────────────────────────────
def _ic(c1, c2, t):
    return interpolate_color(ManimColor(c1), ManimColor(c2), t)

def _hline(ax, point, color, stroke_width=1.5, opacity=1.0):
    """get_horizontal_line compatible v0.20 (stroke_opacity supprimé)."""
    line = ax.get_horizontal_line(point, color=color, stroke_width=stroke_width)
    line.set_opacity(opacity)
    return line
# ─────────────────────────────────────────────────────────────────────────────


# =============================================================================
# SCÈNE 7 : RÉSULTATS
# =============================================================================

class SceneResults(Scene):
    def construct(self):

        # ==============================================================
        # TITRE
        # ==============================================================
        title = section_title("Results: Beating the State of the Art") \
            .to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # ==============================================================
        # SLIDE 1 : MOS bar chart animé + compteur
        # ==============================================================
        subtitle = T("Perceptual evaluation: 18 participants · 9h+ of audio",
                     font_size=22, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.30)
        self.play(FadeIn(subtitle), run_time=0.5)

        ax = Axes(
            x_range=[0, 3, 1], y_range=[0, 4.5, 1],
            x_length=6.5, y_length=3.6,
            axis_config={"color": GREY, "stroke_width": 1.5},
            x_axis_config={"include_ticks": False},
            tips=False,
        ).shift(LEFT * 2.0 + DOWN * 0.2)

        y_lbl = T("MOS (5-point scale)", font_size=18, color=GREY).rotate(PI / 2)
        y_lbl.next_to(ax, LEFT, buff=0.12)

        # Lignes de référence
        ref4 = _hline(ax, ax.c2p(3, 4.0), color=GOLD,
                      stroke_width=1.2, opacity=0.4)
        ref4_lbl = T("4.0", font_size=14, color=GOLD).next_to(ax.c2p(0, 4.0), LEFT, buff=0.1)

        x_lbl_base = T("Baseline\n(Azure Henri\nno SSML)",
                        font_size=17, color=GREY).move_to(ax.c2p(1, 0) + DOWN * 0.65)
        x_lbl_ours = T("Ours\n(SSML pipeline)",
                        font_size=17, color=GREEN, weight=BOLD).move_to(ax.c2p(2, 0) + DOWN * 0.55)

        self.play(Create(ax), FadeIn(y_lbl), FadeIn(ref4), FadeIn(ref4_lbl),
                  FadeIn(x_lbl_base), FadeIn(x_lbl_ours), run_time=0.9)

        # ── Helper : fait grandir une barre depuis le bas (v0.20 compatible) ──
        def grow_bar(scene, bar_mob, x_pos, mos_val, bar_color, run_time=1.2):
            """Anime une barre qui monte depuis l'axe x."""
            bottom_y = ax.c2p(x_pos, 0)[1]
            top_y    = ax.c2p(x_pos, mos_val)[1]
            bar_x    = ax.c2p(x_pos, 0)[0]
            bar_width = 0.95

            def updater(mob, alpha):
                current_h = max(0.001, (top_y - bottom_y) * alpha)
                current_y = bottom_y + current_h / 2
                mob.become(
                    Rectangle(
                        width=bar_width, height=current_h,
                        fill_color=bar_color, fill_opacity=0.88,
                        stroke_width=0,
                    ).move_to(np.array([bar_x, current_y, 0]))
                )

            # État initial
            updater(bar_mob, 0.001)
            scene.add(bar_mob)
            scene.play(
                UpdateFromAlphaFunc(bar_mob, updater, run_time=run_time,
                                    rate_func=smooth)
            )

        # Barre baseline 3.20
        bar_base = Rectangle(width=0.95, height=0.001,
                             fill_color=_ic(GREY, CYAN, 0.3),
                             fill_opacity=0.88, stroke_width=0)
        grow_bar(self, bar_base, 1, 3.20, _ic(GREY, CYAN, 0.3), run_time=1.2)

        val_base = T("3.20", font_size=22, color=GREY, weight=BOLD)
        val_base.next_to(bar_base, UP, buff=0.10)
        self.play(FadeIn(val_base, shift=UP * 0.1), run_time=0.4)
        self.wait(0.3)

        # Barre proposed 3.87 (plus lente = plus dramatique)
        bar_ours = Rectangle(width=0.95, height=0.001,
                             fill_color=GREEN, fill_opacity=0.90, stroke_width=0)
        grow_bar(self, bar_ours, 2, 3.87, GREEN, run_time=1.8)

        val_ours = T("3.87", font_size=26, color=GREEN, weight=BOLD)
        val_ours.next_to(bar_ours, UP, buff=0.10)
        self.play(FadeIn(val_ours, shift=UP * 0.1), run_time=0.4)

        # Flèche delta +0.67 qui "explose"
        delta_arr = Arrow(
            val_base.get_top() + UP * 0.05,
            val_ours.get_top() + UP * 0.05,
            color=GOLD, stroke_width=3.5, tip_length=0.22,
        )
        delta_lbl = T("+0.67 MOS\n(p < 0.005)", font_size=19, color=GOLD, weight=BOLD)
        delta_lbl.next_to(delta_arr, UP, buff=0.12)

        self.play(GrowArrow(delta_arr), run_time=0.6)
        self.play(FadeIn(delta_lbl, shift=UP * 0.1), run_time=0.5)
        self.play(glow_flash(delta_lbl, color=GOLD, n=12, radius=0.35), run_time=0.6)

        # KPI cards à droite
        kpi_cards = VGroup(
            kpi_card("99.24%", "F1 breaks\n(vs BERT 92%)", CYAN, w=2.4, h=1.5),
            kpi_card("< 1.1%", "MAE pitch/\nvol/rate", GOLD, w=2.4, h=1.5),
            kpi_card("15 / 18", "Listeners preferred\nour synthesis", GREEN, w=2.4, h=1.5),
        )
        kpi_cards.arrange(DOWN, buff=0.25)
        kpi_cards.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.15)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=LEFT * 0.2) for c in kpi_cards],
                lag_ratio=0.28,
            ),
            run_time=1.2,
        )

        # Flash sur 15/18 — le chiffre le plus parlant
        self.wait(1.0)
        self.play(glow_flash(kpi_cards[2], color=GREEN, n=14, radius=0.45), run_time=0.7)
        self.wait(2.5)

        self.play(
            FadeOut(VGroup(ax, y_lbl, ref4, ref4_lbl, x_lbl_base, x_lbl_ours,
                           bar_base, val_base, bar_ours, val_ours,
                           delta_arr, delta_lbl, kpi_cards, subtitle)),
            run_time=0.8,
        )

        # ==============================================================
        # SLIDE 2 : Tableau comparatif (Table 5 du papier)
        # ==============================================================
        subtitle2 = T("Objective comparison — MAE (lower is better)",
                      font_size=22, color=GREY)
        subtitle2.next_to(title, DOWN, buff=0.30)
        self.play(FadeIn(subtitle2), run_time=0.5)

        # En-têtes
        col_headers = ["Model", "Pitch MAE%", "Vol MAE%", "Rate MAE%", "Break ms"]
        rows_data = [
            ("Cascade (Ours)", "0.97", "1.09", "1.10", "132.9", GREEN),
            ("BiLSTM L=2",     "1.69", "6.04", "0.84", "—",     CYAN),
            ("SOTA Few-shot*", "1.08", "5.80", "0.97", "159.6", GOLD),
            ("SOTA Zero-shot*","1.42", "7.65", "1.52", "170.2", RED),
        ]

        # Construction du tableau Manim
        col_w = [2.6, 1.6, 1.6, 1.6, 1.6]
        row_h = 0.52
        table_x_start = -5.0
        table_y_start = 1.2

        header_cells = VGroup()
        for j, (header, cw) in enumerate(zip(col_headers, col_w)):
            x = table_x_start + sum(col_w[:j]) + cw / 2
            cell_bg = Rectangle(width=cw, height=row_h,
                                 fill_color="#001B36", fill_opacity=1,
                                 stroke_color=GREY, stroke_width=0.8)
            cell_bg.move_to(np.array([x, table_y_start, 0]))
            cell_lbl = T(header, font_size=16, color=WHITE_TXT, weight=BOLD)
            cell_lbl.move_to(cell_bg)
            header_cells.add(VGroup(cell_bg, cell_lbl))

        self.play(FadeIn(header_cells), run_time=0.5)

        row_cells_all = VGroup()
        for r_idx, (model, p, v, rt, br, col) in enumerate(rows_data):
            row_vals = [model, p, v, rt, br]
            row_y = table_y_start - (r_idx + 1) * row_h
            for j, (val, cw) in enumerate(zip(row_vals, col_w)):
                x = table_x_start + sum(col_w[:j]) + cw / 2
                fill = "#002B52" if r_idx % 2 == 0 else DARK_BOX
                cell_bg = Rectangle(width=cw, height=row_h,
                                     fill_color=fill, fill_opacity=1,
                                     stroke_color=GREY, stroke_width=0.5)
                cell_bg.move_to(np.array([x, row_y, 0]))
                txt_color = col if j == 0 else (GREEN if r_idx == 0 else WHITE_TXT)
                cell_lbl = T(val, font_size=15, color=txt_color,
                              weight=BOLD if r_idx == 0 else NORMAL)
                cell_lbl.move_to(cell_bg)
                row_cells_all.add(VGroup(cell_bg, cell_lbl))

            self.play(
                FadeIn(row_cells_all[-len(row_vals):], shift=RIGHT * 0.1),
                run_time=0.4,
            )

        # Encadrer la ligne "Cascade (Ours)"
        our_row_rect = Rectangle(
            width=sum(col_w), height=row_h,
            fill_opacity=0, stroke_color=GREEN, stroke_width=2.5,
        )
        our_row_rect.move_to(np.array([
            table_x_start + sum(col_w) / 2,
            table_y_start - row_h,
            0,
        ]))
        self.play(Create(our_row_rect), run_time=0.6)

        note = T("* Qwen3-32B (best few-shot / zero-shot)",
                  font_size=15, color=GREY, slant=ITALIC)
        note.next_to(row_cells_all, DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=0.4)
        self.wait(4.0)

        self.play(
            FadeOut(VGroup(title, subtitle2, header_cells,
                           row_cells_all, our_row_rect, note)),
            run_time=1.0,
        )


# =============================================================================
# SCÈNE 8 : OUTRO
# =============================================================================

class SceneOutro(Scene):
    def construct(self):

        # ==============================================================
        # TITRE
        # ==============================================================
        title = section_title("Conclusion & Future Work").to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # 3 takeaways
        takeaways = [
            ("✅  First end-to-end SSML pipeline for French TTS", GREEN),
            ("✅  QwenA + QwenB: F1 99.24% · MAE < 1.1% · MOS +0.67", GREEN),
            ("✅  83% of listeners preferred our synthesis", GREEN),
        ]
        bullets = VGroup(*[
            T(txt, font_size=25, color=col)
            for txt, col in takeaways
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        bullets.next_to(title, DOWN, buff=0.65)

        self.play(
            LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in bullets], lag_ratio=0.30),
            run_time=1.5,
        )
        self.wait(0.8)

        # Future work
        future_head = T("Future directions", font_size=26, color=GOLD, weight=BOLD)
        future_items = [
            "→  Multilingual extension (Arabic, English, Spanish)",
            "→  Emotion-aware prosody prediction",
            "→  Unified single end-to-end model",
        ]
        future_bullets = VGroup(*[
            T(t, font_size=21, color=GREY) for t in future_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        future_group = VGroup(future_head, future_bullets).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28
        )
        future_group.next_to(bullets, DOWN, buff=0.60)

        self.play(FadeIn(future_group, shift=UP * 0.1), run_time=1.0)
        self.wait(0.8)

        # Liens
        links = T(
            "📄  aclanthology.org/2025.icnlsp-1.30"
            "    💻  github.com/hi-paris/Prosody-Control-French-TTS",
            font_size=17, color=CYAN, slant=ITALIC,
        )
        links.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(links, shift=UP * 0.08), run_time=0.8)

        # Onde finale qui pulse
        final_wave = sine_wave(amplitude=0.55, freq=2.5, color=CYAN, sw=3)
        final_wave.next_to(links, DOWN, buff=0.05).set_opacity(0)
        self.play(final_wave.animate.set_opacity(0.6), run_time=0.7)
        self.play(
            final_wave.animate.scale([1, 1.4, 1]).set_opacity(0.9),
            run_time=0.6, rate_func=there_and_back,
        )

        self.wait(3.5)

        # Flash final sur le titre
        self.play(glow_flash(title, color=RED, n=14, radius=0.5), run_time=0.7)
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(title, bullets, future_group, links, final_wave)),
            run_time=1.5,
        )
