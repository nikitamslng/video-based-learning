import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *

BRUTE = [
    "BRUTE-FORCE-SUM(A)",
    "n = A.length",
    "if n == 0",
    "    return 0",
    "global_max = -∞",
    "for end = 1 to n  //for every end index",
    "    for start = 1 to end  //search for every possible start index",
    "        current_subarray_sum = 0",
    "        for i = start to end  //calculate the sum of the subarray",
    "            current_subarray_sum = current_subarray_sum + A[i]",
    "        global_max = max(global_max, current_subarray_sum)",
    "return global_max",
]
LABELS = ["1", "2", "3", "…", "n"]


def mini_row(lo, hi, cell=0.5, size=20, hl=BLUE):
    """Array simbolik [1 2 3 … n] dengan sel lo..hi (posisi 0..4) di-highlight."""
    g = VGroup()
    x = 0
    for k, lab in enumerate(LABELS):
        if lab == "…":
            t = T("…", size, MUTED).move_to([x + cell * 0.55, 0, 0])
            g.add(t)
            x += cell * 1.1
            continue
        on = lo <= k <= hi
        sq = Square(cell, stroke_color=hl if on else BORDER, stroke_width=2.5 if on else 2,
                    fill_color="#0B5E86" if on else PANEL, fill_opacity=1)
        sq.move_to([x + cell / 2, 0, 0])
        t = T(lab, size, FG if on else MUTED, BOLD).move_to(sq)
        g.add(VGroup(sq, t))
        x += cell if k < 2 else cell + 0.0
    return g


class S08Naive(LectureScene):
    def construct(self):
        bar = title_bar("Maximum Subarray Sum: Kadane's Algorithm", "Naïve Approach")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        head = M("For every index <i>i</i>, there are <i>i</i> possible subarrays ending exactly at that index.", 26)
        head.move_to([0, 2.2, 0])
        specs = [
            ("i = 1", [(0, 0)]),
            ("i = 2", [(1, 1), (0, 1)]),
            ("i = 3", [(2, 2), (1, 2), (0, 2)]),
            ("i = n", [(4, 4), None, (0, 4)]),
        ]
        groups = VGroup()
        for lab, rows in specs:
            col = VGroup()
            for r in rows:
                if r is None:
                    col.add(T("⋮", 30, MUTED))
                else:
                    col.add(mini_row(*r))
            col.arrange(DOWN, buff=0.28)
            # pastikan semua kolom rata atas
            title = T(lab, 22, BLUE, BOLD, slant=ITALIC)
            grp = VGroup(title, col).arrange(DOWN, buff=0.22)
            groups.add(grp)
        groups.arrange(RIGHT, buff=0.55, aligned_edge=UP).next_to(head, DOWN, buff=0.4)
        with self.say("s08_enum") as seg:
            self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.8)
            seg.wait_sentence(2)
            span = seg.duration - seg.at(2) - 0.5
            for g in groups:
                self.play(FadeIn(g[0]), LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in g[1]], lag_ratio=0.3),
                          run_time=max(0.8, span / 4 - 0.1))

        count = M("1 + 2 + 3 + ⋯ + n  =  n(n+1)/2  =  " + c("<b>O(n²)</b>", ORANGE) + "  possible subarrays", 28)
        count.move_to([0, -1.55, 0])
        cost = M("each sum costs " + c("O(n)", ORANGE) + "   ⇒   total time  " + c("<b>O(n³)</b>", RED), 28)
        cost.next_to(count, DOWN, buff=0.3)
        with self.say("s08_count") as seg:
            self.play(Write(count), run_time=1.6)
            seg.wait_sentence(1)
            self.play(FadeIn(cost[:12], shift=UP * 0.1), run_time=0.7)
            seg.wait_sentence(2)
            self.play(FadeIn(cost[12:], shift=UP * 0.1), run_time=0.7)
            self.play(Indicate(cost[-6:], color=RED), run_time=0.8)
        self.fade_all_except(bar)

        # ------------------------------------------------ pseudocode
        code = CodePanel(BRUTE, size=19).move_to([0, -0.1, 0])
        with self.say("s08_code") as seg:
            self.play(FadeIn(code, shift=UP * 0.2), run_time=0.8)
            seg.wait_sentence(1)
            span = seg.at(2) - seg.at(1)
            hl = code.highlight_box(5, BLUE)
            self.play(FadeIn(hl), run_time=0.4)
            self.wait(max(0.1, span / 3 - 0.4))
            self.play(hl.animate.become(code.highlight_box(6, PURPLE)), run_time=0.4)
            self.wait(max(0.1, span / 3 - 0.4))
            self.play(hl.animate.become(code.lines_box(8, 9, ORANGE)), run_time=0.4)
            seg.wait_sentence(2)
            self.play(hl.animate.become(code.highlight_box(10, GREEN)), run_time=0.4)
            seg.wait_sentence(3)
            self.play(FadeOut(hl), run_time=0.3)
            # tiga kurung kurawal loop bersarang
            right = code.bg.get_right()[0]
            braces = VGroup()
            labels = VGroup()
            for (a, b), col, lab in [((5, 10), BLUE, "end: n"), ((6, 10), PURPLE, "start: ≤ n"), ((8, 9), ORANGE, "i: ≤ n")]:
                top = code.line(a)[0].get_top()[1]
                bot = code.line(b)[0].get_bottom()[1]
                br = Line([0, top, 0], [0, bot, 0], color=col, stroke_width=5)
                braces.add(br)
                labels.add(T(lab, 18, col, BOLD))
            for k, (br, lb) in enumerate(zip(braces, labels)):
                br.set_x(right - 0.25 - 0.22 * (2 - k))
            self.play(LaggedStart(*[Create(b) for b in braces], lag_ratio=0.3), run_time=0.9)
            total = pill("n × n × n  →  O(n³)", RED, 24).next_to(code, DOWN, buff=0.15)
            self.play(FadeIn(total, shift=UP * 0.1), run_time=0.6)
        self.fade_all_except(bar)

        # ------------------------------------------------ overlapping
        new_bar = title_bar("Maximum Subarray Sum: Kadane's Algorithm", "Naïve Approach: Overlapping Subproblems")
        self.play(Transform(bar, new_bar), run_time=0.5)
        r2 = mini_row(0, 1, cell=0.8, size=30)
        r3 = mini_row(0, 2, cell=0.8, size=30)
        l2 = T("i = 2", 28, BLUE, BOLD, slant=ITALIC)
        l3 = T("i = 3", 28, BLUE, BOLD, slant=ITALIC)
        row2 = VGroup(l2, r2).arrange(RIGHT, buff=0.5)
        row3 = VGroup(l3, r3).arrange(RIGHT, buff=0.5)
        rows = VGroup(row2, row3).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([-2.6, 0.75, 0])
        s2 = M("A[1] + A[2]", 28).next_to(r2, RIGHT, buff=0.7)
        s3 = M("A[1] + A[2] + A[3]", 28).next_to(r3, RIGHT, buff=0.7)
        with self.say("s08_overlap") as seg:
            self.play(FadeIn(rows), run_time=0.7)
            seg.wait_sentence(1)
            e2 = Ellipse(width=2.1, height=1.25, color=RED, stroke_width=5).move_to(VGroup(r2[0], r2[1]))
            self.play(Create(e2), FadeIn(s2, shift=LEFT * 0.2), run_time=0.9)
            seg.wait_sentence(2)
            e3 = Ellipse(width=2.1, height=1.25, color=RED, stroke_width=5).move_to(VGroup(r3[0], r3[1]))
            self.play(Create(e3), FadeIn(s3, shift=LEFT * 0.2), run_time=0.9)
            u = Underline(s3[:9], color=RED, stroke_width=5)
            u2 = Underline(s2, color=RED, stroke_width=5)
            seg.wait_sentence(3)
            self.play(Create(u), Create(u2), run_time=0.6)
            rep = T("computed again!", 24, RED, BOLD).next_to(u, DOWN, buff=0.15)
            self.play(FadeIn(rep), run_time=0.5)

        with self.say("s08_idea") as seg:
            look = M("On a closer look, we only care about the <b>previous maximum sum</b>\nfor the current ending index.", 25)
            look.move_to([0, -1.25, 0])
            self.play(FadeIn(look, shift=UP * 0.1), run_time=0.8)
            seg.wait_sentence(1)
            cells = VGroup(*[Square(0.6, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.12) for _ in range(6)])
            cells.arrange(RIGHT, buff=0)
            qs = VGroup(*[T("?", 24, GREEN, BOLD).move_to(cl) for cl in cells])
            lab = M(c("<b>So, what if we save the maximum sum for every ending index?</b>", YELLOW), 25)
            lab.scale_to_fit_width(min(lab.width, 9.0))
            grp = VGroup(lab, VGroup(cells, qs)).arrange(RIGHT, buff=0.4).move_to([0, -2.3, 0])
            self.play(FadeIn(lab, shift=UP * 0.1), LaggedStart(*[FadeIn(VGroup(a, b)) for a, b in zip(cells, qs)],
                                                               lag_ratio=0.15), run_time=1.4)
        self.clear_scene()
