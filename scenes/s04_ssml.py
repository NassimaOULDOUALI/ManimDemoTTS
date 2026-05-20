"""
s04_ssml.py — Scène 4 : SSML — la solution (~35s)
==================================================
Niveau : intermédiaire
Effets :
  - Code SSML qui s'écrit lettre par lettre (typewriter)
  - Highlight dynamique des attributs (rate, pitch, volume, break)
  - Schéma "text → SSML → TTS engine → audio"
  - Exemple concret : "Bonjour, je m'appelle Bertrand Perier"
"""

from manim import *
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *


class SceneSSML(Scene):
    def construct(self):

        # ==============================================================
        # TITRE
        # ==============================================================
        title = section_title("SSML: Markup for Expressive Speech") \
            .to_edge(UP, buff=0.5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # ==============================================================
        # SLIDE 1 : Définition + exemple code "Bertrand Perier"
        # ==============================================================
        subtitle = T("Speech Synthesis Markup Language — W3C standard",
                     font_size=25, color=GREY)
        subtitle.next_to(title, DOWN, buff=0.32)
        self.play(FadeIn(subtitle), run_time=0.5)

        # Code SSML ligne par ligne
        code_lines = [
            ('<speak>', WHITE_TXT),
            ('  <prosody pitch="-7%" volume="-10%" rate="+5%">', CYAN),
            ('    Bonjour,', WHITE_TXT),
            ('  </prosody>', CYAN),
            ('  <break time="500ms"/>', GREEN),
            ('  <prosody pitch="+2%" volume="+10%" rate="+3%">', CYAN),
            ('    je m\'appelle Bertrand Perier', WHITE_TXT),
            ('  </prosody>', CYAN),
            ('</speak>', WHITE_TXT),
        ]

        code_group = VGroup(*[
            TM(line, font_size=21, color=col)
            for line, col in code_lines
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        code_group.next_to(subtitle, DOWN, buff=0.5)
        code_group.to_edge(LEFT, buff=1.0)

        # Code box
        code_bg = SurroundingRectangle(code_group, color=DARK_BOX,
                                        fill_color=DARK_BOX, fill_opacity=0.9,
                                        buff=0.3, corner_radius=0.12)

        self.play(FadeIn(code_bg), run_time=0.4)

        # Typewriter effect ligne par ligne
        for line_obj in code_group:
            self.play(
                AddTextLetterByLetter(line_obj, time_per_char=0.018),
                run_time=len(line_obj.text) * 0.022,
            )

        self.wait(0.5)

        # Highlight les 4 paramètres clés
        highlights = [
            (code_lines[1][0], 'pitch="-7%"', GOLD),
            (code_lines[1][0], 'volume="-10%"', GREEN),
            (code_lines[1][0], 'rate="+5%"', CYAN),
            (code_lines[4][0], '<break time="500ms"/>', RED),
        ]

        # On encadre les lignes concernées
        rects = []
        for i, (_, _, color) in enumerate([(None, None, GOLD),
                                            (None, None, GREEN),
                                            (None, None, CYAN),
                                            (None, None, RED)]):
            target_line = code_group[[1, 1, 1, 4][i]]
            r = SurroundingRectangle(target_line, color=color,
                                      buff=0.08, stroke_width=2)
            rects.append(r)

        param_labels = [
            T("← pitch", font_size=18, color=GOLD),
            T("← volume", font_size=18, color=GREEN),
            T("← rate", font_size=18, color=CYAN),
            T("← break", font_size=18, color=RED),
        ]

        for r, lbl, target_i in zip(rects[:1], param_labels[:1], [1]):
            lbl.next_to(code_group[target_i], RIGHT, buff=0.3)
            self.play(Create(r), FadeIn(lbl), run_time=0.5)

        r2 = SurroundingRectangle(code_group[4], color=RED, buff=0.08, stroke_width=2)
        lbl2 = T("← break 500ms", font_size=18, color=RED)
        lbl2.next_to(code_group[4], RIGHT, buff=0.3)
        self.play(Create(r2), FadeIn(lbl2), run_time=0.5)

        self.wait(3.5)

        self.play(
            FadeOut(VGroup(code_bg, code_group, rects[0], r2,
                           param_labels[0], lbl2, subtitle)),
            run_time=0.8,
        )

        # ==============================================================
        # SLIDE 2 : Flux Text → SSML → TTS → Audio
        # ==============================================================
        subtitle2 = T("Text → SSML → TTS Engine → Expressive Audio",
                      font_size=25, color=GREY)
        subtitle2.next_to(title, DOWN, buff=0.32)
        self.play(FadeIn(subtitle2), run_time=0.5)

        flow_items = [
            ("📝 Raw text",     WHITE_TXT, '"Bonjour, je..."'),
            ("🏷  SSML markup",  CYAN,     '<prosody rate="+5%">'),
            ("🔧 TTS Engine",   GREEN,     "Microsoft Azure / Google"),
            ("🔊 Audio",        GOLD,     "Expressive speech !"),
        ]

        flow_boxes = VGroup()
        flow_arrows = VGroup()

        for label, color, sub in flow_items:
            bg = RoundedRectangle(
                corner_radius=0.15, width=2.8, height=1.55,
                fill_color=DARK_BOX, fill_opacity=1,
                stroke_color=color, stroke_width=2.2,
            )
            head = T(label, font_size=19, color=color, weight=BOLD)
            sub_t = T(sub, font_size=14, color=GREY)
            content = VGroup(head, sub_t).arrange(DOWN, buff=0.12)
            content.move_to(bg)
            flow_boxes.add(VGroup(bg, content))

        flow_boxes.arrange(RIGHT, buff=1.0)
        flow_boxes.next_to(subtitle2, DOWN, buff=0.7)

        for i in range(len(flow_boxes) - 1):
            arr = Arrow(flow_boxes[i].get_right() + RIGHT * 0.1,
                        flow_boxes[i + 1].get_left() - RIGHT * 0.1,
                        color=GREY, stroke_width=3, tip_length=0.20)
            flow_arrows.add(arr)

        self.play(FadeIn(flow_boxes[0], shift=RIGHT * 0.2), run_time=0.5)
        for i in range(len(flow_boxes) - 1):
            self.play(
                GrowArrow(flow_arrows[i]),
                FadeIn(flow_boxes[i + 1], shift=RIGHT * 0.2),
                run_time=0.5,
            )

        # SSML = post-hoc control (avantage clé)
        advantage = T(
            "✓  Post-hoc control · Compatible with all commercial TTS engines",
            font_size=20, color=GREEN, weight=BOLD,
        )
        advantage.next_to(flow_boxes, DOWN, buff=0.55)
        self.play(FadeIn(advantage, shift=UP * 0.1), run_time=0.7)
        self.wait(3.5)

        self.play(
            FadeOut(VGroup(title, subtitle2, flow_boxes, flow_arrows, advantage)),
            run_time=1.0,
        )
