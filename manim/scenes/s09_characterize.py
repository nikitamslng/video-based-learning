import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *

A = [-2, 1, -3, 4, -1, 2, 1, -5, 4]


def glyphs(mob, text, sub, occ=0):
    """Ambil glyph dari Text/MarkupText untuk substring `sub` (spasi tidak dihitung)."""
    flat = text.replace(" ", "")
    s = sub.replace(" ", "")
    start = -1
    for _ in range(occ + 1):
        start = flat.find(s, start + 1)
    return VGroup(*mob.submobjects[start:start + len(s)])


def sym_cells(labels, colors, cell=1.05, size=22):
    g = VGroup()
    for lab, col in zip(labels, colors):
        sq = Square(cell, stroke_color=BORDER if col is None else col, stroke_width=2.5,
                    fill_color=PANEL if col is None else col, fill_opacity=1 if col is None else 0.25)
        t = T(lab, size, FG if col else MUTED).move_to(sq)
        g.add(VGroup(sq, t))
    g.arrange(RIGHT, buff=0)
    return g


class S09Characterize(LectureScene):
    def construct(self):
        bar = title_bar("Maximum Subarray Sum: Kadane's Algorithm",
                        "Step 1 – Characterize the Structure: Optimal Substructure")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        d = M(c("<b>Subproblem definition:</b>", BLUE) + "  let " + c("<b>dp[i]</b>", YELLOW)
              + " be the maximum subarray sum ending <b>exactly</b> at index <i>i</i>.", 26)
        if d.width > 12.6:
            d.scale_to_fit_width(12.6)
        dbox = panel(d.width + 0.7, d.height + 0.5, color=PANEL_2, stroke=BLUE)
        definition = VGroup(dbox, d.move_to(dbox)).move_to([0, 2.0, 0])

        arr = ArrayRow(A, cell=0.82, size=28).move_to([0, 0.35, 0])
        i = 5  # index ke-6
        ptr = Arrow(arr.cells[i].get_top() + UP * 0.6, arr.cells[i].get_top(), buff=0.05, color=YELLOW)
        ptr_l = M(c("<i>i</i> = 6", YELLOW), 24).next_to(ptr, UP, buff=0.05)

        with self.say("s09_def") as seg:
            self.play(FadeIn(dbox), Write(d), run_time=1.6)
            self.play(FadeIn(arr), GrowArrow(ptr), FadeIn(ptr_l), run_time=0.8)
            seg.wait_sentence(1, 0.8)
            win = arr.window(i, i, BLUE)
            val = T("", 26, BLUE)
            self.play(Create(win), run_time=0.4)
            best = None
            for s in range(i, -1, -1):
                tot = sum(A[s:i + 1])
                nv = M(f"sum A[{s+1}..6] = {tot}", 26, FG).move_to([0, -1.05, 0])
                self.play(win.animate.become(arr.window(s, i, BLUE)), FadeOut(val), FadeIn(nv), run_time=0.45)
                val = nv
                self.wait(0.15)
                if best is None or tot > best[0]:
                    best = (tot, s)
            res = M(c("dp[6] = 5", YELLOW) + "  → best subarray ending at 6 is [4, −1, 2]", 26).move_to([0, -1.05, 0])
            self.play(win.animate.become(arr.window(best[1], i, YELLOW)), FadeOut(val), FadeIn(res), run_time=0.7)

        # ------------------------------------------------ dua opsi
        with self.say("s09_options") as seg:
            self.play(*self.fade_out_anims(arr, ptr, ptr_l, win, res),
                      definition.animate.scale(0.85).move_to([0, 2.1, 0]), run_time=0.7)
            intro = M("<b>The structural choice:</b> any optimal subarray ending at <i>i</i> must choose between two options:", 24, FG)
            intro.scale_to_fit_width(min(intro.width, 12.8)).move_to([0, 1.3, 0])
            self.play(FadeIn(intro), run_time=0.6)

            def option(title, color, cells, bracket_from, label, result):
                box = panel(6.35, 3.45)
                t = T(title, 25, color, BOLD).next_to(box.get_corner(UL), DR, buff=0.25)
                cells.next_to(t, DOWN, buff=0.35).set_x(box.get_x())
                br = Brace(VGroup(*cells[bracket_from[0]:bracket_from[1] + 1]), DOWN, color=BLUE, buff=0.08)
                bl = M(label, 18, MUTED).next_to(br, DOWN, buff=0.06)
                r = M(result, 24)
                rb = RoundedRectangle(corner_radius=0.1, width=r.width + 0.4, height=r.height + 0.25,
                                      fill_color=BG, fill_opacity=1, stroke_color=color, stroke_width=2)
                res = VGroup(rb, r.move_to(rb)).next_to(box.get_bottom(), UP, buff=0.2)
                return VGroup(box, t, cells, br, bl, res)

            labs = ["…", "A[i−3]", "A[i−2]", "A[i−1]", "A[i]"]
            ca = sym_cells(labs, [None, BLUE, BLUE, BLUE, ORANGE], size=18)
            cb = sym_cells(labs, [None, None, None, None, ORANGE], size=18)
            optA = option("Option A — Extend", BLUE, ca, (1, 3), "dp[i−1] = best ending at i−1",
                          c("dp[i−1]", BLUE) + " + " + c("A[i]", ORANGE))
            optB = option("Option B — Start new", GREEN, cb, (4, 4), "brand-new subarray at i",
                          c("A[i]", ORANGE) + "   if Option A gives a lower value")
            optB[3].set_color(ORANGE)
            VGroup(optA, optB).arrange(RIGHT, buff=0.35).move_to([0, -0.85, 0])
            seg.wait_sentence(1)
            self.play(FadeIn(optA[0]), FadeIn(optA[1]), LaggedStart(*[FadeIn(x) for x in optA[2]], lag_ratio=0.1),
                      run_time=0.9)
            self.play(GrowFromCenter(optA[3]), FadeIn(optA[4]), run_time=0.6)
            self.play(Write(optA[5]), run_time=0.8)
            seg.wait_sentence(2)
            self.play(FadeIn(optB[0]), FadeIn(optB[1]), LaggedStart(*[FadeIn(x) for x in optB[2]], lag_ratio=0.1),
                      run_time=0.9)
            self.play(GrowFromCenter(optB[3]), FadeIn(optB[4]), run_time=0.6)
            self.play(Write(optB[5]), run_time=0.8)

        with self.say("s09_theorem") as seg:
            th = M(c("<b>The Theorem:</b>", BLUE) + " an optimal solution to the subproblem at index <i>i</i>\n"
                   "contains within it the optimal solution to the subproblem at index <i>i</i> − 1.", 24)
            tb = panel(th.width + 0.6, th.height + 0.4, color="#0F2A22", stroke=GREEN)
            theorem = VGroup(tb, th.move_to(tb)).move_to([0, -0.85, 0])
            self.play(*self.fade_out_anims(optB, intro), optA.animate.scale(0.8).move_to([0, 0.45, 0]), run_time=0.8)
            theorem.next_to(optA, DOWN, buff=0.3)
            self.play(FadeIn(theorem, shift=UP * 0.15), run_time=0.8)
            seg.wait_sentence(1)
            tag = pill("= OPTIMAL SUBSTRUCTURE", GREEN, 22).next_to(theorem, DOWN, buff=0.18)
            self.play(FadeIn(tag, scale=0.8), Indicate(optA[3], color=GREEN), run_time=0.9)
        self.clear_scene()

        # ------------------------------------------------ Step 2: recurrence
        bar2 = title_bar("Maximum Subarray Sum: Kadane's Algorithm",
                         "Step 2 – Define Optimal Solution Recursively: Recurrence Relation")
        self.play(FadeIn(bar2, shift=RIGHT * 0.3), run_time=0.5)
        ftxt = "dp[i] = max( A[i] , dp[i−1] + A[i] )"
        f = Text(ftxt, font=MONO, font_size=46, color=FG, weight=BOLD)
        f.move_to([0, 1.35, 0])
        glyphs(f, ftxt, "dp[i]").set_color(YELLOW)
        g_start = glyphs(f, ftxt, "A[i]", 0)
        g_ext = glyphs(f, ftxt, "dp[i−1] + A[i]")
        g_start.set_color(GREEN)
        g_ext.set_color(BLUE)
        b1 = Brace(g_start, DOWN, color=GREEN)
        b1t = T("start new\n(Option B)", 22, GREEN).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(g_ext, DOWN, color=BLUE)
        b2t = T("extend\n(Option A)", 22, BLUE).next_to(b2, DOWN, buff=0.1)
        mdef = M(c("<b>Mathematical definition:</b>", BLUE) + " define the value of an optimal solution recursively"
                 " based on our two structural options:", 22, FG)
        mdef.scale_to_fit_width(min(mdef.width, 12.8)).move_to([0, 2.25, 0])
        with self.say("s09_recurrence") as seg:
            self.play(FadeIn(mdef), run_time=0.6)
            seg.wait_sentence(1)
            self.play(Write(f), run_time=2.0)
            seg.wait_sentence(2)
            self.play(GrowFromCenter(b1), FadeIn(b1t), run_time=0.6)
            self.play(GrowFromCenter(b2), FadeIn(b2t), run_time=0.6)

        with self.say("s09_base") as seg:
            base = M(c("<b>Base case:</b>", BLUE) + "\ncannot look back before the first element", 22)
            base_f = Text("dp[1] = A[1]", font=MONO, font_size=36, color=YELLOW, weight=BOLD)
            gm = M(c("<b>Global maximum:</b>", BLUE) + "\nthe maximum subarray sum can end anywhere", 22)
            gm_f = M("<b>GlobalMax</b> = max<sub>1 ≤ i ≤ n</sub> " + c("<b>dp[i]</b>", YELLOW), 34)
            left = VGroup(base, base_f).arrange(DOWN, buff=0.3)
            right = VGroup(gm, gm_f).arrange(DOWN, buff=0.3)
            lb = panel(6.3, 2.0)
            rb = panel(6.3, 2.0)
            VGroup(lb, rb).arrange(RIGHT, buff=0.35).move_to([0, -1.6, 0])
            left.move_to(lb)
            right.move_to(rb)
            for m_ in (base, gm):
                if m_.width > 6.0:
                    m_.scale_to_fit_width(6.0)
            self.play(FadeIn(lb), FadeIn(base), run_time=0.6)
            self.play(Write(base_f), run_time=0.8)
            seg.wait_sentence(1)
            self.play(FadeIn(rb), FadeIn(gm), run_time=0.6)
            self.play(Write(gm_f), run_time=1.0)
        self.clear_scene()
