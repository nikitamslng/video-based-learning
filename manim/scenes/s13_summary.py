import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *

ITEMS = [
    ("1", "Dynamic Programming", BLUE,
     "<b>DP</b> solves problems by <b>caching solutions</b> to\noverlapping subproblems; requires\noptimal substructure."),
    ("2", "Memoization vs Tabulation", GREEN,
     "<b>Memoization</b> (top-down): cache recursive calls.\n<b>Tabulation</b> (bottom-up): fill table iteratively."),
    ("3", "Kadane's Algorithm", ORANGE,
     c("dp[i] = max(A[i], dp[i−1] + A[i])", YELLOW) + "\n" + c("O(n)", GREEN) + " time, " + c("O(1)", GREEN)
     + " space in the optimized version."),
    ("4", "Kadane is DP", PURPLE,
     "Each <b>dp[i]</b> depends on <b>dp[i−1]</b>\n(optimal substructure); decisions cannot be\n"
     "made greedily without the past optimal state."),
]


class S13Summary(LectureScene):
    def construct(self):
        bar = title_bar("Session 15", "Summary")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)
        cards = VGroup()
        for num, title, col, body in ITEMS:
            box = panel(6.4, 2.3)
            circ = Circle(0.3, color=col, fill_opacity=0.2, stroke_width=3)
            n = T(num, 24, col, BOLD).move_to(circ)
            t = T(title, 26, col, BOLD)
            head = VGroup(VGroup(circ, n), t).arrange(RIGHT, buff=0.25).next_to(box.get_corner(UL), DR, buff=0.25)
            b = M(body, 20).next_to(head, DOWN, aligned_edge=LEFT, buff=0.2)
            if b.width > 5.75:
                b.scale_to_fit_width(5.75)
                b.next_to(head, DOWN, aligned_edge=LEFT, buff=0.2)
            cards.add(VGroup(box, head, b))
        cards.arrange_in_grid(2, 2, buff=(0.35, 0.3)).move_to([0, -0.2, 0])

        with self.say("s13_a") as seg:
            seg.wait_sentence(1)
            self.play(FadeIn(cards[0], shift=UP * 0.2), run_time=0.8)
            seg.wait_sentence(2)
            self.play(FadeIn(cards[1], shift=UP * 0.2), run_time=0.8)
        with self.say("s13_b") as seg:
            self.play(FadeIn(cards[2], shift=UP * 0.2), run_time=0.8)
            seg.wait_sentence(1)
            self.play(FadeIn(cards[3], shift=UP * 0.2), run_time=0.8)
            self.play(*[c_[0].animate.set_stroke(ITEMS[k][2], 2.5) for k, c_ in enumerate(cards)], run_time=0.8)
        self.clear_scene()
