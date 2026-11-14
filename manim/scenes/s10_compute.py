import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *

A = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

KADANE_TABLE = [
    "KADANE-TABLE(A)",
    "n = A.length",
    "let dp[1..n] be a new array",
    "dp[1] = A[1]",
    "global_max = A[1]",
    "for i = 2 to n",
    "    dp[i] = max(A[i], dp[i - 1] + A[i])",
    "    if dp[i] > global_max",
    "        global_max = dp[i]",
    "return global_max",
]
KADANE_OPT = [
    "KADANE-SPACE-OPTIMIZED(A)",
    "n = A.length",
    "curr_max = A[1]",
    "global_max = A[1]",
    "for i = 2 to n",
    "    curr_max = max(A[i], curr_max + A[i])",
    "    if curr_max > global_max",
    "        global_max = curr_max",
    "return global_max",
]
FIB_OPT = [
    "FIB-SPACE-OPTIMIZED(n)",
    "if n == 0 return 0",
    "prev2 = 0",
    "prev1 = 1",
    "for i = 2 to n",
    "    curr = prev1 + prev2",
    "    prev2, prev1 = prev1, curr",
    "return prev1",
]


def kadane_steps(arr):
    out = []
    dp = arr[0]
    g = arr[0]
    out.append(dict(i=1, dp=dp, g=g, kind="base", up=True, f=f"dp[1] = A[1] = {arr[0]}"))
    for i in range(1, len(arr)):
        ext = dp + arr[i]
        new = max(arr[i], ext)
        kind = "start" if arr[i] > ext else "extend"
        a_s = str(arr[i]).replace("-", "−")
        dp_s = f"({dp})".replace("-", "−") if dp < 0 and False else str(dp).replace("-", "−")
        ai_s = f"({arr[i]})".replace("-", "−") if arr[i] < 0 else str(arr[i])
        f = f"dp[{i+1}] = max({a_s}, {dp_s} + {ai_s}) = {str(new).replace('-', '−')}"
        dp = new
        up = dp > g
        g = max(g, dp)
        out.append(dict(i=i + 1, dp=dp, g=g, kind=kind, up=up, f=f))
    return out


class S10Compute(LectureScene):
    def construct(self):
        bar = title_bar("Maximum Subarray Sum: Kadane's Algorithm", "Step 3 – Compute the Value Bottom-up")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        code = CodePanel(KADANE_TABLE, size=16).move_to([-3.6, 0.25, 0])
        arrA = ArrayRow(A, cell=0.72, size=24).move_to([3.4, 1.8, 0])
        arrD = ArrayRow([""] * 9, cell=0.72, size=24, fill=PANEL, show_index=False).move_to([3.4, 0.2, 0])
        la = T("A", 22, BLUE, BOLD).next_to(arrA, UP, buff=0.12).align_to(arrA, LEFT)
        ld = T("dp", 22, GREEN, BOLD).next_to(arrD, UP, buff=0.12).align_to(arrD, LEFT)
        gbox = panel(3.0, 0.75, color=PANEL_2, stroke=YELLOW)
        gl = T("global_max", 22, YELLOW, font=MONO)
        gv = T("—", 30, YELLOW, BOLD)
        gm = VGroup(gbox, VGroup(gl, gv).arrange(RIGHT, buff=0.35).move_to(gbox)).move_to([3.4, -2.05, 0])
        legend = VGroup(M(c("■", GREEN) + " start new", 18, MUTED), M(c("■", BLUE) + " extend", 18, MUTED))
        legend.arrange(RIGHT, buff=0.4).next_to(arrD, DOWN, buff=0.15)

        with self.say("s10_code") as seg:
            self.play(FadeIn(code, shift=RIGHT * 0.2), run_time=0.8)
            hl = code.highlight_box(0, YELLOW)
            self.play(FadeIn(hl), run_time=0.3)
            seg.wait_sentence(2)
            self.play(hl.animate.become(code.lines_box(3, 4, BLUE)), run_time=0.4)
            seg.wait_sentence(3)
            self.play(hl.animate.become(code.lines_box(5, 6, ORANGE)), run_time=0.4)
            self.wait(1.6)
            self.play(hl.animate.become(code.lines_box(7, 8, GREEN)), run_time=0.4)
            self.play(FadeIn(VGroup(arrA, la)), FadeIn(VGroup(arrD, ld)), FadeIn(gm), FadeIn(legend), run_time=0.8)

        steps = kadane_steps(A)
        state = {"f": VMobject(), "vals": {}, "g": gv}
        fpos = [3.4, -1.05, 0]

        def do_step(st, rt=1.0):
            k = st["i"] - 1
            color = {"base": BLUE, "start": GREEN, "extend": BLUE}[st["kind"]]
            fr_a = arrA.window(k, k, ORANGE, width=4)
            anims = [FadeIn(fr_a)]
            fr_d = None
            if k > 0:
                fr_d = arrD.window(k - 1, k - 1, BLUE, width=4)
                anims.append(FadeIn(fr_d))
            nf = Text(st["f"], font=MONO, font_size=22, color=FG).move_to(fpos)
            if nf.width > 6.8:
                nf.scale_to_fit_width(6.8)
            anims += [FadeOut(state["f"]), FadeIn(nf)]
            line = 3 if k == 0 else 6
            anims.append(hl.animate.become(code.highlight_box(line, color)))
            self.play(*anims, run_time=rt * 0.4)
            v = arrD.set_value(k, st["dp"], color, size=24)
            self.play(FadeIn(v, scale=1.4), arrD.cells[k].animate.set_fill(color, 0.22).set_stroke(color, 2.5),
                      run_time=rt * 0.3)
            state["vals"][k] = v
            out = [FadeOut(fr_a)] + ([FadeOut(fr_d)] if fr_d else [])
            if st["up"]:
                ng = T(str(st["g"]).replace("-", "−"), 30, YELLOW, BOLD).move_to(state["g"])
                out += [Transform(state["g"], ng), Flash(gbox, color=YELLOW, flash_radius=1.0, num_lines=10)]
                if k > 0:
                    out.append(hl.animate.become(code.lines_box(7, 8, YELLOW)))
            self.play(*out, run_time=rt * 0.3)
            state["f"] = nf

        with self.say("s10_fill1") as seg:
            seg.wait_sentence(1)
            do_step(steps[0], 1.1)
            seg.wait_sentence(2)
            do_step(steps[1], 1.6)
            seg.wait_sentence(3)
            do_step(steps[2], 1.6)

        with self.say("s10_fill2") as seg:
            do_step(steps[3], 1.6)
            seg.wait_sentence(1)
            span = seg.at(2) - seg.at(1)
            for st in steps[4:7]:
                do_step(st, max(0.9, span / 3 - 0.1))
            seg.wait_sentence(2)
            span = seg.at(3) - seg.at(2)
            for st in steps[7:9]:
                do_step(st, max(0.9, span / 2 - 0.1))
            seg.wait_sentence(3)
            best = arrD.window(6, 6, YELLOW, width=6)
            self.play(Create(best), FadeOut(state["f"]), Indicate(gm, color=YELLOW), run_time=0.9)
            ans = M("max over dp = " + c("<b>6</b>", YELLOW) + "  ✓", 26).move_to(fpos)
            self.play(FadeIn(ans), run_time=0.4)

        with self.say("s10_observe") as seg:
            self.play(FadeOut(ans), FadeOut(best), run_time=0.4)
            win = VGroup(arrD.window(0, 0, BLUE, width=5), arrD.window(1, 1, GREEN, width=5))
            self.play(Create(win), run_time=0.5)
            arc = CurvedArrow(arrD.cells[0].get_bottom() + DOWN * 0.08, arrD.cells[1].get_bottom() + DOWN * 0.08,
                              angle=TAU / 4, color=BLUE, tip_length=0.15)
            self.play(Create(arc), run_time=0.4)
            for k in range(1, 8):
                self.play(win[0].animate.become(arrD.window(k, k, BLUE, width=5)),
                          win[1].animate.become(arrD.window(k + 1, k + 1, GREEN, width=5)),
                          arc.animate.shift(RIGHT * arrD.cell), run_time=0.45)
            seg.wait_sentence(1)
            others = VGroup(*[VGroup(arrD.cells[k], state["vals"][k]) for k in range(7)])
            self.play(others.animate.set_opacity(0.2), run_time=0.6)
            one = M("only <b>dp[i−1]</b> is needed  →  keep <b>one variable</b>", 24, YELLOW).move_to(fpos)
            self.play(FadeIn(one, shift=UP * 0.1), run_time=0.6)
        self.fade_all_except(bar, run_time=0.7)

        # ------------------------------------------------ space-optimized
        code2 = CodePanel(KADANE_OPT, size=17).move_to([-3.45, 0.3, 0])
        cells = VGroup(*[Square(0.6, stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.2) for _ in range(9)])
        cells.arrange(RIGHT, buff=0).move_to([3.4, 1.2, 0])
        cl = T("dp[1..n]   space O(n)", 22, MUTED).next_to(cells, UP, buff=0.15)
        one_box = panel(2.4, 0.9, color=PANEL_2, stroke=GREEN)
        one_t = T("curr_max", 26, GREEN, font=MONO).move_to(one_box)
        single = VGroup(one_box, one_t).move_to([3.4, 1.2, 0])
        sl = T("one variable   space O(1)", 22, GREEN).next_to(single, UP, buff=0.15)
        cmp_ = VGroup(
            M("Time:   " + c("O(n)", FG) + "  →  " + c("<b>O(n)</b>", GREEN), 28),
            M("Space:  " + c("O(n)", RED) + "  →  " + c("<b>O(1)</b>", GREEN), 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -0.55, 0])
        lesson = pill("DP is not always about tables!", ORANGE, 24).move_to([3.4, -1.9, 0])
        with self.say("s10_space") as seg:
            self.play(FadeIn(code2, shift=RIGHT * 0.2), FadeIn(cells), FadeIn(cl), run_time=0.8)
            seg.wait_sentence(1)
            hl2 = code2.lines_box(2, 2, GREEN)
            self.play(FadeIn(hl2), run_time=0.3)
            self.play(ReplacementTransform(cells, single), ReplacementTransform(cl, sl), run_time=1.2)
            self.play(hl2.animate.become(code2.highlight_box(5, GREEN)), run_time=0.4)
            seg.wait_sentence(2)
            self.play(FadeIn(cmp_[0], shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(cmp_[1], shift=UP * 0.1), run_time=0.5)
            seg.wait_sentence(3)
            self.play(FadeIn(lesson, scale=0.8), run_time=0.6)
        self.fade_all_except(bar, code2, run_time=0.5)

        # ------------------------------------------------ fib space-optimized
        code3 = CodePanel(FIB_OPT, size=19).move_to([-3.45, 0.3, 0])
        seq = ArrayRow([0, 1, 1, 2, 3, 5, 8], cell=0.75, size=26, index_from=0).move_to([3.4, 0.9, 0])
        seq_l = T("fib(i)", 22, MUTED).next_to(seq.cells, LEFT, buff=0.25)
        p2 = seq.window(0, 0, PURPLE, width=5)
        p1 = seq.window(1, 1, BLUE, width=5)
        p2l = T("prev2", 20, PURPLE, font=MONO).next_to(seq.idx[0], DOWN, buff=0.12)
        p1l = T("prev1", 20, BLUE, font=MONO).next_to(seq.cells[1], UP, buff=0.12)
        note = M("In fact, you may have done this in <b>Fibonacci</b> before.", 26).move_to([0, -2.3, 0])
        with self.say("s10_fib") as seg:
            self.play(ReplacementTransform(code2, code3), run_time=0.8)
            self.play(FadeIn(seq), FadeIn(seq_l), FadeIn(note), run_time=0.6)
            seg.wait_sentence(1)
            self.play(Create(p2), Create(p1), FadeIn(p2l), FadeIn(p1l), run_time=0.6)
            hl3 = code3.lines_box(5, 6, ORANGE)
            self.play(FadeIn(hl3), run_time=0.3)
            for k in range(1, 6):
                self.play(p2.animate.become(seq.window(k, k, PURPLE, width=5)),
                          p1.animate.become(seq.window(k + 1, k + 1, BLUE, width=5)),
                          p2l.animate.next_to(seq.idx[k], DOWN, buff=0.12),
                          p1l.animate.next_to(seq.cells[k + 1], UP, buff=0.12), run_time=0.6)
        self.clear_scene()
