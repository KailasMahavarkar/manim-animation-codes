from manim import *

class TreeUtility:
    @staticmethod
    def create_tree(
        data,
        node_radius=0.3,
        node_color=YELLOW,
        node_fill_opacity=1.0,
        edge_color=WHITE,
        edge_thickness=3,
        label_color=BLACK,
        label_font_size=24,
        show_labels=True,
        level_gap=1.5,
        sibling_gap=1.5,
    ):
        """Creates a tree visualization with visible nodes and connecting edges."""

        def build_tree(data, parent=None, level=0, x_offset=0):
            tree_group = VGroup()
            y_pos = -level * level_gap
            x_pos = x_offset

            for i, (node_label, subtree) in enumerate(data.items()):
                # Create the node
                node = Circle(
                    radius=node_radius,
                    color=node_color,
                    fill_opacity=node_fill_opacity
                ).move_to([x_pos, y_pos, 0])
                tree_group.add(node)

                # Add label inside node
                if show_labels:
                    label = Text(
                        str(node_label),
                        font_size=label_font_size,
                        color=label_color
                    ).move_to(node.get_center())
                    tree_group.add(label)

                # Draw edge to parent if exists
                if parent:
                    edge = Line(
                        start=parent.get_center(),
                        end=node.get_center(),
                        color=edge_color,
                        stroke_width=edge_thickness
                    )
                    tree_group.add(edge)

                # Recursively build subtree
                if subtree:
                    num_children = len(subtree)
                    total_width = (num_children - 1) * sibling_gap
                    start_offset = -(total_width / 2)

                    for j, (child_label, child_subtree) in enumerate(subtree.items()):
                        child_x_pos = x_pos + start_offset + j * sibling_gap
                        tree_group.add(
                            build_tree({child_label: child_subtree},
                                       node, level + 1, child_x_pos)
                        )

            return tree_group

        return build_tree(data)
