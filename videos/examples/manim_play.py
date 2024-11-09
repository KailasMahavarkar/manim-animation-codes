from exporter import *

class Sample(Scene):
    def construct(self):
        needle = Arrow(
            start=ORIGIN,
            end=RIGHT * 2,
            buff=0,
            thickness=0.1,
            color=WHITE,
        )

        self.add(
            Arrow(
                tip_shape=ArrowCircleTip
            )
        )

        self.play(Create(needle))
        self.wait(1)
