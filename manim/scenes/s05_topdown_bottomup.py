import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *

FIB_DP = [
    "FIB-DP(n)",
    "let dp[0..n] be a new array",
    "dp[0] = 0",
    "dp[1] = 1",
    "for i = 2 to n",
    "    dp[i] = dp[i - 1] + dp[i - 2]",
    "return dp[n]",
]


class S05TopDownBottomUp(LectureScene):
    def construct(self):
        bar = title_bar("Dynamic Programming Paradigm", "Two Implementations")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        # ------------------------------------------------ dua kartu
        def card(title, sub, color, body, visual):
            box = panel(6.3, 4.9)
            t = T(title, 30, color, BOLD).next_to(box.get_corner(UL), DR, buff=0.3)
            s = T(sub, 22, MUTED).next_to(t, DOWN, aligned_edge=LEFT, buff=0.1)
            b = M(body, 21).next_to(s, DOWN, aligned_edge=LEFT, buff=0.25)
            if b.width > 5.7:
                b.scale_to_fit_width(5.7).next_to(s, DOWN, aligned_edge=LEFT, buff=0.25)
            visual.next_to(b, DOWN, buff=0.35).set_x(box.get_x())
            return VGroup(box, t, s, b, visual)

        # visual top-down: panggil turun, cache di samping
        calls = VGroup(*[T(f"fib({k})", 20, FG, slant=ITALIC) for k in (5, 4, 3, 2)]).arrange(DOWN, buff=0.3)
        arrows = VGroup(*[Arrow(calls[k].get_bottom(), calls[k + 1].get_top(), buff=0.05, stroke_width=2.5,
                                color=BLUE, tip_length=0.1) for k in range(3)])
        cache = VGroup(*[Square(0.42, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.15) for _ in range(4)])
        cache.arrange(DOWN, buff=0.05).next_to(calls, RIGHT, buff=1.0)
        cache_lbl = T("cache", 18, BLUE).next_to(cache, UP, buff=0.1)
        td_vis = VGroup(calls, arrows, cache, cache_lbl)
        # visual bottom-up: tabel diisi kiri -> kanan
        cells = VGroup(*[Square(0.55, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.15) for _ in range(6)])
        cells.arrange(RIGHT, buff=0)
        idx = VGroup(*[T(str(k), 16, MUTED).next_to(cells[k], DOWN, buff=0.08) for k in range(6)])
        sweep = Arrow(cells.get_left() + DOWN * 0.75, cells.get_right() + DOWN * 0.75, buff=0, color=GREEN,
                      stroke_width=3, tip_length=0.15)
        bu_vis = VGroup(cells, idx, sweep)

        td = card("Top-down", "(Memoization)", BLUE,
                  "Write the natural recursion;\ncache results to avoid recomputation.", td_vis)
        bu = card("Bottom-up", "(Tabulation)", GREEN,
                  "Fill a table in an order ensuring subproblems\nare solved before they are needed.", bu_vis)
        VGroup(td, bu).arrange(RIGHT, buff=0.4).move_to([0, -0.25, 0])

        with self.say("s05_two") as seg:
            seg.wait_sentence(1)
            self.play(FadeIn(td[0]), FadeIn(td[1:4], shift=UP * 0.1), run_time=0.7)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(calls[k]), GrowArrow(arrows[k - 1]) if k else Wait(0))
                                    for k in range(4)], lag_ratio=0.5), run_time=1.6)
            self.play(LaggedStart(*[FadeIn(cache[k]) for k in range(4)], lag_ratio=0.2), FadeIn(cache_lbl), run_time=0.8)
            seg.wait_sentence(2)
            self.play(FadeIn(bu[0]), FadeIn(bu[1:4], shift=UP * 0.1), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(cl) for cl in cells], lag_ratio=0.2), FadeIn(idx), run_time=1.2)
            self.play(GrowArrow(sweep), run_time=0.8)

        with self.say("s05_question") as seg:
            tag = pill("MEMOIZED-FIB  =  Top-down", BLUE, 22).next_to(td[0], DOWN, buff=0.2)
            self.play(FadeIn(tag, shift=UP * 0.1), td[0].animate.set_stroke(BLUE, 3), run_time=0.6)
            seg.wait_sentence(1)
            q = T("Can we make it a Bottom-up implementation?", 26, YELLOW, BOLD).next_to(bu[0], DOWN, buff=0.2)
            q.set_x(0)
            self.play(FadeOut(tag), Write(q), bu[0].animate.set_stroke(GREEN, 3), run_time=1.2)
        self.fade_all_except(bar)

        # ------------------------------------------------ FIB-DP + tabel
        new_bar = title_bar("Dynamic Programming Paradigm", "Bottom-up Fibonacci")
        self.play(Transform(bar, new_bar), run_time=0.5)
        code = CodePanel(FIB_DP, size=20).move_to([-3.55, 0.55, 0])
        dp = ArrayRow([""] * 6, cell=0.85, size=30, index_from=0).move_to([3.55, 0.9, 0])
        dp_lbl = T("dp[0..5]   (n = 5)", 22, GREEN, BOLD).next_to(dp, UP, buff=0.25)
        vals = [0, 1, 1, 2, 3, 5]
        shown = {}

        def put(k, color=GREEN):
            t = dp.set_value(k, vals[k], color)
            shown[k] = t
            return AnimationGroup(FadeIn(t, scale=1.4), dp.cells[k].animate.set_fill(color, 0.18).set_stroke(color, 2.5))

        with self.say("s05_code") as seg:
            self.play(FadeIn(code, shift=RIGHT * 0.2), run_time=0.7)
            hl = code.highlight_box(0, YELLOW)
            self.play(FadeIn(hl), run_time=0.3)
            seg.wait_sentence(2)
            self.play(hl.animate.become(code.highlight_box(1)), FadeIn(dp), FadeIn(dp_lbl), run_time=0.6)
            self.play(hl.animate.become(code.lines_box(2, 3)), put(0, BLUE), put(1, BLUE), run_time=0.8)
            seg.wait_sentence(3)
            self.play(hl.animate.become(code.lines_box(4, 5, ORANGE)), run_time=0.5)
            seg.wait_sentence(4)
            self.play(hl.animate.become(code.highlight_box(6, GREEN)), run_time=0.5)

        with self.say("s05_fill") as seg:
            self.play(hl.animate.become(code.highlight_box(5, ORANGE)), run_time=0.4)
            seg.wait_sentence(1)
            span = seg.at(2) - seg.at(1)
            per = max(0.9, span / 4 - 0.1)
            eq = VGroup()
            for k in range(2, 6):
                a1 = CurvedArrow(dp.cells[k - 1].get_top() + UP * 0.05, dp.cells[k].get_top() + UP * 0.05,
                                 angle=-TAU / 4, color=BLUE, stroke_width=3, tip_length=0.15)
                a2 = CurvedArrow(dp.cells[k - 2].get_bottom() + DOWN * 0.45, dp.cells[k].get_bottom() + DOWN * 0.45,
                                 angle=TAU / 5, color=PURPLE, stroke_width=3, tip_length=0.15)
                new_eq = M(f"dp[{k}] = dp[{k-1}] + dp[{k-2}] = {vals[k-1]} + {vals[k-2]} = " + c(str(vals[k]), GREEN), 26)
                new_eq.scale_to_fit_width(min(new_eq.width, 6.2)).move_to([3.55, -0.75, 0])
                self.play(Create(a1), Create(a2), FadeOut(eq), FadeIn(new_eq), run_time=per * 0.45)
                self.play(put(k), run_time=per * 0.35)
                self.play(FadeOut(a1), FadeOut(a2), run_time=per * 0.2)
                eq = new_eq
            seg.wait_sentence(2)
            on = pill("one loop · no recursion · O(n)", GREEN, 22).move_to([3.55, -1.6, 0])
            self.play(FadeIn(on, shift=UP * 0.1), run_time=0.6)
        note = M("Initialize <b>dp</b>, then compute Fibonacci values from 2 to n  →  " + c("O(n)", GREEN) + " time.", 24)
        note.move_to([0, -2.45, 0])
        self.play(FadeIn(note), run_time=0.5)
        self.wait(0.6)
        self.fade_all_except(bar)

        # ------------------------------------------------ tabel perbandingan
        new_bar = title_bar("Dynamic Programming Paradigm", "Top-down vs Bottom-up")
        self.play(Transform(bar, new_bar), run_time=0.5)
        rows = [
            ["", "Memoization", "Tabulation"],
            ["Computation", "Only needed subproblems", "All subproblems"],
            ["Space", "O(subproblems computed)", "O(table size)"],
            ["Overhead", "Recursion", "Iteration"],
        ]
        tbl = grid_table(rows, [3.2, 4.6, 4.6], row_height=0.95, size=26).move_to([0, 0, 0])
        with self.say("s05_table") as seg:
            self.play(FadeIn(row_of(tbl, 0, 3), shift=DOWN * 0.1), run_time=0.6)
            for r in range(1, 4):
                seg.wait_sentence(r)
                self.play(FadeIn(row_of(tbl, r, 3), shift=UP * 0.1), run_time=0.6)
                self.play(Indicate(tbl.cells_map[(r, 0)][1], color=YELLOW), run_time=0.6)
        self.clear_scene()
