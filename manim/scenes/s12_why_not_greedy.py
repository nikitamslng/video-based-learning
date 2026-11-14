import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *

G = [-1, 3, -1, 4]


def state_box(txt, color, w=1.0, h=0.62, size=24):
    r = RoundedRectangle(corner_radius=0.1, width=w, height=h, fill_color=color, fill_opacity=0.18,
                         stroke_color=color, stroke_width=2.5)
    return VGroup(r, T(txt, size, FG, BOLD).move_to(r))


class S12WhyNotGreedy(LectureScene):
    def construct(self):
        bar = title_bar("Why Kadane's is DP and Not Greedy", "DP Identification")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        intro = T("Kadane satisfies both DP properties:", 28, MUTED).move_to([0, 2.15, 0])

        def card(title, color, body):
            box = panel(6.35, 4.1)
            chk = T("✓", 34, color, BOLD)
            t = T(title, 26, color, BOLD)
            head = VGroup(chk, t).arrange(RIGHT, buff=0.2).next_to(box.get_corner(UL), DR, buff=0.3)
            b = M(body, 20).next_to(head, DOWN, aligned_edge=LEFT, buff=0.25)
            if b.width > 5.8:
                b.scale_to_fit_width(5.8)
            return VGroup(box, head, b)

        c1 = card("Optimal substructure", GREEN,
                  "The optimal subarray ending at <i>i</i> is either <b>A[i]</b> alone,\n"
                  "or <b>A[i]</b> appended to the optimal subarray ending at\n<i>i</i> − 1. The subproblem solution "
                  "(best ending at <i>i</i> − 1)\nis <b>directly used</b>.")
        c2 = card("Overlapping subproblems", RED,
                  "If we naïvely asked <i>\"what is the best subarray ending\nat i?\"</i> for each <i>i</i>, and computed it "
                  "from scratch\neach time, we would <b>re-examine the same prefixes</b>.\nDP avoids this with "
                  + c("<b>dp[i−1]</b>", YELLOW) + " or " + c("<b>curr_max</b>", YELLOW) + ".")
        VGroup(c1, c2).arrange(RIGHT, buff=0.35).move_to([0, -0.4, 0])
        # visual kecil: rantai dp
        chain = VGroup(*[state_box(f"dp[{k}]", BLUE, 0.95, 0.5, 18) for k in range(1, 6)]).arrange(RIGHT, buff=0.18)
        chain.next_to(c2[2], DOWN, buff=0.35).set_x(c2.get_x())
        links = VGroup(*[Arrow(chain[k].get_right(), chain[k + 1].get_left(), buff=0.02, color=YELLOW,
                               stroke_width=3, tip_length=0.1) for k in range(4)])
        opt = VGroup(state_box("A[i]", ORANGE, 1.0, 0.5, 18), T("or", 20, MUTED),
                     state_box("best(i−1)", BLUE, 1.6, 0.5, 18), T("+", 22, MUTED), state_box("A[i]", ORANGE, 1.0, 0.5, 18))
        opt.arrange(RIGHT, buff=0.15).next_to(c1[2], DOWN, buff=0.35).set_x(c1.get_x())

        with self.say("s12_props") as seg:
            seg.wait_sentence(1)
            self.play(FadeIn(intro), run_time=0.6)
            seg.wait_sentence(2)
            self.play(FadeIn(c1, shift=UP * 0.2), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(o) for o in opt], lag_ratio=0.2), run_time=1.0)
            seg.wait_sentence(3)
            self.play(Indicate(opt[2], color=GREEN), run_time=0.8)
        with self.say("s12_overlap") as seg:
            self.play(FadeIn(c2, shift=UP * 0.2), run_time=0.8)
            seg.wait_sentence(1)
            self.play(LaggedStart(*[FadeIn(x) for x in chain], lag_ratio=0.15), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.2), run_time=1.0)
        self.clear_scene()

        # ------------------------------------------------ greedy vs kadane
        bar2 = title_bar("Why Kadane's is DP and Not Greedy", "Why Not Greedy")
        self.play(FadeIn(bar2, shift=RIGHT * 0.3), run_time=0.5)
        rule_t = M("Greedy rule (single pass, fixed rule):  <b>take elements while positive; reset on negative</b>", 24)
        rule_b = panel(rule_t.width + 0.6, rule_t.height + 0.4, color=PANEL_2, stroke=ORANGE)
        rule = VGroup(rule_b, rule_t.move_to(rule_b)).move_to([0, 2.05, 0])
        arr = ArrayRow(G, cell=1.0, size=34).move_to([0.6, 0.85, 0])
        al = M("A =", 30).next_to(arr.cells, LEFT, buff=0.3)
        with self.say("s12_greedy") as seg:
            seg.wait_sentence(1)
            self.play(FadeIn(rule, shift=DOWN * 0.1), run_time=0.8)
            seg.wait_sentence(2)
            self.play(FadeIn(al), LaggedStart(*[FadeIn(VGroup(arr.cells[k], arr.vals[k], arr.idx[k]))
                                                for k in range(4)], lag_ratio=0.2), run_time=1.0)

        gy = -0.75
        ky = -1.95
        g_lab = T("Greedy", 26, ORANGE, BOLD).move_to([arr.cells[0].get_x() - 2.05, gy, 0])
        k_lab = T("Kadane", 26, GREEN, BOLD).move_to([arr.cells[0].get_x() - 2.05, ky, 0])
        g_states = ["reset", "3", "reset", "4"]
        k_states = ["−1", "3", "2", "6"]
        with self.say("s12_fail") as seg:
            self.play(FadeIn(g_lab), run_time=0.4)
            gb = []
            for k in range(3):
                col = RED if g_states[k] == "reset" else ORANGE
                b = state_box(g_states[k], col, 0.95, 0.6, 20 if g_states[k] == "reset" else 26)
                b.move_to([arr.cells[k].get_x(), gy, 0])
                gb.append(b)
                self.play(Indicate(arr.cells[k], color=col), FadeIn(b, shift=DOWN * 0.1), run_time=0.6)
            seg.wait_sentence(1)
            b = state_box("4", ORANGE, 0.95, 0.6, 26).move_to([arr.cells[3].get_x(), gy, 0])
            self.play(Indicate(arr.cells[3], color=ORANGE), FadeIn(b, shift=DOWN * 0.1), run_time=0.6)
            gb.append(b)
            seg.wait_sentence(2)
            gres = M("best = " + c("<b>4</b>", RED) + "  ✗", 28).next_to(gb[3], RIGHT, buff=0.5)
            self.play(FadeIn(gres), run_time=0.5)
            seg.wait_sentence(3)
            miss = arr.window(1, 3, GREEN, width=5)
            miss_t = M("[3, −1, 4] = " + c("<b>6</b>", GREEN), 26).next_to(arr, UP, buff=0.15)
            self.play(Create(DashedVMobject(miss, num_dashes=40)), FadeIn(miss_t), FadeOut(rule), run_time=0.9)
            seg.wait_sentence(4)
            self.play(Indicate(gb[2], color=RED, scale_factor=1.2), run_time=0.8)

        with self.say("s12_kadane") as seg:
            self.play(FadeIn(k_lab), run_time=0.4)
            kb = []
            for k in range(2):
                b = state_box(k_states[k], BLUE if k else BLUE, 0.95, 0.6, 26).move_to([arr.cells[k].get_x(), ky, 0])
                kb.append(b)
                self.play(FadeIn(b, shift=DOWN * 0.1), run_time=0.4)
            seg.wait_sentence(1)
            b = state_box("2", BLUE, 0.95, 0.6, 26).move_to([arr.cells[2].get_x(), ky, 0])
            note = M("3 + (−1) = 2  &gt;  −1  → <b>extend</b>", 22, BLUE).next_to(b, DOWN, buff=0.12)
            self.play(FadeIn(b, shift=DOWN * 0.1), FadeIn(note), run_time=0.7)
            kb.append(b)
            seg.wait_sentence(2)
            b = state_box("6", GREEN, 0.95, 0.6, 26).move_to([arr.cells[3].get_x(), ky, 0])
            kres = M("best = " + c("<b>6</b>", GREEN) + "  ✓", 28).next_to(b, RIGHT, buff=0.5)
            self.play(FadeIn(b, shift=DOWN * 0.1), FadeIn(kres), run_time=0.7)
            kb.append(b)
            seg.wait_sentence(3)
            arrows = VGroup(*[CurvedArrow(kb[k].get_top(), kb[k + 1].get_top(), angle=-TAU / 5, color=YELLOW,
                                          tip_length=0.12) for k in range(3)])
            self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.3), run_time=1.2)
            lab = M("decision at each step (extend / restart) based on " + c("<b>dp[i−1]</b>", YELLOW), 22)
            lab.next_to(arrows, UP, buff=0.05).set_x(1.3)
            self.play(FadeOut(note), run_time=0.2)
            self.play(FadeIn(lab), run_time=0.5)
        self.clear_scene()

        # ------------------------------------------------ tabel DP vs Greedy
        bar3 = title_bar("Why Kadane's is DP and Not Greedy", "DP vs Greedy")
        self.play(FadeIn(bar3, shift=RIGHT * 0.3), run_time=0.5)
        rows = [
            ["Property", "Greedy", "Dynamic Programming"],
            ["How it decides?", "Uses only raw input data/heuristic\navailable right now/at current step",
             "Uses previously computed\nsubproblem states"],
            ["Decision Pipeline", "Makes a choice before\nsolving subproblems",
             "Makes a choice after evaluating\nprevious subproblems"],
            ["Can it look back?", "No. It makes a choice and never revisits\nor relies on a calculated state table.",
             "Yes. It must read from the table/state of a solved\nsubproblem to make the current calculation."],
            ["Examples", "Activity Selection, Fractional Knapsack,\nHuffman Code, Dijkstra",
             "Max Subarray Sum, 0/1 Knapsack,\nCoin Change (Non Canonical)"],
        ]
        tbl = grid_table(rows, [3.0, 5.15, 5.15], row_height=0.6, size=21).move_to([0, -0.2, 0])
        for r in range(1, 5):
            tbl.cells_map[(r, 1)][1].set_color("#FED7AA")
            tbl.cells_map[(r, 2)][1].set_color("#BBF7D0")
        with self.say("s12_table") as seg:
            self.play(FadeIn(row_of(tbl, 0, 3), shift=DOWN * 0.1), run_time=0.6)
            for r in range(1, 4):
                seg.wait_sentence(r)
                self.play(FadeIn(row_of(tbl, r, 3), shift=UP * 0.1), run_time=0.7)
        with self.say("s12_examples") as seg:
            self.play(FadeIn(tbl.cells_map[(4, 0)]), FadeIn(tbl.cells_map[(4, 1)], shift=UP * 0.1), run_time=0.7)
            seg.wait_sentence(1)
            self.play(FadeIn(tbl.cells_map[(4, 2)], shift=UP * 0.1), run_time=0.7)
            self.play(Indicate(tbl.cells_map[(4, 2)][1], color=GREEN, scale_factor=1.05), run_time=0.8)
        self.clear_scene()
