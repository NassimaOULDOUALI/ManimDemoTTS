# TTS SSML Prosody Control — Manim Demo (v2, VivaTech Edition)

**Paper:** [Improving French Synthetic Speech Quality via SSML Prosody Control](https://aclanthology.org/2025.icnlsp-1.30/)  
**Authors:** Nassima Ould Ouali, Awais Hussain Sani, Ruben Bueno, Jonah Dauvet, Tim Luka Horstmann, Eric Moulines  
**Venue:** ICNLSP 2025 · École Polytechnique / Hi! PARIS

---

## Structure

```
ManimDemoTTS_v2/
├── scenes/
│   ├── s00_hook.py          # 0 — Hook : onde sonore "wow" d'entrée (15s)
│   ├── s01_sound.py         # 1 — C'est quoi le son ? (waveform live, 35s)
│   ├── s02_speech.py        # 2 — La parole humaine : F0, formants (40s)
│   ├── s03_tts.py           # 3 — TTS moderne : pipeline + problème expressivité (40s)
│   ├── s04_ssml.py          # 4 — SSML : balises prosodiques (35s)
│   ├── s05_pipeline.py      # 5 — Notre pipeline bout-en-bout (45s)
│   ├── s06_qwen.py          # 6 — Architecture QwenA + QwenB (50s)
│   ├── s07_results.py       # 7 — Résultats : MOS, F1, MAE (45s)
│   └── s08_outro.py         # 8 — Conclusion + futur (20s)
├── main.py                  # Composition complète (~6 min)
├── main_short.py            # Version 3 min directeur
├── theme.py                 # Palette, fonts, helpers partagés
├── assets/                  # Images (pipeline.png, etc.)
├── manim.cfg                # Config rendu
└── README.md
```

## Durée cible

| Version | Durée | Usage |
|---------|-------|-------|
| `main.py` | ~6 min | VivaTech, conférence |
| `main_short.py` | ~3 min | Pitch directeur |

## Rendu

```bash
# Version complète
manim -pqh main.py Main -o demo_vivatech.mp4 --fps 30

# Version courte
manim -pqh main_short.py MainShort -o demo_3min.mp4 --fps 30

# Scène individuelle (test)
manim -pqh scenes/s07_results.py SceneResults
manim -pqh scenes/s00_hook.py SceneHook
```

## Installation

```bash
pip install manim
manim --version  # >= 0.18.0
```

## Palette

- Background : `#004178` (bleu Hi! PARIS)
- Accent rouge : `#FF0049`
- Cyan : `#14B8FF`
- Or : `#FFD166`
- Vert résultat : `#06D6A0`
- Texte : `#F4F6FA`
