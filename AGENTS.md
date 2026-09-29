# AGENTS.md — GATE Prep (working guide for AI agents)

> Operational playbook for this repository. Live site: https://gate-prep.pages.dev (Cloudflare Pages project `gate-prep`). Forked from ExamPrep Hub; the IIT/AIIMS site and ExamPrep Hub are separate repos.

## TL;DR

Public, login-free **GATE 2027 (ECE) notes site**. React 18 + Vite 5, HashRouter, Deep Focus light/dark theme. Content = generated block-AST modules built from the owner's Master Guide markdown. No Supabase, no auth, no server — pure static.

## Content pipeline (the core invariant)

1. Source of truth: `D:/GATE 2027/Digital electronics/*_Master_Guide.md` (outside this repo).
2. `npm run build:notes` (`scripts/build_notes.py`) parses each MD into typed blocks (`p / h3 / h4 / ul / ol / table / code / alert / details / img / math`), splits at `## ` headings, drops the MD's own TOC (both `## Table of Contents` sections and bare internal-anchor link lines), captures the pre-heading preamble as an "About this chapter" section, and rewrites figure paths to `/notes/de/...`.
3. Outputs `src/data/notes/de/<file>.js` (per-chapter `file` stem — ch4 parts are `ch4p1.js`/`ch4p2.js`) + `index.js` + copies figures (PNG **and JPG**) to `public/notes/de/`.
4. **Never hand-edit `src/data/notes/**`** — regenerate. Adding a chapter = drop its MD path into `CHAPTERS` in `build_notes.py` (with a unique `file` stem) + add the chapter to `src/data/courses.js`.
5. Table cells split on `|` only OUTSIDE `$math$` (`split_table_row`) — ch3 magnitude cells contain literal pipes inside math; keep that rule.
6. Part-split chapters carry `part` in the registry + module; labels use `chapterLabel()` ("Ch 4.2").
7. Audit-concatenated Masters (ss-ch1) use `section_split: 'module'` — sections split at `## Module N:` only; interior `## `/`# ` lines become h2 divider blocks; TOC-named H2s dropped; alerts may carry inline `title`.
8. Notes output/index: `src/data/notes/<subject>/<file>.js` + ONE combined `src/data/notes/index.js` (Course/Home import it; Chapter lazy-imports via `notes/<subjectId>/<file>`).
9. ss-ch1 is a ~1 MB lazy chunk (12.7k words) — expected; per-section pagination keeps rendering comfortable. One mermaid fence renders as literal code.

## Site structure

- `/` Home · `/course/gate-2027-ece` course page (Content|Tests tabs, chapter accordion, search) · `/course/:courseId/:subjectId/:chapterId` chapter reader (sticky TOC, per-section "Mark read" → localStorage `gp_progress_v1`, prev/next) · `/tests` placeholder.
- `src/data/courses.js` = the only registry. Chapter pages lazy-load their module (code-split chunks).
- `MathText.jsx` is a GATE-Prep-specific upgrade of the sibling renderer: **bold/code tokens are processed OUTERMOST** so `**text ($math$)**` renders correctly — keep that ordering when editing.
- Theme: `lib/theme.js` + `df-theme` localStorage + anti-FOUC script in `index.html`.

## Before every deploy

```bash
npm run verify         # scripts/verify_notes.mjs must be green
rm -rf dist && npm run build   # emptyOutDir is false — clean stale chunks first
npx wrangler pages deploy dist --project-name=gate-prep
```

Then commit/push to `studyassistglobal/gate-prep` (gh account: switch to `studyassistglobal` if pushes 404).

## Gotchas learned the hard way

- `verify_notes.mjs` walks `liveChapterSequence()` objects as `{subject, chapter}` — don't read `c.id` off them.
- The fork's stale files (papers, auth, exam pages) were removed at creation; if a new file imports `supabase`/`auth.jsx`/`recharts`, the verifier's fork-hygiene gate will fail the build — intentional.
- HashRouter + in-page anchors: use react-router's parsed `location.hash` (see Chapter.jsx) and `scroll-margin-top` on sections; never `window.location.hash.split('#')`.


## 15. Signalling updates (2026-09-29) — SS Ch1 refresh + Ch2 live

- `ss-ch1` regenerated from the Sep-28 Master Guide (947 KB → 1.19 MB; 17 sections / 8,472 blocks, 7 figures still resolve to `/notes/ss/figures_ch1/`).
- **`ss-ch2` "Basics of Systems" is live** (717 KB, 12 sections / 5,756 blocks, no figures) — registered in `src/data/courses.js`; reader volume nav now chains Ch1 ⇄ Ch2.
- Parser upgrades this pass (all in `scripts/build_notes.py`):
  1. Module-split accepts H1–H6 module headers (`^#{1,6} (?=Module )`) — Ch2 authors `# Module 01:` at H1, Ch1 uses `## Module`. Interior `## N.` sub-headings become h2 divider blocks.
  2. **Display math may be bullet-prefixed** (`* $$…`): the math branch now strips a leading list marker before testing, so display math inside list items isn't shredded by the ul branch.
  3. **Quoted problem statements** (`"Q. … $$…\end{cases}$$"`) trail a `"` after the closing `$$` — peel quotes before the delimiter strip, else a stray `$$` survives into the tex.
  4. **Table splitter treats `$$` as ONE paired toggle** — previously each `$` toggled math-state, so `$$…|h(t)|…$$` cells split at the absolute-value bar (broke the BIBO table in Ch2 M10).
  5. `scripts/verify_notes.mjs`: code fences are literal by design — their content is exempt from the math-balance check; live-chapter count is 7.
- Lesson: a 2 MB lazy chapter chunk can take ~3–5 s to render on a cold load — browser spot-checks must wait generously before judging a chapter page empty.

## 16. Content audit (2026-09-29) — all chapters swept clean

- `node scripts/audit_content.mjs` (new) walks every live chapter module and checks: control chars, mojibake (Devanagari/Latin-ext/Greek-archaic), `$`/`$$` parity, `\(` `\)` balance, stray `#`/`**`/fence markers, empty sections, ragged table rows, missing figure files, registry↔index coherence. Writes `scratch/audit_content.json` (scratch/ is gitignored). Severity HIGH (renders broken) / MED (structural) / LOW (cosmetic).
- **Final result: 17,011 blocks / 28,881 text leaves / 7 chapters — HIGH 0 · MED 0 · LOW 5.** The 5 remaining LOWs are heuristic false positives: literal `**` inside code fences (ASCII diagrams) and inside `$**$` math (double-star notation) — all render correctly by design.
- Fixes that came out of the audit (all in `scripts/build_notes.py`, then full regeneration):
  1. **OCR control-char repair** in `build_chapter`: LaTeX escapes `\a \b \t \v \f \r` that survive MD export as literal control chars (BEL/BS/TAB/VT/FF/CR) are restored to backslash + macro letter when followed by a lowercase letter (FF+`rac` → `\frac`, CR+`ight` → `\right`). Same CTRL_MAP pattern as the examhub mock repair.
  2. **`#####`/`######` headings** now parse as h4 blocks (previously fell through to p blocks and rendered literal hashes). ~100 per-problem sub-headings across ss-ch1/ss-ch2 were affected.
  3. **`split_table_row` tracks backtick code spans** — pipes inside `` `…` `` (e.g. `` `y(t) = |x(t)|` ``) no longer split a table row into ragged cells (Ch2 M11 trap table).
- Verification after fixes: `npm run verify` green (registry 7 live, 102 sections); live spot-checks on deployed build — Module 09 (934 KaTeX nodes, no raw-TeX leaks, no literal hashes), Module 11 Trap-08 row intact with 0 ragged tables, ss-ch1 Module 02 `Problem (j/k)` h4 headings render with math.

## 17. Formula & Revision Sheets live (2026-09-29) — ssf-ch1..ch3

- New registry subject group **`ssf` "S&S Formula Sheets"** with three chapters built from the `*_Formula_and_Revision_Sheet.md` sources (Signals Ch1: 9 sections/498 blocks · Systems Ch2: 10/558 · CTFS Ch3: 10/599). Modules live in `src/data/notes/ssf/` — **the registry subject id drives the lazy-import path**, so `notes_sub` in build_notes.py must equal the subject id (`ssf`), not `ss`.
- Parser upgrades for the sheet format (all in `scripts/build_notes.py`):
  1. **`section_split: "section"`** — splits at `Section N:` headers at any heading level (`^#{1,6} (?=Section )`), mirroring module mode.
  2. **Sheet TOC drop** — the sheets' `## Master Table of Contents` (plain-text sub-entries the anchor dropper can't catch) is cut from the preamble in section mode; the app renders its own TOC.
  3. **Ordered lists carry `start`** — display math interleaves numbered items, splitting each into its own ol block; the original start number is now parsed and NoteBlock renders `<ol start>` so items don't all show "1.".
- Rendering notes: the sheets lean on `$$\begin{array}` matrix tables and `$$…$$` inside GitHub alerts — MathText already handles both (block-math regex in `renderInlineContent`); KaTeX renders arrays via `.mtable`. Fenced mermaid renders as literal code (same as ss-ch1).
- verify_notes.mjs live-chapter gate is now **10**. Audit after adding sheets: 18,666 blocks / 31,715 leaves across 10 chapters — HIGH 0 · MED 0 · LOW 5 (same benign `**` literals).
- Lesson (recurring): Git-Bash heredocs mangle `\` even when quoted — inspection scripts with backslash needles must use chr(92)/Write tool, or they silently report false negatives.
