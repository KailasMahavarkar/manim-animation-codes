from types import SimpleNamespace
from manim import *
from exporter import *
from bloom import BloomFilter


CODE_PATH = os.path.abspath(os.path.dirname(__file__))
IMAGE_PATH = os.path.join(CODE_PATH, "images")


class ConfusionMatrix(Scene):
    def construct(self):
        # Title
        title = Text("Confusion Matrix", font_size=24)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Create the matrix
        matrix = MathTable(
            [["True-Positive", "False-Positive"],
             ["False-Negative", "True-Negative"]],
            row_labels=[Text("Positive"), Text("Negative")],
            col_labels=[Text("True"), Text("False")],
            include_outer_lines=True
        )

        # Add descriptions
        descriptions = [
            Text("A username is in bloom filter data structure.\nSearch confirms username existence.", font_size=18),
            Text("A username is Not in BF.\nSearch confirms username existence.", font_size=18),
            Text("A username is Not in BF.\nSearch confirms the nonexistence of a username.", font_size=18),
            Text("A username is in BF.\nSearch confirms the nonexistence of a username.", font_size=18)
        ]

        # Position descriptions
        for i, description in enumerate(descriptions):
            if i < 2:
                description.next_to(matrix, DOWN, buff=0.5).shift(2.5 * LEFT if i % 2 == 0 else 2.5 * RIGHT)
            else:
                description.next_to(matrix, DOWN, buff=0.5).shift(2.5 * LEFT if i % 2 == 0 else 2.5 * RIGHT).shift(1.5 * DOWN)

        # Add to scene
        self.play(Create(matrix))
        self.wait(1)

        for description in descriptions:
            self.play(Write(description))
            self.wait(2)

        self.wait(1)


class BloomBase():
    _has_instance = False

    def __init__(self) -> None:
        self.bloom_size = 32
        self.bloom_hash_count = 4
        self.bloom_filter = BloomFilter(
            size=self.bloom_size,
            hash_count=self.bloom_hash_count
        )
        self.bloom_group = VGroup()
        self.text_bloom_filter = Text("Hash Space", font_size=32, color=WHITE)
        self._has_instance = True


class Video(MovingCameraScene, BloomBase, Effects):
    def __init__(self, *args, **kwargs):
        MovingCameraScene.__init__(self, *args, **kwargs)
        BloomBase.__init__(self)
        Effects.__init__(self)

    def construct(self):
        self.next_section(skip_animations=True)
        # add border overlay
        self.add(FullScreenRectangle(
            stroke_width=1, fill_color=RED, fill_opacity=0))

        self.cam = self.camera.frame.animate

        shuriken = Shuriken.create_shuriken(self)
        shuriken.scale(0.35)
        shuriken.to_corner(UR, buff=0.25)
        shuriken.add_updater(lambda m, dt: m.rotate(-PI * dt * 1 / 2))

        # TITLE BLOOM FILTER
        bloom_title = VGroup(
            Text("Bloom Filter", font_size=48, color=WHITE).scale(1.75),
            VGroup(
                Tex(
                    "A Bloom Filter is a ", "probabilistic" ", space-efficient data structure.",
                    tex_to_color_map={"probabilistic": RED}
                ),
                Text("used to determine whether an element is part of a set.").set_color(
                    WHITE)
            ).arrange(DOWN, buff=0.25)
        ).arrange(DOWN, buff=0.5)

        bloom_title.scale(0.7)

        probability_rect = SurroundingRectangle(
            bloom_title[1][0][1], color=BLUE, fill_opacity=0.5
        )

        # Shuriken and Bloom Filter
        shuriken, bloom_title = self.shadow_clone_transform(
            shuriken,
            bloom_title,
            call=lambda: [
                self.play(Write(probability_rect)),
                bloom_title.add(probability_rect)
            ],
            post_call=lambda: []
        )

        for idx in range(self.bloom_size):
            rect = Rectangle(
                width=1, height=1, fill_opacity=0.5, color=BLUE
            )

            rect.add(
                Text("0", font_size=32, color=WHITE)
            )

            # index rect
            index_rect = Rectangle(
                width=1 / 3.5, height=1 / 3.5,
                fill_color=BLUE_D,
                fill_opacity=0.2,
                stroke_width=0.5
            )

            index_rect.add(
                Text(str(idx), font_size=14, color=WHITE)
            )

            index_rect.move_to(rect, [1, -1, 0])
            rect.add(index_rect)
            self.bloom_group.add(rect)

        self.bloom_group.arrange_in_grid(4, 8, buff=0)
        self.text_bloom_filter.next_to(self.bloom_group, UP, buff=0.5)

        self.play(
            Write(self.text_bloom_filter, run_time=1.5)
        )

        self.play(
            FadeIn(self.bloom_group)
        )

        self.wait(1)

        bucket = VGroup()
        bucket.add(
            self.bloom_group,
            self.text_bloom_filter
        )

        self.wait(1)
        self.play(
            FadeOut(self.bloom_group),
            FadeOut(self.text_bloom_filter)
        )
        self.wait(1)

        for word in ['ios']:
            hash_text_group = VGroup()
            hash_value_group = VGroup()
            word_to_hash_text_arrow_group = VGroup()
            hash_text_to_hash_value_arrow_group = VGroup()
            animation_stack = []
            animation_group = VGroup()

            self.bloom_filter.add(word)
            hash_list = self.bloom_filter._hashes(word)
            word_text = Text(word, font_size=48, color=WHITE)
            word_text.to_edge(UP, buff=0.5)

            animation_stack.append(Create(word_text))
            animation_group.add(word_text)

            for idx in range(self.bloom_hash_count):
                rect = Rectangle(
                    width=2,
                    height=0.9,
                    fill_color=RED,
                    fill_opacity=0.5
                )
                rect.add(
                    Tex(rf"H({word.lower()}) \% {idx}", font_size=32, color=WHITE)
                )
                hash_text_group.add(rect)

            hash_text_group.arrange(RIGHT, buff=0.75, center=True)
            hash_text_group.next_to(word_text, DOWN * 3, buff=0.5)
            animation_group.add(hash_text_group)

            for x in hash_list:
                rect = Rectangle(
                    width=2,
                    height=0.9,
                    fill_color=BLUE,
                    fill_opacity=0.5
                )
                rect.add(
                    Text(str(x), font_size=32, color=WHITE)
                )
                hash_value_group.add(rect)

            hash_value_group.arrange(RIGHT, buff=0.75)
            hash_value_group.next_to(hash_text_group, DOWN * 3, buff=0.5)
            animation_group.add(hash_value_group)

            for i in range(self.bloom_hash_count):
                arrow1 = Arrow(
                    word_text.get_bottom(),
                    hash_text_group[i].get_top(),
                    stroke_width=1
                )
                arrow2 = Arrow(
                    hash_text_group[i].get_bottom(),
                    hash_value_group[i].get_top(),
                    stroke_width=1
                )
                word_to_hash_text_arrow_group.add(arrow1)
                hash_text_to_hash_value_arrow_group.add(arrow2)

            animation_group.add(word_to_hash_text_arrow_group)
            animation_group.add(hash_text_to_hash_value_arrow_group)

            for i in range(self.bloom_hash_count):
                animation_stack.append(
                    Succession(
                        Create(
                            word_to_hash_text_arrow_group[i], run_time=0.5),
                        Create(hash_text_group[i], run_time=0.5),
                        Create(
                            hash_text_to_hash_value_arrow_group[i], run_time=0.5),
                        Create(hash_value_group[i], run_time=0.5)
                    )
                )

            self.play(
                Succession(
                    *animation_stack
                ),
            )

            self.wait(2)

            self.play(
                FadeOut(
                    animation_group
                )
            )

            self.wait(1)

            self.play(
                FadeIn(self.bloom_group)
            )

            self.wait(2)

            hash_list = self.bloom_filter._hashes(word)

            # updated text
            t = Text(
                "Words: [" +
                ",".join([word for word in self.bloom_filter.word_list]) + "]",
                font_size=32,
                color=WHITE
            )

            t.move_to(self.text_bloom_filter.get_center())

            self.play(
                ReplacementTransform(
                    self.text_bloom_filter,
                    t,
                )
            )

            for i in range(len(hash_list)):
                old_text = self.bloom_group[hash_list[i]][1]
                new_text = Text("1", font_size=32, color=RED).move_to(
                    old_text.get_center())

                self.wait(0.25)

                if (old_text.get_text() == "0"):
                    self.play(ReplacementTransform(
                        old_text, new_text), run_time=0.2)

            # fade out
            self.wait(1)
            self.play(
                FadeOut(self.bloom_group),
                FadeOut(t)
            )

            self.wait(5)

        self.next_section(skip_animations=False)

        # lets get back to the hash space again
        self.play(
            FadeIn(self.bloom_group)
        )

        self.wait(2)

        # scale down and move the bloom group to up
        self.play(
            self.bloom_group.animate.scale(0.75).to_edge(UP, buff=0.5)
        )

        t = Text(
            "check if a word 'cat' is in the bloom filter",
            font_size=32,
            color=WHITE
        ).move_to(
            self.bloom_group.get_bottom() + DOWN
        )

        self.play(
            Create(t)
        )

        # hide t
        self.wait(2)

        self.play(
            FadeOut(t)
        )

        # ----------------------------------------------------------------------------------
        # ---------------------------------------CAT ---------------------------------------
        # ----------------------------------------------------------------------------------

        # lets first get the hash values
        single_word_text = Text('cat', font_size=48, color=WHITE)
        single_word_text.to_edge(UP, buff=0.5)

        hash_text_group = VGroup()
        hash_value_group = VGroup()
        hash_list = self.bloom_filter._hashes(word)

        single_word_text.move_to(self.bloom_group.get_bottom() + DOWN)

        self.play(
            Create(single_word_text)
        )

        # lets get the hash values
        for idx in range(self.bloom_hash_count):
            rect = Rectangle(
                width=2,
                height=0.9,
                fill_color=RED,
                fill_opacity=0.5
            )
            rect.add(
                Tex(rf"H({word.lower()}) \% {idx}", font_size=32, color=WHITE)
            )
            hash_text_group.add(rect)

            # lets get the hash values
            rect = Rectangle(
                width=2,
                height=0.9,
                fill_color=BLUE,
                fill_opacity=0.5
            )

            rect.add(
                Text(str(hash_list[idx]), font_size=32, color=WHITE)
            )

            hash_value_group.add(rect)

        hash_text_group.arrange(RIGHT, buff=0.75, center=True)
        hash_text_group.next_to(single_word_text, DOWN, buff=0.5)

        self.wait(2)

        hash_value_group.arrange(RIGHT, buff=0.75)
        hash_value_group.next_to(hash_text_group, DOWN, buff=0.5)

        self.play(
            Create(hash_text_group)
        )

        self.play(
            Create(hash_value_group)
        )

        common = VGroup()
        common.add(single_word_text, hash_text_group, hash_value_group)

        # scale down and move the bloom group to up
        self.play(
            common.animate.scale(0.75).to_edge(DOWN, buff=0.5)
        )

        self.wait(1)

        # scale up the bloom group
        self.play(
            self.bloom_group.animate.scale(1.25).to_edge(UP, buff=0.5)
        )

        # highlight the hash values
        for i in range(self.bloom_hash_count):
            self.play(
                self.bloom_group[hash_list[i]].animate.set_fill(color=G_GREEN)
            )
        self.wait(2)

        # run cleaup
        self.play(
            FadeOut(common)
        )

        # lets get back to the hash space again
        self.play(
            FadeOut(self.bloom_group)
        )

        self.wait(2)

        # scale down and move the bloom group to up
        self.play(
            self.bloom_group.animate.scale(0.75).to_edge(UP, buff=0.5)
        )

        t = Text(
            "check if a word 'dog' is in the bloom filter",
            font_size=32,
            color=WHITE
        ).move_to(
            self.bloom_group.get_bottom() + DOWN
        )

        self.play(
            Create(t)
        )

        # hide t
        self.wait(2)

        self.play(
            FadeOut(t)
        )

        # ----------------------------------------------------------------------------------
        # ---------------------------------------DOG ---------------------------------------
        # ----------------------------------------------------------------------------------

        # lets first get the hash values
        single_word_text = Text('dog', font_size=48, color=WHITE)
        single_word_text.to_edge(UP, buff=0.5)
        hash_text_group = VGroup()
        hash_value_group = VGroup()

        hash_list = self.bloom_filter._hashes(word)

        single_word_text.move_to(self.bloom_group.get_bottom() + DOWN)

        self.play(
            Create(single_word_text)
        )

        # lets get the hash values
        for idx in range(self.bloom_hash_count):
            rect = Rectangle(
                width=2,
                height=0.9,
                fill_color=RED,
                fill_opacity=0.5
            )
            rect.add(
                Tex(rf"H({word.lower()}) \% {idx}", font_size=32, color=WHITE)
            )
            hash_text_group.add(rect)

            # lets get the hash values
            rect = Rectangle(
                width=2,
                height=0.9,
                fill_color=BLUE,
                fill_opacity=0.5
            )

            rect.add(
                Text(str(hash_list[idx]), font_size=32, color=WHITE)
            )

            hash_value_group.add(rect)

        hash_text_group.arrange(RIGHT, buff=0.75, center=True)
        hash_text_group.next_to(single_word_text, DOWN, buff=0.5)

        self.wait(2)

        hash_value_group.arrange(RIGHT, buff=0.75)
        hash_value_group.next_to(hash_text_group, DOWN, buff=0.5)

        self.play(
            Create(hash_text_group)
        )

        self.play(
            Create(hash_value_group)
        )

        common = VGroup()

        common.add(single_word_text, hash_text_group, hash_value_group)

        # scale down and move the bloom group to up
        self.play(
            common.animate.scale(0.75).to_edge(DOWN, buff=0.5)
        )

        self.wait(1)

        # scale up the bloom group
        self.play(
            self.bloom_group.animate.scale(1.25).to_edge(UP, buff=0.5)
        )

        # highlight the hash values
        for i in range(self.bloom_hash_count):
            self.play(
                self.bloom_group[hash_list[i]].animate.set_fill(color=G_GREEN)
            )

        self.wait(2)

        # run cleaup
        self.play(
            FadeOut(common)
        )

        self.wait(1)
