from exporter import *

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
CODE_PATH = os.path.join(ROOT_PATH, "code.cpp")

font_index = 1
code_fonts = [
    "Consolas",
    "Fira Code",
    "Hack",
    "Inconsolata",
    "Monaco",
    "Source Code Pro",
    "Ubuntu Mono",
]


class Sample(Effects, Shuriken, MovingCameraScene):
    def construct(self):
        self.cam = self.camera.frame
        self.cam.scale(2)

        code = ""
        with open(CODE_PATH, "r") as file:
            code = file.read()

        listing = Code(
            **base_code_config,
            code=code,
        )

        line_numbers = listing.line_numbers
        for line_number in line_numbers:
            line_number.set_color(WHITE)
            line_number.set_opacity(0.2)

        # Modify the range to select different lines
        lines_to_surround = listing.code[10:12]

        # SurroundingRectangle for multiple lines
        # sr = SurroundingRectangle(
        #     lines_to_surround,
        #     buff=0.3,
        #     color=WHITE,
        #     corner_radius=0.1,
        # )

        # listing.add(sr)
        # self.add(listing)
