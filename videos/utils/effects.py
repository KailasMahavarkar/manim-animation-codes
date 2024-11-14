from exporter import *


class Shuriken(Scene):
    def create_shuriken(self, blade_color=GRAY, outline_color=BLACK):
        blade = Polygon(
            [0.0, 1.25, 0.0],
            [0.375, 0.375, 0.0],
            [1.25, 0.0, 0.0],
            [0.375, -0.375, 0.0],
            [0.0, -1.25, 0.0],
            [-0.375, -0.375, 0.0],
            [-1.25, 0.0, 0.0],
            [-0.375, 0.375, 0.0],
            [0.0, 1.25, 0.0],
            fill_opacity=1, color=blade_color, stroke_color=outline_color, stroke_width=4
        )

        hollow_circle = Circle(
            radius=0.2, color=outline_color, fill_opacity=1, stroke_width=4)

        shuriken = VGroup(blade,  hollow_circle)
        return shuriken
