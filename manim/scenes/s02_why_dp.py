import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *
from fibtree import FibTree


def fib_calls(n):
    a, b = 1, 1  # fib(1), fib(2)
    for _ in range(n):
        a, b = b, a + b
    return 2 * a - 1  # jumlah pemanggilan FIB(n) naif = 2*fib(n+1) - 1


class S02WhyDP(LectureScene):
    def construct(self):
        bar = title_bar("Dynamic Programming Paradigm", "Why DP?")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        code = CodePanel(["FIB(n)", "if n <= 1", "    return n", "return FIB(n - 1) + FIB(n - 2)"], size=22)
        code.move_to([0, 0.6, 0])
        task = M("Compute <b>fib(5)</b> by hand recursively. Draw the recursion tree.", 26, MUTED)
        task.next_to(code, UP, buff=0.4)

        with self.say("s02_code") as seg:
            self.play(FadeIn(task, shift=DOWN * 0.1), run_time=0.6)
            self.play(FadeIn(code, shift=UP * 0.2), run_time=0.8)
            seg.wait_sentence(3)
            hl = code.lines_box(1, 2, GREEN)
            self.play(FadeIn(hl), run_time=0.4)
            seg.wait_sentence(4)
            self.play(hl.animate.become(code.highlight_box(3, ORANGE)), run_time=0.4)

        # ---- pindahkan kode ke kiri, gambar tree di kanan
        tree = FibTree(5, leaf_dx=1.08, level_dy=1.0, size=20)
        tree.move_to([2.45, -0.2, 0])
        with self.say("s02_tree") as seg:
            self.play(FadeOut(task), FadeOut(hl), code.animate.scale(0.62).to_corner(UL).shift(DOWN * 1.35 + RIGHT * 0.05),
                      run_time=0.9)
            seg.wait_sentence(1)
            self.play(tree.level_anim(0), run_time=0.6)
            self.play(tree.level_anim(1), run_time=0.9)
            seg.wait_sentence(2)
            for d in range(2, 5):
                self.play(tree.level_anim(d), run_time=1.0)
            leaves = [nd["mob"] for nd in tree.nodes if nd["n"] <= 1]
            self.play(*[nd[0].animate.set_stroke(GREEN, 2.5) for nd in leaves], run_time=0.6)
            base = M(c("■", GREEN) + " base case", 20, MUTED).next_to(code, DOWN, aligned_edge=LEFT, buff=0.3)
            self.play(FadeIn(base), run_time=0.4)

        # ---- pertanyaan: berapa kali fib(2) & fib(3)?
        with self.say("s02_question") as seg:
            q = M("<i>Question: how many times do we\ncompute fib(2)? How about fib(3)?</i>", 22, FG)
            q.scale_to_fit_width(min(q.width, 4.1))
            q.next_to(base, DOWN, aligned_edge=LEFT, buff=0.35)
            self.play(FadeIn(q, shift=RIGHT * 0.2), run_time=0.6)
            seg.wait_sentence(1)
            reds = VGroup(*[Ellipse(width=1.3, height=0.72, color=RED, stroke_width=4).move_to(nd["mob"])
                            for nd in tree.with_n(2)])
            self.play(LaggedStart(*[Create(e) for e in reds], lag_ratio=0.35), run_time=1.5)
            c2 = M(c("fib(2)", RED) + "  dihitung  " + c("3×", RED), 26).next_to(q, DOWN, aligned_edge=LEFT, buff=0.4)
            self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
            seg.wait_sentence(3)
            blues = VGroup(*[Ellipse(width=1.3, height=0.72, color=BLUE, stroke_width=4).move_to(nd["mob"])
                             for nd in tree.with_n(3)])
            self.play(LaggedStart(*[Create(e) for e in blues], lag_ratio=0.35), run_time=1.2)
            c3 = M(c("fib(3)", BLUE) + "  dihitung  " + c("2×", BLUE), 26).next_to(c2, DOWN, aligned_edge=LEFT, buff=0.25)
            self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.5)

        # ---- eksponensial
        with self.say("s02_problem") as seg:
            # subtree duplikat berdenyut
            dup = VGroup(*[tree.with_n(3)[1]["mob"]], *[nd["mob"] for nd in tree.subtree(tree.with_n(3)[1])])
            self.play(Indicate(dup, color=RED, scale_factor=1.08), run_time=1.2)
            seg.wait_sentence(2)
            left = VGroup(q, c2, c3)
            stats = VGroup(
                M(f"n = 5   →  {fib_calls(5)} calls", 24, FG),
                M(f"n = 10  →  {fib_calls(10)} calls", 24, FG),
                M(f"n = 30  →  {fib_calls(30):,} calls".replace(",", "."), 24, RED),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            stats.next_to(base, DOWN, aligned_edge=LEFT, buff=0.35)
            self.play(*self.fade_out_anims(left), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in stats], lag_ratio=0.5), run_time=1.6)
            big = M(c("O(2ⁿ)", RED), 48).next_to(stats, DOWN, aligned_edge=LEFT, buff=0.25)
            self.play(Write(big), run_time=0.8)
            seg.wait_sentence(3)
            idea_t = M("<b>What if we wrote the result\nthe first time it is calculated?</b>", 22, YELLOW)
            idea = VGroup(panel(idea_t.width + 0.5, idea_t.height + 0.4, color="#10263A", stroke=YELLOW))
            idea.add(idea_t.move_to(idea[0]))
            idea.next_to(big, DOWN, aligned_edge=LEFT, buff=0.25)
            self.play(FadeIn(idea, shift=UP * 0.2), run_time=0.7)
        self.clear_scene()
