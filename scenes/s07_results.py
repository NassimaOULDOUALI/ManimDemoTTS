"""
s07_results.py — Scène 7+8 fusionnée : Résultats + Conclusion (~60s)
=====================================================================
Fusion de SceneResults + SceneOutro en une seule scène dense.

Nouveautés v2 (branche vivatech_v2) :
  - KPI cards remplacées par des jauges circulaires animées (Arc + ChangeDecimalToValue)
  - Compteur live MOS : 3.20 → 3.87
  - Tout en ~60s sans coupure

Contraintes Manim v0.20.1 :
  - Pas de stroke_opacity= → .set_stroke(opacity=...) ou .set_opacity()
  - Pas d'aligned_edge=None dans .animate
  - Barres via UpdateFromAlphaFunc
  - Arc(start_angle, angle) pour les jauges
  - ChangeDecimalToValue pour les compteurs
"""

from manim import *
from manim.utils.color import ManimColor
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *

# ── Compat v0.20 ──────────────────────────────────────────────────────────────
def _ic(c1, c2, t):
    return interpolate_color(ManimColor(c1), ManimColor(c2), t)

def _hline(ax, point, color, stroke_width=1.5, opacity=1.0):
    line = ax.get_horizontal_line(point, color=color, stroke_width=stroke_width)
    line.set_opacity(opacity)
    return line
# ─────────────────────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────────────────────
# HELPER : jauge circulaire animée
# ─────────────────────────────────────────────────────────────────────────────
def animated_gauge(
    scene,
    value: float,          # valeur cible
    max_val: float,        # valeur max de l'arc (100% = demi-cercle)
    label: str,            # label affiché sous la jauge
    num_label: str,        # texte fixe affiché au centre (ex. "99.24%")
    color,                 # couleur de l'arc rempli
    center=ORIGIN,
    radius: float = 0.72,
    run_time: float = 1.6,
    fmt_str: str = "{:.0f}",   # format du compteur numérique
    unit: str = "",            # unité affichée après le compteur (ex. "%", " ms")
):
    """
    Dessine une jauge semi-circulaire animée (arc du bas vers le haut).
    - Arc fond gris (demi-cercle fixe)
    - Arc coloré qui se remplit via UpdateFromAlphaFunc
    - Compteur DecimalNumber au centre qui monte de 0 → value
    - Label texte en dessous
    Retourne le VGroup complet (pour FadeOut ou repositionnement ultérieur).
    """
    sw = 10  # stroke_width des arcs

    # Arc de fond (demi-cercle complet, gris)
    bg_arc = Arc(
        radius=radius,
        start_angle=0,       # part du côté droit (est)
        angle=PI,            # demi-cercle vers le haut (antihoraire)
        color=GREY,
        stroke_width=sw,
    )
    bg_arc.set_stroke(opacity=0.3)
    bg_arc.move_arc_center_to(center)

    # Arc coloré — commence vide, sera animé
    fg_arc = Arc(
        radius=radius,
        start_angle=0,
        angle=0.001,
        color=color,
        stroke_width=sw + 2,
    )
    fg_arc.move_arc_center_to(center)

    # Fraction de remplissage (clamp 0..1)
    fill_frac = min(1.0, max(0.0, value / max_val))

    def arc_updater(mob, alpha):
        target_angle = PI * fill_frac * alpha
        new_arc = Arc(
            radius=radius,
            start_angle=0,
            angle=max(0.001, target_angle),
            color=color,
            stroke_width=sw + 2,
        )
        new_arc.move_arc_center_to(center)
        mob.become(new_arc)

    # Compteur numérique au centre
    counter = DecimalNumber(
        0,
        num_decimal_places=0,
        color=color,
        font_size=28,
    )
    counter.move_to(center + UP * 0.08)

    # Unité (optionnelle, affichée à côté du compteur)
    unit_txt = T(unit, font_size=18, color=color) if unit else None

    # Label sous la jauge
    lbl = T(label, font_size=17, color=GREY)
    lbl.move_to(center + DOWN * (radius + 0.38))
    lbl.set_width(min(lbl.width, radius * 2.8))

    group_mobs = [bg_arc, fg_arc, counter, lbl]
    if unit_txt:
        unit_txt.next_to(counter, RIGHT, buff=0.04)
        group_mobs.append(unit_txt)

    group = VGroup(*group_mobs)

    scene.add(bg_arc, fg_arc, counter, lbl)
    if unit_txt:
        scene.add(unit_txt)

    scene.play(
        UpdateFromAlphaFunc(fg_arc, arc_updater, run_time=run_time, rate_func=smooth),
        ChangeDecimalToValue(counter, value, run_time=run_time, rate_func=smooth),
        run_time=run_time,
    )

    if unit_txt:
        unit_txt.next_to(counter, RIGHT, buff=0.04)

    return group


# =============================================================================
# SCÈNE FUSIONNÉE : RÉSULTATS + CONCLUSION
# =============================================================================

class SceneResultsOutro(Scene):
    def construct(self):

        # ══════════════════════════════════════════════════════════════
        # BLOC 1 — Titre + MOS barchart (~15s)
        # ══════════════════════════════════════════════════════════════
        title = section_title("Results: Beating the State of the Art") \
            .to_edge(UP, buff=0.45)
        subtitle = T("Perceptual evaluation: 18 participants · 9h+ of audio",
                     font_size=21, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.28)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.7)
        self.play(FadeIn(subtitle), run_time=0.4)

        # ── Axes ────────────────────────────────────────────────────
        ax = Axes(
            x_range=[0, 3, 1], y_range=[0, 4.5, 1],
            x_length=5.8, y_length=3.2,
            axis_config={"color": GREY, "stroke_width": 1.5},
            x_axis_config={"include_ticks": False},
            tips=False,
        ).shift(LEFT * 2.2 + DOWN * 0.3)

        y_lbl = T("MOS (5-point scale)", font_size=17, color=GREY).rotate(PI / 2)
        y_lbl.next_to(ax, LEFT, buff=0.10)

        ref4 = _hline(ax, ax.c2p(3, 4.0), color=GOLD, stroke_width=1.2, opacity=0.35)
        ref4_lbl = T("4.0", font_size=13, color=GOLD).next_to(ax.c2p(0, 4.0), LEFT, buff=0.08)

        x_lbl_base = T("Baseline\n(Azure Henri\nno SSML)",
                        font_size=15, color=GREY).move_to(ax.c2p(1, 0) + DOWN * 0.65)
        x_lbl_ours = T("Ours\n(SSML pipeline)",
                        font_size=15, color=GREEN, weight=BOLD).move_to(ax.c2p(2, 0) + DOWN * 0.55)

        self.play(Create(ax), FadeIn(y_lbl), FadeIn(ref4), FadeIn(ref4_lbl),
                  FadeIn(x_lbl_base), FadeIn(x_lbl_ours), run_time=0.8)

        # ── Helper barres (UpdateFromAlphaFunc) ─────────────────────
        def grow_bar(bar_mob, x_pos, mos_val, bar_color, run_time=1.2):
            bottom_y = ax.c2p(x_pos, 0)[1]
            top_y    = ax.c2p(x_pos, mos_val)[1]
            bar_x    = ax.c2p(x_pos, 0)[0]
            bar_width = 0.90

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

            updater(bar_mob, 0.001)
            self.add(bar_mob)
            self.play(
                UpdateFromAlphaFunc(bar_mob, updater,
                                    run_time=run_time, rate_func=smooth)
            )

        # Barre baseline
        bar_base = Rectangle(width=0.90, height=0.001,
                             fill_color=_ic(GREY, CYAN, 0.3),
                             fill_opacity=0.88, stroke_width=0)
        grow_bar(bar_base, 1, 3.20, _ic(GREY, CYAN, 0.3), run_time=1.0)

        val_base = T("3.20", font_size=20, color=GREY, weight=BOLD)
        val_base.next_to(bar_base, UP, buff=0.08)
        self.play(FadeIn(val_base, shift=UP * 0.1), run_time=0.3)
        self.wait(0.2)

        # Barre ours (compteur live)
        bar_ours = Rectangle(width=0.90, height=0.001,
                             fill_color=GREEN, fill_opacity=0.90, stroke_width=0)

        bottom_y_ours = ax.c2p(2, 0)[1]
        top_y_ours    = ax.c2p(2, 3.87)[1]
        bar_x_ours    = ax.c2p(2, 0)[0]

        mos_counter = DecimalNumber(
            3.20, num_decimal_places=2,
            color=GREEN, font_size=24,
        )

        def bar_updater(mob, alpha):
            current_h = max(0.001, (top_y_ours - bottom_y_ours) * alpha)
            current_y = bottom_y_ours + current_h / 2
            mob.become(
                Rectangle(
                    width=0.90, height=current_h,
                    fill_color=GREEN, fill_opacity=0.90, stroke_width=0,
                ).move_to(np.array([bar_x_ours, current_y, 0]))
            )
            mos_counter.move_to(
                np.array([bar_x_ours, bottom_y_ours + current_h + 0.22, 0])
            )

        bar_updater(bar_ours, 0.001)
        self.add(bar_ours)
        mos_counter.move_to(np.array([bar_x_ours, bottom_y_ours + 0.22, 0]))
        self.add(mos_counter)

        self.play(
            UpdateFromAlphaFunc(bar_ours, bar_updater, run_time=1.8, rate_func=smooth),
            ChangeDecimalToValue(mos_counter, 3.87, run_time=1.8, rate_func=smooth),
        )

        # Flèche delta
        delta_arr = Arrow(
            val_base.get_top() + UP * 0.05,
            mos_counter.get_top() + UP * 0.05,
            color=GOLD, stroke_width=3.0, tip_length=0.20,
        )
        delta_lbl = T("+0.67 MOS\n(p < 0.005)", font_size=18, color=GOLD, weight=BOLD)
        delta_lbl.next_to(delta_arr, UP, buff=0.10)

        self.play(GrowArrow(delta_arr), run_time=0.5)
        self.play(FadeIn(delta_lbl, shift=UP * 0.1), run_time=0.4)
        self.play(glow_flash(delta_lbl, color=GOLD, n=12, radius=0.32), run_time=0.5)

        # ══════════════════════════════════════════════════════════════
        # BLOC 2 — Jauges KPI animées — layout horizontal sous le barchart
        # 3 jauges côte à côte, chacune avec assez d'espace
        # ══════════════════════════════════════════════════════════════

        # FadeOut du barchart d'abord pour libérer tout l'espace
        all_bar_mobs_tmp = VGroup(
            ax, y_lbl, ref4, ref4_lbl, x_lbl_base, x_lbl_ours,
            bar_base, val_base, bar_ours, mos_counter,
            delta_arr, delta_lbl, subtitle,
        )
        self.play(FadeOut(all_bar_mobs_tmp), run_time=0.6)

        # 3 centres espacés horizontalement, centrés verticalement
        gauge_y   = DOWN * 0.3
        gauge_sep = 4.5   # distance entre centres
        gauge_centers = [
            LEFT  * gauge_sep + gauge_y,
            ORIGIN + gauge_y,
            RIGHT * gauge_sep + gauge_y,
        ]

        gauge_configs = [
            dict(value=99.24, max_val=100, label="F1 score\n(vs BERT 92%)",
                 color=CYAN,  unit="%"),
            dict(value=1.1,   max_val=10,  label="MAE pitch /\nvol / rate",
                 color=GOLD,  unit="%"),
            dict(value=15,    max_val=18,  label="Listeners preferred\nour synthesis",
                 color=GREEN, unit="/18"),
        ]

        gauge_groups = []
        for cfg, ctr in zip(gauge_configs, gauge_centers):
            g = animated_gauge(
                self,
                value=cfg["value"],
                max_val=cfg["max_val"],
                label=cfg["label"],
                num_label="",
                color=cfg["color"],
                center=ctr,
                radius=1.0,       # radius plus grand → jauge lisible
                run_time=1.5,
                unit=cfg["unit"],
            )
            gauge_groups.append(g)
            self.wait(0.2)

        self.wait(0.5)
        self.play(glow_flash(gauge_groups[2], color=GREEN, n=14, radius=0.9), run_time=0.6)
        self.wait(1.5)

        self.play(FadeOut(VGroup(*gauge_groups)), run_time=0.6)

        # ══════════════════════════════════════════════════════════════
        # BLOC 3 — Tableau comparatif Table 5 (~12s)
        # ══════════════════════════════════════════════════════════════
        subtitle2 = T("Objective comparison — MAE (lower is better)",
                      font_size=21, color=GREY)
        subtitle2.next_to(title, DOWN, buff=0.28)
        self.play(FadeIn(subtitle2), run_time=0.4)

        col_headers = ["Model", "Pitch MAE%", "Vol MAE%", "Rate MAE%", "Break ms"]
        rows_data = [
            ("Cascade (Ours)", "0.97", "1.09", "1.10", "132.9", GREEN),
            ("BiLSTM L=2",     "1.69", "6.04", "0.84", "—",     CYAN),
            ("SOTA Few-shot*", "1.08", "5.80", "0.97", "159.6", GOLD),
            ("SOTA Zero-shot*","1.42", "7.65", "1.52", "170.2", RED),
        ]

        col_w     = [2.6, 1.55, 1.55, 1.55, 1.55]
        row_h     = 0.50
        table_x0  = -5.0
        table_y0  = 1.1

        # En-têtes
        header_cells = VGroup()
        for j, (header, cw) in enumerate(zip(col_headers, col_w)):
            x = table_x0 + sum(col_w[:j]) + cw / 2
            bg = Rectangle(width=cw, height=row_h,
                           fill_color="#001B36", fill_opacity=1,
                           stroke_color=GREY, stroke_width=0.8)
            bg.move_to(np.array([x, table_y0, 0]))
            lbl = T(header, font_size=15, color=WHITE_TXT, weight=BOLD)
            lbl.move_to(bg)
            header_cells.add(VGroup(bg, lbl))

        self.play(FadeIn(header_cells), run_time=0.4)

        row_cells_all = VGroup()
        for r_idx, (model, p, v, rt, br, col) in enumerate(rows_data):
            row_vals = [model, p, v, rt, br]
            row_y = table_y0 - (r_idx + 1) * row_h
            row_group = VGroup()
            for j, (val, cw) in enumerate(zip(row_vals, col_w)):
                x = table_x0 + sum(col_w[:j]) + cw / 2
                fill = "#002B52" if r_idx % 2 == 0 else DARK_BOX
                bg = Rectangle(width=cw, height=row_h,
                               fill_color=fill, fill_opacity=1,
                               stroke_color=GREY, stroke_width=0.5)
                bg.move_to(np.array([x, row_y, 0]))
                txt_color = col if j == 0 else (GREEN if r_idx == 0 else WHITE_TXT)
                cell_lbl = T(val, font_size=14, color=txt_color,
                             weight=BOLD if r_idx == 0 else NORMAL)
                cell_lbl.move_to(bg)
                row_group.add(VGroup(bg, cell_lbl))
            row_cells_all.add(row_group)
            self.play(FadeIn(row_group, shift=RIGHT * 0.1), run_time=0.35)

        # Encadrer "Cascade (Ours)"
        our_row_rect = Rectangle(
            width=sum(col_w), height=row_h,
            fill_opacity=0, stroke_color=GREEN, stroke_width=2.5,
        )
        our_row_rect.move_to(np.array([
            table_x0 + sum(col_w) / 2,
            table_y0 - row_h,
            0,
        ]))
        self.play(Create(our_row_rect), run_time=0.5)

        note = T("* Qwen3-32B (best few-shot / zero-shot)",
                 font_size=14, color=GREY, slant=ITALIC)
        note.next_to(row_cells_all, DOWN, buff=0.28)
        self.play(FadeIn(note), run_time=0.3)
        self.wait(3.0)

        self.play(
            FadeOut(VGroup(subtitle2, header_cells, row_cells_all,
                           our_row_rect, note)),
            run_time=0.7,
        )

        # ══════════════════════════════════════════════════════════════
        # BLOC 4 — Conclusion — layout 2 colonnes (~12s)
        # ══════════════════════════════════════════════════════════════
        title_new = section_title("Conclusion & Future Work") \
            .to_edge(UP, buff=0.45)
        self.play(Transform(title, title_new), run_time=0.6)

        # ── Colonne gauche : takeaways dans une box verte ────────────
        takeaway_items = [
            "First end-to-end SSML pipeline for French TTS",
            "QwenA + QwenB : F1 99.24% · MAE < 1.1%",
            "MOS +0.67 · 83% listeners preferred our synthesis",
        ]
        takeaway_rows = VGroup(*[
            VGroup(
                T("✅", font_size=20, color=GREEN),
                T(txt, font_size=19, color=WHITE_TXT),
            ).arrange(RIGHT, buff=0.18, aligned_edge=LEFT)
            for txt in takeaway_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)

        ta_bg = RoundedRectangle(
            corner_radius=0.16, width=6.6, height=3.0,
            fill_color=DARK_BOX, fill_opacity=1,
            stroke_color=GREEN, stroke_width=2,
        )
        ta_head = T("Key Results", font_size=21, color=GREEN, weight=BOLD)
        ta_content = VGroup(ta_head, takeaway_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        # Rescale si dépassement
        if ta_content.width > 6.2:
            ta_content.scale(6.2 / ta_content.width)
        ta_content.move_to(ta_bg)
        ta_box = VGroup(ta_bg, ta_content)
        ta_box.move_to(LEFT * 3.5 + DOWN * 0.5)

        # ── Colonne droite : future work dans une box dorée ──────────
        future_items = [
            "Multilingual extension",
            "Emotion-aware prosody prediction",
            "Unified end-to-end model",
        ]
        future_rows = VGroup(*[
            VGroup(
                T("→", font_size=20, color=GOLD),
                T(txt, font_size=19, color=WHITE_TXT),
            ).arrange(RIGHT, buff=0.18, aligned_edge=LEFT)
            for txt in future_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)

        fw_bg = RoundedRectangle(
            corner_radius=0.16, width=5.6, height=3.0,
            fill_color=DARK_BOX, fill_opacity=1,
            stroke_color=GOLD, stroke_width=2,
        )
        fw_head = T("Future Directions", font_size=21, color=GOLD, weight=BOLD)
        fw_content = VGroup(fw_head, future_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        if fw_content.width > 5.2:
            fw_content.scale(5.2 / fw_content.width)
        fw_content.move_to(fw_bg)
        fw_box = VGroup(fw_bg, fw_content)
        fw_box.move_to(RIGHT * 3.8 + DOWN * 0.5)

        # ── Animation ────────────────────────────────────────────────
        self.play(FadeIn(ta_box, shift=RIGHT * 0.2), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in takeaway_rows],
                        lag_ratio=0.25),
            run_time=0.9,
        )
        self.wait(0.3)
        self.play(FadeIn(fw_box, shift=LEFT * 0.2), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in future_rows],
                        lag_ratio=0.25),
            run_time=0.9,
        )
        self.wait(0.5)

        # ── Liens en bas ─────────────────────────────────────────────
        links = T(
            "📄 aclanthology.org/2025.icnlsp-1.30"
            "   💻 github.com/hi-paris/Prosody-Control-French-TTS",
            font_size=15, color=CYAN, slant=ITALIC,
        )
        links.to_edge(DOWN, buff=0.38)
        self.play(FadeIn(links, shift=UP * 0.08), run_time=0.6)

        # ── Onde finale ──────────────────────────────────────────────
        final_wave = sine_wave(amplitude=0.40, freq=2.5, color=CYAN, sw=2.5)
        final_wave.next_to(links, UP, buff=0.12).set_opacity(0)
        self.play(final_wave.animate.set_opacity(0.5), run_time=0.5)
        self.play(
            final_wave.animate.scale([1, 1.5, 1]).set_opacity(0.8),
            run_time=0.5, rate_func=there_and_back,
        )
        self.wait(2.0)

        self.play(glow_flash(title, color=RED, n=14, radius=0.5), run_time=0.6)
        self.wait(0.8)

        self.play(
            FadeOut(VGroup(title, ta_box, fw_box, links, final_wave)),
            run_time=1.2,
        )