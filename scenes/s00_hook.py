"""
s00_hook.py — Scène 0 : Hook cinématique (~15s)
================================================
Effet WOW d'entrée : particules sonores qui convergent,
onde qui explose au centre, titre qui pulse.
Aucun prérequis — accroche immédiate.
"""

from manim import *
from manim.utils.color import ManimColor
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from theme import *

# ── Compat v0.20 ────────────────────────────────────────────────────────────
# interpolate_color attend des ManimColor, pas des str hex
def _ic(c1, c2, t):
    return interpolate_color(ManimColor(c1), ManimColor(c2), t)

# random_bright_color a été retiré en v0.20 → remplacé
_BRIGHT = [RED, CYAN, GOLD, GREEN, PURPLE, WHITE]
def _rbc():
    import random
    return random.choice(_BRIGHT)

# bounce supprimé → there_and_back_with_pause est l'équivalent
try:
    from manim.utils.rate_functions import bounce as _bounce
except ImportError:
    def _bounce(t):
        # Simulation simple d'un rebond
        if t < 0.7:
            return smooth(t / 0.7)
        u = (t - 0.7) / 0.3
        return 1.0 - 0.15 * np.sin(np.pi * u)
# ────────────────────────────────────────────────────────────────────────────


class SceneHook(Scene):
    """Hook d'entrée ~15s — effet "particules sonores" + titre pulsant."""

    def construct(self):
        # ------------------------------------------------------------------
        # 1. Particules qui convergent depuis les bords vers le centre
        # ------------------------------------------------------------------
        np.random.seed(7)
        particles = VGroup()
        for _ in range(28):
            angle = np.random.uniform(0, 2 * np.pi)
            r = np.random.uniform(4.5, 7.0)
            x, y = r * np.cos(angle), r * np.sin(angle)
            dot = Dot(point=np.array([x, y, 0]),
                      radius=np.random.uniform(0.04, 0.09),
                      color=_rbc())
            dot.set_opacity(0.0)
            particles.add(dot)

        self.add(particles)

        # Les particules apparaissent puis convergent
        self.play(
            LaggedStart(
                *[p.animate.set_opacity(0.8) for p in particles],
                lag_ratio=0.04,
            ),
            run_time=0.6,
        )
        self.play(
            *[p.animate.move_to(ORIGIN).scale(0.3).set_opacity(0) for p in particles],
            run_time=1.0,
            rate_func=rush_into,
        )

        # ------------------------------------------------------------------
        # 2. Explosion d'onde circulaire au centre
        # ------------------------------------------------------------------
        rings = VGroup()
        for i in range(4):
            ring = Circle(radius=0.01,
                          stroke_color=_ic(CYAN, RED, i / 3),
                          stroke_width=max(1.5, 4 - i),
                          fill_opacity=0)
            rings.add(ring)

        self.add(rings)

        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        ring.animate.scale(18 + i * 6).set_opacity(0),
                    )
                    for i, ring in enumerate(rings)
                ],
                lag_ratio=0.18,
            ),
            run_time=1.4,
            rate_func=linear,
        )

        # ------------------------------------------------------------------
        # 3. Stack d'ondes harmoniques (fond sonore visuel)
        # ------------------------------------------------------------------
        waves = VGroup()
        colors_wave = [CYAN, _ic(CYAN, RED, 0.3),
                       _ic(CYAN, RED, 0.6), RED]
        for k, col in enumerate(colors_wave, start=1):
            w = sine_wave(
                amplitude=0.55 / k,
                freq=2.0 * k,
                phase=k * 0.5,
                color=col,
                sw=max(1.2, 3.5 - k * 0.5),
            )
            w.shift(DOWN * 2.9)
            w.set_opacity(0)
            waves.add(w)

        self.play(
            LaggedStart(*[w.animate.set_opacity(0.6 / k) for k, w in enumerate(waves, 1)],
                        lag_ratio=0.15),
            run_time=0.7,
        )

        # Pulse d'amplitude
        self.play(
            waves[0].animate.scale([1, 1.6, 1]).set_opacity(0.9),
            run_time=0.5, rate_func=there_and_back,
        )

        # ------------------------------------------------------------------
        # 4. Titre principal qui "tape" depuis le haut
        # ------------------------------------------------------------------
        l1 = T("Improving French Synthetic Speech",
               font_size=46, color=WHITE_TXT, weight=BOLD)
        l2 = T("Quality via SSML Prosody Control",
               font_size=46, color=RED, weight=BOLD)
        title = VGroup(l1, l2).arrange(DOWN, buff=0.18)
        title.to_edge(UP, buff=0.65)

        # Entrée depuis le haut avec rebond
        title.shift(UP * 3)
        self.play(
            title.animate.shift(DOWN * 3),
            run_time=0.9, rate_func=_bounce,
        )

        # Pulse scale + glow
        self.play(
            title.animate.scale(1.06).set_stroke(RED, width=2, opacity=0.7),
            run_time=0.45, rate_func=there_and_back,
        )
        self.play(title.animate.scale(1 / 1.06).set_stroke(width=0),
                  run_time=0.35)

        # ── Tagline FR (accroche grand public, ancrage "techno française") ──
        tagline = T("Quand l'IA apprend à intoner le français",
                    font_size=28, color=CYAN, slant=ITALIC)
        tagline.next_to(title, DOWN, buff=0.34)
        self.play(FadeIn(tagline, shift=UP * 0.12), run_time=0.6)

        # ------------------------------------------------------------------
        # 5. Badge conférence + auteurs condensés
        # ------------------------------------------------------------------
        badge = T("ICNLSP 2025", font_size=28, color=GOLD, weight=BOLD)
        badge.next_to(tagline, DOWN, buff=0.32)

        authors = T(
            "N. Ould Ouali · A.H. Sani · R. Bueno · J. Dauvet · T.L. Horstmann · E. Moulines",
            font_size=20, color=GREY,
        )
        authors.next_to(badge, DOWN, buff=0.30)

        affil = T("École Polytechnique · Hi! PARIS · McGill University",
                  font_size=17, color=GREY, slant=ITALIC)
        affil.next_to(authors, DOWN, buff=0.22)

        self.play(
            FadeIn(badge, shift=UP * 0.1),
            run_time=0.7,
        )
        self.play(
            FadeIn(authors, shift=UP * 0.08),
            FadeIn(affil, shift=UP * 0.08),
            run_time=0.8,
        )

        # Second pulse onde + flash titre
        self.play(
            waves[0].animate.set_opacity(0.8).scale([1, 1.3, 1]),
            run_time=0.6, rate_func=there_and_back,
        )
        self.wait(2.5)
        self.play(glow_flash(l2, color=RED, n=14, radius=0.4), run_time=0.7)
        self.wait(1.5)

        # ------------------------------------------------------------------
        # 6. Sortie — tout fond sauf les ondes (transition vers s01)
        # ------------------------------------------------------------------
        self.play(
            FadeOut(VGroup(badge, authors, affil, tagline)),
            run_time=0.8,
        )
        self.play(FadeOut(title), FadeOut(waves), run_time=1.2)