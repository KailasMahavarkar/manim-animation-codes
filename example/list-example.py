from manim import *
from utils.list import ListUtility

class List1D(Scene):
    def construct(self):
        r = 10
        # Use the utility to create a 1D vector
        numbers = range(r)
        content = ["0" for _ in range(r)]

        box_group, index_group, content_group = ListUtility.create_1d_list(
            numbers,
            content,
            show_content=True,
            show_indexes=True,
            index_color=YELLOW,
            content_color=GREEN,
            box_overrides={
                "stroke_width": 1,
            },
            index_overrides={
                "font_size": 18,
            }
        )

        # Center the groups
        box_group.move_to(ORIGIN)
        content_group.move_to(ORIGIN)
        index_group.move_to(ORIGIN + DOWN * 0.75)

        # # merge them into a single group
        # singleton = VGroup()
        # singleton.add(box_group, index_group, content_group)

        # # scale down the group and move it to the top-right corner using animation
        # self.play(Create(singleton))

        # # scale down the group and move it to the top-right corner using animation
        # scaleDownTopRight = singleton.animate.scale(0.5).to_corner(UR)
        # self.play(scaleDownTopRight)

        # # scale up the group and move it to the bottom-left corner using animation
        # scaleUPCenter = singleton.animate.scale(2).center()
        # self.play(scaleUPCenter)

        # Add to the scene
        self.add(box_group, index_group, content_group)
        self.wait(10)


class List2D(Scene):
    def construct(self):
        # Use the utility to create a 2D vector (3x3 grid)
        rows, cols = 1, 26

        indexes = []
        data = [[0 for _ in range(cols)] for _ in range(rows)]
        counter = 0
        for _ in range(rows):
            v = []
            for _ in range(cols):
                v.append(counter)
                counter += 1
            indexes.append(v)

        data[0][10] = "248"

        grid, index_group, _, _ = ListUtility.create_2d_list(
            data=data,
            indexes=indexes,
            cell_fill_opacity=0,
            show_axis=False,
            show_indexes=True
        )

        # final group
        main_group = VGroup()
        main_group.add(grid, index_group)
        main_group.scale(0.5)

        self.add(main_group)
        self.wait(20)
