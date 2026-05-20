"""
main_short.py — Version 3 minutes (pitch directeur)
====================================================

Scènes sélectionnées :
  0. SceneHook        ~15s   Hook cinématique
  2. SceneSpeech      ~25s   Parole + 4 paramètres prosodiques (tronquée)
  3. SceneTTS         ~20s   Problème expressivité (tronqué)
  4. SceneSSML        ~20s   SSML solution (tronqué)
  5. ScenePipeline    ~25s   Pipeline + stats corpus
  6. SceneQwen        ~25s   QwenA/QwenB (tronqué)
  7. SceneResults     ~30s   MOS + KPIs
  8. SceneOutro       ~20s   Conclusion

Total : ~180s

Usage :
    manim -pqh main_short.py MainShort -o demo_3min.mp4 --fps 30
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manim import *
from theme import *

from scenes.s00_hook     import SceneHook
from scenes.s02_speech   import SceneSpeech
from scenes.s03_tts      import SceneTTS
from scenes.s05_pipeline import ScenePipeline
from scenes.s07_results  import SceneResults, SceneOutro


def _run_scene(parent_scene, SceneClass):
    instance = SceneClass()
    instance.camera = parent_scene.camera
    instance.renderer = parent_scene.renderer
    instance.construct()
    parent_scene.wait(0.3)


class MainShort(Scene):
    """Pitch deck 3 minutes."""

    def construct(self):
        scenes_sequence = [
            SceneHook,
            SceneSpeech,
            SceneTTS,
            ScenePipeline,
            SceneResults,
            SceneOutro,
        ]
        for SceneClass in scenes_sequence:
            _run_scene(self, SceneClass)
