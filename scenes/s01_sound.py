"""
s01_sound.py — Scène 1 : C'est quoi le son ? (~35s)
=====================================================
Niveau : zéro (grand public, VivaTech)
Concept : pression d'air → waveform → amplitude → fréquence

Effets :
  - Molécules d'air qui vibrent (animation particules)
  - Waveform qui se dessine en live (Create)
  - Zoom sur une période → définition fréquence
  - Comparaison grave / aigu (deux courbes côte à côte)
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *


class SceneSound(Scene):
    def construct(self):

        # ==============================================================
        # TITRE
        # ==============================================================
        title = section_title("What is Sound ?").to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # ==============================================================
        # SLIDE 1 : Molécules qui vibrent → onde de pression
        # ==============================================================
        subtitle1 = T("Air molecules vibrating → pressure wave",
                      font_size=28, color=GREY)
        subtitle1.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(subtitle1), run_time=0.6)

        # Grille de molécules
        n_rows, n_cols = 3, 14
        spacing_x, spacing_y = 0.72, 0.55
        molecules = VGroup()
        for r in range(n_rows):
            for c in range(n_cols):
                x = -4.8 + c * spacing_x
                y = -0.2 + r * spacing_y - (n_rows - 1) * spacing_y / 2
                dot = Dot(point=np.array([x, y, 0]),
                          radius=0.09, color=CYAN)
                dot.set_opacity(0.6)
                molecules.add(dot)

        molecules.shift(DOWN * 0.5)
        self.play(FadeIn(molecules, lag_ratio=0.02), run_time=1.0)
        self.wait(0.3)

        # Animation vibration : vague de compression se propage de gauche à droite
        for wave_pass in range(2):
            anims = []
            for i, mol in enumerate(molecules):
                col_idx = i % n_cols
                delay = col_idx * 0.04
                # Compression vers la droite puis retour
                anims.append(
                    Succession(
                        Wait(delay),
                        mol.animate(run_time=0.18, rate_func=there_and_back)
                            .shift(RIGHT * 0.18)
                            .set_color(RED)
                            .set_opacity(1.0),
                        mol.animate(run_time=0.10).set_color(CYAN).set_opacity(0.6),
                    )
                )
            self.play(*anims, run_time=1.4)

        self.wait(0.4)

        # Flèche "sound source → ear"
        src_lbl = T("Source", font_size=20, color=GOLD)
        ear_lbl = T("Ear", font_size=20, color=GOLD)
        src_lbl.next_to(molecules, LEFT, buff=0.3)
        ear_lbl.next_to(molecules, RIGHT, buff=0.3)
        arr_sound = Arrow(src_lbl.get_right() + RIGHT * 0.1,
                          ear_lbl.get_left() - RIGHT * 0.1,
                          color=GOLD, stroke_width=3, tip_length=0.22)
        arr_sound.next_to(molecules, DOWN, buff=0.3)

        self.play(FadeIn(src_lbl), FadeIn(ear_lbl), GrowArrow(arr_sound), run_time=0.8)
        self.wait(0.5)

        # Transition : on efface les molécules, on garde le titre
        self.play(
            FadeOut(VGroup(molecules, src_lbl, ear_lbl, arr_sound, subtitle1)),
            run_time=0.7,
        )

        # ==============================================================
        # SLIDE 2 : Waveform dessinée en live
        # ==============================================================
        subtitle2 = T("We record this as a waveform: Amplitude vs. Time",
                      font_size=26, color=GREY)
        subtitle2.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(subtitle2), run_time=0.5)

        ax = axes_xy([0, 1, 0.25], [-1.2, 1.2, 0.5],
                     x_len=9.5, y_len=2.8).shift(DOWN * 0.3)
        x_lbl = T("Time (s)", font_size=20, color=GREY)
        y_lbl = T("Amplitude", font_size=20, color=GREY)
        x_lbl.next_to(ax, DOWN, buff=0.15).to_edge(RIGHT, buff=0.9)
        y_lbl.next_to(ax, LEFT, buff=0.15).rotate(PI / 2)

        self.play(Create(ax), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.7)

        wave_graph = ax.plot(speech_signal_func, x_range=[0, 1, 0.001],
                             color=CYAN, stroke_width=2.5)

        # Dessin progressif — l'effet clé
        self.play(Create(wave_graph), run_time=2.2, rate_func=linear)

        caption = T("Each sample = air pressure at one instant",
                    font_size=21, color=GREY)
        caption.next_to(ax, DOWN, buff=0.30)
        self.play(FadeIn(caption), run_time=0.5)
        self.wait(2.5)

        # ==============================================================
        # SLIDE 3 : Grave vs Aigu — deux sinusoïdes
        # ==============================================================
        self.play(FadeOut(VGroup(ax, wave_graph, x_lbl, y_lbl,
                                  caption, subtitle2)),
                  run_time=0.7)

        subtitle3 = T("Low frequency = deep voice · High frequency = high voice",
                      font_size=25, color=GREY)
        subtitle3.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(subtitle3), run_time=0.5)

        # Deux axes côte à côte
        ax_low = axes_xy([0, 1, 0.5], [-1.2, 1.2, 1],
                         x_len=4.2, y_len=2.4).shift(LEFT * 2.8 + DOWN * 0.4)
        ax_high = axes_xy([0, 1, 0.5], [-1.2, 1.2, 1],
                          x_len=4.2, y_len=2.4).shift(RIGHT * 2.8 + DOWN * 0.4)

        # Labels
        lbl_low = T("100 Hz (deep)", font_size=20, color=CYAN, weight=BOLD)
        lbl_high = T("400 Hz (high)", font_size=20, color=GOLD, weight=BOLD)
        lbl_low.next_to(ax_low, UP, buff=0.2)
        lbl_high.next_to(ax_high, UP, buff=0.2)

        wave_low = ax_low.plot(
            lambda t: 0.85 * np.sin(2 * np.pi * 3 * t),
            x_range=[0, 1, 0.002], color=CYAN, stroke_width=3,
        )
        wave_high = ax_high.plot(
            lambda t: 0.85 * np.sin(2 * np.pi * 12 * t),
            x_range=[0, 1, 0.001], color=GOLD, stroke_width=3,
        )

        # Annotation période — flèche double + label (plus robuste que BraceBetweenPoints)
        period_arr_low = DoubleArrow(
            ax_low.c2p(0, -1.05), ax_low.c2p(1/3, -1.05),
            color=CYAN, stroke_width=2, tip_length=0.15, buff=0,
        )
        period_lbl_low = T("T = 10ms", font_size=17, color=CYAN)
        period_lbl_low.next_to(period_arr_low, DOWN, buff=0.08)

        period_arr_high = DoubleArrow(
            ax_high.c2p(0, -1.05), ax_high.c2p(1/12, -1.05),
            color=GOLD, stroke_width=2, tip_length=0.15, buff=0,
        )
        period_lbl_high = T("T = 2.5ms", font_size=17, color=GOLD)
        period_lbl_high.next_to(period_arr_high, DOWN, buff=0.08)

        # Aliases pour le FadeOut final (même noms)
        period_brace_low  = period_arr_low
        period_brace_high = period_arr_high

        self.play(
            Create(ax_low), Create(ax_high),
            FadeIn(lbl_low), FadeIn(lbl_high),
            run_time=0.8,
        )
        self.play(
            Create(wave_low), Create(wave_high),
            run_time=1.5,
        )
        self.play(
            FadeIn(period_brace_low), FadeIn(period_lbl_low),
            FadeIn(period_brace_high), FadeIn(period_lbl_high),
            run_time=0.7,
        )

        # Formule fréquence
        freq_formula = MathTex(r"f = \frac{1}{T}", font_size=36,
                               color=WHITE_TXT)
        freq_formula.to_edge(DOWN, buff=0.4)
        self.play(Write(freq_formula), run_time=0.8)
        self.wait(4.0)

        self.play(
            FadeOut(VGroup(title, subtitle3, ax_low, ax_high, wave_low, wave_high,
                           lbl_low, lbl_high, period_brace_low, period_lbl_low,
                           period_brace_high, period_lbl_high, freq_formula)),
            run_time=1.0,
        )
