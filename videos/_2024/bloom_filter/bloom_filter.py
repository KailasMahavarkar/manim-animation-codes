from manim.camera.moving_camera import MovingCamera
from exporter import *
from bloom import BloomFilter


class Video(MovingCameraScene):
    def construct(self):
        self.bloom_size = 32
        self.bloom_hash_count = 4
        self.bloom_filter = BloomFilter(
            size=self.bloom_size, hash_count=self.bloom_hash_count)
        self.bloom = VGroup()
        self.cam = self.camera.frame.animate

        self.next_section("Make Bloom Filter", skip_animations=True)
        for idx in range(self.bloom_size):
            rect = Rectangle(
                width=1, height=1, fill_opacity=0.5, color=BLUE
            )

            rect.add(
                Text("0", font_size=32, color=WHITE)
            )

            # index rect
            index_rect = Rectangle(
                width=1/3.5, height=1/3.5,
                fill_color=BLUE_D,
                fill_opacity=0.2,
                stroke_width=0.5
            )

            index_rect.add(
                Text(str(idx), font_size=14, color=WHITE)
            )

            index_rect.move_to(rect, [1, -1, 0])
            rect.add(index_rect)
            self.bloom.add(rect)

        self.bloom.arrange_in_grid(4, 8, buff=0)
        text_bloom_filter = Text("Hash Space", font_size=32, color=WHITE)
        text_bloom_filter.next_to(self.bloom, UP, buff=0.5)

        self.play(
            Create(self.bloom, run_time=1.5)
        )

        self.play(
            Write(text_bloom_filter, run_time=1.5)
        )

        self.play(
            FadeOut(self.bloom),
            FadeOut(text_bloom_filter)
        )
        self.wait(2)

        for idx, word in enumerate(["Cat", "Dog", "Python"]):
            self.next_section(f"Word {word}", skip_animations=False)

            hash_list = self.bloom_filter._hashes(word)
            hash_text_group = VGroup()
            hash_value_group = VGroup()
            word_to_hash_text_arrow_group = VGroup()
            hash_text_to_hash_value_arrow_group = VGroup()

            word_text = Text(word, font_size=48, color=WHITE)
            word_text.to_edge(UP, buff=0.5)

            self.play(
                Write(word_text)
            )

            # Create hash function text
            for idx in range(self.bloom_hash_count):
                rect = Rectangle(
                    width=2,
                    height=0.9,
                    fill_color=RED,
                    fill_opacity=0.5
                )

                rect.add(
                    Tex(rf"H({word.lower()}) \% {idx}",
                        font_size=32, color=WHITE)
                )
                hash_text_group.add(rect)

            # Create hash value text
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

            hash_text_group.arrange(RIGHT, buff=0.75, center=True)
            hash_text_group.next_to(word_text, DOWN * 3, buff=0.5)

            hash_value_group.arrange(RIGHT, buff=0.75)
            hash_value_group.next_to(hash_text_group, DOWN * 3, buff=0.5)

            # Create arrow from word to hash function
            for i in range(self.bloom_hash_count):
                arrow = Arrow(
                    word_text.get_bottom(),
                    hash_text_group[i].get_top(),
                    stroke_width=1
                )
                word_to_hash_text_arrow_group.add(arrow)

            # Create arrow from hash function to hash value
            for i in range(self.bloom_hash_count):
                arrow = Arrow(
                    hash_text_group[i].get_bottom(),
                    hash_value_group[i].get_top(),
                    stroke_width=1
                )
                hash_text_to_hash_value_arrow_group.add(arrow)

            for i in range(self.bloom_hash_count):
                self.play(
                    Create(word_to_hash_text_arrow_group[i], run_time=0.5)
                )

                self.play(
                    Create(hash_text_group[i], run_time=0.5)
                )

                self.play(
                    Create(
                        hash_text_to_hash_value_arrow_group[i], run_time=0.5)
                )

                self.play(
                    Create(hash_value_group[i], run_time=0.5)
                )

                self.wait(0.2)

            self.wait(3)

            self.play(
                FadeOut(word_text),
                FadeOut(hash_text_group),
                # FadeOut(hash_value_group),
                FadeOut(word_to_hash_text_arrow_group),
                FadeOut(hash_text_to_hash_value_arrow_group)
            )

            self.remove(
                word_text,
                hash_text_group,
                # hash_value_group,
                word_to_hash_text_arrow_group,
                hash_text_to_hash_value_arrow_group
            )

            self.play(
                hash_value_group.animate.to_edge(DOWN, buff=0.5).scale(0.75),
            )

            self.wait(0.5)
            
            self.play(
                FadeIn(self.bloom),
                FadeIn(text_bloom_filter)
            )


            # create arrow from hash_value_group to bloom filter index
            arrow_group = VGroup()
            for i in range(len(hash_list)):
                arrow = Arrow(
                    hash_value_group[i].get_top(),
                    self.bloom[hash_list[i]][0].get_center(),
                    stroke_width=1
                )

                arrow_group.add(arrow)

                old_text = self.bloom[hash_list[i]][1]
                new_text = Text("1", font_size=32, color=RED).move_to(
                old_text.get_center())
                self.play(
                    Create(arrow)
                )
                self.play(ReplacementTransform(old_text, new_text))


            self.bloom_filter.add(word)

            # dade out the arrow
            self.play(
                FadeOut(arrow_group),
                FadeOut(hash_value_group)
            )

            self.wait(1)

            # self.play(
            #     FadeOut(self.bloom),
            #     FadeOut(text_bloom_filter)
            # )

            break

        self.wait(3)
