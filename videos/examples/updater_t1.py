from exporter import *

class Video(Scene):
    def construct(self):
        # Initial camera setup (move camera to origin)
        self.camera.move_to(ORIGIN)

        boxes = VGroup(*[
            Dot() for _ in range(16*9)
        ]).arrange_in_grid(9, 16, buff=1)

        self.add(boxes)

        growing_circle = Circle(
            0.1,
            color=PURPLE,
            fill_opacity=0.5
        ).shift(0.1*LEFT + 0.3*UP)

        self.add(growing_circle)

        growing_circle.add_updater(
            lambda c, dt: c.scale_to_fit_width(c.width + dt)
        )

        def number_of_dots_in_circle():
            return len([
                dot for dot in boxes
                if np.linalg.norm(dot.get_center() - growing_circle.get_center()) < growing_circle.width/2
            ])

        for _ in range(15):
            dots_inside = number_of_dots_in_circle()
            self.wait_until(lambda: number_of_dots_in_circle() != dots_inside)
            growing_circle.suspend_updating()
            self.wait(0.5)
            growing_circle.resume_updating()
