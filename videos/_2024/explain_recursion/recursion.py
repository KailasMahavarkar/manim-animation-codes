from exporter import *

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
CODE_PATH = os.path.join(ROOT_PATH, "codes")


def read_code(file_name):
    with open(os.path.join(CODE_PATH, file_name), "r") as file:
        return file.read()


class Video(Effects, Shuriken, MovingCameraScene):
    def construct(self):
        self.cam = self.camera.frame
        self.cam.scale(2)

        listing = Code(
            **base_code_config,
            code=read_code("direct_recursion.py"),
        )

        line_numbers = listing.line_numbers
        for line_number in line_numbers:
            line_number.set_color(WHITE)
            line_number.set_opacity(0.2)

        sr = SurroundingRectangle(
            listing.code[0:4],
            buff=0.3,
            color=GRAY_A,
            corner_radius=0.1,
        )

        listing.add(sr)
        self.add(listing)
