# Builds GATE note chapter modules from the Master_Guide markdown sources.
# MD -> typed block AST -> src/data/notes/de/chN.js  (GENERATED — do not hand-edit)
#
# Block types: p, h3, h4, ul, ol, table, code, alert, details, img, math
# The MD's own Table-of-Contents sections are dropped (the app generates its own).
import json, os, re, shutil, datetime

BASE = r"D:\UVM\PROJECTS\qp to test\gate-prep"
SRC_DIR = r"D:\GATE 2027\Digital electronics"

CHAPTERS = [
    {
        "id": "de-ch1",
        "file": "ch1",
        "num": 1,
        "title": "Logic Gates & Boolean Algebra",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_DIR, "Chapter_01_Logic_Gates_and_Boolean_Algebra_Master_Guide.md"),
        "figures_src": os.path.join(SRC_DIR, "figures"),
        "figures_dst": "notes/de/figures",
        "fig_prefix": "figures/",
        "web_prefix": "/notes/de/figures/",
    },
    {
        "id": "de-ch2",
        "file": "ch2",
        "num": 2,
        "title": "Representation of Boolean Expressions & K-Maps",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_DIR, "Chapter_02_Representation_of_Boolean_Expressions_and_K_Maps_Master_Guide.md"),
        "figures_src": os.path.join(SRC_DIR, "figures_ch2"),
        "figures_dst": "notes/de/figures_ch2",
        "fig_prefix": "figures_ch2/",
        "web_prefix": "/notes/de/figures_ch2/",
    },
    {
        "id": "de-ch3",
        "file": "ch3",
        "num": 3,
        "title": "Number Systems & Digital Representation",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_DIR, "Chapter_03_Number_Systems_Master_Guide.md"),
        "figures_src": os.path.join(SRC_DIR, "figures_ch3"),
        "figures_dst": "notes/de/figures_ch3",
        "fig_prefix": "figures_ch3/",
        "web_prefix": "/notes/de/figures_ch3/",
    },
    {
        "id": "de-ch4-p1",
        "file": "ch4p1",
        "num": 4,
        "part": 1,
        "title": "Combinational Circuits — Arithmetic Logic",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_DIR, "chapters", "Chapter_04_Part1_Combinational_Circuits.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/de/figures_ch4/",
    },
    {
        "id": "de-ch4-p2",
        "file": "ch4p2",
        "num": 4,
        "part": 2,
        "title": "Combinational Circuits — Advanced Architectures",
        "subject": "Digital Electronics",
        "md": os.path.join(SRC_DIR, "chapters", "Chapter_04_Part2_Combinational_Circuits.md"),
        "figures_src": None,
        "figures_dst": None,
        "fig_prefix": "",
        "web_prefix": "/notes/de/figures_ch4/",
    },
]


def slugify(title):
    t = re.sub(r"\$[^$]*\$", " ", title)          # strip inline math for stable slugs
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return re.sub(r"-{2,}", "-", t)


def rewrite_img_src(src, ch):
    if src.startswith(ch["fig_prefix"]):
        return ch["web_prefix"] + src[len(ch["fig_prefix"]):]
    if src.startswith("http"):
        return src
    return ch["web_prefix"] + os.path.basename(src)


IMG_RE = re.compile(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$")

def split_table_row(line):
    """Split a pipe-table row into cells, ignoring `|` inside $math$ or escaped \\|."""
    s = line.strip().strip("|")
    cells, cur, in_math = [], [], False
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            cur.append(ch)
            cur.append(s[i + 1])
            i += 2
            continue
        if ch == "$":
            in_math = not in_math
            cur.append(ch)
            i += 1
            continue
        if ch == "|" and not in_math:
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

        # <details> collapsible (worked solutions)
        if stripped.startswith("<details>"):
            flush_para()
            i += 1
            summary = "Solution"
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
                    summary = re.sub(r"[^A-Za-z0-9 &']+", " ", m.group(1)).strip() or "Solution"
                elif not s2.startswith("<summary>"):
                    inner.append(lines[i])
                i += 1
            blocks.append({"t": "details", "summary": summary, "blocks": parse_blocks(inner, ch)})
            continue
        if stripped.startswith("<summary>"):
            i += 1
            continue

        # GitHub alert callout
        m = re.match(r">\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$", stripped, re.IGNORECASE)
        if m:
            flush_para()
            i += 1
            body = []
            while i < n and lines[i].lstrip().startswith(">"):
                body.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append({"t": "alert", "type": m.group(1).upper(), "text": inline_clean("\n".join(body).strip(), ch)})
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
            blocks.append({"t": "table", "header": [inline_clean(c, ch) for c in header],
                           "align": align, "rows": [[inline_clean(c, ch) for c in r] for r in data]})
            continue

        # display math $$ ... $$ (single-line or multi-line)
        if stripped.startswith("$$"):
            if stripped.count("$$") >= 2 and len(stripped) > 4:
                flush_para()
                blocks.append({"t": "math", "tex": stripped.strip("$").strip()})
                i += 1
                continue
            flush_para()
            chunk = [stripped.lstrip("$").strip()]
            i += 1
            while i < n and "$$" not in lines[i]:
                chunk.append(lines[i])
                i += 1
            if i < n:
                tail = lines[i].strip()
                chunk.append(tail.rstrip("$").strip())
                i += 1
            flush_math_chunk(chunk)
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

        # unordered / ordered lists
        m = re.match(r"^[-*]\s+(.*)$", stripped)
        if m:
            flush_para()
            items = []
            while i < n:
                m2 = re.match(r"^[-*]\s+(.*)$", lines[i].strip())
                if not m2:
                    break
                items.append(inline_clean(m2.group(1).strip(), ch))
                i += 1
            blocks.append({"t": "ul", "items": items})
            continue
        m = re.match(r"^(\d+)[.)]\s+(.*)$", stripped)
        if m:
            flush_para()
            items = []
            while i < n:
                m2 = re.match(r"^(\d+)[.)]\s+(.*)$", lines[i].strip())
                if not m2:
                    break
                items.append(inline_clean(m2.group(2).strip(), ch))
                i += 1
            blocks.append({"t": "ol", "items": items})
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
    # drop the MD's own TOC: both the `## Table of Contents` section and the
    # `# Table of Contents` h1. ch2's TOC has NO section heading — its entries
    # are bare internal-anchor link lines, so drop those lines directly
    # (the only internal links in these documents are TOC links).
    raw = re.sub(r"^# Table of Contents\s*$", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"^## Table of Contents\s*$.*?(?=^## )", "", raw, flags=re.MULTILINE | re.DOTALL)
    raw = re.sub(r"(?m)^\s*\d*[.)]?\s*\[[^\]]*\]\(#[^)]+\)\s*$", "", raw)

    # split at h2 headings; keep the pre-heading preamble (h1 + metadata lines)
    # as a lead "About this chapter" section so nothing from the MD is lost
    parts = re.split(r"^## +", raw, flags=re.MULTILINE)
    sections = []
    if parts[0].strip():
        pre_lines = parts[0].strip().split("\n")
        # drop the h1 title itself (module metadata already carries it)
        pre_blocks = parse_blocks([l for l in pre_lines if not l.startswith("# ")], ch)
        if pre_blocks:
            sections.append({"id": "about", "title": "About this chapter", "blocks": pre_blocks})
    for part in parts[1:]:
        lines = part.split("\n")
        title = lines[0].strip()
        if not title:
            continue
        sid = slugify(title)
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
        out = os.path.join(BASE, "src", "data", "notes", "de", f"{ch['file']}.js")
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

    idx_path = os.path.join(BASE, "src", "data", "notes", "de", "index.js")
    with open(idx_path, "w", encoding="utf-8", newline="\n") as fp:
        fp.write("// GENERATED by scripts/build_notes.py — do not hand-edit.\n")
        fp.write("// Lightweight per-chapter section index (course page accordion + search).\n")
        fp.write(f"export const NOTES_INDEX = {json.dumps(index, ensure_ascii=True, indent=1)};\n")
    print(f"index -> {os.path.relpath(idx_path, BASE)}")


if __name__ == "__main__":
    main()
