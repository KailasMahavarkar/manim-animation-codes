from manim import ImageMobject
import os

ASSETS_PATH = os.path.abspath("assets")
IM_HAND_POINTER = ImageMobject(os.path.join(ASSETS_PATH, "hand_pointer.png")).scale(0.25)
