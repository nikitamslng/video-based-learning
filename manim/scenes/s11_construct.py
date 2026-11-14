import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *

CONSTRUCT = [
    "KADANE-CONSTRUCT(A)",
    "n = A.length",
    "curr_max = A[1]",
    "global_max = A[1]",
    "start = 1; end = 1; temp_start = 1",
    "for i = 2 to n",
    "    if A[i] > curr_max + A[i]",
    "        curr_max = A[i]",
    "        temp_start = i",
    "    else curr_max = curr_max + A[i]",
    "    if curr_max > global_max",
    "        global_max = curr_max",
    "        start = temp_start",
    "        end = i",
    "return A[start..end] with sum global_max",
]
A = [-2, 1, -3, 4, -1, 2, 1]


def trace(arr):
    """Hasil trace KADANE-CONSTRUCT yang benar (dipakai untuk tabel)."""
    rows = []
    curr = g = arr[0]
    start = end = ts = 0
    rows.append(dict(i="", el=arr[0], f="Initialization", curr=f"{curr}", g=f"{g}", ts=ts, s=start, e=end))
    for i in range(1, len(arr)):
        ai = arr[i]
        a_txt = f"({ai})" if ai < 0 else f"{ai}"
        reset = ai > curr + ai
        f = f"max({ai}, {curr} + {a_txt}) = {max(ai, curr + ai)}"
        if reset:
            curr, ts = ai, i
        else:
            curr = curr + ai
        up = curr > g
        if up:
            g, start, end = curr, ts, i
        rows.append(dict(i=str(i + 1), el=ai, f=f, curr=f"{curr}" + (" (reset)" if reset else ""),
                         g=f"{g}" + (" (UP)" if up else ""), ts=ts, s=start, e=end))
    return rows


def fmt(x):
    return str(x).replace("-", "−")


class S11Construct(LectureScene):
    def construct(self):
        bar = title_bar("Maximum Subarray Sum: Kadane's Algorithm",
                        "Step 4 – Construct the Solution: Tracking Indices")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        arr9 = ArrayRow([-2, 1, -3, 4, -1, 2, 1, -5, 4], cell=0.8, size=28).move_to([0, 1.1, 0])
        got = M("We have got the optimal value:  " + c("<b>global_max = 6</b>", GREEN), 28).move_to([0, 2.15, 0])
        q = M("<b>Now, from which subarray does the solution come from?</b>", 28, YELLOW).move_to([0, -0.4, 0])
        with self.say("s11_question") as seg:
            self.play(FadeIn(got), FadeIn(arr9), run_time=0.8)
            seg.wait_sentence(1)
            qm = VGroup(*[T("?", 26, YELLOW, BOLD).next_to(arr9.cells[k], UP, buff=0.12) for k in range(9)])
            self.play(Write(q), LaggedStart(*[FadeIn(x) for x in qm], lag_ratio=0.08), run_time=1.4)
            seg.wait_sentence(2)
            idx = M("→ we need the <b>indices</b>: track index boundaries when values change", 24).next_to(q, DOWN, buff=0.35)
            self.play(FadeIn(idx, shift=UP * 0.1), run_time=0.6)
            sb = arr9.window(3, 6, GREEN, width=6)
            st_ = T("start", 20, GREEN, BOLD).next_to(arr9.idx[3], DOWN, buff=0.1)
            en_ = T("end", 20, GREEN, BOLD).next_to(arr9.idx[6], DOWN, buff=0.1)
            self.play(FadeOut(qm), Create(sb), FadeIn(st_), FadeIn(en_), run_time=0.8)
        self.fade_all_except(bar, run_time=0.5)

        with self.say("s11_rules") as seg:
            def rule(title, color, body):
                box = panel(6.3, 2.6)
                t = T(title, 28, color, BOLD).next_to(box.get_corner(UL), DR, buff=0.3)
                b = M(body, 22).next_to(t, DOWN, aligned_edge=LEFT, buff=0.25)
                return VGroup(box, t, b)
            r1 = rule("Expansion Rule", BLUE, "If <b>curr_max</b> resets,\nthe start boundary shifts to the current index.\n\n"
                      + c("temp_start = i", BLUE))
            r2 = rule("Global Rule", GREEN, "If a new <b>global maximum</b> is achieved,\nupdate start and end permanently.\n\n"
                      + c("start = temp_start;  end = i", GREEN))
            VGroup(r1, r2).arrange(RIGHT, buff=0.35).move_to([0, 0, 0])
            seg.wait_sentence(1)
            self.play(FadeIn(r1, shift=UP * 0.2), run_time=0.8)
            seg.wait_sentence(2)
            self.play(FadeIn(r2, shift=UP * 0.2), run_time=0.8)
        self.fade_all_except(bar, run_time=0.5)

        code = CodePanel(CONSTRUCT, size=18).move_to([0, -0.1, 0])
        with self.say("s11_code") as seg:
            self.play(FadeIn(code, shift=UP * 0.2), run_time=0.8)
            seg.wait_sentence(1)
            hl = code.highlight_box(4, YELLOW)
            self.play(FadeIn(hl), run_time=0.4)
            seg.wait_sentence(2)
            self.play(hl.animate.become(code.lines_box(6, 8, BLUE)), run_time=0.4)
            seg.wait_sentence(3)
            self.play(hl.animate.become(code.lines_box(10, 13, GREEN)), run_time=0.4)
        self.fade_all_except(bar, run_time=0.5)

        # ------------------------------------------------ trace table
        bar2 = title_bar("Maximum Subarray Sum: Kadane's Algorithm", "Trace on Array = [−2, 1, −3, 4, −1, 2, 1]")
        self.play(Transform(bar, bar2), run_time=0.5)
        arr = ArrayRow(A, cell=0.62, size=24).move_to([-2.2, 1.95, 0])
        leg = VGroup(M(c("▢", BLUE) + " current  A[temp_start..i]", 18, MUTED),
                     M(c("▢", GREEN) + " best  A[start..end]", 18, MUTED)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        leg.next_to(arr, RIGHT, buff=0.6)
        rows = trace(A)
        data = [["i", "Element", "Formula", "curr_max", "global_max", "Subarray Tracked"]]
        for r in rows:
            sub = "[" + ", ".join(fmt(x) for x in A[r["ts"]:(int(r["i"]) if r["i"] else 1)]) + "]"
            data.append([r["i"], fmt(r["el"]), fmt(r["f"]), fmt(r["curr"]), fmt(r["g"]), sub])
        tbl = grid_table(data, [0.7, 1.35, 4.1, 2.0, 2.0, 2.75], row_height=0.47, size=20, first_col_bold=False)
        tbl.move_to([0, -0.85, 0])
        for (rr, cc), cell in tbl.cells_map.items():
            if rr > 0 and cc == 2:
                cell[1].become(Text(data[rr][2], font=MONO, font_size=17, color=FG).move_to(cell[0]))
            if rr > 0 and ("UP" in data[rr][cc] or "reset" in data[rr][cc]):
                cell[1].set_color(GREEN if "UP" in data[rr][cc] else BLUE)

        cur = arr.window(0, 0, BLUE, width=4)
        best = arr.window(0, 0, GREEN, width=7, buff=0.11)

        def show_row(r, rt=1.2):
            st = rows[r]
            k = int(st["i"]) - 1 if st["i"] else 0
            self.play(FadeIn(row_of(tbl, r + 1, 6), shift=UP * 0.1),
                      cur.animate.become(arr.window(st["ts"], k, BLUE, width=4)), run_time=rt * 0.5)
            if best_state["s"] != (st["s"], st["e"]):
                best_state["s"] = (st["s"], st["e"])
                self.play(best.animate.become(arr.window(st["s"], st["e"], GREEN, width=7, buff=0.11)),
                          Indicate(tbl.cells_map[(r + 1, 4)][1], color=GREEN), run_time=rt * 0.5)

        best_state = {"s": (0, 0)}
        with self.say("s11_init") as seg:
            self.play(FadeIn(arr), FadeIn(leg), FadeIn(row_of(tbl, 0, 6)), run_time=0.8)
            seg.wait_sentence(1)
            self.play(FadeIn(row_of(tbl, 1, 6), shift=UP * 0.1), Create(cur), Create(best), run_time=0.8)

        with self.say("s11_i23") as seg:
            show_row(1, 1.6)
            seg.wait_sentence(2)
            show_row(2, 1.6)
        with self.say("s11_i45") as seg:
            show_row(3, 1.6)
            seg.wait_sentence(2)
            show_row(4, 1.6)
        with self.say("s11_i67") as seg:
            show_row(5, 1.6)
            seg.wait_sentence(1)
            show_row(6, 1.6)
            seg.wait_sentence(2)
            res = pill("start = 4, end = 7  →  [4, −1, 2, 1],  sum = 6", GREEN, 20)
            res.scale_to_fit_width(min(res.width, 6.2)).next_to(arr, RIGHT, buff=0.5)
            self.play(FadeOut(leg), run_time=0.3)
            self.play(FadeIn(res, scale=0.9), Indicate(best, color=GREEN), run_time=0.9)
        self.clear_scene()
