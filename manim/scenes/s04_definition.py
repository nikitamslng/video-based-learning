import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # noqa: E401,E702
from lecture import *


def node(label, color=BLUE, w=0.9, h=0.42, size=18):
    r = RoundedRectangle(corner_radius=0.1, width=w, height=h, fill_color=PANEL_2, fill_opacity=1,
                         stroke_color=color, stroke_width=2.5)
    return VGroup(r, T(label, size, FG).move_to(r))


def link(a, b, color=MUTED):
    return Arrow(a.get_bottom(), b.get_top(), buff=0.05, stroke_width=2.5, color=color,
                 max_tip_length_to_length_ratio=0.15, tip_length=0.12)


class S04Definition(LectureScene):
    def construct(self):
        bar = title_bar("Dynamic Programming Paradigm", "Definition")
        self.play(FadeIn(bar, shift=RIGHT * 0.3), run_time=0.6)

        # ------------------------------------------------ definisi
        d_txt = M("<b>Dynamic Programming (DP)</b> is an algorithm design technique for solving problems\n"
                  "with " + c("overlapping subproblems", RED) + " and " + c("optimal substructure", GREEN)
                  + " by " + c("<b>storing intermediate results</b>", YELLOW) + ".", 25)
        if d_txt.width > 12.6:
            d_txt.scale_to_fit_width(12.6)
        d_box = panel(d_txt.width + 0.8, d_txt.height + 0.55, color=PANEL_2, stroke=BLUE)
        definition = VGroup(d_box, d_txt.move_to(d_box)).move_to([0, 1.85, 0])
        with self.say("s04_def") as seg:
            self.play(FadeIn(d_box), Write(d_txt), run_time=2.5)
            seg.wait_sentence(0, 4.0)
            self.play(Indicate(d_txt, color=YELLOW, scale_factor=1.02), run_time=1.0)

        # ------------------------------------------------ dua syarat
        def prop_card(title, color, body, icon):
            t = T(title, 26, color, BOLD)
            b = M(body, 21, FG)
            box = panel(6.3, 3.0)
            t.next_to(box.get_corner(UL), DR, buff=0.3)
            b.next_to(t, DOWN, aligned_edge=LEFT, buff=0.2)
            icon.next_to(b, DOWN, buff=0.25).set_x(box.get_x())
            return VGroup(box, t, b, icon)

        # ikon optimal substructure: solusi besar memuat solusi optimal sub-masalah
        big = RoundedRectangle(corner_radius=0.12, width=3.4, height=0.95, stroke_color=GREEN, stroke_width=3)
        s1 = RoundedRectangle(corner_radius=0.08, width=1.35, height=0.55, stroke_color=GREEN, fill_color=GREEN,
                              fill_opacity=0.25).move_to(big).shift(LEFT * 0.75)
        s2 = s1.copy().shift(RIGHT * 1.5)
        lbl1 = T("opt sub", 16, FG).move_to(s1)
        lbl2 = T("opt sub", 16, FG).move_to(s2)
        icon1 = VGroup(big, s1, s2, lbl1, lbl2)
        # ikon overlapping: dua parent menunjuk sub-masalah yang sama
        p1, p2 = node("fib(4)", MUTED), node("fib(5)", MUTED)
        VGroup(p2, p1).arrange(RIGHT, buff=1.6)
        ch = node("fib(3)", RED).next_to(VGroup(p1, p2), DOWN, buff=0.5)
        icon2 = VGroup(p1, p2, ch, link(p1, ch, RED), link(p2, ch, RED))

        card1 = prop_card("Optimal substructure", GREEN,
                          "The optimal solution to the problem\ncontains optimal solutions to subproblems.", icon1)
        card2 = prop_card("Overlapping subproblems", RED,
                          "The same subproblems are solved\nrepeatedly in a naïve recursive solution.", icon2)
        cards = VGroup(card1, card2).arrange(RIGHT, buff=0.4).move_to([0, -0.85, 0])
        when = T("DP is applicable when:", 24, MUTED).next_to(cards, UP, aligned_edge=LEFT, buff=0.18)

        with self.say("s04_props") as seg:
            self.play(definition.animate.scale(0.82).move_to([0, 2.0, 0]), FadeIn(when), run_time=0.7)
            seg.wait_sentence(1)
            self.play(FadeIn(card1[0]), FadeIn(card1[1:3], shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(big), GrowFromCenter(s1), GrowFromCenter(s2), FadeIn(lbl1), FadeIn(lbl2), run_time=0.9)
            seg.wait_sentence(2)
            self.play(FadeIn(card2[0]), FadeIn(card2[1:3], shift=UP * 0.1), run_time=0.7)
            self.play(FadeIn(p1), FadeIn(p2), run_time=0.4)
            self.play(GrowArrow(icon2[3]), GrowArrow(icon2[4]), FadeIn(ch), run_time=0.8)
            self.play(Indicate(ch, color=RED), run_time=0.8)

        # ------------------------------------------------ kontras D&C / DP / Greedy
        with self.say("s04_contrast") as seg:
            self.fade_out(cards, when)

            def column(title, color, caption, diagram):
                t = T(title, 24, color, BOLD)
                cap = M(caption, 19, MUTED)
                box = panel(4.2, 4.85)
                t.next_to(box.get_top(), DOWN, buff=0.28)
                diagram.move_to(box).shift(UP * 0.15)
                cap.next_to(box.get_bottom(), UP, buff=0.25)
                return VGroup(box, t, diagram, cap)

            # D&C: subtree yang terpisah (independen)
            r = node("P", BLUE)
            a, b = node("P₁", BLUE), node("P₂", PURPLE)
            VGroup(a, b).arrange(RIGHT, buff=0.9).next_to(r, DOWN, buff=0.45)
            a1, a2 = node("P₁₁", BLUE, 0.75), node("P₁₂", BLUE, 0.75)
            b1, b2 = node("P₂₁", PURPLE, 0.75), node("P₂₂", PURPLE, 0.75)
            VGroup(a1, a2).arrange(RIGHT, buff=0.15).next_to(a, DOWN, buff=0.45)
            VGroup(b1, b2).arrange(RIGHT, buff=0.15).next_to(b, DOWN, buff=0.45)
            dc = VGroup(r, a, b, a1, a2, b1, b2, link(r, a), link(r, b), link(a, a1), link(a, a2), link(b, b1), link(b, b2))
            # DP: DAG dengan sub-masalah yang dibagi bersama + tabel
            r2 = node("f(4)", GREEN)
            x1, x2 = node("f(3)", GREEN), node("f(2)", YELLOW)
            VGroup(x1, x2).arrange(RIGHT, buff=0.9).next_to(r2, DOWN, buff=0.45)
            x3 = node("f(1)", GREEN).next_to(x1, DOWN, buff=0.45)
            dp_ = VGroup(r2, x1, x2, x3, link(r2, x1), link(r2, x2), link(x1, x3),
                         Arrow(x1.get_bottom(), x2.get_left() + DOWN * 0.05, buff=0.05, color=YELLOW, stroke_width=2.5,
                               tip_length=0.12).shift(RIGHT * 0.25),
                         link(x2, x3, MUTED))
            memo = VGroup(*[Square(0.38, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW, fill_opacity=0.15)
                            for _ in range(5)]).arrange(RIGHT, buff=0).next_to(x3, RIGHT, buff=0.35)
            dp_.add(memo)
            # Greedy: satu pilihan per langkah, tanpa evaluasi ulang
            g0 = node("start", ORANGE)
            g1, g1b, g1c = node("c₁", ORANGE, 0.6), node("c₂", MUTED, 0.6), node("c₃", MUTED, 0.6)
            VGroup(g1, g1b, g1c).arrange(RIGHT, buff=0.3).next_to(g0, DOWN, buff=0.45)
            g2, g2b = node("c₄", ORANGE, 0.6), node("c₅", MUTED, 0.6)
            VGroup(g2, g2b).arrange(RIGHT, buff=0.3).next_to(g1, DOWN, buff=0.45)
            g2.align_to(g1, LEFT)
            gr = VGroup(g0, g1, g1b, g1c, g2, g2b, link(g0, g1, ORANGE), link(g0, g1b), link(g0, g1c),
                        link(g1, g2, ORANGE), link(g1, g2b))
            for m_ in (g1b, g1c, g2b):
                m_.set_opacity(0.4)

            col1 = column("Divide & Conquer", BLUE, "<b>independent</b> subproblems", dc)
            col2 = column("Dynamic Programming", GREEN, "<b>overlapping</b> subproblems,\nresults stored &amp; reused", dp_)
            col3 = column("Greedy", ORANGE, "<b>single greedy choice</b> +\noptimal substructure,\nno re-evaluation", gr)
            cols = VGroup(col1, col2, col3).arrange(RIGHT, buff=0.3).move_to([0, -0.15, 0])
            self.fade_out(definition, run_time=0.5)
            self.play(FadeIn(col2[0]), FadeIn(col2[1]), FadeIn(col2[2]), FadeIn(col2[3]), run_time=0.8)
            self.play(FadeIn(col1[0]), FadeIn(col1[1]), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(m) for m in col1[2]], lag_ratio=0.05), FadeIn(col1[3]), run_time=1.2)
            seg.wait_sentence(1)
            self.play(FadeIn(col3[0]), FadeIn(col3[1]), run_time=0.4)
            seg.wait_sentence(2)
            self.play(LaggedStart(*[FadeIn(m) for m in col3[2]], lag_ratio=0.05), FadeIn(col3[3]), run_time=1.4)
            self.play(Indicate(VGroup(g1, g2), color=ORANGE), run_time=0.8)
        self.clear_scene()
