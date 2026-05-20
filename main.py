"""
main.py — Composition complète (~6 minutes, VivaTech)
=====================================================

Scènes enchaînées :
  0. SceneHook          ~15s   Hook cinématique
  1. SceneSound         ~35s   C'est quoi le son ?
  2. SceneSpeech        ~40s   La parole humaine
  3. SceneTTS           ~40s   TTS moderne & problème
  4. SceneSSML          ~35s   SSML : la solution
  5. ScenePipeline      ~45s   Notre pipeline
  6. SceneQwen          ~50s   QwenA + QwenB
  7. SceneResults       ~45s   Résultats
  8. SceneOutro         ~20s   Conclusion

Usage :
    manim -pqh main.py Main -o demo_vivatech.mp4 --fps 30
"""

import sys
import os

# Ajoute le répertoire courant au path pour importer theme et les scènes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from manim import *
from theme import *

# Imports des scènes
from scenes.s00_hook     import SceneHook
from scenes.s01_sound    import SceneSound
from scenes.s02_speech   import SceneSpeech
from scenes.s03_tts      import SceneTTS
from scenes.s04_ssml     import SceneSSML
from scenes.s05_pipeline import ScenePipeline
from scenes.s06_qwen     import SceneQwen
from scenes.s07_results  import SceneResults, SceneOutro


def _run_scene(parent_scene, SceneClass):
    """
    Exécute le construct() d'une scène dans le contexte de la scène parente.
    Technique standard Manim pour composer plusieurs scènes.
    """
    instance = SceneClass()
    instance.camera = parent_scene.camera
    instance.renderer = parent_scene.renderer
    instance.construct()
    parent_scene.wait(0.4)   # courte pause noire entre scènes


class Main(Scene):
    """Vidéo complète ~6 minutes."""

    def construct(self):
        scenes_sequence = [
            SceneHook,
            SceneSound,
            SceneSpeech,
            SceneTTS,
            SceneSSML,
            ScenePipeline,
            SceneQwen,
            SceneResults,
            SceneOutro,
        ]
        for SceneClass in scenes_sequence:
            _run_scene(self, SceneClass)
