from exporter import *

class Sample(Effects, MovingCameraScene):
    def construct(self):
        self.cam = self.camera.frame.animate
        self.arr = [8, 9, 10, 1, 2, 3, 4, 5, 6]
        self.target = 4

        # Create the array visualization with surrounding rectangles
        array_group = VGroup()
        for i, x in enumerate(self.arr):
            index_text = Text(str(self.arr.index(x)), font_size=24)

            box = Rectangle(color=RED, width=1, height=1)

            text = Text(text=str(x), font_size=24)
            text.move_to(box.get_center())
            box.add(text)
            index_text.move_to(box.get_top() + UP*0.2)
            box.add(index_text)

            # Surrounding rectangle
            surrounding_rect = Rectangle(color=WHITE, width=1.2, height=1.2)  # White border
            surrounding_rect.move_to(box.get_center())

            array_group.add(surrounding_rect, box)  # Add both the surrounding rect and the box

        array_group.arrange(RIGHT, buff=0.1)
        self.add(array_group)

        # Create the arrows with labels
        sp_arrow = Arrow(DOWN, 0.5 * UP).next_to(array_group[0], DOWN)
        ep_arrow = Arrow(DOWN, 0.5 * UP).next_to(array_group[-1], DOWN)
        mp_arrow = Arrow(DOWN, 0.5 * UP).next_to(array_group[len(self.arr) // 2], DOWN)

        # Labels for the arrows
        sg = VGroup(sp_arrow, Text("s", font_size=32).next_to(sp_arrow, DOWN))
        eg = VGroup(ep_arrow, Text("e", font_size=32).next_to(ep_arrow, DOWN))
        mg = VGroup(mp_arrow, Text("m", font_size=32).next_to(mp_arrow, DOWN))

        sg.set_color(G_BLUE)
        eg.set_color(G_RED)
        mg.set_color(G_GREEN)

        # Title text
        title = Text("Binary Search in Rotated Sorted Array", font_size=32, color=G_YELLOW)
        title.next_to(array_group, UP, buff=0.5)
        self.play(Write(title))

        def code(arr, target):
            s = 0
            e = len(arr) - 1
            mid = s + (e - s) // 2
            iteration = 1

            # Set positions for the initial arrows and labels
            sg.move_to(array_group[s].get_bottom() + DOWN + LEFT * 0.35)
            mg.move_to(array_group[mid].get_bottom() + DOWN)
            eg.move_to(array_group[e].get_bottom() + DOWN + RIGHT * 0.35)

            self.play(Create(sg), Create(eg))
            self.wait(1)

            # Move the title above the array group
            self.play(title.animate.scale(1).to_edge(UP, buff=0.5))

            while s <= e:
                prev_s = s
                prev_e = e

                if iteration == 1:
                    self.play(Create(mg))
                    self.wait(0.5)

                # Display iteration and dynamic mid calculation
                iteration_text = Text(f"Iteration: {iteration}", font_size=32).to_edge(UP, buff=1.25)
                dynamic_mid_text = MathTex(
                    r"mid = \left( \frac{e + (s - e)}{2} \right) \rightarrow ",
                    fr"\left( \frac{{{s} + ({e} - {s})}}{{2}} \right) \rightarrow"
                    fr"\left( \frac{s + (e - s)}{{2}} \right) \rightarrow",
                    fr"\left( {s + (e-s) // 2} \right) ",
                    font_size=32
                ).to_edge(UP, buff=2)

                self.play(
                    Write(iteration_text),
                    Write(dynamic_mid_text),
                )
                self.wait(2)

                # Update mid value
                mid = s + (e - s) // 2

                # Update the positions for the arrows and labels
                sg_next = sg.animate.move_to(array_group[mid + 1].get_bottom() + DOWN + LEFT * 0.35)
                eg_next = eg.animate.move_to(array_group[mid - 1].get_bottom() + DOWN + RIGHT * 0.35)
                mg_next = mg.animate.move_to(array_group[mid].get_bottom() + DOWN)

                self.play(mg_next)
                self.wait(0.5)

                # Check if target is found
                if arr[mid] == target:
                    array_group[mid].set_fill(GREEN, opacity=0.5)
                    self.wait(1)
                    return mid

                # Adjust start and end arrows
                if arr[s] <= arr[mid]:
                    if arr[s] <= target <= arr[mid]:
                        self.play(eg_next)
                        e = mid - 1
                    else:
                        self.play(sg_next)
                        s = mid + 1
                else:
                    if arr[mid] <= target <= arr[e]:
                        self.play(sg_next)
                        s = mid + 1
                    else:
                        self.play(eg_next)
                        e = mid - 1

                # Update the visuals of the discarded elements
                if prev_s != s:
                    for i in range(prev_s, mid + 1):
                        array_group[i].set_fill(RED, opacity=0.5)
                else:
                    for i in range(mid, prev_e + 1):
                        array_group[i].set_fill(RED, opacity=0.5)

                iteration += 1
                self.wait(3)
                self.remove(iteration_text, dynamic_mid_text)

            return -1

        # Call the binary search function
        code(self.arr, self.target)

        self.wait(5)
