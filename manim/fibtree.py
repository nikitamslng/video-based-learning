"""Recursion tree untuk FIB(n) — dipakai di S02 (naive) dan S03 (memoization)."""
from lecture import *


class FibTree(VGroup):
    def __init__(self, n=5, leaf_dx=1.08, level_dy=1.02, size=20, **kw):
        super().__init__(**kw)
        self.nodes = []  # preorder (= urutan pemanggilan)
        counter = [0]

        def rec(k, depth, parent):
            node = {"n": k, "depth": depth, "parent": parent, "children": [], "id": len(self.nodes)}
            self.nodes.append(node)
            if k <= 1:
                node["x"] = counter[0]
                counter[0] += 1
            else:
                node["children"] = [rec(k - 1, depth + 1, node), rec(k - 2, depth + 1, node)]
                node["x"] = sum(ch["x"] for ch in node["children"]) / 2
            return node

        self.root = rec(n, 0, None)
        width = (counter[0] - 1) * leaf_dx
        self.boxes = VGroup()
        self.edges = VGroup()
        for nd in self.nodes:
            t = Text(f"fib({nd['n']})", font=SANS, font_size=size, color=FG, slant=ITALIC)
            box = RoundedRectangle(corner_radius=0.12, width=0.98, height=0.46, fill_color=PANEL,
                                   fill_opacity=1, stroke_color=BORDER, stroke_width=2)
            pos = np.array([nd["x"] * leaf_dx - width / 2, -nd["depth"] * level_dy, 0])
            box.move_to(pos)
            t.move_to(pos)
            nd["mob"] = VGroup(box, t)
            self.boxes.add(nd["mob"])
        for nd in self.nodes:
            if nd["parent"] is not None:
                p = nd["parent"]["mob"]
                e = Line(p.get_bottom(), nd["mob"].get_top(), color=MUTED, stroke_width=2.2, buff=0.04)
                e.add_tip(tip_length=0.12, tip_width=0.1)
                nd["edge"] = e
                self.edges.add(e)
        self.add(self.edges, self.boxes)

    def by_depth(self, d):
        return [nd for nd in self.nodes if nd["depth"] == d]

    def with_n(self, k):
        return [nd for nd in self.nodes if nd["n"] == k]

    def subtree(self, nd, include_self=False):
        out = [nd] if include_self else []
        for ch in nd["children"]:
            out += self.subtree(ch, include_self=True)
        return out

    def level_anim(self, d):
        anims = []
        for nd in self.by_depth(d):
            if "edge" in nd:
                anims.append(Create(nd["edge"]))
            anims.append(FadeIn(nd["mob"], scale=0.7))
        return AnimationGroup(*anims, lag_ratio=0.08)
