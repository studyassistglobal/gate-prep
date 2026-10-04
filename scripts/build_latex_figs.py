# Compile the circuitikz/TikZ figures from the Rectifiers & Filters LaTeX
# Master Guide into standalone SVGs for the site (public/notes/ae/figures_latex/).
# The .md source only carries the generated blueprint posters; the .tex is the
# polished original with real circuit schematics + waveform plots — the user
# wants those on the site.
#
# Pipeline per figure: extract figure env -> wrap in standalone doc with the
# master preamble -> pdflatex -> dvisvgm --pdf -n (glyphs as paths) -> .svg
import os
import re
import subprocess
import tempfile
import shutil

TEX_PATH = r"D:/GATE 2027/analog electronics/Rectifiers_and_Filters_Master_Guide.tex"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "public", "notes", "ae", "figures_latex")

# packages that clash with the standalone class or are irrelevant to figures
BLOCKLIST = ("geometry", "fancyhdr", "titlesec", "hyperref", "microtype")
# preamble lines that depend on the blocklisted packages
DROP_LINES = ("\\pagestyle", "\\fancy", "\\rhead", "\\lhead", "\\cfoot",
              "\\titleformat", "\\titlespacing", "\\hypersetup", "\\geometry")

# figure order in the TeX -> file name (drives the builder's injection config)
FIG_NAMES = [
    "tex_dc_power_supply_block_diagram",
    "tex_pwl_diode_model",
    "tex_hwr_circuit_schematic",
    "tex_hwr_waveforms",
    "tex_fwr_ct_circuit_schematic",
    "tex_graetz_bridge_schematic",
    "tex_fwr_waveforms_piv",
    "tex_filter_topologies",
    "tex_c_filter_ripple_surge",
    "tex_ripple_factor_vs_load",
    "tex_rectifier_filter_decision_tree",
]


def strip_braced(text, cmd):
    """Remove `\\cmd{...}` with brace matching; return (new_text, inner)."""
    i = text.find("\\" + cmd + "{")
    if i == -1:
        return text, None
    j, depth = i + len(cmd) + 2, 1
    while depth:
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
        j += 1
    return text[:i] + text[j:], text[i + len(cmd) + 2 : j - 1]


def tex_to_plain(s):
    s = re.sub(r"\\&", "&", s)
    s = re.sub(r"\$", "", s)
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", "", s)
    return re.sub(r"\s+", " ", s).strip()


def extract_preamble(raw):
    pre = raw.split("\\begin{document}")[0]
    lines = []
    ls = pre.split("\n")
    i = 0
    while i < len(ls):
        line = ls[i]
        if line.startswith("\\documentclass"):
            i += 1
            continue
        if any(line.startswith("\\usepackage[" + b) or line.startswith("\\usepackage{" + b + "}") for b in BLOCKLIST):
            i += 1
            continue
        if any(line.startswith(d) for d in DROP_LINES):
            # drop the command AND its continuation lines (the format argument
            # usually starts on the next line) until braces close and a new
            # command (or blank/comment line) begins
            depth = line.count("{") - line.count("}")
            i += 1
            while i < len(ls):
                nxt = ls[i]
                if depth <= 0 and (nxt.startswith("\\") or nxt.strip() == "" or nxt.startswith("%")):
                    break
                depth += nxt.count("{") - nxt.count("}")
                i += 1
            continue
        lines.append(line)
        i += 1
    return "\n".join(lines) + "\n\\usepackage{graphicx}\n"


def main():
    raw = open(TEX_PATH, encoding="utf-8").read().replace("\r\n", "\n")
    preamble = extract_preamble(raw)
    os.makedirs(OUT_DIR, exist_ok=True)

    figs = re.findall(r"\\begin\{figure\}.*?\\end\{figure\}", raw, re.S)
    m_tree = re.search(
        r"\\begin\{center\}\s*\\resizebox\{\\textwidth\}\{!\}\{\s*(\\begin\{forest\}.*?\\end\{forest\})\s*\}\s*\\end\{center\}",
        raw, re.S)
    contents = figs + ([m_tree.group(1)] if m_tree else [])
    assert len(contents) == len(FIG_NAMES), f"{len(contents)} figures found, {len(FIG_NAMES)} names"

    tmp = tempfile.mkdtemp(prefix="latexfigs_")
    try:
        for name, content in zip(FIG_NAMES, contents):
            content, caption = strip_braced(content, "caption")
            content = re.sub(r"\\label\{[^}]*\}", "", content)
            # the standalone doc holds the figure BODY only — drop the float
            content = re.sub(r"\\begin\{figure\}\[[^\]]*\]\s*|\s*\\end\{figure\}", "", content).strip()
            alt = tex_to_plain(caption) if caption else name
            doc = f"\\documentclass[border=10pt]{{standalone}}\n{preamble}\\begin{{document}}\n{content}\n\\end{{document}}\n"
            texf = os.path.join(tmp, name + ".tex")
            open(texf, "w", encoding="utf-8").write(doc)
            r = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "--enable-installer", name + ".tex"],
                cwd=tmp, capture_output=True, text=True, timeout=180)
            if not os.path.exists(os.path.join(tmp, name + ".pdf")):
                logf = os.path.join(tmp, name + ".log")
                log = open(logf, encoding="utf-8", errors="replace").read() if os.path.exists(logf) else r.stderr
                errs = "\n".join(l for l in log.split("\n") if l.startswith("! ") or l.startswith("l."))
                raise RuntimeError(f"pdflatex failed for {name}:\n{errs[:2000]}")
            subprocess.run(["dvisvgm", "--pdf", "-n", name + ".pdf"], cwd=tmp,
                           check=True, capture_output=True, text=True, timeout=120)
            shutil.copy2(os.path.join(tmp, name + ".svg"), os.path.join(OUT_DIR, name + ".svg"))
            size = os.path.getsize(os.path.join(OUT_DIR, name + ".svg")) // 1024
            print(f"  {name}.svg  ({size} KB)  alt: {alt[:80]}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"done -> {OUT_DIR}")


if __name__ == "__main__":
    main()
