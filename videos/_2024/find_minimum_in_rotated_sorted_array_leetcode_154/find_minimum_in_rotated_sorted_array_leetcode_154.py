import os
from exporter import *
config.frame_size = (1000, 1000)


ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
CODE_PATH = os.path.join(ROOT_PATH, "code.cpp")


class Sample(Effects, Shuriken, MovingCameraScene):
    def construct(self):
        self.cam = self.camera.frame
        self.cam.scale(1)

        def points_maker(arr):
            # Adjust points to align with the NumberPlane's coordinate system
            x_index = np.arange(len(arr))  # x coordinates
            z_index = np.zeros(len(arr))  # z coordinates

            # Convert the input data into points
            points = [axes.c2p(x, y, z)
                      for x, y, z in zip(x_index, arr, z_index)]

            # Create dots and lines for the points
            dots = VGroup(*[Dot(p, radius=0.1) for p in points])
            lines = VGroup(*[Line(points[i], points[i + 1])
                           for i in range(len(points) - 1)])

            # Create labels for the points
            labels = VGroup()
            for i, (x, y) in enumerate(zip(x_index, arr)):
                coord_label = MathTex(f"{y}").scale(0.7)

                label_pos = UP * 0.8 + RIGHT * 0.5
                if (i < len(arr) - 1):
                    if points[i][1] < points[i + 1][1]:
                        label_pos = DOWN * 0.8 + RIGHT * 0.5

                coord_label.next_to(points[i],  label_pos)
                labels.add(coord_label)

            return dots, lines, labels

        # Create the NumberPlane
        axes = NumberPlane(
            x_range=[0, 8, 1],  # x-range with step size
            y_range=[0, 8, 1],  # y-range with step size
            x_length=8,  # Length of x-axis
            y_length=8,  # Length of y-axis
            x_axis_config={
                "include_numbers": True
            },
            y_axis_config={
                "include_numbers": True,
                "label_direction": 1.5*LEFT
            },
            background_line_style={"stroke_width": 0.5},

        )

        y_label = axes.get_y_axis_label(
            "value", edge=LEFT, direction=LEFT, buff=0.4)
        x_label = axes.get_x_axis_label(
            "index", edge=UR, direction=UP, buff=0.4)

        grid_label = VGroup(y_label, x_label)

        # Add the axes
        # self.add(axes, grid_label)

        def play_arr(arr):
            dots, lines, labels = points_maker(arr)
            self.add(dots, lines, labels)
            # self.wait(3)
            # self.remove(dots, lines, labels)

        # play_arr([5, 5, 5, 2, 5, 5])

        # play_arr([6, 1, 2, 2, 5, 5])
        # play_arr([5, 5, 5, 2, 5, 5, 5, 5])
        # Wait to view the output
        # self.wait(2)

       