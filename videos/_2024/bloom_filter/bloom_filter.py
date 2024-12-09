from manim import *
from exporter import *
from bloom import BloomFilter


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


class AnimateWord(MovingCameraScene, BloomBase):
    def __init__(self) -> None:
        MovingCameraScene.__init__(self)
        BloomBase.__init__(self)

        self.hash_text_group = VGroup()
        self.hash_value_group = VGroup()
        self.word_to_hash_text_arrow_group = VGroup()
        self.hash_text_to_hash_value_arrow_group = VGroup()
        self.animation_stack = []
        self.animation_group = VGroup()
        self.word = ""

    def construct(self, word=""):
        self.word = word
        self.bloom_filter.add(word)
        hash_list = self.bloom_filter._hashes(word)
        word_text = Text(word, font_size=48, color=WHITE)
        word_text.to_edge(UP, buff=0.5)

        # self.play(Write(word_text))
        self.animation_stack.append(Create(word_text))
        self.animation_group.add(word_text)

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
            self.hash_text_group.add(rect)

        self.hash_text_group.arrange(RIGHT, buff=0.75, center=True)
        self.hash_text_group.next_to(word_text, DOWN * 3, buff=0.5)
        self.animation_group.add(self.hash_text_group)

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
            self.hash_value_group.add(rect)

        self.hash_value_group.arrange(RIGHT, buff=0.75)
        self.hash_value_group.next_to(self.hash_text_group, DOWN * 3, buff=0.5)
        self.animation_group.add(self.hash_value_group)

        for i in range(self.bloom_hash_count):
            arrow1 = Arrow(
                word_text.get_bottom(),
                self.hash_text_group[i].get_top(),
                stroke_width=1
            )
            arrow2 = Arrow(
                self.hash_text_group[i].get_bottom(),
                self.hash_value_group[i].get_top(),
                stroke_width=1
            )
            self.word_to_hash_text_arrow_group.add(arrow1)
            self.hash_text_to_hash_value_arrow_group.add(arrow2)

        self.animation_group.add(self.word_to_hash_text_arrow_group)
        self.animation_group.add(self.hash_text_to_hash_value_arrow_group)

        for i in range(self.bloom_hash_count):
            self.animation_stack.append(
                Succession(
                    Create(
                        self.word_to_hash_text_arrow_group[i], run_time=0.5),
                    Create(self.hash_text_group[i], run_time=0.5),
                    Create(
                        self.hash_text_to_hash_value_arrow_group[i], run_time=0.5),
                    Create(self.hash_value_group[i], run_time=0.5)
                )
            )

    def map_to_hash_space(self):
        hash_list = self.bloom_filter._hashes(self.word)

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

        arrow_group = VGroup()
        for i in range(len(hash_list)):
            print(hash_list[i], len(self.bloom_group))
            # print(self.bloom_group[hash_list[i]])
            # print(hash_list[i])
            pass
            # arrow = Arrow(
            #     self.hash_value_group[i].get_top(),
            #     self.bloom_group[hash_list[i]][0].get_center(),
            #     stroke_width=1
            # )

            # arrow_group.add(arrow)

            # old_text = self.bloom_group[hash_list[i]][1]
            # new_text = Text("1", font_size=32, color=RED).move_to(
            #     old_text.get_center())
            # self.play(
            #     Create(arrow)
            # )

            # self.wait(0.25)

            # if (old_text.get_text() == "0"):
            #     self.play(ReplacementTransform(
            #         old_text, new_text), run_time=0.2)

    def get_animation(self):
        return self.animation_group

    def get_animation_stack(self):
        return self.animation_stack


class Video(AnimateWord, MovingCameraScene, BloomBase, Effects):
    def __init__(self, *args, **kwargs):
        MovingCameraScene.__init__(self, *args, **kwargs)
        BloomBase.__init__(self)
        Effects.__init__(self)
        AnimateWord.__init__(self)

    def construct(self):
        self.next_section("Make Bloom Filter", skip_animations=False)
        # add border overlay
        self.add(FullScreenRectangle(
            stroke_width=1, fill_color=RED, fill_opacity=0))

        self.cam = self.camera.frame.animate

        shuriken = Shuriken.create_shuriken(self)
        shuriken.scale(0.35)
        shuriken.to_corner(UR, buff=0.25)
        shuriken.add_updater(lambda m, dt: m.rotate(-PI * dt * 1/2))

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

        shuriken, bloom_title = self.shadow_clone_transform(
            shuriken,
            bloom_title,
            call=lambda: [
                self.play(Write(probability_rect)),
                bloom_title.add(probability_rect)
            ],
            post_call=lambda: []
        )

        self.wait(3)

        shuriken, bloom_title = self.shadow_clone_transform(
            shuriken,
            bloom_title
        )

        self.wait(2)

        # self.next_section("Make Bloom Filter", skip_animations=False)
        # for idx in range(self.bloom_size):
        #     rect = Rectangle(
        #         width=1, height=1, fill_opacity=0.5, color=BLUE
        #     )

        #     rect.add(
        #         Text("0", font_size=32, color=WHITE)
        #     )

        #     # index rect
        #     index_rect = Rectangle(
        #         width=1/3.5, height=1/3.5,
        #         fill_color=BLUE_D,
        #         fill_opacity=0.2,
        #         stroke_width=0.5
        #     )

        #     index_rect.add(
        #         Text(str(idx), font_size=14, color=WHITE)
        #     )

        #     index_rect.move_to(rect, [1, -1, 0])
        #     rect.add(index_rect)
        #     self.bloom_group.add(rect)

        # self.bloom_group.arrange_in_grid(4, 8, buff=0)
        # self.text_bloom_filter.next_to(self.bloom_group, UP, buff=0.5)

        # self.play(
        #     Write(self.text_bloom_filter, run_time=1.5)
        # )

        # self.play(
        #     FadeIn(self.bloom_group)
        # )

        # bucket = VGroup()
        # bucket.add(
        #     self.bloom_group,
        #     self.text_bloom_filter
        # )

        # self.wait(1)
        # self.play(
        #     FadeOut(self.bloom_group),
        #     FadeOut(self.text_bloom_filter)
        # )
        # self.wait(1)

        # for word in ['apple', 'cat', 'dog']:
        #     x = AnimateWord()
        #     x.construct(word=word)
        #     x.map_to_hash_space()

        #     self.play(
        #         Succession(
        #             *x.get_animation_stack()
        #         ),
        #     )

        #     self.wait(2)

        #     self.play(
        #         FadeOut(x.get_animation())
        #     )

        # self.next_section("Check Bloom Filter", skip_animations=False)
        # self.add(bucket)
        # self.play(
        #     bucket.animate.scale(0.75).to_edge(LEFT, buff=0.5)
        # )

        # self.wait(2)

        # temp = Text("check for word \"ice\"",
        #             font_size=28, color=WHITE)

        # temp.next_to(self.text_bloom_filter, 8*RIGHT, buff=0.5)

        # self.play(Write(temp))
        # self.wait(1)

        # # Check if word is in the bloom filter
        # self.wait(3)

    