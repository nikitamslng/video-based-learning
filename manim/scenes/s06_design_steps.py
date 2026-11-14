import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *

STEPS = [
    ("1", "Characterize", "the structure of\nan optimal solution", BLUE),
    ("2", "Define", "the value of an optimal\nsolution recursively", GREEN),
    ("3", "Compute", "the value bottom-up\n(or top-down with memoization)", ORANGE),
    ("4", "Construct", "an optimal solution from\nthe computed information", PURPLE),
]
KADANE = [
    "dp[i]: best ending at i",
    "max(A[i], dp[i−1]+A[i])",
    "table → O(1) space",
    "track start / end",
]


class S06DesignSteps(LectureScene):
    def construct(self):
        bar = title_bar("Dynamic Programming Paradigm", "Design Steps")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)
        intro = T("Generally, there are 4 steps to design a DP algorithm:", 28, MUTED).move_to([0, 2.15, 0])

        cards = VGroup()
        for num, name, desc, col in STEPS:
            box = panel(3.1, 3.1)
            circ = Circle(0.38, color=col, fill_opacity=0.2, stroke_width=3)
            n = T(num, 30, col, BOLD).move_to(circ)
            head = T(name, 28, col, BOLD)
            body = T(desc, 18, FG, line_spacing=0.9)
            if body.width > 2.8:
                body.scale_to_fit_width(2.8)
            inner = VGroup(VGroup(circ, n), head, body).arrange(DOWN, buff=0.25)
            inner.move_to(box)
            cards.add(VGroup(box, inner))
        cards.arrange(RIGHT, buff=0.38).move_to([0, 0.4, 0])
        arrows = VGroup(*[Arrow(cards[k].get_right(), cards[k + 1].get_left(), buff=0.04, color=MUTED,
                                stroke_width=3, tip_length=0.14) for k in range(3)])

        with self.say("s06_steps") as seg:
            self.play(FadeIn(intro), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(cd, shift=UP * 0.2) for cd in cards], lag_ratio=0.15),
                      *[GrowArrow(a) for a in arrows], run_time=1.4)
            veils = VGroup(*[Rectangle(width=cd.width + 0.1, height=cd.height + 0.1, fill_color=BG, fill_opacity=0.62,
                                       stroke_width=0).move_to(cd) for cd in cards])
            self.play(FadeIn(veils), run_time=0.3)
            for k in range(4):
                seg.wait_sentence(k + 1)
                col = STEPS[k][3]
                anims = [FadeOut(veils[k]), cards[k][0].animate.set_stroke(col, 3)]
                if k:
                    anims.append(cards[k - 1][0].animate.set_stroke(BORDER, 2))
                self.play(*anims, run_time=0.5)
                self.play(Indicate(cards[k][1][1], color=col, scale_factor=1.12), run_time=0.6)
            self.play(cards[3][0].animate.set_stroke(BORDER, 2), run_time=0.3)

        with self.say("s06_apply") as seg:
            tgt = pill("Applied to: Maximum Subarray Sum (Kadane's Algorithm)", ORANGE, 22).move_to([0, -2.35, 0])
            maps = VGroup()
            for t, cd in zip(KADANE, cards):
                m = T(t, 18, YELLOW, font=MONO)
                if m.width > 3.0:
                    m.scale_to_fit_width(3.0)
                bg = panel(3.1, 0.5, color="#1E1A0E", stroke=YELLOW, radius=0.1)
                bg.next_to(cd, DOWN, buff=0.2)
                maps.add(VGroup(bg, m.move_to(bg)))
            self.play(FadeIn(tgt, shift=UP * 0.1), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.1) for m in maps], lag_ratio=0.25), run_time=1.6)
        self.clear_scene()
