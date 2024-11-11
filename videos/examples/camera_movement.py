from exporter import *


class Video(MovingCameraScene, Scene):
    def construct(self):
        self.camera.frame.save_state()

        # create the axes and the curve
        ax = Axes(x_range=[0, 20], y_range=[0, 20])
        graph = ax.plot(lambda x: np.sin(x), color=BLUE, x_range=[0, 5 * PI])

        # create dots based on the graph
        moving_dot = Dot(ax.i2gp(graph.t_min, graph), color=ORANGE)

        self.add(ax, graph, moving_dot)
        self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))

        def update_curve(m): return m.move_to(moving_dot)

        self.camera.frame.add_updater(update_curve)
        self.play(MoveAlongPath(moving_dot, graph, rate_func=linear))

        self.camera.frame.remove_updater(update_curve)
        self.play(Restore(self.camera.frame))


class CameraMovement(MovingCameraScene, Scene):
    def construct(self):

        self.cam = self.camera.frame.animate

        group = VGroup()
        group.add(*[Rectangle(
            width=1, height=1, fill_opacity=0.5, color=BLUE
        ) for _ in range(10)])
        group.arrange(RIGHT, buff=0)

        # glowing dot
        dot = Dot(color=RED, fill_opacity=0, stroke_width=2)
        dot.move_to(group[0].get_center())

        self.add(group, dot)

        scale_count = 0
        for i in range(1, len(group)):
            self.play(self.cam.move_to(
                group[i].get_center()), run_time=0.5)

            # make dot active
            dot.move_to(group[i].get_center())
            self.wait(1)
            if scale_count == 0:
                self.play(self.cam.scale(0.25), run_time=0.5)
                self.wait(1)
                scale_count = 1

        self.remove(dot)
        dot.move_to(group[0].get_center())

        

        # rows, cols = 5, 6

        # indexes = []
        # data = [[0 for _ in range(cols)] for _ in range(rows)]
        # counter = 0
        # for _ in range(rows):
        #     v = []
        #     for _ in range(cols):
        #         v.append(counter)
        #         counter += 1
        #     indexes.append(v)

        # grid, index_group, _, _ = ListUtility.create_2d_list(
        #     data=data,
        #     indexes=indexes,
        #     cell_fill_opacity=0,
        #     show_axis=False,
        #     show_indexes=True
        # )

        # self.add(grid)
        # scale_factor = 1/4
        # self.play(self.cam.move_to(grid[6]).scale(scale_factor), run_time=2)
        # self.play(self.cam.move_to(grid[10]), run_time=2)
        # self.play(self.cam.move_to(ORIGIN).scale(1/scale_factor), run_time=2)

        # self.wait(10)
