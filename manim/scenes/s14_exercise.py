import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *


def staircase(n=3, w=0.62, h=0.5, color=BORDER):
    blocks = VGroup()
    for k in range(1, n + 1):
        col = Rectangle(width=w, height=k * h, fill_color=PANEL_2, fill_opacity=1, stroke_color=color, stroke_width=2)
        col.move_to([k * w, k * h / 2, 0])
        blocks.add(col)
    ground = Line([-0.1, 0, 0], [(n + 0.6) * w, 0, 0], color=MUTED, stroke_width=2)
    pts = [np.array([0, 0.02, 0])] + [np.array([k * w, k * h + 0.02, 0]) for k in range(1, n + 1)]
    labels = VGroup(*[T(str(k), 16, MUTED).next_to(blocks[k - 1], DOWN, buff=0.08) for k in range(1, n + 1)])
    g = VGroup(ground, blocks, labels)
    g.pts = pts
    return g


def hop(st, a, b, color):
    p, q = st.pts[a], st.pts[b]
    arc = ArcBetweenPoints(p + UP * 0.05, q + UP * 0.05, angle=-PI * 0.75, color=color, stroke_width=4)
    arc.add_tip(tip_length=0.12, tip_width=0.12)
    lab = T(f"+{b - a}", 16, color, BOLD).next_to(arc, UP, buff=0.02)
    return VGroup(arc, lab)


class S14Exercise(LectureScene):
    def construct(self):
        bar = title_bar("Exercise", "The Climbing Stairs Problem")
        stmt = M("You are climbing a staircase that has exactly <b><i>n</i></b> steps to reach the top.\n"
                 "Each move, you can climb either <b>1 step</b> or <b>2 steps</b>.\n"
                 "How many <b>distinct ways</b> exist to reach the very top?", 25)
        stmt.move_to([0, 1.75, 0])
        io = M(c("Input:", BLUE) + " a single positive integer <i>n</i>     " + c("Output:", BLUE)
               + " number of distinct ways", 22, MUTED).next_to(stmt, DOWN, buff=0.25)
        paths = [[0, 1, 2, 3], [0, 1, 3], [0, 2, 3]]
        names = ["1 + 1 + 1", "1 + 2", "2 + 1"]
        cols = [BLUE, ORANGE, GREEN]
        stairs = VGroup()
        for pth, nm, col in zip(paths, names, cols):
            st = staircase()
            hops = VGroup(*[hop(st, a, b, col) for a, b in zip(pth[:-1], pth[1:])])
            lab = T(nm, 24, col, BOLD).next_to(st, DOWN, buff=0.25)
            stairs.add(VGroup(st, hops, lab))
        stairs.arrange(RIGHT, buff=1.0).move_to([0, -1.5, 0])
        ex = M("Example:  <i>n</i> = 3  →  Output: " + c("<b>3</b>", YELLOW), 26).next_to(io, DOWN, buff=0.22)

        with self.say("s14_stairs") as seg:
            self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)
            seg.wait_sentence(2)
            self.play(FadeIn(stmt[: len("Youareclimbingastaircasethathasexactlynstepstoreachthetop.")]), run_time=0.8)
            for s_ in stairs:
                self.play(FadeIn(s_[0]), run_time=0.25)
            seg.wait_sentence(3)
            self.play(FadeIn(stmt), run_time=0.6)
            self.play(Create(stairs[0][1][0]), run_time=0.6)
            seg.wait_sentence(4)
            self.play(FadeIn(io), run_time=0.6)
            seg.wait_sentence(5)
            self.play(FadeIn(ex), run_time=0.5)
            for s_ in stairs:
                self.play(LaggedStart(*[Create(h) for h in s_[1]], lag_ratio=0.5), FadeIn(s_[2]), run_time=1.0)

        with self.say("s14_stairs_task") as seg:
            task = M("➤  Give the <b>pseudocode</b> using the <b>Dynamic Programming</b> approach with the <b>4 steps</b>.", 24, YELLOW)
            tb = panel(task.width + 0.6, task.height + 0.4, color="#2A2410", stroke=YELLOW)
            tgrp = VGroup(tb, task.move_to(tb)).move_to([0, -0.15, 0])
            self.play(FadeOut(ex), FadeOut(io), FadeIn(tgrp, shift=UP * 0.1), run_time=0.7)
            seg.wait_sentence(1)
            big = staircase(4, w=0.7, h=0.42)
            big.move_to([0, -1.6, 0])
            self.play(*self.fade_out_anims(stairs), FadeIn(big), run_time=0.7)
            n_lab = T("n", 20, YELLOW, BOLD).move_to(big[2][3])
            self.play(Transform(big[2][3], n_lab), big[1][3].animate.set_stroke(YELLOW, 3), run_time=0.4)
            a1 = hop(big, 3, 4, BLUE)
            a2 = hop(big, 2, 4, PURPLE)
            a1[1].become(T("from n−1 ?", 18, BLUE, BOLD).next_to(a1[0], UP, buff=0.05))
            a2[1].become(T("from n−2 ?", 18, PURPLE, BOLD).next_to(a2[0], LEFT, buff=0.1))
            self.play(Create(a1), run_time=0.6)
            self.play(Create(a2), run_time=0.6)
            seg.wait_sentence(2)
            fam = T("a familiar pattern?", 22, MUTED).next_to(big, RIGHT, buff=0.6)
            self.play(FadeIn(fam), run_time=0.5)
        self.clear_scene()

        # ------------------------------------------------ max product subarray
        bar2 = title_bar("Exercise", "Maximum Product Subarray")
        self.play(FadeIn(bar2, shift=RIGHT * 0.3), run_time=0.5)
        stmt2 = M("Given an integer array " + c("A[1..n]", BLUE) + " (positive, negative or zero), find a <b>contiguous</b>\n"
                  "subarray (at least one number) which has the <b>largest product</b>.", 25).move_to([0, 1.85, 0])
        arr = ArrayRow([-1, 3, -4, -2], cell=1.05, size=36).move_to([0, 0.35, 0])
        with self.say("s14_product") as seg:
            seg.wait_sentence(1)
            self.play(FadeIn(stmt2), run_time=0.8)
            seg.wait_sentence(2)
            self.play(FadeIn(arr), run_time=0.6)
            win = arr.window(1, 3, GREEN, width=6)
            self.play(Create(win), arr.tint(1, 3, GREEN, 0.25), run_time=0.8)
            prod = M("3 × (−4) × (−2) = " + c("<b>24</b>", GREEN), 34).next_to(arr, DOWN, buff=0.45)
            self.play(Write(prod), run_time=1.0)

        with self.say("s14_product_task") as seg:
            qs = M("➤  Why doesn't the standard Kadane algorithm work here?\n"
                   "     How to make it work, and why?", 25, YELLOW)
            qb = panel(qs.width + 0.6, qs.height + 0.4, color="#2A2410", stroke=YELLOW)
            qgrp = VGroup(qb, qs.move_to(qb)).next_to(prod, DOWN, buff=0.3)
            self.play(FadeIn(qgrp, shift=UP * 0.1), run_time=0.7)
            seg.wait_sentence(2)
            hint = M("hint:  " + c("(−)", RED) + " × " + c("(−)", RED) + " = " + c("(+)", GREEN)
                     + "     the <b>smallest</b> product can suddenly become the <b>largest</b>", 22, FG)
            hint.next_to(qgrp, DOWN, buff=0.2)
            sign = VGroup(T("3 × (−4) = −12", 24, RED), T("↓", 24, MUTED), T("−12 × (−2) = +24", 24, GREEN))
            sign.arrange(DOWN, buff=0.1).next_to(arr, RIGHT, buff=0.5)
            self.play(FadeIn(hint), FadeIn(sign, shift=LEFT * 0.1), run_time=0.8)
        self.clear_scene()

        # ------------------------------------------------ references & closing
        bar3 = title_bar("Session 15", "References")
        refs = VGroup(
            M("Cormen, T.H., Leiserson, C.E., Rivest, R.L., &amp; Stein, C. (2022).\n<i>Introduction to Algorithms, 4th Edition.</i>"
              " MIT Press. Chapter 14.3.", 24),
            M("Skiena, S.S. (2020). <i>The Algorithm Design Manual, 3rd Edition.</i>\nSpringer. Chapter 10.1.", 24),
        )
        rows = VGroup()
        for r in refs:
            d = Dot(radius=0.06, color=BLUE).next_to(r, LEFT, buff=0.25).align_to(r, UP).shift(DOWN * 0.13)
            rows.add(VGroup(d, r))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, 1.0, 0])
        thanks = T("Terima kasih!", 56, ORANGE, BOLD).move_to([0, -1.4, 0])
        sub = T("Sampai jumpa di sesi berikutnya", 26, MUTED).next_to(thanks, DOWN, buff=0.2)
        with self.say("s14_refs") as seg:
            self.play(FadeIn(bar3, shift=RIGHT * 0.3), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.5), run_time=1.4)
            seg.wait_sentence(1)
            self.play(Write(thanks), FadeIn(sub, shift=UP * 0.1), run_time=1.2)
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.3)
