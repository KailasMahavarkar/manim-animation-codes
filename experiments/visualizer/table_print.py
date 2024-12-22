from prettytable import PrettyTable


class TreePrinter:
    @staticmethod
    def table(tree, alignment="left", ignore_args_list=[]):
        """
        Prints the tree structure in a tabular format with dynamic column widths
        based on the maximum length of each column's data, with depth-based colors applied to the entire row.

        :param tree: A list containing recursion tree nodes.
        :param alignment: Alignment for arguments ('left', 'center', 'right').
        :param ignore_args_list: A list of arguments to be ignored in the table.
        """
        # Dictionary to store maximum widths for each column
        max_lengths = {
            "Depth": len("Depth"),
            "Function Name": len("Function Name"),
            "Hierarchy": len("Hierarchy"),
        }
        max_arg_lengths = {}  # To handle dynamic number of arguments

        color_palette = [
            "\033[37m",  # White
            "\033[91m",  # Red
            "\033[92m",  # Green
            "\033[93m",  # Yellow
            "\033[94m",  # Blue
            "\033[95m",  # Magenta
            "\033[96m",  # Cyan
        ]

        def colorize(text, color_code):
            """Apply color to text."""
            if color_code:
                return f"{color_code}{text}\033[0m"
            return text

        def first_pass(tree, depth, prefix):
            """First pass: Calculate max widths for each column."""
            for node in tree:
                # Filter arguments based on ignore_args_list
                args = [arg for i, arg in enumerate(
                    node.get('args', [])) if i not in ignore_args_list]
                hierarchy = f"{prefix} └── {node['fn_name']}({[*args]})"
                max_lengths["Depth"] = max(
                    max_lengths["Depth"], len(str(depth)))
                max_lengths["Function Name"] = max(
                    max_lengths["Function Name"], len(node['fn_name']))
                max_lengths["Hierarchy"] = max(
                    max_lengths["Hierarchy"], len(hierarchy))

                # Update max lengths for arguments
                for i, arg in enumerate(args):
                    arg_key = f"Arg {i + 1}"
                    max_arg_lengths[arg_key] = max(
                        max_arg_lengths.get(arg_key, 0), len(str(arg)))

                # Recurse for children
                if 'children' in node and node['children']:
                    first_pass(node['children'], depth + 1, prefix + "    ")

        def second_pass(tree, depth, prefix, table):
            """Second pass: Populate the table with data."""
            for node in tree:
                # Filter arguments based on ignore_args_list
                args = [arg for i, arg in enumerate(
                    node.get('args', [])) if i not in ignore_args_list]
                hierarchy = f"{prefix} └── {node['fn_name']}({[*args]})"

                # Apply color based on depth (indexing from color_palette)
                depth_color = color_palette[depth % len(
                    color_palette)] if depth < len(color_palette) else None

                row = [
                    colorize(depth, depth_color),
                    colorize(node['fn_name'], None),
                    colorize(hierarchy, None),
                ]

                # Add arguments with padding for missing ones
                for i in range(len(max_arg_lengths)):
                    row.append(
                        colorize(args[i] if i < len(args) else "", None))

                # Apply color to the entire row
                colored_row = [colorize(cell, depth_color) for cell in row]
                table.add_row(colored_row)

                # Recurse for children
                if 'children' in node and node['children']:
                    second_pass(
                        node['children'],
                        depth + 1,
                        prefix + "    ",
                        table
                    )

        # First pass to calculate maximum widths
        first_pass(tree, 0, "")

        headers = ["Depth", "Function Name", "Hierarchy"] + \
            list(max_arg_lengths.keys())
        table = PrettyTable()
        table.field_names = headers

        # Set alignment
        align_options = {"left": "l", "center": "c", "right": "r"}
        if alignment not in align_options:
            raise ValueError(
                "Invalid alignment. Choose from 'left', 'center', or 'right'."
            )

        for key, max_length in max_lengths.items():
            table.max_width[key] = max_length
        for arg_key, max_length in max_arg_lengths.items():
            table.max_width[arg_key] = max_length
            table.align[arg_key] = align_options[alignment]  # Set alignment

        # Always left-align the hierarchy
        table.align["Hierarchy"] = "l"

        second_pass(tree, 0, "", table)
        print(table)
