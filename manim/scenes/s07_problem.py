import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *

A = [-2, 1, -3, 4, -1, 2, 1, -5, 4]


class S07Problem(LectureScene):
    def construct(self):
        bar = title_bar("Maximum Subarray Sum: Kadane's Algorithm", "Problem")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        stmt = M("Given an array " + c("A[1..n]", BLUE) + " of integers (possibly negative), find the\n"
                 + c("<b>contiguous</b>", ORANGE) + " subarray " + c("A[i..j]", ORANGE) + " with the "
                 + c("<b>maximum sum</b>", GREEN) + ".", 28)
        stmt.move_to([0, 1.85, 0])
        arr = ArrayRow(A, cell=1.0, size=34).move_to([0, -0.15, 0])

        with self.say("s07_statement") as seg:
            self.play(FadeIn(stmt, shift=DOWN * 0.1), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(VGroup(arr.cells[k], arr.vals[k], arr.idx[k]), shift=UP * 0.2)
                                    for k in range(9)], lag_ratio=0.08), run_time=1.4)
            seg.wait_sentence(2)
            # contiguous vs not contiguous
            ok = arr.window(1, 3, GREEN)
            ok_t = T("contiguous ✓", 22, GREEN).next_to(ok, DOWN, buff=0.55)
            self.play(Create(ok), FadeIn(ok_t), run_time=0.7)
            bad = VGroup(arr.window(0, 0, RED), arr.window(2, 2, RED), arr.window(5, 5, RED))
            bad_t = T("not contiguous ✗", 22, RED).next_to(arr.cells[5], DOWN, buff=0.85)
            self.wait(0.8)
            self.play(ReplacementTransform(ok, bad), ReplacementTransform(ok_t, bad_t), run_time=0.8)
            self.wait(0.8)
            self.play(FadeOut(bad), FadeOut(bad_t), run_time=0.5)

        with self.say("s07_example") as seg:
            self.play(LaggedStart(*[Indicate(arr.vals[k], color=YELLOW, scale_factor=1.25) for k in range(9)],
                                  lag_ratio=0.25), run_time=min(4.5, seg.at(1) - 0.3))
            seg.wait_sentence(1)
            win = arr.window(3, 6, ORANGE, width=6)
            self.play(Create(win), arr.tint(3, 6, ORANGE, 0.3), run_time=0.8)
            terms = M("4 + (−1) + 2 + 1 = " + c("<b>6</b>", GREEN), 34).next_to(arr, DOWN, buff=0.6)
            lbl = M(c("A[4..7]", ORANGE) + " = [4, −1, 2, 1]", 28).next_to(win, UP, buff=0.2)
            self.play(FadeIn(lbl, shift=DOWN * 0.1), run_time=0.5)
            self.play(Write(terms), run_time=1.2)

        with self.say("s07_insight") as seg:
            ring = Circle(0.62, color=RED, stroke_width=5).move_to(arr.cells[4])
            self.play(FadeOut(stmt), Create(ring), run_time=0.8)
            seg.wait_sentence(1)
            alt = VGroup(
                M("[4] alone           = 4", 24, MUTED, font=MONO),
                M("[2, 1]              = 3", 24, MUTED, font=MONO),
                M("[4, −1, 2, 1]       = " + c("6", GREEN), 24, FG, font=MONO),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0, 1.95, 0])
            self.play(lbl.animate.scale(0.85).next_to(win, UP, buff=0.12), run_time=0.4)
            self.play(FadeIn(alt, shift=DOWN * 0.1), run_time=0.8)
            seg.wait_sentence(2)
            msg = M("Swallowing a negative number can pay off\nif larger positives follow.", 24, YELLOW)
            msg.next_to(terms, DOWN, buff=0.25)
            self.play(FadeIn(msg, shift=UP * 0.1), Indicate(VGroup(arr.cells[5], arr.cells[6]), color=GREEN), run_time=1.0)
        self.clear_scene()
