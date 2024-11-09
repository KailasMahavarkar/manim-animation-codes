from exporter import *


class WeightedTreeUtility:
    @staticmethod
    def build_tree_with_weights(
        tree_data,
        edge_weights,
        parent_pos=ORIGIN,
        level_gap=2,
        sibling_gap=3,
        x_offset=0,
    ):
        """
        Recursively builds tree with weighted edges.

        Args:
            tree_data (dict): Nested dictionary defining node structure.
            edge_weights (dict): Edge weights {("A", "B"): "5", ("A", "C"): "3"}.
            parent_pos (array): Position of the parent node.
        """
        nodes = VGroup()
        edges = VGroup()

        for node_label, (left_child, right_child) in tree_data.items():
            # Create node
            node = WeightedTreeUtility.create_node(
                node_label).move_to(parent_pos)
            nodes.add(node)

            # Define positions for left and right children
            x_pos_left = parent_pos[0] - sibling_gap / (level_gap + 0.5)
            x_pos_right = parent_pos[0] + sibling_gap / (level_gap + 0.5)
            y_pos = parent_pos[1] - level_gap

            # Add left child
            if left_child != "X":
                left_pos = [x_pos_left, y_pos, 0]
                left_node = WeightedTreeUtility.create_node(
                    left_child).move_to(left_pos)
                edge_left = WeightedTreeUtility.create_edge_with_weight(
                    parent_pos, left_pos, edge_weights.get(
                        (node_label, left_child), "")
                )
                nodes.add(left_node)
                edges.add(edge_left)

                # Recursive call for left subtree
                child_nodes, child_edges = WeightedTreeUtility.build_tree_with_weights(
                    {left_child: tree_data.get(left_child, ("X", "X"))},
                    edge_weights,
                    parent_pos=left_pos,
                    level_gap=level_gap,
                    sibling_gap=sibling_gap,
                )
                nodes.add(child_nodes)
                edges.add(child_edges)

            # Add right child
            if right_child != "X":
                right_pos = [x_pos_right, y_pos, 0]
                right_node = WeightedTreeUtility.create_node(
                    right_child).move_to(right_pos)
                edge_right = WeightedTreeUtility.create_edge_with_weight(
                    parent_pos, right_pos, edge_weights.get(
                        (node_label, right_child), "")
                )
                nodes.add(right_node)
                edges.add(edge_right)

                # Recursive call for right subtree
                child_nodes, child_edges = WeightedTreeUtility.build_tree_with_weights(
                    {right_child: tree_data.get(right_child, ("X", "X"))},
                    edge_weights,
                    parent_pos=right_pos,
                    level_gap=level_gap,
                    sibling_gap=sibling_gap,
                )
                nodes.add(child_nodes)
                edges.add(child_edges)

        return nodes, edges

    @staticmethod
    def create_node(label, node_radius=0.3, node_color=YELLOW, font_size=24):
        """Creates a labeled node (circle + text inside)."""
        node = Circle(radius=node_radius, color=node_color, fill_opacity=1)
        label = Text(str(label), font_size=font_size,
                     color=BLACK).move_to(node.get_center())
        return VGroup(node, label)

    @staticmethod
    def create_edge_with_weight(start, end, weight, edge_color=WHITE, font_size=18):
        """Creates a line between two points with a weight in the middle."""
        edge = Line(start=start, end=end, color=edge_color, stroke_width=2)
        weight_label = Text(str(weight), font_size=font_size, color=WHITE).move_to(
            edge.get_center() + UP * 0.2
        )
        return VGroup(edge, weight_label)


class WeightedTreeScene(Scene):
    def construct(self):
        # Tree Structure: "X" means no child (empty)
        tree_data = {
            "A": ("B", "C"),
            "B": ("D", "E"),
            "C": ("X", "F"),
            "D": ("X", "X"),
            "E": ("X", "X"),
            "F": ("G", "H"),
            "G": ("X", "X"),
            "H": ("X", "X"),
        }

        # Edge weights
        edge_weights = {
            ("A", "B"): "5",
            ("A", "C"): "3",
            ("B", "D"): "2",
            ("B", "E"): "7",
            ("C", "F"): "1",
            ("F", "G"): "4",
            ("F", "H"): "6",
        }

        # Build tree
        nodes, edges = WeightedTreeUtility.build_tree_with_weights(
            tree_data, edge_weights)

        # Animate
        self.play(Create(edges), run_time=2)
        self.play(FadeIn(nodes), run_time=2)
        self.wait(3)
