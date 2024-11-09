from exporter import *

class Sample(Scene):
    def construct(self):
        r = 10
        # Use the utility to create a 1D vector
        numbers = range(r)
        content = ["0" for _ in range(r)]

        p = ListUtility.create_1d_list(
            numbers,
            content,
            show_content=True,
            show_indexes=True,
            box_index_spacing=1,
        )

        self.add(*p)
        self.wait(10)
