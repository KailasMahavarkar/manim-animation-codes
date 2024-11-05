from manim import *


class ListUtility:
    @staticmethod
    def create_1d_list(
        numbers,
        content,
        box_width=1,
        box_height=1,
        box_color=RED,
        box_fill_opacity=0,

        index_color=WHITE,
        content_color=WHITE,
        show_content=True,
        show_indexes=True,

        index_overrides={},
        box_overrides={},
        content_overrides={},
    ):
        """Creates a 1D vector (a series of boxes with numbers).

        Args:
            numbers (iterable): The numbers to display inside the boxes.
            indexes (iterable): The indexes to display above/below the boxes(controlled outside).
            box_width (float): The width of each box.
            box_height (float): The height of each box.
            box_color (Color): The color of each box.
            fill_opacity (float): The opacity of the box fill.
            show_content (bool): Whether to show the content inside the boxes.
            show_indexes (bool): Whether to show the indexes above/below the boxes
            index_color (Color): The color of the indexes.
            content_color (Color): The color of the content.
            index_overrides (dict): Additional arguments to pass to the Math Tex object for the indexes.
            box_overrides (dict): Additional arguments to pass to the Rectangle object for the boxes.
            content_overrides (dict): Additional arguments to pass to the Math Tex object for the content.

        Returns:
            VGroup: A group containing the boxes and a group containing the numbers.
        """

        if show_content and len(numbers) != len(content):
            raise ValueError(
                "The length of numbers and content must be the same.")

        content_group = VGroup()
        box_group = VGroup()
        index_group = VGroup()

        for i in numbers:
            # Create a rectangle for each number
            box = Rectangle(
                width=box_width,
                height=box_height,
                color=box_color,
                fill_opacity=box_fill_opacity,
                **box_overrides
            )

            # Position the box horizontally
            box.move_to([i * box_width, 0, 0])
            box_group.add(box)

            if show_indexes:
                # Create a MathTex object for the number
                number_text = MathTex(str(i), **index_overrides)
                number_text.set_color(index_color)
                number_text.move_to(box.get_center())
                index_group.add(number_text)

            if show_content:
                # Create a MathTex object for the content
                content_text = MathTex(content[i], **content_overrides)
                content_text.set_color(content_color)
                content_text.move_to(box.get_center())
                content_group.add(content_text)

        return box_group, index_group, content_group


    # TODO: Add support for 2d List 
    @staticmethod
    def create_2d_list(rows, cols, box_width=1, box_height=1, box_color=BLUE):
        """Creates a 2D vector (a grid of boxes with row, column indices).

        Args:
            rows (int): Number of rows.
            cols (int): Number of columns.
            box_width (float): The width of each box.
            box_height (float): The height of each box.
            box_color (Color): The color of each box.

        Returns:
            VGroup: A group containing the boxes and a group containing the numbers.
        """
        grid_group = VGroup()
        number_group = VGroup()

        for i in range(rows):
            for j in range(cols):
                # Create a rectangle for each grid cell
                box = Rectangle(
                    width=box_width,
                    height=box_height,
                    color=box_color,
                    fill_opacity=0.5
                )

                # Position each box in a grid
                box.move_to([j * box_width, -i * box_height, 0])
                grid_group.add(box)

                # Create a MathTex object for the (i, j) index
                number = MathTex(f"({i},{j})", font_size=24)
                number.move_to(box.get_center())
                number_group.add(number)

        return grid_group, number_group


class List1D(Scene):
    def construct(self):
        # Use the utility to create a 1D vector
        numbers = range(7)
        content = [0 for i in range(7)]

        box_group, index_group, content_group = ListUtility.create_1d_list(
            numbers,
            content,
            show_content=True,
            show_indexes=True,
            index_color=YELLOW,
            content_color=GREEN,
            box_overrides={
                "stroke_width": 1,
            }
        )

        # Center the groups
        box_group.move_to(ORIGIN)
        content_group.move_to(ORIGIN)
        index_group.move_to(ORIGIN + UP)

        # Add to the scene
        self.add(box_group, index_group, content_group)
        self.wait(10)


class List2D(Scene):
    def construct(self):
        # Use the utility to create a 2D vector (3x3 grid)
        rows, cols = 3, 3
        grid, index_group = ListUtility.create_2d_list(rows, cols)

        # Center the groups
        grid.move_to(ORIGIN)
        index_group.move_to(ORIGIN)

        # Add to the scene
        self.add(grid, index_group)
        self.wait(10)
