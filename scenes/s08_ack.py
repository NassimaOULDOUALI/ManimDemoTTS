"""
s08_ack.py — Scène 8 : Acknowledgements / Financement (~14s)
=============================================================
Carte institutionnelle de fin (VivaTech).

Contenu (texte verbatim imposé par le directeur) :
  - Hi! PARIS
  - ANR/France 2030 (ANR-23-IACL-0005)
  - IDRIS / GENCI — allocation 2025-AD011015141R2
  - État · France 2030
  - Union européenne – NextGenerationEU · plan France Relance

Bandeau logos : barre claire en bas → les logos officiels (versions
couleur sur fond clair) ressortent sur le bleu Hi! PARIS.
Dépose les PNG transparents dans  assets/  avec EXACTEMENT ces noms :
  hi-paris.png · anr.png · france2030.png · genci.png · idris.png
  ue-nextgeneration.png · france-relance.png
Tant qu'un logo est absent, un chip texte propre s'affiche à la place.

Rendu standalone :
    manim -pqh scenes/s08_ack.py SceneAck

Contraintes Manim v0.20.1 :
  - ImageMobject n'est PAS un VMobject → utiliser Group (pas VGroup)
    pour mélanger images et chips.
"""

from manim import *
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *


class SceneAck(Scene):
    def construct(self):

        # ── Titre ───────────────────────────────────────────────────
        title = section_title("Acknowledgements").to_edge(UP, buff=0.55)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.7)

        # ── Texte de financement (verbatim) ─────────────────────────
        en_lines = [
            "This work was supported by Hi! PARIS and by the ANR/France 2030 program",
            "(ANR-23-IACL-0005). We acknowledge access to the IDRIS high-performance",
            "computing resources under allocation 2025-AD011015141R2, granted by",
            "GENCI (Grand Équipement National de Calcul Intensif).",
        ]
        fr_lines = [
            "Ce projet a été financé par l'État dans le cadre de France 2030.",
            "Financé par l'Union européenne – NextGenerationEU",
            "dans le cadre du plan France Relance.",
        ]

        en_block = VGroup(*[
            T(l, font_size=22, color=WHITE_TXT) for l in en_lines
        ]).arrange(DOWN, buff=0.16)

        fr_block = VGroup(*[
            T(l, font_size=21, color=CYAN, slant=ITALIC) for l in fr_lines
        ]).arrange(DOWN, buff=0.14)

        text_block = VGroup(en_block, fr_block).arrange(DOWN, buff=0.42)
        # Garde-fou largeur (toutes les lignes tiennent dans le cadre)
        if text_block.width > 12.0:
            text_block.scale(12.0 / text_block.width)

        box = RoundedRectangle(
            corner_radius=0.18,
            width=text_block.width + 1.1,
            height=text_block.height + 0.9,
            fill_color=DARK_BOX, fill_opacity=1,
            stroke_color=CYAN, stroke_width=2,
        ).move_to(UP * 0.55)
        text_block.move_to(box)

        self.play(FadeIn(box, scale=0.98), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.06) for l in en_block],
                        lag_ratio=0.15),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[FadeIn(l, shift=UP * 0.06) for l in fr_block],
                        lag_ratio=0.20),
            run_time=0.8,
        )
        self.wait(0.4)

        # ── Bandeau logos ───────────────────────────────────────────
        # (stem fichier, label fallback, couleur accent du chip)
        logo_specs = [
            ("hi-paris",          "Hi! PARIS",            CYAN),
            ("anr",               "ANR",                  RED),
            ("france2030",        "France 2030",          GOLD),
            ("genci",             "GENCI",                GREEN),
            ("idris",             "IDRIS",                CYAN),
            ("ue-nextgeneration", "UE · NextGenerationEU", GOLD),
            ("france-relance",    "France Relance",       RED),
        ]

        LOGO_H = 0.82

        def make_logo(stem, label, color):
            """Logo officiel si présent dans assets/, sinon chip texte."""
            try:
                img = load_img(stem)
                img.set_height(LOGO_H)
                return img
            except FileNotFoundError:
                txt = T(label, font_size=15, color=BG, weight=BOLD)
                chip = RoundedRectangle(
                    corner_radius=0.10,
                    width=max(txt.width + 0.4, 1.3), height=LOGO_H,
                    fill_color=GREY, fill_opacity=1,
                    stroke_color=color, stroke_width=2,
                )
                if txt.width > chip.width - 0.25:
                    txt.set_width(chip.width - 0.25)
                txt.move_to(chip)
                return VGroup(chip, txt)

        logos = Group(*[make_logo(*spec) for spec in logo_specs]) \
            .arrange(RIGHT, buff=0.45)

        bar_w = 13.2
        if logos.width > bar_w - 0.8:
            logos.scale((bar_w - 0.8) / logos.width)

        bar = RoundedRectangle(
            corner_radius=0.16,
            width=bar_w, height=logos.height + 0.5,
            fill_color=WHITE_TXT, fill_opacity=0.97, stroke_width=0,
        ).to_edge(DOWN, buff=0.5)
        logos.move_to(bar)

        self.play(FadeIn(bar, shift=UP * 0.1), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(m, shift=UP * 0.08) for m in logos],
                        lag_ratio=0.12),
            run_time=1.0,
        )

        # ── Sortie ──────────────────────────────────────────────────
        self.wait(2.8)
        self.play(
            FadeOut(Group(title, box, text_block, bar, logos)),
            run_time=1.2,
        )
