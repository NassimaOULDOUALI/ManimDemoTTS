"""
s05_pipeline.py — Scène 5 : Notre pipeline bout-en-bout (~45s)
==============================================================
Niveau : avancé
Basé sur Figure 1 du papier ICNLSP 2025

Pipeline :
  Natural Audio → Demucs → WhisperTS → TextGrid
  → Syntagm Segmentation → Feature Extraction (F0/Vol/Rate/Break)
  → SSML → TTS (Azure) → Improved Synthetic Audio

Effets :
  - Boîtes qui s'allument en cascade avec données réelles
  - Zoom sur "Feature Extraction" avec les formules du papier
  - Stats du corpus (122 303 mots, 14 locuteurs, 17 695 tags)
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *


def pipeline_box(label, sub="", color=CYAN, w=2.2, h=1.3):
    bg = RoundedRectangle(
        corner_radius=0.14, width=w, height=h,
        fill_color=DARK_BOX, fill_opacity=1,
        stroke_color=color, stroke_width=2,
    )
    head = T(label, font_size=18, color=color, weight=BOLD)
    items = [head]
    if sub:
        items.append(T(sub, font_size=13, color=GREY))
    content = VGroup(*items).arrange(DOWN, buff=0.10)
    content.move_to(bg)
    return VGroup(bg, content)


class ScenePipeline(Scene):
    def construct(self):

        # ==============================================================
        # TITRE
        # ==============================================================
        title = section_title("Our End-to-End SSML Pipeline") \
            .to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # ==============================================================
        # SLIDE 1 : Pipeline complet animé (Row 1 + Row 2)
        # ==============================================================

        # Rangée 1 : prétraitement audio
        b_audio = pipeline_box("Natural\nAudio", "ETX Majelan\n14h · 14 speakers", WHITE_TXT)
        b_demucs = pipeline_box("Demucs\nSep.", "Source separation\nBackground removal", CYAN)
        b_whisper = pipeline_box("WhisperTS\nAlignment", "medium WER 5.95%\nARR 96.3%", CYAN)
        b_textgrid = pipeline_box("TextGrid\nSyntagms", "Pause + punct.\ndetection", GREEN)

        row1 = VGroup(b_audio, b_demucs, b_whisper, b_textgrid)
        arrows1 = VGroup()
        for i in range(len(row1) - 1):
            arr = Arrow(RIGHT * 0.05, RIGHT * 0.45, color=GREY,
                        stroke_width=2.5, tip_length=0.18, buff=0)
            arrows1.add(arr)

        # Interleave boxes and arrows
        row1_full = VGroup()
        for i, box in enumerate(row1):
            row1_full.add(box)
            if i < len(row1) - 1:
                row1_full.add(arrows1[i])
        row1_full.arrange(RIGHT, buff=0.0)

        # Rangée 2 : feature extraction + SSML + TTS
        b_feat = pipeline_box("Feature\nExtraction", "F₀ · Vol · Rate\n· Break", GOLD, w=2.4)
        b_ssml = pipeline_box("SSML\nMarkup", "<prosody>\n<break>", RED, w=2.0)
        b_tts = pipeline_box("TTS\n(Azure)", "fr-FR Henri\nbaseline voice", CYAN, w=2.0)
        b_out = pipeline_box("Improved\nSpeech", "MOS 3.87\n+20% quality", GREEN, w=2.2)

        row2 = VGroup(b_feat, b_ssml, b_tts, b_out)
        arrows2 = VGroup()
        for i in range(len(row2) - 1):
            arr = Arrow(RIGHT * 0.05, RIGHT * 0.45, color=GREY,
                        stroke_width=2.5, tip_length=0.18, buff=0)
            arrows2.add(arr)

        row2_full = VGroup()
        for i, box in enumerate(row2):
            row2_full.add(box)
            if i < len(row2) - 1:
                row2_full.add(arrows2[i])
        row2_full.arrange(RIGHT, buff=0.0)

        # Positionnement
        row1_full.next_to(title, DOWN, buff=0.55)
        row1_full.scale_to_fit_width(config.frame_width - 0.9)

        row2_full.next_to(row1_full, DOWN, buff=0.45)
        row2_full.scale_to_fit_width(config.frame_width - 0.9)

        # Flèche de descente TextGrid → Feature Extraction
        down_arrow = Arrow(
            b_textgrid.get_bottom() + DOWN * 0.05,
            b_feat.get_top() + UP * 0.05,
            color=GREY, stroke_width=2.5, tip_length=0.18,
        )

        # Animation : allumage en cascade
        self.play(FadeIn(b_audio, shift=RIGHT * 0.2), run_time=0.4)
        for i in range(len(row1) - 1):
            self.play(
                GrowArrow(arrows1[i]),
                FadeIn(row1[i + 1], shift=RIGHT * 0.15),
                run_time=0.35,
            )

        self.play(GrowArrow(down_arrow), run_time=0.45)

        self.play(FadeIn(b_feat, shift=DOWN * 0.15), run_time=0.35)
        for i in range(len(row2) - 1):
            self.play(
                GrowArrow(arrows2[i]),
                FadeIn(row2[i + 1], shift=RIGHT * 0.15),
                run_time=0.35,
            )

        self.wait(1.0)

        # Highlight Feature Extraction (cœur du papier)
        feat_rect = SurroundingRectangle(b_feat, color=GOLD,
                                          stroke_width=3, buff=0.10)
        feat_lbl = T("Key step: prosodic delta extraction",
                     font_size=18, color=GOLD)
        feat_lbl.next_to(b_feat, DOWN, buff=0.4)
        self.play(Create(feat_rect), FadeIn(feat_lbl, shift=UP * 0.1), run_time=0.7)
        self.wait(1.5)

        self.play(
            FadeOut(VGroup(row1_full, row2_full, down_arrow,
                           feat_rect, feat_lbl)),
            run_time=0.8,
        )

        # ==============================================================
        # SLIDE 2 : Feature extraction — formules du papier
        # ==============================================================
        subtitle2 = T("Prosodic delta computation (relative to TTS baseline)",
                      font_size=24, color=GREY)
        subtitle2.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(subtitle2), run_time=0.5)

        # Les 4 formules clés du papier (Section 3)
        formulas = VGroup(
            MathTex(r"\text{Pitch: } p_i = \left(2^{s_i/12} - 1\right) \times 100\%",
                    font_size=28, color=CYAN),
            MathTex(r"\text{Volume: } v_i = \left(10^{\Delta L_i/20} - 1\right) \times 100\%",
                    font_size=28, color=GOLD),
            MathTex(r"\text{Rate: } r_i = \frac{n_i/d_{nat} - n_i/d_{syn}}{n_i/d_{syn}} \times 100\%",
                    font_size=28, color=GREEN),
            MathTex(r"\text{Break: raw ms from inter-syntagm silence}",
                    font_size=26, color=RED),
        )
        formulas.arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        formulas.next_to(subtitle2, DOWN, buff=0.5)

        self.play(
            LaggedStart(
                *[Write(f) for f in formulas],
                lag_ratio=0.30,
            ),
            run_time=2.5,
        )

        # Note smoothing
        smooth_note = T(
            "Exponential smoothing α=0.2 · clipped at ΔMax=8% per syntagm",
            font_size=18, color=GREY, slant=ITALIC,
        )
        smooth_note.next_to(formulas, DOWN, buff=0.4)
        self.play(FadeIn(smooth_note), run_time=0.6)
        self.wait(3.0)

        # ==============================================================
        # SLIDE 3 : Stats du corpus
        # ==============================================================
        self.play(FadeOut(VGroup(subtitle2, formulas, smooth_note)), run_time=0.7)

        subtitle3 = T("Dataset: 14h French podcast corpus (ETX Majelan)",
                      font_size=24, color=GREY)
        subtitle3.next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(subtitle3), run_time=0.5)

        stats_data = [
            ("14", "Speakers (42% female)", GREEN),
            ("122,303", "Words annotated", CYAN),
            ("17,695", "<prosody> tags", GOLD),
            ("18,746", "<break> tags", RED),
        ]

        stat_cards = VGroup(*[
            kpi_card(val, lbl, color=col, w=2.8, h=1.55)
            for val, lbl, col in stats_data
        ])
        stat_cards.arrange(RIGHT, buff=0.35)
        stat_cards.next_to(subtitle3, DOWN, buff=0.6)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.3) for c in stat_cards],
                lag_ratio=0.22,
            ),
            run_time=1.6,
        )
        self.wait(3.0)

        self.play(
            FadeOut(VGroup(title, subtitle3, stat_cards)),
            run_time=1.0,
        )
