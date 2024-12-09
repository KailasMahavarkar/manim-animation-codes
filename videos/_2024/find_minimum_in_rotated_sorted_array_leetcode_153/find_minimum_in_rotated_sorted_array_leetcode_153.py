from manim import *

class BarChartExample(Scene):
    def construct(self):
        chart = BarChart(
            values=[5, 6, 8, 1, 2],
            bar_names=[x for x in range(5)],
            y_range=[0, 10, 1],
            y_length=6,
            x_length=10, 
            x_axis_config={"font_size": 36},
        )

        c_bar_lbls = chart.get_bar_labels(font_size=48)
        self.add(chart, c_bar_lbls)