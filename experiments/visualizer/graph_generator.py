from manim import *
from viz import callgraph, viz

G_BLUE = ManimColor.from_hex("#5182eb")
G_RED = ManimColor.from_hex("#de1b3d")
G_YELLOW = ManimColor.from_hex("#f2c32d")


@viz
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


class CallGraphScene(MovingCameraScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.node_positions = {}
        self.node_spacing = 2
        self.depth_spacing = 2.2

        self.max_height = float('-inf')
        self.max_width = float('-inf')

    def compute_positions(self, node, depth=0, x_offset=0):
        """
        Recursively compute positions for nodes while centering them horizontally.
        """
        # If the node has no children, it's a leaf. Center it at the current x_offset.
        if not node["children"]:
            self.node_positions[node["uuid"]] = (
                x_offset, -depth * self.depth_spacing, 0)
            return 1  # Width of this subtree is 1

        # Calculate subtree widths and positions for all children
        subtree_widths = []
        total_width = 0
        total_height = 0

        for child in node["children"]:
            child_width = self.compute_positions(
                child,
                depth + 1,
                x_offset + total_width
            )
            subtree_widths.append(child_width)
            total_width += child_width * self.node_spacing
            total_height = max(total_height,  depth + 1)

        # Center the current node based on its children's total width
        width = sum(subtree_widths) * self.node_spacing
        height = total_height + 1

        center_x = x_offset + width / 2 - self.node_spacing / 2

        self.node_positions[node["uuid"]] = (
            center_x,
            -depth * self.depth_spacing,
            0
        )

        self.max_height = max(self.max_height, height)
        self.max_width = max(self.max_width, sum(subtree_widths))

        return sum(subtree_widths)

    def build_graph(self, node):
        node_uuid = node["uuid"]
        pos = self.node_positions[node_uuid]

        current_node = Rectangle(
            width=1.5,
            height=0.8,
            color=G_YELLOW,
        ).move_to(pos)
        label = Text(f"{node['fn_name']}({', '.join(map(str, node['args']))})", font_size=18).next_to(
            current_node, UP, buff=0.1
        )
        return_value = Text(f"Ret: {node['ret']}", font_size=16).next_to(
            current_node, DOWN, buff=0.1
        )

        node_group = VGroup(current_node, label, return_value)
        self.play(Create(node_group))

        for child in node["children"]:
            child_pos = self.node_positions[child["uuid"]]
            edge = CurvedArrow(
                current_node.get_bottom(),
                child_pos + 0.7*UP,
                color=DARK_BLUE,
                fill_opacity=0,
                angle=TAU / 5,
                stroke_color=G_BLUE,
                tip_length=0.2
            )
            edge.z_index = -1

            self.play(Create(edge))
            self.build_graph(child)

            return_edge = CurvedArrow(
                child_pos + 0.7*UP,
                current_node.get_bottom(),
                color=RED,
                angle=TAU / 5,
                fill_opacity=0,
                stroke_color=G_RED,
                tip_length=0.2
            )
            self.play(Create(return_edge))

        return node_group

    def construct(self):
        self.camera.frame.scale(1.5)
        self.camera.frame.move_to(ORIGIN + 3*RIGHT + 3*DOWN)

        callgraph.reset()
        fibonacci(10, 20)

        call_graph_data = callgraph.get_graph_dictionary()

        self.compute_positions(call_graph_data[0])  # First pass
        self.build_graph(call_graph_data[0])

        print("max_width:", self.max_width)
        print("max_height:", self.max_height)

        self.wait(3)
