from manim import *


class Effects:
    def shadow_clone_transform(self, old, new, delay=3, run_time=2, call=None, pre_call=None, post_call=None):
        old_shadow_clone = old.copy()
        if pre_call:
            pre_call()
        self.play(ReplacementTransform(old, new), run_time=2)
        if call:
            call()

        self.wait(delay)

        new_shadow_clone = new.copy()
        self.play(ReplacementTransform(new, old_shadow_clone), run_time=run_time)
        if post_call:
            post_call()
        return old_shadow_clone, new_shadow_clone
    
    def blink(self, obj, color=RED, time=0.5):
        obj.set_color(color)
        self.wait(time)


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
