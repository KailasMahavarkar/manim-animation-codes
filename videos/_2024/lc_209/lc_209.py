from exporter import *
from contextlib import suppress


class MinimumSizeSubarraySum(MovingCameraScene):
    def construct(self):
        self.cam = self.camera.frame.animate
        self.arr = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 40, 40, 0, 0]
        self.target = 82
        self.cam.scale(1.2)

        self.box_size = 1

        # Create array visualization
        array_group = VGroup()

        for i, x in enumerate(self.arr):
            index_text = Text(str(i), font_size=24)
            box = Rectangle(color=BLUE, width=self.box_size,
                            height=self.box_size)
            text = Text(text=str(x), font_size=24)
            text.move_to(box.get_center())
            box.add(text)
            index_text.move_to(box.get_top() + UP * 0.2)
            box.add(index_text)

            array_group.add(box)
        array_group.arrange(RIGHT, buff=0.1)

        self.add(array_group)

        # Title
        title = Text(
            "Minimum Size Subarray Sum: Binary Search + Sliding Window",
            font_size=32,
            color=GOLD,
        )
        title.next_to(array_group, UP, buff=0.5)
        self.play(Write(title))

        # Create the arrows with labels
        sp_arrow = Arrow(DOWN, 0.5 * UP).next_to(array_group[0], DOWN)
        ep_arrow = Arrow(DOWN, 0.5 * UP).next_to(array_group[-1], DOWN)
        mp_arrow = Arrow(
            DOWN, 0.5 * UP).next_to(array_group[len(self.arr) // 2], DOWN)

        # Labels for the arrows
        sg = VGroup(sp_arrow, Text(
            "s", font_size=32).next_to(sp_arrow, DOWN))
        eg = VGroup(ep_arrow, Text(
            "e", font_size=32).next_to(ep_arrow, DOWN))
        mg = VGroup(mp_arrow, Text(
            "m", font_size=32).next_to(mp_arrow, DOWN))

        sg.set_color(G_BLUE)
        eg.set_color(G_RED)
        mg.set_color(G_GREEN)

        self.play(Create(sg), Create(eg))
        self.wait(1)

        # Sliding Window Check

        def isValid(length):
            current_sum = sum(self.arr[:length])
            window_rect = SurroundingRectangle(
                array_group[:length], color=YELLOW, buff=0.1)
            self.play(Create(window_rect))
            self.wait(0.5)

            if current_sum >= self.target:
                self.play(window_rect.animate.set_fill(GREEN, 0.5))
                self.wait(5)
                self.remove(window_rect)
                return True

            for i in range(length, len(self.arr)):
                current_sum += self.arr[i] - self.arr[i - length]
                self.play(
                    window_rect.animate.surround(
                        array_group[i - length + 1:i + 1])
                )
                self.wait(0.5)
                if current_sum >= self.target:
                    self.play(window_rect.animate.set_fill(GREEN, 0.5))
                    self.wait(3)
                    self.remove(window_rect)
                    return True

            self.play(FadeOut(window_rect))
            return False

        def binary_search(nums):
            s = 0
            e = len(nums) - 1
            result = -1  # To store the result of the minimum length subarray
            iteration = 1

            # Set positions for the initial arrows and labels
            self.play(
                sg.animate.move_to(
                    array_group[s].get_bottom() + DOWN + LEFT * 0.35),
                mg.animate.move_to(
                    array_group[s + (e - s) // 2].get_bottom() + DOWN),
                eg.animate.move_to(
                    array_group[e].get_bottom() + DOWN + RIGHT * 0.35)
            )
            self.wait(1)

            self.play(title.animate.scale(1).to_edge(UP, buff=0.5))

            while s <= e:
                mid = s + (e - s) // 2  # Calculate the midpoint

                # update the positions for the arrows and labels
                self.play(
                    mg.animate.move_to(
                        array_group[mid].get_bottom() + DOWN),
                )

                if isValid(mid):
                    result = mid
                    e = mid - 1  # Try smaller subarrays
                    with suppress(Exception):
                        self.play(eg.animate.move_to(
                            array_group[e].get_bottom() + DOWN + RIGHT * 0.35))
                else:
                    # If the sum is not valid, try larger subarrays
                    s = mid + 1
                    with suppress(Exception):
                        self.play(
                            sg.animate.move_to(
                                array_group[s].get_bottom() + DOWN + LEFT * 0.35)
                        )

                iteration += 1

            print("result -->", result)

        # Call binary search
        binary_search(self.arr)
