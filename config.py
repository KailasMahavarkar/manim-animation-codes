from manim import *
import os

MEDIA_DIR = os.path.abspath("media")

# config.renderer = "opengl"
# config.progress_bar = "display"
config.max_files_cached = 1000
config.media_dir = MEDIA_DIR
config.frame_rate = 24


Text.set_default(
    font="CMU Serif",
)
