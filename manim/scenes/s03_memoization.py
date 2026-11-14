import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *
from fibtree import FibTree

MEMO_CODE = [
    "MEMOIZED-FIB(n)",
    "let memo[0..n] be a new array",
    "for i = 0 to n",
    "    memo[i] = NIL",
    "return MEMOIZED-FIB-AUX(n, memo)",
    "",
    "MEMOIZED-FIB-AUX(n, memo)",
    "if n <= 1",
    "    return n",
    "if memo[n] != NIL  //if saved, no need to recalculate",
    "    return memo[n]",
    "memo[n] = MEMOIZED-FIB-AUX(n - 1, memo) + MEMOIZED-FIB-AUX(n - 2, memo)",
    "return memo[n]",
]


def renumber(lines):
    out, num = [], 0
    for k, ln in enumerate(lines):
        if k in (0, 6) or ln == "":
            out.append("    " + ln)
            num = 0
        else:
            num += 1
            out.append(f"{num:>2}  " + ln)
    return out


class S03Memoization(LectureScene):
    def construct(self):
        bar = title_bar("Dynamic Programming Paradigm", "Why DP? — Memoization")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        code = CodePanel(renumber(MEMO_CODE), size=18, header=False, numbered=False)
        # warnai header prosedur
        for k in (0, 6):
            code.line(k)[1:].set_color(YELLOW)
        code.move_to([0, -0.2, 0])

        with self.say("s03_code1") as seg:
            self.play(FadeIn(code, shift=UP * 0.2), run_time=0.9)
            seg.wait_sentence(1)
            hl = code.highlight_box(0, YELLOW)
            self.play(FadeIn(hl), run_time=0.4)
            seg.wait_sentence(2)
            self.play(hl.animate.become(code.lines_box(1, 3, BLUE)), run_time=0.5)
        with self.say("s03_code2") as seg:
            self.play(hl.animate.become(code.lines_box(6, 8, MUTED)), run_time=0.5)
            seg.wait_sentence(1)
            self.play(hl.animate.become(code.lines_box(9, 10, GREEN)), run_time=0.5)
            seg.wait_sentence(2)
            self.play(hl.animate.become(code.lines_box(11, 12, ORANGE)), run_time=0.5)

        # ------------------------------------------------ trace pada tree
        self.play(FadeOut(code), FadeOut(hl), run_time=0.6)
        tree = FibTree(5, leaf_dx=1.08, level_dy=1.0, size=20)
        tree.move_to([2.65, -0.2, 0])
        ghost = tree.copy().set_opacity(0.12)

        memo = VGroup()
        for k in range(6):
            sq = Square(0.78, fill_color=PANEL, fill_opacity=1, stroke_color=BORDER, stroke_width=2)
            memo.add(sq)
        memo.arrange(RIGHT, buff=0).move_to([-4.55, 1.55, 0])
        memo_t = VGroup(*[T("NIL", 16, MUTED).move_to(memo[k]) for k in range(6)])
        memo_i = VGroup(*[T(str(k), 18, MUTED).next_to(memo[k], DOWN, buff=0.1) for k in range(6)])
        memo_lbl = T("memo[0..5]", 22, BLUE, BOLD).next_to(memo, UP, buff=0.18)
        legend = VGroup(
            M(c("■", GREEN) + " computed &amp; saved", 20, MUTED),
            M(c("■", YELLOW) + " memo hit (not recomputed)", 20, MUTED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(memo_i, DOWN, aligned_edge=LEFT, buff=0.45)

        def mark(nd, color, fill=None):
            box = nd["mob"][0]
            return box.animate.set_stroke(color, 3).set_fill(fill or PANEL, 1)

        def show(nd):
            anims = [FadeIn(nd["mob"], scale=0.8)]
            if "edge" in nd:
                anims.insert(0, Create(nd["edge"]))
            return AnimationGroup(*anims)

        def value_tag(nd, v, color):
            return T(f"={v}", 18, color, BOLD).next_to(nd["mob"], RIGHT, buff=0.06)

        def save(k, v, src):
            new = T(str(v), 24, GREEN, BOLD).move_to(memo[k])
            fly = T(str(v), 24, GREEN, BOLD).move_to(src)
            return Succession(FadeIn(fly, run_time=0.01),
                              AnimationGroup(fly.animate.move_to(memo[k]), FadeOut(memo_t[k]),
                                             memo[k].animate.set_fill(GREEN, 0.18).set_stroke(GREEN, 2.5),
                                             run_time=0.7)), new, fly

        N = tree.nodes
        # preorder index: 0 f5, 1 f4, 2 f3, 3 f2, 4 f1, 5 f0, 6 f1, 7 f2*, 8 f1, 9 f0, 10 f3*, ...
        f5, f4, f3, f2, f1a, f0a, f1b, f2b = N[0], N[1], N[2], N[3], N[4], N[5], N[6], N[7]
        f3b = [nd for nd in N if nd["depth"] == 1 and nd["n"] == 3][0]

        with self.say("s03_trace") as seg:
            self.play(FadeIn(ghost), FadeIn(memo), FadeIn(memo_t), FadeIn(memo_i), FadeIn(memo_lbl), run_time=0.8)
            seg.wait_sentence(1)
            for nd in [f5, f4, f3, f2, f1a, f0a]:
                self.play(show(nd), run_time=0.45)
            self.play(mark(f1a, GREEN), mark(f0a, GREEN), run_time=0.3)
            seg.wait_sentence(2)
            tags = VGroup()
            # fib(2) = 1 -> memo[2]
            a, new, fly = save(2, 1, f2["mob"])
            t = value_tag(f2, 1, GREEN); tags.add(t)
            self.play(mark(f2, GREEN), FadeIn(t), a)
            self.remove(fly); self.add(new)
            # fib(3) memanggil fib(1) (kanan)
            self.play(show(f1b), run_time=0.4)
            self.play(mark(f1b, GREEN), run_time=0.2)
            a, new3, fly = save(3, 2, f3["mob"])
            t = value_tag(f3, 2, GREEN); tags.add(t)
            self.play(mark(f3, GREEN), FadeIn(t), a)
            self.remove(fly); self.add(new3)

        with self.say("s03_hit") as seg:
            # fib(4) -> fib(2) : memo hit
            self.play(show(f2b), run_time=0.5)
            hit1 = Indicate(memo[2], color=YELLOW, scale_factor=1.15)
            self.play(mark(f2b, YELLOW, "#2A2410"), hit1, run_time=0.8)
            a, new4, fly = save(4, 3, f4["mob"])
            t = value_tag(f4, 3, GREEN); tags.add(t)
            self.play(mark(f4, GREEN), FadeIn(t), a)
            self.remove(fly); self.add(new4)
            # fib(5) -> fib(3) : memo hit
            self.play(show(f3b), run_time=0.5)
            self.play(mark(f3b, YELLOW, "#2A2410"), Indicate(memo[3], color=YELLOW, scale_factor=1.15), run_time=0.8)
            a, new5, fly = save(5, 5, f5["mob"])
            t = value_tag(f5, 5, GREEN); tags.add(t)
            self.play(mark(f5, GREEN), FadeIn(t), a)
            self.remove(fly); self.add(new5)
            self.play(FadeIn(legend), run_time=0.4)
            seg.wait_sentence(1)
            # subtree yang tidak dihitung lagi: silang lalu hilang
            pruned = VGroup()
            gidx = [nd["id"] for nd in tree.subtree(f2b) + tree.subtree(f3b)]
            gboxes = VGroup(*[ghost.boxes[i] for i in gidx])
            gedges = VGroup(*[ghost.edges[i - 1] for i in gidx])
            pruned.add(gboxes, gedges)
            crosses = VGroup(*[Cross(ghost.boxes[i], stroke_color=RED, stroke_width=3).scale(0.6) for i in gidx])
            self.play(gboxes.animate.set_opacity(0.45), gedges.animate.set_opacity(0.45), run_time=0.4)
            self.play(LaggedStart(*[Create(cx) for cx in crosses], lag_ratio=0.1), run_time=1.0)
            seg.wait_sentence(2)
            self.play(*self.fade_out_anims(crosses, ghost), run_time=0.9)
            note = M("The same subproblems are <b>called</b>,\nbut <b>not calculated further</b>.", 22, FG)
            note.next_to(legend, DOWN, aligned_edge=LEFT, buff=0.4)
            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)

        with self.say("s03_complexity") as seg:
            before = M(c("O(2ⁿ)", RED), 34)
            arrow = Arrow(LEFT, RIGHT, color=MUTED).scale(0.45)
            after = M(c("O(n)", GREEN), 34)
            cmp_ = VGroup(before, arrow, after).arrange(RIGHT, buff=0.35)
            box = panel(cmp_.width + 0.6, cmp_.height + 0.5, color=PANEL_2)
            grp = VGroup(box, cmp_.move_to(box))
            grp.next_to(note, DOWN, aligned_edge=LEFT, buff=0.35)
            self.play(FadeIn(box), Write(before), run_time=0.8)
            self.play(GrowArrow(arrow), run_time=0.4)
            strike = Line(before.get_left(), before.get_right(), color=RED, stroke_width=5)
            self.play(Create(strike), FadeIn(after, shift=LEFT * 0.2), run_time=0.8)
            sub = T("each subproblem solved at most once", 20, MUTED).next_to(grp, DOWN, buff=0.2)
            self.play(FadeIn(sub), run_time=0.5)
        self.clear_scene()
