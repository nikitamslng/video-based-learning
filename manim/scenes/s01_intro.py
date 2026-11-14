import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *


class S01Intro(LectureScene):
    def construct(self):
        # ---------------------------------------------------------- title card
        with self.say("s01_title") as seg:
            sess = pill("SESSION 15", ORANGE, 22)
            t1 = T("Dynamic Programming", 74, FG, BOLD)
            t2 = T("Maximum Subarray Sum", 46, ORANGE, BOLD)
            grp = VGroup(sess, t1, t2).arrange(DOWN, buff=0.32).shift(UP * 1.25)
            arr = ArrayRow([-2, 1, -3, 4, -1, 2, 1, -5, 4], cell=0.72, size=26, show_index=False)
            arr.next_to(grp, DOWN, buff=0.75)
            credit = T("Subject Matter Expert: Henry Lucky, S.Kom., M.Kom.", 20, MUTED)
            credit.move_to([0, -2.45, 0])
            self.play(FadeIn(sess, shift=DOWN * 0.2), Write(t1), run_time=1.6)
            self.play(FadeIn(t2, shift=UP * 0.2), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(VGroup(arr.cells[k], arr.vals[k]), shift=UP * 0.3)
                                    for k in range(9)], lag_ratio=0.08), FadeIn(credit), run_time=1.4)
            seg.wait_sentence(2)
            win = arr.window(0, 1, ORANGE)
            self.play(Create(win), run_time=0.5)
            for a, b in [(1, 3), (3, 5), (3, 6)]:
                self.play(win.animate.become(arr.window(a, b, ORANGE)), run_time=0.6)
            total = T("sum = 6", 26, ORANGE, BOLD).next_to(win, UP, buff=0.12)
            self.play(arr.tint(3, 6, ORANGE, 0.3), FadeIn(total, shift=UP * 0.1), run_time=0.7)
        self.clear_scene()

        # ---------------------------------------------------------- learning outcomes
        bar = title_bar("Session 15", "Learning Outcomes")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        def lo_card(tag, color, points):
            body = VGroup(*[M(p, 22, line_spacing=0.9) for p in points])
            for b in body:
                if b.width > 5.6:
                    b.scale_to_fit_width(5.6)
            rows = VGroup()
            for b in body:
                d = Dot(radius=0.05, color=color)
                d.next_to(b, LEFT, buff=0.18).align_to(b, UP).shift(DOWN * 0.1)
                rows.add(VGroup(d, b))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
            head = pill(tag, color, 22)
            box = panel(6.5, rows.height + 1.55)
            head.next_to(box.get_corner(UL), DR, buff=0.3)
            rows.next_to(head, DOWN, aligned_edge=LEFT, buff=0.35).shift(RIGHT * 0.2)
            return VGroup(box, head, rows)

        lo2 = lo_card("LO 2 · Analyze", BLUE, [
            "Identify <b>optimal substructure</b> &amp;\n<b>overlapping subproblems</b> as conditions for DP",
            "Distinguish DP from <b>greedy</b> (no re-evaluation)\nand <b>D&amp;C</b> (independent subproblems)",
            "Classify <b>Kadane's algorithm</b> as DP by its\nstate-dependent decision",
        ])
        lo3 = lo_card("LO 3 · Design", ORANGE, [
            "Design Kadane's algorithm with\n" + c("dp[i] = max(A[i], dp[i−1] + A[i])", YELLOW),
            "Apply the four-step DP design process\ncharacterize → define → compute → construct",
            "Implement both <b>memoization</b>\nand <b>tabulation</b>",
        ])
        cards = VGroup(lo2, lo3).arrange(RIGHT, buff=0.4).move_to([0, -0.15, 0])

        with self.say("s01_lo2") as seg:
            self.play(FadeIn(lo2[0]), FadeIn(lo2[1], shift=DOWN * 0.1), run_time=0.7)
            for k, row in enumerate(lo2[2]):
                seg.wait_sentence(k + 1)
                self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.6)
        with self.say("s01_lo3") as seg:
            self.play(lo2.animate.set_opacity(0.45), FadeIn(lo3[0]), FadeIn(lo3[1], shift=DOWN * 0.1), run_time=0.7)
            self.play(FadeIn(lo3[2][0], shift=RIGHT * 0.2), run_time=0.6)
            seg.wait_sentence(1)
            self.play(FadeIn(lo3[2][1], shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(lo3[2][2], shift=RIGHT * 0.2), run_time=0.6)
            self.play(lo2.animate.set_opacity(1), run_time=0.5)
        self.fade_out(cards)

        # ---------------------------------------------------------- outline
        new_bar = title_bar("Session 15", "Outline")
        self.play(Transform(bar, new_bar), run_time=0.6)
        items = [
            "DP Paradigm — Optimal Substructure and Overlapping Subproblems",
            "Memoization vs. Tabulation",
            "Maximum Subarray Sum: Kadane's Algorithm",
            "Why Kadane's is DP and Not Greedy",
        ]
        colors = [BLUE, GREEN, ORANGE, PURPLE]
        rows = VGroup()
        for k, (it, col) in enumerate(zip(items, colors)):
            num = Circle(0.32, color=col, fill_opacity=0.18, stroke_width=3)
            nt = T(str(k + 1), 26, col, BOLD).move_to(num)
            txt = T(it, 28, FG)
            row = VGroup(VGroup(num, nt), txt).arrange(RIGHT, buff=0.35)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.1, 0])
        frames = VGroup(*[panel(rows.width + 0.8, r.height + 0.3, color=PANEL_2)
                          .move_to([rows.get_center()[0], r.get_center()[1], 0]) for r in rows])

        def dim(row, o):
            circ, nt = row[0]
            return AnimationGroup(circ.animate.set_stroke(opacity=o).set_fill(opacity=0.18 * o),
                                  nt.animate.set_opacity(o), row[1].animate.set_opacity(o))
        for f in frames:
            f.set_opacity(0)
        self.add(frames)
        with self.say("s01_outline") as seg:
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in rows], lag_ratio=0.15), run_time=1.2)
            self.play(*[dim(r, 0.4) for r in rows], run_time=0.3)
            for k in range(4):
                seg.wait_sentence(k + 1)
                anims = [dim(rows[k], 1), frames[k].animate.set_fill(PANEL_2, 1).set_stroke(colors[k], 2, 1)]
                if k > 0:
                    anims += [dim(rows[k - 1], 0.55), frames[k - 1].animate.set_fill(opacity=0).set_stroke(opacity=0)]
                self.play(*anims, run_time=0.5)
            self.play(*[dim(r, 1) for r in rows], run_time=0.4)
        self.clear_scene()
