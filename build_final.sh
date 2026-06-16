#!/usr/bin/env bash
# =====================================================================
# build_final.sh — Assemble la vidéo VivaTech complète
# ---------------------------------------------------------------------
# Rend les 9 scènes en 1080p60, régénère concat_list.txt, puis
# concatène le tout avec ffmpeg.
#
# À LANCER DEPUIS LA RACINE DU PROJET :
#     cd /mnt/c/Users/NassimaOULDOUALI/Desktop/ManimDemoTTS_v2/ManimDemoTTS_v2
#     bash build_final.sh
# =====================================================================
set -e

RES="1080p60"                       # correspond à -qh
OUT="demo_vivatech_final.mp4"

# (fichier scène : classe Manim)  — ordre = ordre de la vidéo
scenes=(
  "scenes/s00_hook.py:SceneHook"
  "scenes/s01_sound.py:SceneSound"
  "scenes/s02_speech.py:SceneSpeech"
  "scenes/s03_tts.py:SceneTTS"
  "scenes/s04_ssml.py:SceneSSML"
  "scenes/s05_pipeline.py:ScenePipeline"
  "scenes/s06_qwen.py:SceneQwen"
  "scenes/s07_results.py:SceneResultsOutro"
  "scenes/s08_ack.py:SceneAck"
)

echo "==================================================================="
echo " 1/3  Rendu des 9 scènes en ${RES}"
echo "==================================================================="
for entry in "${scenes[@]}"; do
  file="${entry%%:*}"
  cls="${entry##*:}"
  echo ""
  echo ">>> $cls  ($file)"
  manim -qh --disable_caching "$file" "$cls"
done

echo ""
echo "==================================================================="
echo " 2/3  Génération de concat_list.txt"
echo "==================================================================="
: > concat_list.txt
for entry in "${scenes[@]}"; do
  file="${entry%%:*}"
  cls="${entry##*:}"
  stem="$(basename "$file" .py)"           # ex. s00_hook
  echo "file 'media/videos/${stem}/${RES}/${cls}.mp4'" >> concat_list.txt
done
cat concat_list.txt

echo ""
echo "==================================================================="
echo " 3/3  Concaténation ffmpeg -> ${OUT}"
echo "==================================================================="
# Copie des flux sans ré-encodage (rapide). Toutes les scènes ont les
# mêmes paramètres (1080p60, h264), donc -c copy fonctionne.
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy "$OUT"

# --- Si la vidéo finale a des saccades / problèmes de transition, ---
# --- commente la ligne ci-dessus et décommente celle-ci (ré-encodage) :
# ffmpeg -y -f concat -safe 0 -i concat_list.txt \
#        -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow "$OUT"

echo ""
echo "✓ Terminé. Vidéo finale : $(pwd)/${OUT}"
