from manim import *
config.renderer = "opengl"


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
                number_text = Text(str(i), **index_overrides)
                number_text.set_color(index_color)
                number_text.move_to(box.get_center())
                index_group.add(number_text)

            if show_content:
                # Create a MathTex object for the content
                content_text = Text(content[i], **content_overrides)
                content_text.set_color(content_color)
                content_text.move_to(box.get_center())
                content_group.add(content_text)

        return box_group, index_group, content_group

    @staticmethod
    def create_2d_list(
        data,
        indexes,
        cell_width=1,
        cell_height=1,
        cell_color=WHITE,
        cell_fill_opacity=0,
        cell_font_size=36,
        show_axis=True,
        show_indexes=True,
        x_axis_position=UP,
        y_axis_position=LEFT,
        x_axis_font_size=36,
        y_axis_font_size=36,
        x_axis_label="x",
        y_axis_label="y",
        y_axis_color=WHITE,
        x_axis_color=WHITE,
        y_axis_overrides={},
        x_axis_overrides={},
    ):
        """Creates a 2D vector (a grid of boxes with row, column indices).

        Args:
            data (iterable): The numbers to display inside the boxes.
            indexes (iterable): The indexes to display above/below the boxes(controlled outside).
            cell_width (float): The width of each box.
            cell_height (float): The height of each box.
            cell_color (Color): The color of each box.
            cell_fill_opacity (float): The opacity of the box fill.
            cell_font_size (int): The font size of the numbers inside the boxes.
            show_axis (bool): Whether to show the axis.
            show_indexes (bool): Whether to show the indexes above/below the boxes
            x_axis_position (np.array): The position of the x-axis.
            y_axis_position (np.array): The position of the y-axis.
            x_axis_font_size (int): The font size of the x-axis label.
            y_axis_font_size (int): The font size of the y-axis label.
            x_axis_label (str): The label for the x-axis.
            y_axis_label (str): The label for the y-axis.
            y_axis_color (Color): The color of the y-axis.
            x_axis_color (Color): The color of the x-axis.
            y_axis_overrides (dict): Additional arguments to pass to the Math

        Returns:
            VGroup: A group containing the boxes and a group containing the numbers.
        """
        if data == []:
            data = [[0, 0], [0, 0]]

        rows = len(data)
        cols = len(data[0])

        grid_group = VGroup()
        cell_group = VGroup()

        # axis representation
        y_axis = Line(ORIGIN, [0, (-rows * cell_height), 0], color=WHITE)
        x_axis = Line(ORIGIN, [(cols * cell_width), 0, 0], color=WHITE)

        for i in range(rows):
            for j in range(cols):
                # Create a rectangle for each grid cell
                cell = Rectangle(
                    width=cell_width,
                    height=cell_height,
                    color=cell_color,
                    fill_opacity=cell_fill_opacity
                )

                # Position each box in a grid
                cell.move_to([j * cell_width, -i * cell_height, 0])

                # Create a MathTex object for the (i, j) index
                cell_text = Text(f"{data[i][j]}", font_size=cell_font_size)
                cell_text.move_to(cell.get_center())
                cell_group.add(cell_text)

                if show_indexes:
                    # create a rectangle for each grid cell
                    index_rect = Rectangle(
                        width=cell_width,
                        height=cell_height / 4,
                        color=cell_color,
                        fill_opacity=0,
                        stroke_width=1
                    )

                    index_rect.move_to(cell, [1, -1, 0])
                    index_text = Text(f"{indexes[i][j]}", font_size=18)
                    index_text.move_to(index_rect.get_center())
                    index_rect.add(index_text)
                    cell.add(index_rect)

                grid_group.add(cell)

        grid_group.move_to(ORIGIN)
        cell_group.move_to(ORIGIN)

        if show_axis:
            x_axis.next_to(grid_group, x_axis_position, buff=0.25)
            y_axis.next_to(grid_group, y_axis_position, buff=0.25)

            x_axis_text = Text(
                x_axis_label,
                font_size=x_axis_font_size,
                color=x_axis_color,
                **x_axis_overrides
            ).next_to(
                x_axis, ORIGIN + x_axis_position
            )

            y_axis_text = Text(
                y_axis_label,
                font_size=y_axis_font_size,
                color=y_axis_color,
                **y_axis_overrides
            ).next_to(
                y_axis, ORIGIN + y_axis_position
            )

            grid_group.add(
                x_axis,
                y_axis,
                x_axis_text,
                y_axis_text
            )

            return grid_group, cell_group, [x_axis, y_axis], [x_axis_text, y_axis_text]

        return grid_group, cell_group, [], []
