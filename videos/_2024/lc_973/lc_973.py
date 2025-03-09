from exporter import *
import math


class LC973(MovingCameraScene):
    def construct(self):
        # Text Label for Problem Statement
        title = Text("LC 973: K Closest Points to Origin",
                     font_size=48, color=WHITE)
        self.play(Write(title))
        self.wait(1)

        # Points to display
        points = [
            [2, 3],
            [3, 4],
            [1, -1],
            [-2, -3],
            [-3, 3],
            [4, 1],
            [0, 0],
            [-1, 2]
        ]

        # Create 2D plane
        plane = NumberPlane(
            x_range=[-5, 5], y_range=[-5, 5], axis_config={"color": BLUE})
        self.play(Create(plane))

        # Create points as dots on the plane
        points_dots = []
        for point in points:
            dot = Dot(plane.c2p(point[0], point[1]), color=RED)
            points_dots.append(dot)
            self.play(FadeIn(dot))

        self.wait(1)

        # Calculate the distances of each point and use a max heap to find k closest points
        k = 3
        distances = MaxHeap()
        for point in points:
            x1, y1 = point
            d = math.sqrt(x1**2 + y1**2)
            # Use negative distance to simulate max heap
            distances.push((-d, point))

        # Visualize the heap process (adding and removing elements)
        heap_group = VGroup(*points_dots)
        self.play(Write(heap_group))
        self.wait(1)

        # Pop points from heap until we have k closest points
        while distances.size > k:
            popped = distances.pop()
            # Remove the farthest point
            farthest_point = popped[1]
            farthest_dot = next(dot for dot in points_dots if np.allclose(
                dot.get_center(), plane.c2p(farthest_point[0], farthest_point[1])))

            self.play(FadeOut(farthest_dot))
            points_dots.remove(farthest_dot)

        self.wait(1)

        # Highlight the k closest points (those left in the heap)
        closest_points = [dot for dot in points_dots]
        for dot in closest_points:
            dot.set_color(YELLOW)
            self.play(dot.animate.set_color(YELLOW))

        # Final state of the scene with highlighted closest points
        self.wait(2)

