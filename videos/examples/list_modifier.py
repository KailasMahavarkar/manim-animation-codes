from manim import *

class Video(Scene):
    def construct(self):
        grid = VGroup()

        # Create initial grid with rectangles containing "0"
        for _ in range(4):
            r = Rectangle(width=1, height=1, fill_opacity=0.5, color=BLUE)
            r.add(Text("0", font_size=32, color=WHITE))
            grid.add(r)

        grid.arrange_in_grid(2, 2, buff=0)

        self.play(Create(grid))
        self.wait(1)

        # Replace the text in grid[0] from "0" to "1"
        old_text = grid[0][1]  # Text inside the first rectangle
        new_text = Text("1", font_size=32, color=WHITE).move_to(old_text.get_center())

        print(grid[0][1].get_text())
        self.play(ReplacementTransform(old_text, new_text))
        print(grid[0][1].get_text())

        self.wait(2)
        self.play(FadeOut(grid))


        self.wait(3)
