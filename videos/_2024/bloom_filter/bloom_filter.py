from manim.camera.moving_camera import MovingCamera
from exporter import *
from bloom import BloomFilter


class Anima:
    def shadow_clone_transform(self, func):
        def wrapper(self, old_object, new_object, *args, **kwargs):
            shadow_clone = old_object.copy()
            self.play(ReplacementTransform(old_object, new_object), run_time=2)
            func(self, old_object, new_object, *args, **kwargs)
            self.play(ReplacementTransform(
                new_object, shadow_clone), run_time=2)
            return shadow_clone
        return wrapper

    # Static method for transformation
    @staticmethod
    def transform_logic(self, old_obj, new_obj):
        self.play(ReplacementTransform(old_obj, new_obj), run_time=2)


class Video(MovingCameraScene, Anima):
    def shadow_clone_transform(self, old, new, delay=3):
        old_shadow_clone = old.copy()
        new_shadow_clone = new.copy()
        self.play(ReplacementTransform(old, new), run_time=2)
        self.wait(delay)
        self.play(ReplacementTransform(new, old_shadow_clone), run_time=2)
        return old_shadow_clone, new_shadow_clone

    def construct(self):
        self.next_section("Make Bloom Filter", skip_animations=False)
        # add border overlay
        self.add(FullScreenRectangle(
            stroke_width=1, fill_color=RED, fill_opacity=0))

        self.bloom_size = 32
        self.bloom_hash_count = 4
        self.bloom_filter = BloomFilter(
            size=self.bloom_size, hash_count=self.bloom_hash_count)
        self.bloom = VGroup()
        self.cam = self.camera.frame.animate

        shuriken = Shuriken.create_shuriken(self)
        shuriken.scale(0.35)
        shuriken.to_corner(UR, buff=0.25)
        shuriken.add_updater(lambda m, dt: m.rotate(-PI * dt * 1/2))

        temp = VGroup(
            Text("Bloom Filter", font_size=48, color=WHITE).scale(1.75),
            VGroup(
                Text(
                    "A Bloom Filter is a", "probabilistic" ", space-efficient data structure.",
                    tex_to_color_map={"Bloom Filter": BLUE}
                ),
                Text("used to determine whether an element is part of a set.").set_color(
                    WHITE)
            ).arrange(DOWN, buff=0.25)
        ).arrange(DOWN, buff=0.5)

        temp.scale(0.7)

        shuriken, temp = self.shadow_clone_transform(shuriken, temp, 5)



        shuriken, temp = self.shadow_clone_transform(shuriken, temp, 3)

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
            Write(text_bloom_filter, run_time=1.5)
        )

        self.play(
            FadeIn(self.bloom)
        )

        self.wait(1)
        self.play(
            FadeOut(self.bloom),
            FadeOut(text_bloom_filter)
        )
        self.wait(1)

        for idx, word in enumerate(["Cat", "Dog", "Python"]):
            self.bloom_filter.add(word)
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

            # updated text
            t = Text(
                "Words: [" +
                ",".join([word for word in self.bloom_filter.word_list]) + "]",
                font_size=32,
                color=WHITE
            )

            t.move_to(text_bloom_filter.get_center())

            self.play(
                ReplacementTransform(
                    text_bloom_filter,
                    t,
                )
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

                self.wait(0.25)

                if (old_text.get_text() == "0"):
                    self.play(ReplacementTransform(
                        old_text, new_text), run_time=0.2)

            # dade out the arrow
            self.play(
                FadeOut(arrow_group),
                FadeOut(hash_value_group),
                run_time=1
            )

            self.wait(2)

            self.play(
                FadeOut(self.bloom),
                FadeOut(text_bloom_filter),
                FadeOut(t)
            )

            break

        self.wait(1)

        self.next_section("Check Bloom Filter", skip_animations=True)

        self.play(
            FadeIn(self.bloom),
            FadeIn(text_bloom_filter)
        )

        self.wait(3)
