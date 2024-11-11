from manim import *

class ListUtility:
    @staticmethod
    def create_1d_list(
        numbers,
        content=None,
        box_width=1.0,
        box_height=1.0,
        show_content=True,
        show_indexes=True,
        box_index_spacing=0.8,
        index_overrides={},
        box_overrides={},
        content_overrides={},
    ):

        index_props = {
            "color": YELLOW,
            "font_size": 32,
            **index_overrides
        }

        content_props = {
            "color": RED,
            "font_size": 36,
            **content_overrides
        }

        box_props = {
            "stroke_color": WHITE,
            "stroke_width": 1,
            "color": BLUE,
            "fill_color": BLUE,
            "fill_opacity": 1,
            **box_overrides
        }

        """Creates a 1D vector (series of boxes with optional numbers and content)."""

        # Content length validation
        if show_content and content and len(numbers) != len(content):
            raise ValueError("The length of numbers and content must match.")

        content_group = VGroup()
        box_group = VGroup()
        index_group = VGroup()

        for i, number in enumerate(numbers):
            # Create a rectangle (box) for each number
            box = Rectangle(
                width=box_width,
                height=box_height,
                **box_props,
            )
            box.move_to([i * box_width, 0, 0])  # Position boxes horizontally
            box_group.add(box)

            # Create index numbers above the boxes
            if show_indexes:
                number_text = Text(str(number), **index_overrides)
                number_text.font_size = index_props["font_size"]
                number_text.font = "Times New Roman"
                number_text.set_color(index_props["color"])
                number_text.next_to(box, DOWN)  # Position below box
                index_group.add(number_text)

            # Add content inside the boxes (optional)
            if show_content and content:
                content_text = Text(str(content[i]),  **content_props)
                content_text.font_size = content_props["font_size"]
                content_text.set_color(content_props["color"])
                content_text.move_to(box.get_center())
                content_group.add(content_text)

        box_group.move_to(ORIGIN)
        content_group.move_to(ORIGIN)
        index_group.move_to(ORIGIN + DOWN * box_index_spacing)

        # Return all grouped elements
        return box_group, index_group, content_group

    @staticmethod
    def create_2d_list(
        # base props
        data,
        indexes,

        # cell props
        cell_width=1,
        cell_height=1,
        cell_color=WHITE,
        cell_fill_opacity=0,
        cell_font_size=36,

        # index props
        index_font_size=24,

        # control props
        show_axis=True,
        show_indexes=True,

        # axis props
        x_axis_position=UP,
        y_axis_position=LEFT,
        x_axis_font_size=36,
        y_axis_font_size=36,
        x_axis_label="x",
        y_axis_label="y",
        y_axis_color=WHITE,
        x_axis_color=WHITE,

        # overrides
        y_axis_overrides={},
        x_axis_overrides={},
        index_overrides={},
        index_text_overrides={},
        content_text_overrides={},
        box_overrides={},

        # transformers
        cell_transform_func=None,
        index_cell_transform_func=None,
        index_text_transform_func=None,
        content_text_transform_func=None,
    ):

        _content_text_overrides = {
            "font_size": cell_font_size,
            "color": WHITE,
            **content_text_overrides
        }

        _index_text_overrides = {
            "font_size": index_font_size,
            "color": WHITE,
            **index_text_overrides
        }

        """Creates a 2D vector (a grid of boxes with row, column indices).

        Args:
            # base props
            data (List[List[Any]]): A 2D list containing the data to be displayed.
            indexes (List[List[Any]]): A 2D list containing the row, column indices.

            # cell props
            cell_width (int, optional): The width of each cell. Defaults to 1.
            cell_height (int, optional): The height of each cell. Defaults to 1.
            cell_color (str, optional): The color of each cell. Defaults to WHITE.
            cell_fill_opacity (float, optional): The fill opacity of each cell. Defaults to 0.
            cell_font_size (int, optional): The font size of the cell content. Defaults to 36.

            # index props
            index_font_size (int, optional): The font size of the row, column indices. Defaults to 24.

            # control props
            show_axis (bool, optional): Whether to show the axis. Defaults to True.
            show_indexes (bool, optional): Whether to show the row, column indices. Defaults to True.

            # axis props
            x_axis_position (str, optional): The position of the x-axis. Defaults to UP.
            y_axis_position (str, optional): The position of the y-axis. Defaults to LEFT.
            x_axis_font_size (int, optional): The font size of the x-axis label. Defaults to 36.
            y_axis_font_size (int, optional): The font size of the y-axis label. Defaults to 36.
            x_axis_label (str, optional): The label of the x-axis. Defaults to "x".
            y_axis_label (str, optional): The label of the y-axis. Defaults to "y".
            y_axis_color (str, optional): The color of the y-axis. Defaults to WHITE.
            x_axis_color (str, optional): The color of the x-axis. Defaults to WHITE.

            # overrides
            y_axis_overrides (dict, optional): Additional properties for the y-axis. Defaults to {}.
            x_axis_overrides (dict, optional): Additional properties for the x-axis. Defaults to {}.
            index_overrides (dict, optional): Additional properties for the row, column indices. Defaults to {}.
            index_text_overrides (dict, optional): Additional properties for the row, column index text. Defaults to {}.
            content_text_overrides (dict, optional): Additional properties for the cell content text. Defaults to {}.
            box_overrides (dict, optional): Additional properties for the cell box. Defaults to {}.

            # transformers
            cell_transform_func (function, optional): A function to transform each cell. Defaults to None.
            index_cell_transform_func (function, optional): A function to transform each row, column index cell. Defaults to None.
            index_text_transform_func (function, optional): A function to transform each row, column index text. Defaults to None.  
            content_text_transform_func (function, optional): A function to transform each cell content text. Defaults to None.
            

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
                    fill_opacity=cell_fill_opacity,
                    **box_overrides
                )

                # Position each box in a grid
                cell.move_to([j * cell_width, -i * cell_height, 0])

                # Create a MathTex object for the (i, j) index
                cell_text = Text(
                    f"{str(data[i][j])}",  **_content_text_overrides)
                cell_text.move_to(cell.get_center())

                if content_text_transform_func and callable(content_text_transform_func):
                    content_text_transform_func(cell_text, i, j)

                if cell_transform_func and callable(cell_transform_func):
                    cell_transform_func(cell, i, j)

                cell_group.add(cell_text)

                if show_indexes:
                    # create a rectangle for each grid cell
                    index_rect = Rectangle(
                        width=cell_width,
                        height=cell_height / 4,
                        color=cell_color,
                        fill_opacity=0,
                        stroke_width=1,
                        **index_overrides
                    )

                    index_rect.move_to(cell, [1, -1, 0])
                    index_text = Text(
                        f"{indexes[i][j]}",  **_index_text_overrides)
                    index_text.move_to(index_rect.get_center())
                    index_rect.add(index_text)

                    if index_cell_transform_func and callable(index_cell_transform_func):
                        index_cell_transform_func(index_rect, i, j)

                    if index_text_transform_func and callable(index_text_transform_func):
                        index_text_transform_func(index_text, i, j)

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
