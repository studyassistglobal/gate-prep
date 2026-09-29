# Builds GATE note chapter modules from the Master_Guide markdown sources.
# MD -> typed block AST -> src/data/notes/de/chN.js  (GENERATED — do not hand-edit)
#
# Block types: p, h3, h4, ul, ol, table, code, alert, details, img, math
# The MD's own Table-of-Contents sections are dropped (the app generates its own).
import json, os, re, shutil, datetime

BASE = r"D:\UVM\PROJECTS\qp to test\gate-prep"
SRC_ROOT = r"D:\GATE 2027"

CHAPTERS = [
    {
        "id": "de-ch1",
        "file": "ch1",
        "notes_sub": "de",
        "num": 1,
        "title": "Logic Gates & Boolean Algebra",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_ROOT, "Digital electronics", "Chapter_01_Logic_Gates_and_Boolean_Algebra_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Digital electronics", "figures"),
        "figures_dst": "notes/de/figures",
        "fig_prefix": "figures/",
        "web_prefix": "/notes/de/figures/",
    },
    {
        "id": "de-ch2",
        "file": "ch2",
        "notes_sub": "de",
        "num": 2,
        "title": "Representation of Boolean Expressions & K-Maps",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_ROOT, "Digital electronics", "Chapter_02_Representation_of_Boolean_Expressions_and_K_Maps_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Digital electronics", "figures_ch2"),
        "figures_dst": "notes/de/figures_ch2",
        "fig_prefix": "figures_ch2/",
        "web_prefix": "/notes/de/figures_ch2/",
    },
    {
        "id": "de-ch3",
        "notes_sub": "de",
        "file": "ch3",
        "num": 3,
        "title": "Number Systems & Digital Representation",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_ROOT, "Digital electronics", "Chapter_03_Number_Systems_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Digital electronics", "figures_ch3"),
        "figures_dst": "notes/de/figures_ch3",
        "fig_prefix": "figures_ch3/",
        "web_prefix": "/notes/de/figures_ch3/",
    },
    {
        "id": "de-ch4-p1",
        "notes_sub": "de",
        "file": "ch4p1",
        "num": 4,
        "part": 1,
        "title": "Combinational Circuits — Arithmetic Logic",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_ROOT, "Digital electronics", "chapters", "Chapter_04_Part1_Combinational_Circuits.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/de/figures_ch4/",
    },
    {
        "id": "de-ch4-p2",
        "notes_sub": "de",
        "file": "ch4p2",
        "num": 4,
        "part": 2,
        "title": "Combinational Circuits — Advanced Architectures",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_ROOT, "Digital electronics", "chapters", "Chapter_04_Part2_Combinational_Circuits.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/de/figures_ch4/",
    },
    {
        "id": "ss-ch1",
        "file": "ssch1",
        "notes_sub": "ss",
        "num": 1,
        "title": "Basics of Signals",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_01_Basics_of_Signals_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch1"),
        "figures_dst": "notes/ss/figures_ch1",
        "fig_prefix": "figures_ch1/",
        "web_prefix": "/notes/ss/figures_ch1/",
    },
    {
        "id": "ss-ch2",
        "file": "ssch2",
        "notes_sub": "ss",
        "num": 2,
        "title": "Basics of Systems",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_02_Basics_of_Systems_Master_Guide.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ss/",
    },
    {
        "id": "ssf-ch1",
        "file": "ssfch1",
        "notes_sub": "ssf",
        "num": 1,
        "title": "Basics of Signals — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_01_Basics_of_Signals_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ss/",
    },
    {
        "id": "ssf-ch2",
        "file": "ssfch2",
        "notes_sub": "ssf",
        "num": 2,
        "title": "Basics of Systems — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_02_Basics_of_Systems_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ss/",
    },
    {
        "id": "ssf-ch3",
        "file": "ssfch3",
        "notes_sub": "ssf",
        "num": 3,
        "title": "Fourier Series (CTFS) — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_03_Continuous_Time_Fourier_Series_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ssf/",
    },
    {
        "id": "ss-ch3",
        "unwrap": True,
        "file": "ssch3",
        "notes_sub": "ss",
        "num": 3,
        "title": "Continuous-Time Fourier Series (CTFS)",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_03_Continuous_Time_Fourier_Series_Master_Guide.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ss/",
    },
    {
        "id": "ss-ch4",
        "unwrap": True,
        "file": "ssch4",
        "notes_sub": "ss",
        "num": 4,
        "title": "Fourier Transform & Sampling Theorem",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_04_Continuous_Time_Fourier_Transform_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch4"),
        "figures_dst": "notes/ss/figures_ch4",
        "fig_prefix": "figures_ch4/",
        "web_prefix": "/notes/ss/figures_ch4/",
    },
    {
        "id": "ss-ch5",
        "unwrap": True,
        "file": "ssch5",
        "notes_sub": "ss",
        "num": 5,
        "title": "Continuous-Time Laplace Transform",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_05_Continuous_Time_Laplace_Transform_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch5"),
        "figures_dst": "notes/ss/figures_ch5",
        "fig_prefix": "figures_ch5/",
        "web_prefix": "/notes/ss/figures_ch5/",
    },
    {
        "id": "ss-ch6",
        "unwrap": True,
        "file": "ssch6",
        "notes_sub": "ss",
        "num": 6,
        "title": "Discrete-Time Z-Transform",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_06_Discrete_Time_Z_Transform_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch6"),
        "figures_dst": "notes/ss/figures_ch6",
        "fig_prefix": "figures_ch6/",
        "web_prefix": "/notes/ss/figures_ch6/",
    },
    {
        "id": "ss-ch7",
        "unwrap": True,
        "file": "ssch7",
        "notes_sub": "ss",
        "num": 7,
        "title": "DTFT, DTFS, DFT & FFT",
        "subject": "Signals & Systems",
        "section_split": "module",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_07_DTFT_DTFS_DFT_FFT_Master_Guide.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch7"),
        "figures_dst": "notes/ss/figures_ch7",
        "fig_prefix": "figures_ch7/",
        "web_prefix": "/notes/ss/figures_ch7/",
    },
    {
        "id": "ssf-ch4",
        "unwrap": True,
        "file": "ssfch4",
        "notes_sub": "ssf",
        "num": 4,
        "title": "Fourier Transform & Sampling — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_04_Continuous_Time_Fourier_Transform_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ssf/",
    },
    {
        "id": "ssf-ch5",
        "unwrap": True,
        "file": "ssfch5",
        "notes_sub": "ssf",
        "num": 5,
        "title": "Laplace Transform — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "section_split": "section",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_05_Continuous_Time_Laplace_Transform_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ssf/",
    },
    {
        "id": "ssf-ch6",
        "unwrap": True,
        "file": "ssfch6",
        "notes_sub": "ssf",
        "num": 6,
        "title": "Z-Transform — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_06_Discrete_Time_Z_Transform_Formula_and_Revision_Sheet.md"),
        "figures_src": os.path.join(SRC_ROOT, "Signals and Systems", "figures_ch6"),
        "figures_dst": "notes/ssf/figures_ch6",
        "fig_prefix": "figures_ch6/",
        "web_prefix": "/notes/ssf/figures_ch6/",
    },
    {
        "id": "ssf-ch7",
        "unwrap": True,
        "file": "ssfch7",
        "notes_sub": "ssf",
        "num": 7,
        "title": "DTFT, DTFS, DFT & FFT — Formula & Revision Sheet",
        "subject": "Signals & Systems",
        "md": os.path.join(SRC_ROOT, "Signals and Systems", "Chapter_07_DTFT_DTFS_DFT_FFT_Formula_and_Revision_Sheet.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ssf/",
    },
    {
        "id": "nt-ch1",
        "unwrap": True,
        "file": "nt1",
        "notes_sub": "nt",
        "num": 1,
        "title": "Basics of Network Analysis",
        "subject": "Network Theory",
        "md": os.path.join(SRC_ROOT, "Network Theory", "01_Basics_of_Network.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/nt/",
    },
    {
        "id": "nt-ch2",
        "unwrap": True,
        "file": "nt2",
        "notes_sub": "nt",
        "num": 2,
        "title": "Network Theorems & Circuit Equivalence",
        "subject": "Network Theory",
        "md": os.path.join(SRC_ROOT, "Network Theory", "02_Network_Theorems.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/nt/",
    },
    {
        "id": "nt-ch3",
        "unwrap": True,
        "file": "nt3",
        "notes_sub": "nt",
        "num": 3,
        "title": "Transient Analysis",
        "subject": "Network Theory",
        "md": os.path.join(SRC_ROOT, "Network Theory", "03_Transient_Analysis.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/nt/",
    },
    {
        "id": "ntf-ch1",
        "unwrap": True,
        "file": "ntf1",
        "notes_sub": "ntf",
        "num": 1,
        "title": "Basics of Network — Revision Guide",
        "subject": "Network Theory",
        "md": os.path.join(SRC_ROOT, "Network Theory", "01_Basics_of_Network_Revision_Guide.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ntf/",
    },
    {
        "id": "ntf-ch2",
        "unwrap": True,
        "file": "ntf2",
        "notes_sub": "ntf",
        "num": 2,
        "title": "Network Theorems — Revision Guide",
        "subject": "Network Theory",
        "md": os.path.join(SRC_ROOT, "Network Theory", "02_Network_Theorems_Revision_Guide.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ntf/",
    },
    {
        "id": "ntf-ch3",
        "unwrap": True,
        "file": "ntf3",
        "notes_sub": "ntf",
        "num": 3,
        "title": "Transient Analysis — Revision Guide",
        "subject": "Network Theory",
        "md": os.path.join(SRC_ROOT, "Network Theory", "03_Transient_Analysis_Revision_Guide.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ntf/",
    },
    {
        "id": "ntf-ch4",
        "unwrap": True,
        "file": "ntf4",
        "notes_sub": "ntf",
        "num": 4,
        "title": "Revision Capsule — All Chapters",
        "subject": "Network Theory",
        "md": os.path.join(SRC_ROOT, "Network Theory", "GATE_Network_Theory_Revision_Capsule.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/ntf/",
    },
]

# Exact-match typo repairs applied to the (read-only) sources before parsing.
# Keys are chapter ids; values are (bad, good) literal replacements.
REPAIRS = {
    "nt-ch1": [
        ("the entire $2\\text{ mA} flows through branch BD",
         "the entire $2\\text{ mA}$ flows through branch BD"),
    ],
    # ss-ch5's source truncates module 09 mid-sentence (dangling "5. **The")
    "ss-ch5": [
        ("5. **The \n---", "---"),
    ],
}


def slugify(title):
    t = re.sub(r"\$[^$]*\$", " ", title)          # strip inline math for stable slugs
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return re.sub(r"-{2,}", "-", t)


MATH_SPAN_RE = re.compile(r"\$([^$]+)\$")
PLAIN_MATH_RE = re.compile(r"^[^\\\{\}<>]+$")


def clean_title(title):
    """Section/module titles render as plain text (TOC sidebar, search, header),
    so $math$ cannot stay: keep the inner text when it is plain-readable
    (`$R$` -> R), otherwise drop the span, then tidy leftover punctuation."""
    def sub(m):
        inner = m.group(1).strip()
        return inner if PLAIN_MATH_RE.match(inner) else ""
    t = MATH_SPAN_RE.sub(sub, title)
    t = re.sub(r"\(\s*\)", " ", t)              # parens emptied by dropped spans
    t = re.sub(r"\s+(-)(?=[A-Za-z])", r"\1", t)  # "the -Plane" -> "the-Plane"
    t = re.sub(r"\s{2,}", " ", t).strip(" -,")
    return t or title.strip()


def rewrite_img_src(src, ch):
    if src.startswith(ch["fig_prefix"]):
        return ch["web_prefix"] + src[len(ch["fig_prefix"]):]
    if src.startswith("http"):
        return src
    return ch["web_prefix"] + os.path.basename(src)


IMG_RE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")

STRUCT_START = re.compile(r"^\s*(?:#{1,6}\s|>|[-*]\s|\d+[.)]\s|```|~~~|\$\$|\||<|!\[)")


def unwrap_lines(lines):
    """Repair hard-wrapped lines (the Ch4-7 Masters and Network Theory sources
    wrap headings, bold spans and inline math mid-token). A continuation line
    is joined into its parent ONLY when the parent is actually broken: an
    unclosed bold (** count odd), an unclosed inline $...$ (odd $ count not
    from $$), a heading whose math/bold is broken, or a table row continued on
    a plain line. Healthy headings are never joined (module headers carry
    indented scope lines that must stay separate). Fenced code is untouched."""
    out = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        prev = out[-1] if out else None
        if (not in_fence and prev is not None and prev.strip() and line.strip()
                and not STRUCT_START.match(line)):
            ps = prev.rstrip()
            odd_dollar = (ps.count("$") - 2 * ps.count("$$")) % 2 == 1
            broken_bold = ps.count("**") % 2 == 1
            broken_heading = re.match(r"^\s*#{1,6}\s", ps) and (odd_dollar or broken_bold)
            if broken_heading or (broken_bold and not re.match(r"^\s*#{1,6}\s", ps)) \
                    or (odd_dollar and not re.match(r"^\s*#{1,6}\s", ps)) \
                    or ps.lstrip().startswith("|"):
                out[-1] = ps + " " + line.strip()
                continue
        out.append(line)
    return out


def split_table_row(line):
    """Split a pipe-table row into cells, ignoring `|` inside $math$/$$math$$,
    escaped \\|, or `backtick code spans`."""
    s = line.strip().strip("|")
    # stray trailing `\vert` separators (OCR of a dangling pipe) create a
    # phantom empty last cell — strip them
    s = re.sub(r"(?:\s*\\vert\s*)+$", "", s)
    cells, cur, in_math, in_code = [], [], False, False
    i = 0
    while i < len(s):
        ch = s[i]
        # OCR artifact: `\vert` used as a cell separator outside math
        if s.startswith("\\vert", i) and not in_math and not in_code:
            cells.append("".join(cur).strip())
            cur = []
            i += 5
            continue
        if ch == "\\" and i + 1 < len(s):
            cur.append(ch)
            cur.append(s[i + 1])
            i += 2
            continue
        if ch == "`" and not in_math:
            in_code = not in_code
            cur.append(ch)
            i += 1
            continue
        if s.startswith("$$", i):
            in_math = not in_math
            cur.append("$$")
            i += 2
            continue
        if ch == "$":
            in_math = not in_math
            cur.append(ch)
            i += 1
            continue
        if ch == "|" and not in_math and not in_code:
            cells.append("".join(cur).strip())
            cur = []
            i += 1
            continue
        cur.append(ch)
        i += 1
    cells.append("".join(cur).strip())
    return cells

def inline_clean(text, ch):
    """Rewrite image links inside inline text (kept for p/ul/table cells)."""
    def sub(m):
        return f"![{m.group(1)}]({rewrite_img_src(m.group(2), ch)})"
    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", sub, text)


def parse_blocks(lines, ch):
    """Line-based state machine -> typed blocks."""
    blocks = []
    i, n = 0, len(lines)
    para = []

    def flush_para():
        nonlocal para
        if para:
            text = inline_clean("\n".join(para).strip(), ch)
            if text:
                blocks.append({"t": "p", "text": text})
            para = []

    def flush_math_chunk(chunk):
        tex = "\n".join(chunk).strip()
        if tex:
            blocks.append({"t": "math", "tex": tex})

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # fenced code (no language tags in these sources)
        if stripped.startswith("```"):
            flush_para()
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            blocks.append({"t": "code", "text": "\n".join(code).rstrip()})
            continue

        # <details> collapsible (worked solutions) — the opener line may carry
        # an inline <summary> (single-line form) or it may be a standalone line
        if stripped.startswith("<details>"):
            flush_para()
            summary = "Solution"
            m0 = re.search(r"<summary>(.*?)</summary>", stripped)
            if m0:
                summary = re.sub(r"[^A-Za-z0-9 &'/-]+", " ", m0.group(1)).strip() or "Solution"
            i += 1
            inner = []
            depth = 1
            while i < n:
                s2 = lines[i].strip()
                if s2.startswith("<details>"):
                    depth += 1
                if s2.startswith("</details>"):
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                m = re.match(r"<summary>(.*?)</summary>\s*$", s2)
                if m:
                    summary = re.sub(r"[^A-Za-z0-9 &'/-]+", " ", m.group(1)).strip() or "Solution"
                elif not s2.startswith("<summary>"):
                    inner.append(lines[i])
                i += 1
            blocks.append({"t": "details", "summary": summary, "blocks": parse_blocks(inner, ch)})
            continue
        if stripped.startswith("<summary>"):
            i += 1
            continue

        # section-divider headings (module-split mode keeps interior ## / # lines)
        if stripped.startswith("## "):
            text = stripped[3:].strip()
            if re.match(r"(master )?table of contents$", text, re.IGNORECASE):
                i += 1
                continue
            flush_para()
            blocks.append({"t": "h2", "text": text})
            i += 1
            continue
        if stripped.startswith("# "):
            text = stripped[2:].strip()
            if re.match(r"table of contents$", text, re.IGNORECASE):
                i += 1
                continue
            flush_para()
            blocks.append({"t": "h2", "text": text})
            i += 1
            continue

        # GitHub alert callout (optional inline title: > [!NOTE] My title);
        # fenced ASCII diagrams inside the callout become code blocks between
        # alert fragments
        m = re.match(r">\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*(.*)$", stripped, re.IGNORECASE)
        if m:
            flush_para()
            i += 1
            alert_type = m.group(1).upper()
            title = m.group(2).strip() or None
            body = []

            def flush_alert():
                text = inline_clean("\n".join(body).strip(), ch)
                body.clear()
                if text:
                    blocks.append({"t": "alert", "type": alert_type, "title": title, "text": text})

            while i < n and lines[i].lstrip().startswith(">"):
                s2 = re.sub(r"^\s*>\s?", "", lines[i])
                st2 = s2.strip()
                if st2.startswith("```"):
                    flush_alert()
                    i += 1
                    code = []
                    while i < n:
                        t2 = re.sub(r"^\s*>\s?", "", lines[i]).strip()
                        if t2.startswith("```"):
                            i += 1
                            break
                        code.append(re.sub(r"^\s*>\s?", "", lines[i]))
                        i += 1
                    blocks.append({"t": "code", "text": "\n".join(code).rstrip()})
                    continue
                mm = re.match(r"<summary>(.*?)</summary>\s*$", st2)
                if mm:
                    title = re.sub(r"[^A-Za-z0-9 &'/-]+", " ", mm.group(1)).strip() or "Solution"
                elif not st2.startswith("<summary>"):
                    body.append(s2)
                i += 1
            flush_alert()
            continue

        # plain blockquote (none expected, be safe)
        if stripped.startswith(">"):
            flush_para()
            body = []
            while i < n and lines[i].lstrip().startswith(">"):
                body.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append({"t": "p", "text": inline_clean("\n".join(body).strip(), ch)})
            continue

        # table
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            flush_para()
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                cells = split_table_row(lines[i])
                rows.append(cells)
                i += 1
            header, align, data = rows[0], rows[1], rows[2:]
            # normalize ragged rows to the header width: pad short rows, merge
            # overflow cells into the last cell (OCR-mangled separators keep
            # all their text; the pipes render literally inside that cell)
            ncols = len(header)
            norm = []
            for r in data:
                if len(r) < ncols:
                    r = r + [""] * (ncols - len(r))
                elif len(r) > ncols:
                    r = r[:ncols - 1] + [" | ".join(r[ncols - 1:])]
                norm.append(r)
            blocks.append({"t": "table", "header": [inline_clean(c, ch) for c in header],
                           "align": align, "rows": [[inline_clean(c, ch) for c in r] for r in norm]})
            continue

        # display math $$ ... $$ (single-line or multi-line); the opening line may
        # be bullet-prefixed (`* $$…`) inside list items — strip the marker first
        math_src = re.sub(r"^[-*]\s+", "", stripped)
        if math_src.startswith("$$"):
            flush_para()
            # single-line form: `$…$$ trailing text` — keep trailing text
            # (e.g. `$\checkmark$ …`) as a following paragraph, never inside
            # the tex; a pure-quote trail is peeled like the old behaviour
            m2 = re.match(r"\$\$(.*?)\$\$(.*)$", math_src, re.DOTALL)
            if m2:
                trail = m2.group(2).strip().strip('"').strip()
                blocks.append({"t": "math", "tex": m2.group(1).strip().strip('"').strip()})
                if trail:
                    blocks.append({"t": "p", "text": inline_clean(trail, ch)})
                i += 1
                continue
            chunk = [math_src.lstrip("$").strip()]
            i += 1
            trail = ""
            while i < n and "$$" not in lines[i]:
                chunk.append(lines[i])
                i += 1
            if i < n:
                tail_line = lines[i].strip()
                k = tail_line.find("$$")
                chunk.append(tail_line[:k].strip().strip('"'))
                trail = tail_line[k + 2:].strip().strip('"').strip()
                i += 1
            flush_math_chunk(chunk)
            if trail:
                blocks.append({"t": "p", "text": inline_clean(trail, ch)})
            continue

        # images (own line)
        m = IMG_RE.match(stripped)
        if m:
            flush_para()
            blocks.append({"t": "img", "src": rewrite_img_src(m.group(2), ch), "alt": m.group(1)})
            i += 1
            continue

        # headings
        if stripped.startswith("### "):
            flush_para()
            blocks.append({"t": "h3", "text": stripped[4:].strip()})
            i += 1
            continue
        if stripped.startswith("#### "):
            flush_para()
            blocks.append({"t": "h4", "text": stripped[5:].strip()})
            i += 1
            continue
        # deeper levels (##### / ######) render as h4 — the sources use them for
        # per-problem sub-headings and literal hashes would leak into p blocks
        m = re.match(r"^#{5,6}\s+(.*)$", stripped)
        if m:
            flush_para()
            blocks.append({"t": "h4", "text": m.group(1).strip()})
            i += 1
            continue

        # unordered / ordered lists
        m = re.match(r"^[-*]\s+(.*)$", stripped)
        if m:
            flush_para()
            items = []
            while i < n:
                m2 = re.match(r"^[-*]\s+(.*)$", lines[i].strip())
                if not m2:
                    break
                item = re.sub(r"^\[( |x)\]\s*", lambda mm: "✓ " if mm.group(1) == "x" else "◻ ", m2.group(1).strip())
                items.append(inline_clean(item, ch))
                i += 1
            blocks.append({"t": "ul", "items": items})
            continue
        m = re.match(r"^(\d+)[.)]\s+(.*)$", stripped)
        if m:
            flush_para()
            start = int(m.group(1))
            items = []
            while i < n:
                m2 = re.match(r"^(\d+)[.)]\s+(.*)$", lines[i].strip())
                if not m2:
                    break
                items.append(inline_clean(m2.group(2).strip(), ch))
                i += 1
            # display math often interleaves numbered items — each fragment
            # becomes its own ol block, so preserve the original start number
            blocks.append({"t": "ol", "start": start, "items": items})
            continue

        # horizontal rules / blanks
        if re.match(r"^-{3,}\s*$", stripped) or stripped == "":
            flush_para()
            i += 1
            continue

        para.append(line)
        i += 1

    flush_para()
    return blocks


def build_chapter(ch):
    raw = open(ch["md"], encoding="utf-8").read().replace("\r\n", "\n")
    # per-chapter source typo repairs (sources stay read-only; exact matches)
    for bad, good in REPAIRS.get(ch["id"], []):
        raw = raw.replace(bad, good)
    # OCR corruption repair: LaTeX escapes \a \b \t \v \f \r sometimes survive
    # the MD export as literal control chars (BEL, BS, TAB, VT, FF, CR).
    # Restore each to backslash + macro letter when followed by a lowercase
    # letter (FF+"rac" -> \frac, CR+"ight" -> \right).
    CTRL_MAP = {"\a": "a", "\b": "b", "\t": "t", "\v": "v", "\f": "f", "\r": "r"}
    raw = re.sub("[\x07\x08\x09\x0b\x0c\x0d](?=[a-z])",
                 lambda m: "\\" + CTRL_MAP[m.group(0)], raw)
    # drop the MD's own TOC: the `## Table of Contents` section (entries are
    # internal-anchor link lines — some TOCs are followed by H1 headers, so
    # stop at any H1/H2) and a bare `# Table of Contents` h1. The "Master"
    # variant heading (sheet-style TOCs in the Masters) is dropped as a line;
    # its entries fall to the anchor dropper below.
    raw = re.sub(r"^# Table of Contents\s*$", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"^## (?:Master )?Table of Contents\s*$.*?(?=^## |^# )",
                 "", raw, flags=re.MULTILINE | re.DOTALL)
    # safety net: surviving internal-anchor link lines (TOC remnants), numbered
    # or bullet-prefixed
    raw = re.sub(r"(?m)^\s*(?:[-*]\s*)?(?:\d+[.)]\s*)?\[[^\]]*\]\(#[^)]+\)\s*$", "", raw)
    # repair hard-wrapped headings / bold / math / table rows — new-format
    # sources only (Ch4-7 Masters, sheets Ch4-7, Network Theory); the older
    # chapters are stable and must stay byte-identical
    if ch.get("unwrap"):
        raw = "\n".join(unwrap_lines(raw.split("\n")))

    # section splitting: generic chapters split at every `## `; module-split
    # chapters (audit-concatenated Masters) split only at Module headers at ANY
    # heading level (Ch1 uses `## Module N:`, Ch2 uses `# Module N:`) and keep
    # interior ## / # lines as divider blocks via parse_blocks; section-split
    # chapters (Formula & Revision Sheets) split at `Section N:` headers.
    mode = ch.get("section_split", "h2")
    if mode == "module":
        split_re = r"^#{1,6} (?=Module )"
    elif mode == "section":
        split_re = r"^#{1,6} (?=Section )"
    else:
        split_re = r"^## +"
    parts = re.split(split_re, raw, flags=re.MULTILINE)
    sections = []
    if parts[0].strip():
        pre_text = parts[0].strip()
        if mode == "section":
            # formula sheets carry a huge `## Master Table of Contents` at the
            # end of the preamble — drop it wholesale; the app renders its own
            # TOC sidebar, and the sheet's sub-entries are plain text lines
            # the anchor-line dropper cannot catch
            toc_i = pre_text.find("## Master Table of Contents")
            if toc_i != -1:
                pre_text = pre_text[:toc_i]
        pre_lines = pre_text.split("\n")
        # drop the h1 title itself (module metadata already carries it)
        pre_blocks = parse_blocks([l for l in pre_lines if not l.startswith("# ")], ch)
        if pre_blocks:
            sections.append({"id": "about", "title": "About this chapter", "blocks": pre_blocks})
    for part in parts[1:]:
        lines = part.split("\n")
        title = clean_title(lines[0].strip())
        if not title:
            continue
        sid = slugify(lines[0].strip())
        body = parse_blocks(lines[1:], ch)
        if not body:
            continue
        sections.append({"id": sid, "title": title, "blocks": body})

    module = {
        "id": ch["id"],
        "num": ch["num"],
        "part": ch.get("part"),
        "title": ch["title"],
        "subject": ch["subject"],
        "source": os.path.basename(ch["md"]),
        "generatedAt": datetime.date.today().isoformat(),
        "sections": sections,
    }
    return module


def write_module(module, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("// GENERATED by scripts/build_notes.py — do not hand-edit.\n")
        fp.write(f"// Source: {module['source']} · generated {module['generatedAt']}\n")
        fp.write(f"export default {json.dumps(module, ensure_ascii=True, indent=1)};\n")


def main():
    index = {}
    for ch in CHAPTERS:
        module = build_chapter(ch)
        nblocks = sum(len(s["blocks"]) for s in module["sections"])
        out = os.path.join(BASE, "src", "data", "notes", ch["notes_sub"], f"{ch['file']}.js")
        write_module(module, out)
        index[module["id"]] = {
            "num": module["num"],
            "title": module["title"],
            "subject": module["subject"],
            "sections": [{"id": s["id"], "title": s["title"]} for s in module["sections"]],
        }
        # figures (png/jpg/jpeg)
        if ch["figures_src"] and os.path.isdir(ch["figures_src"]):
            dst = os.path.join(BASE, "public", *ch["figures_dst"].split("/"))
            os.makedirs(dst, exist_ok=True)
            copied = 0
            for f in os.listdir(ch["figures_src"]):
                if f.lower().endswith((".png", ".jpg", ".jpeg")):
                    shutil.copy2(os.path.join(ch["figures_src"], f), os.path.join(dst, f))
                    copied += 1
            print(f"  figures: copied {copied} images -> public/{ch['figures_dst']}")
        print(f"{module['id']}: {len(module['sections'])} sections, {nblocks} blocks -> {os.path.relpath(out, BASE)}")

    idx_path = os.path.join(BASE, "src", "data", "notes", "index.js")
    with open(idx_path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("// GENERATED by scripts/build_notes.py — do not hand-edit.\n")
        fp.write("// Lightweight per-chapter section index (course page accordion + search).\n")
        fp.write(f"export const NOTES_INDEX = {json.dumps(index, ensure_ascii=True, indent=1)};\n")
    print(f"index -> {os.path.relpath(idx_path, BASE)}")


if __name__ == "__main__":
    main()
