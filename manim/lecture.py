"""Shared theme, reusable components, and the narration-synced base scene.

Semua scene meng-import modul ini:  from lecture import *
"""
from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path

from manim import *  # noqa: F401,F403

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "audio" / "manifest.json"
# render_scenes.py men-set LECTURE_QUALITY agar timing preview & final tidak saling menimpa
TIMINGS_DIR = ROOT / "build" / os.environ.get("LECTURE_QUALITY", "dev") / "timings"

# ----------------------------------------------------------------- theme
BG = "#0B1220"
PANEL = "#121C30"
PANEL_2 = "#17233B"
BORDER = "#26344F"
FG = "#E6EDF7"
MUTED = "#8A9BB8"
BLUE = "#38BDF8"
ORANGE = "#FB923C"
GREEN = "#34D399"
RED = "#F87171"
YELLOW = "#FACC15"
PURPLE = "#A78BFA"
PINK = "#F472B6"

SANS = "Inter"
MONO = "DejaVu Sans Mono"  # tanpa ligature -> glyph per karakter (dibutuhkan CodePanel)

CONTENT_TOP = 2.75      # di bawah title bar
CONTENT_BOTTOM = -2.80  # di atas area subtitle (subtitle di-burn di ~140px bawah)

config.background_color = BG


def T(text, size=30, color=FG, weight=NORMAL, font=SANS, **kw):
    return Text(text, font=font, font_size=size, color=color, weight=weight, **kw)


def M(markup, size=30, color=FG, font=SANS, **kw):
    """MarkupText (Pango markup): <b>, <i>, <span foreground='#hex'>."""
    return MarkupText(markup, font=font, font_size=size, color=color, **kw)


def c(text, color):
    return f'<span foreground="{color}">{text}</span>'


def mono(text, size=28, color=FG, **kw):
    return Text(text, font=MONO, font_size=size, color=color, **kw)


def panel(width, height, color=PANEL, stroke=BORDER, radius=0.18, **kw):
    return RoundedRectangle(corner_radius=radius, width=width, height=height,
                            fill_color=color, fill_opacity=1, stroke_color=stroke, stroke_width=2, **kw)


def pill(text, color=BLUE, size=22, text_color=BG, pad=0.22):
    t = T(text, size=size, color=text_color, weight=BOLD)
    r = RoundedRectangle(corner_radius=(t.height + 2 * 0.12) / 2, width=t.width + 2 * pad,
                         height=t.height + 2 * 0.12, fill_color=color, fill_opacity=1, stroke_width=0)
    return VGroup(r, t.move_to(r))


def title_bar(section: str, title: str):
    sec = T(section.upper(), size=20, color=BLUE, weight=BOLD)
    ttl = T(title, size=38, color=FG, weight=BOLD)
    grp = VGroup(sec, ttl).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    if grp.width > 13.0:
        ttl.scale_to_fit_width(13.0 - 0.0)
        grp = VGroup(sec, ttl).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    grp.to_corner(UL, buff=0.45)
    accent = Rectangle(width=0.08, height=grp.height, fill_color=ORANGE, fill_opacity=1, stroke_width=0)
    accent.next_to(grp, LEFT, buff=0.18)
    return VGroup(accent, grp)


def bullet_list(items, size=28, width=12.0, buff=0.32, dot_color=BLUE):
    """items: list of markup strings."""
    rows = VGroup()
    for it in items:
        dot = Dot(radius=0.06, color=dot_color)
        txt = M(it, size=size)
        if txt.width > width:
            txt.scale_to_fit_width(width)
        dot.next_to(txt, LEFT, buff=0.25).align_to(txt, UP).shift(DOWN * 0.13)
        rows.add(VGroup(dot, txt))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return rows


# ----------------------------------------------------------------- code panel
_KEYWORDS = {"if", "else", "for", "to", "return", "let", "be", "a", "new", "array", "with", "sum"}


class CodePanel(VGroup):
    """Pseudocode panel bergaya editor, dengan line number dan highlight per baris.

    lines: list[str]; baris pertama boleh berupa header (nama prosedur) jika header=True.
    Indentasi dipertahankan (spasi diawal baris).
    """

    def __init__(self, lines, size=24, header=True, width=None, numbered=True, comment_color=MUTED,
                 bold_lines=(), **kw):
        super().__init__(**kw)
        self.src = lines
        rendered = []
        num = 0
        for k, ln in enumerate(lines):
            if header and k == 0 or ln.strip() == "" or not numbered:
                rendered.append("│    " + ln)
            else:
                num += 1
                rendered.append(f"│{num:>2}  " + ln)
        txt = Text("\n".join(rendered), font=MONO, font_size=size, color=FG, line_spacing=0.85)
        # map glyphs ke baris
        self.line_glyphs = []
        idx = 0
        for k, (ln_r, ln) in enumerate(zip(rendered, lines)):
            n_glyph = len(ln_r.replace(" ", ""))
            glyphs = VGroup(*txt.submobjects[idx:idx + n_glyph])
            idx += n_glyph
            bar = glyphs[0]
            bar.set_opacity(0)
            # warna per karakter
            chars = [ch for ch in ln_r if ch != " "]
            prefix_len = len(ln_r[:5].replace(" ", ""))  # "│" + nomor
            for g in glyphs[1:prefix_len]:
                g.set_color(MUTED)
            code_part = ln_r[5:]
            colors = self._colorize(code_part, header and k == 0, comment_color, k in bold_lines)
            for g, col in zip(glyphs[prefix_len:], colors):
                g.set_color(col)
            self.line_glyphs.append(VGroup(bar, *glyphs[1:]))
            _ = chars
        self.text = txt
        w = (width or txt.width + 0.9)
        self.bg = panel(w, txt.height + 0.7)
        txt.move_to(self.bg).align_to(self.bg, LEFT).shift(RIGHT * 0.25)
        self.add(self.bg, txt)
        self.size = size

    @staticmethod
    def _colorize(code, is_header, comment_color, bold):
        out = []
        if is_header:
            return [YELLOW] * len(code.replace(" ", ""))
        comment_at = code.find("//")
        i = 0
        tokens = []
        word = ""
        for ch in code + " ":
            if ch.isalnum() or ch == "_":
                word += ch
            else:
                if word:
                    tokens.append(word)
                    word = ""
                tokens.append(ch)
        pos = 0
        for tok in tokens[:-1]:
            if tok == " ":
                pos += 1
                continue
            in_comment = comment_at >= 0 and pos >= comment_at
            if in_comment:
                col = comment_color
            elif tok in _KEYWORDS:
                col = PURPLE
            elif tok.isdigit() or tok in {"NIL", "∞"}:
                col = ORANGE
            elif tok.isupper() and len(tok) > 1 or "-" in tok:
                col = YELLOW
            elif tok in "[](),;=+-<>!.":
                col = MUTED if tok in "(),;" else FG
            else:
                col = FG
            out.extend([col] * len(tok))
            pos += len(tok)
            i += 1
        return out

    def line(self, k):
        return self.line_glyphs[k]

    def highlight_box(self, k, color=BLUE):
        g = self.line_glyphs[k]
        bar = g[0]
        h = bar.height * 1.05
        rect = Rectangle(width=self.bg.width - 0.16, height=h, fill_color=color, fill_opacity=0.16,
                         stroke_color=color, stroke_width=0)
        rect.move_to([self.bg.get_center()[0], bar.get_center()[1], 0])
        edge = Rectangle(width=0.06, height=h, fill_color=color, fill_opacity=1, stroke_width=0)
        edge.next_to(rect, LEFT, buff=0).align_to(rect, LEFT)
        return VGroup(rect, edge)

    def lines_box(self, k0, k1, color=BLUE):
        a = self.highlight_box(k0, color)
        b = self.highlight_box(k1, color)
        top = a.get_top()[1]
        bot = b.get_bottom()[1]
        rect = Rectangle(width=self.bg.width - 0.16, height=top - bot, fill_color=color, fill_opacity=0.16,
                         stroke_width=0)
        rect.move_to([self.bg.get_center()[0], (top + bot) / 2, 0])
        edge = Rectangle(width=0.06, height=top - bot, fill_color=color, fill_opacity=1, stroke_width=0)
        edge.next_to(rect, LEFT, buff=0).align_to(rect, LEFT)
        return VGroup(rect, edge)


# ----------------------------------------------------------------- array visual
class ArrayRow(VGroup):
    def __init__(self, values, cell=0.95, size=32, index_from=1, show_index=True, color=FG,
                 fill=PANEL, stroke=BORDER, index_color=MUTED, **kw):
        super().__init__(**kw)
        self.cells = VGroup()
        self.vals = VGroup()
        self.idx = VGroup()
        for k, v in enumerate(values):
            sq = Square(cell, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=2.5)
            sq.shift(RIGHT * k * cell)
            self.cells.add(sq)
            t = T(str(v).replace("-", "−"), size=size, color=color, weight=BOLD) if v != "" else VMobject()
            t.move_to(sq)
            self.vals.add(t)
            if show_index:
                it = T(str(k + index_from), size=size * 0.62, color=index_color)
                it.next_to(sq, DOWN, buff=0.14)
                self.idx.add(it)
        self.add(self.cells, self.vals, self.idx)
        self.cell = cell

    def window(self, a, b, color=BLUE, buff=0.06, width=5):
        """Rounded frame around cells a..b (0-based, inclusive)."""
        g = VGroup(self.cells[a], self.cells[b])
        r = RoundedRectangle(corner_radius=0.12, width=g.width + 2 * buff, height=self.cell + 2 * buff,
                             stroke_color=color, stroke_width=width)
        r.move_to(g)
        return r

    def tint(self, a, b, color=BLUE, opacity=0.35):
        return AnimationGroup(*[self.cells[k].animate.set_fill(color, opacity=opacity) for k in range(a, b + 1)])

    def set_value(self, k, v, color=FG, size=None):
        size = size or 32
        t = T(str(v).replace("-", "−"), size=size, color=color, weight=BOLD).move_to(self.cells[k])
        return t


# ----------------------------------------------------------------- simple table
def grid_table(rows, col_widths, row_height=0.62, size=24, header_fill="#1D4ED8", fill=PANEL,
               alt_fill=PANEL_2, header_color=FG, first_col_bold=True, markup=False):
    """rows[0] = header. Returns VGroup(cells) with .cell(r,c) accessor via table.cells_map."""
    table = VGroup()
    cells_map = {}
    y = 0
    for r, row in enumerate(rows):
        x = 0
        heights = []
        texts = []
        for cidx, val in enumerate(row):
            w = col_widths[cidx]
            weight = BOLD if r == 0 or (first_col_bold and cidx == 0) else NORMAL
            if markup:
                t = M(val if r > 0 else f"<b>{val}</b>", size=size, color=header_color if r == 0 else FG)
            else:
                t = T(val, size=size, color=header_color if r == 0 else FG, weight=weight,
                      line_spacing=0.8)
            if t.width > w - 0.25:
                t.scale_to_fit_width(w - 0.25)
            texts.append(t)
            heights.append(t.height + 0.3)
        h = max(row_height, *heights)
        for cidx, t in enumerate(texts):
            w = col_widths[cidx]
            bg = Rectangle(width=w, height=h, stroke_color=BORDER, stroke_width=1.5,
                           fill_color=header_fill if r == 0 else (fill if r % 2 else alt_fill), fill_opacity=1)
            bg.move_to([x + w / 2, y - h / 2, 0])
            t.move_to(bg)
            cell = VGroup(bg, t)
            cells_map[(r, cidx)] = cell
            table.add(cell)
            x += w
        y -= h
    table.cells_map = cells_map
    table.center()
    return table


def row_of(table, r, ncols):
    return VGroup(*[table.cells_map[(r, cc)] for cc in range(ncols)])


# ----------------------------------------------------------------- base scene
class _Seg:
    def __init__(self, scene, seg_id, data, t0):
        self.scene, self.id, self.data, self.t0 = scene, seg_id, data, t0
        self.duration = data["duration"]
        self.sentences = data.get("sentences", [])

    def at(self, k):
        """Waktu (relatif segment) saat kalimat ke-k dimulai."""
        if not self.sentences:
            return 0
        k = max(0, min(k, len(self.sentences) - 1))
        return self.sentences[k]["start"]

    def wait_until(self, t_rel):
        now = self.scene.renderer.time - self.t0
        if t_rel - now > 1 / 60:
            self.scene.wait(t_rel - now)

    def wait_sentence(self, k, offset=0.0):
        self.wait_until(self.at(k) + offset)

    def remaining(self):
        return max(0.0, self.duration - (self.scene.renderer.time - self.t0))


class LectureScene(Scene):
    """Scene dasar: narasi tersinkron dengan animasi.

    Pemakaian:
        with self.say("s02_tree") as seg:
            self.play(...)
            seg.wait_sentence(2)   # tunggu sampai kalimat ke-3 mulai diucapkan
            self.play(...)
        # keluar dari blok: otomatis menunggu sampai audio segment selesai (+pad)
    """

    PAD = 0.35

    def setup(self):
        self.camera.background_color = BG
        self._manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {"segments": {}}
        self._timings = []

    @contextmanager
    def say(self, seg_id, pad=None):
        pad = self.PAD if pad is None else pad
        data = self._manifest["segments"].get(seg_id)
        if data is None:
            # fallback (audio belum digenerate): estimasi durasi, tanpa suara
            import narration as N
            text = dict((sid, t) for _, sid, t in N.all_segments())[seg_id]
            data = {"duration": len(text) / 14.0, "sentences": []}
            print(f"[WARN] audio untuk {seg_id} belum ada -> jalankan scripts/generate_audio.py")
        t0 = self.renderer.time
        if "file" in data:
            self.add_sound(str(ROOT / data["file"]))
        self._timings.append({"id": seg_id, "start": round(t0, 4)})
        seg = _Seg(self, seg_id, data, t0)
        yield seg
        rest = seg.remaining() + pad
        if rest > 1 / 60:
            self.wait(rest)

    def fade_out_anims(self, *groups, exclude=()):
        """FadeOut untuk semua mobject top-level di scene yang (sebagian) termasuk dalam `groups`.
        Aman dipakai walaupun anggota group ditambahkan ke scene secara terpisah."""
        fam = set()
        for g in groups:
            fam.update(id(m) for m in g.get_family())
        keep = set()
        for g in exclude:
            keep.update(id(m) for m in g.get_family())
        out = []
        for m in list(self.mobjects):
            ids = {id(x) for x in m.get_family()}
            if ids & fam and not (ids & keep and id(m) in keep):
                out.append(FadeOut(m))
        return out

    def fade_out(self, *groups, run_time=0.6, exclude=()):
        anims = self.fade_out_anims(*groups, exclude=exclude)
        if anims:
            self.play(*anims, run_time=run_time)

    def fade_all_except(self, *keep, run_time=0.6):
        keep_ids = set()
        for g in keep:
            keep_ids.update(id(m) for m in g.get_family())
        anims = [FadeOut(m) for m in self.mobjects if id(m) not in keep_ids]
        if anims:
            self.play(*anims, run_time=run_time)

    def clear_scene(self, run_time=0.6):
        mobs = [m for m in self.mobjects]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def tear_down(self):
        TIMINGS_DIR.mkdir(parents=True, exist_ok=True)
        out = {"scene": type(self).__name__, "duration": round(self.renderer.time, 4), "segments": self._timings}
        (TIMINGS_DIR / f"{type(self).__name__}.json").write_text(json.dumps(out, indent=1))
