from PIL import ImageFont
from matplotlib.font_manager import findSystemFonts
from manim import *
import os


MEDIA_DIR = os.path.abspath("media")

# config.renderer = "opengl"
# config.progress_bar = "display"
config.max_files_cached = 1000
config.media_dir = MEDIA_DIR
config.frame_rate = 30

FONT_NAME = "CMU Serif"

Text.set_default(
    font=FONT_NAME,
)

fonts = []
for filename in findSystemFonts():
    if "Emoji" not in filename and "18030" not in filename:
        font = ImageFont.FreeTypeFont(filename)
        name, weight = font.getname()
        fonts.append([name, weight, filename])


def getFont(name, weight):
    for font in fonts:
        if font[0] == name and font[1] == weight:
            return font

    # fallback font is CMU Serif
    return getFont("CMU Serif", "Regular")


base_code_config = {
    "tab_width": 4,
    "insert_line_no": True,
    "style": 'one-dark',
    "background": "window",
    "language": "cpp",
    "font": 'Consolas',
    "line_spacing": 0.5,
}
