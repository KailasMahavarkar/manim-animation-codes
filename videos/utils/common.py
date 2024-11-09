from typing import Any
from typing import Literal
from manim import *

ShapeType = Literal["ARROW_SLIM", "ARROW"]

DIRECTIONS = Literal["UP", "DOWN", "LEFT", "RIGHT"]
DIRECTION_EXTENDED = Literal[
    "UP", "DOWN", "LEFT", "RIGHT",
    "UP_LEFT", "UP_RIGHT", "DOWN_LEFT", "DOWN_RIGHT"
]


def MakeShape(shape: ShapeType = "ARROW"):
    if shape == "ARROW":
        arrow = Arrow(
            start=[0, 0, 0],
            end=[0.5, 0.5, 0],
            buff=0,
            color=WHITE,
        )

        return arrow
    elif shape == 'ARROW_SLIM':
        polygon = Polygon(
            [0, 0, 0],
            [0.1, 0, 0],
            [0.1, 0.1, 0],
            [0.05, 0.15, 0],
            [0, 0.1, 0],
        )

        polygon.set_color(WHITE)
        polygon.set_fill(WHITE, opacity=1)
        return polygon
    else:
        return None

