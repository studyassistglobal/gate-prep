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

## 18. Full source sweep — 16 new chapters, site now 26 live (2026-09-30)

- Integrated everything new in `D:\GATE 2027\`: **S&S Masters Ch3–Ch7** (CTFS, FT & Sampling, Laplace, Z-Transform, DTFT/DFT/FFT — module-split, figures_ch4..7 copied), **S&S Sheets Ch4–Ch7** (ch4/ch5 section-split; ch6 generic split with figures_ch6; ch7 generic), **Network Theory now live**: `nt-ch1..3` (01_Basics_of_Network / 02_Network_Theorems / 03_Transient_Analysis — generic `## ` split) + new `ntf` "NT Revision Guides" group (`ntf-ch1..3` revision guides + `ntf-ch4` Revision Capsule). Deliberately skipped: `04_GATE_Formula_CheatSheet` (fully contained in the Capsule), `*_Short.md`, parts/ + audit_*/mined_* intermediates.
- **`notes_sub` must equal the registry subject id** (modules lazy-import via `notes/<subjectId>/<file>`): ssf → `notes/ssf/`, ntf → `notes/ntf/`.
- Parser work this pass (all in `scripts/build_notes.py` unless noted):
  1. **`unwrap_lines`** (per-chapter `"unwrap": True` flag — the Ch4-7 Masters + NT sources hard-wrap headings/bold/math mid-token): joins a continuation line ONLY when its parent is actually broken (odd `**`, odd single-`$` excluding `$$`, a heading with broken math, or a `|`-row continued on a plain line). Never joins healthy headings — module headers carry indented scope lines. Fenced code untouched.
  2. **`\vert` as a table cell separator** outside math (OCR of `|`), plus stray trailing `\vert` stripped — killed 64 ragged-table findings in ss-ch6.
  3. **Ragged-row normalization**: rows are padded/merged to the header width (overflow cells join the last cell with ` | `).
  4. **`$$…$$ trailing-text` fix**: single-line math with content after the closing `$$` (e.g. `$\checkmark$`) now emits math + a following p, instead of swallowing the tail into the tex (also fixed the multi-line closing-line tail).
  5. **`clean_title`**: section/module titles render as plain text (sidebar/search), so `$math$` is replaced by its inner text when plain-readable (`$R$` → R), else dropped, then punctuation tidied — no dollar signs leak into the TOC.
  6. **TOC drop**: `## (?:Master )?Table of Contents` drops to the next H1 **or** H2 (ss-ch1 has three mid-document TOCs followed by H1 content that the old regex silently swallowed — 631 blocks of Module 11 restored); anchor dropper now also catches bullet-prefixed link lines.
  7. **`REPAIRS`** dict: exact-match typo repairs applied to the read-only sources (nt-ch1 missing `$` after `$2\text{ mA}`; ss-ch5's source truncates module 09 mid-sentence — dangling "5. **The" dropped).
  8. Alert bodies containing fenced ASCII diagrams emit alert + code + alert fragments (nt-ch2 T-network).
  9. Balance checks in verify_notes.mjs + audit_content.mjs ignore `\$` escaped dollars; audit exempts code blocks from math-delimiter checks (literal by design).
- Regression guard: the 10 previously-live chapters are byte-identical modulo `generatedAt` (checked by JSON-semantic diff) — EXCEPT two intentional improvements: ss-ch1 Module 11 restored (+631 swallowed blocks) and de-ch2 section titles cleaned (`$m_i$` → `m_i` in the sidebar).
- Audit final: 47,323 blocks / 75,898 leaves / 26 chapters — HIGH 0 · MED 0 · LOW 7 (all benign `**`-in-ASCII/notation false positives). verify_notes.mjs live-chapter gate is now **26**.

## 19. Engineering Mathematics — Linear Algebra live (2026-10-01) — 28 chapters

- New subject **`em` "Engineering Mathematics"** (`em-ch1` Linear Algebra Master, 10 sections / 5,915 blocks) + **`emf` "EM Formula Sheets"** (`emf-ch1`, 15 sections / 195 blocks) from the Oct-1 uploads in `D:\GATE 2027\engineering mathematics\`. The LA Master is **audit-concatenated at `# Part I..IX`** (Modules restart per Part, so module-split would collapse Parts V-IX into one section) → new **`section_split: "part"`** mode restricted to Roman numerals (`Part (a):` / `Part 1:` drill sub-parts must not split).
- The MDs reference **no figures** (figures_linear_algebra/ exists only for the Dark PDFs) — figures_src None.
- **Console-encoding lesson:** Git Bash renders clean UTF-8 as CP437 mojibake (`Rouché–Capelli` shows as `Rouch├⌐ΓÇôCapelli`). The files were verified clean via python `ord()` dumps — never trust console output for encoding diagnosis, and never "repair" it in the builder.
- Drill typo repaired via REPAIRS (em-ch1 missing `$` before `\vert A \vert \neq 0`).
- `edc/` folder holds only a 72 MB slide PDF (no MD source) — nothing to integrate until an MD export appears.
- Audit: 53,433 blocks / 84,518 leaves / 28 chapters — HIGH 0 · MED 0 · LOW 7. verify gate is now **28**.

## 20. Mobile-friendliness pass (2026-10-01)

- **Reader TOC = slide-in drawer below 900px**: `.gp-toc` becomes a fixed left drawer (`min(320px, 86vw)`, translateX slide, backdrop, safe-area padding, `100dvh`); a sticky `Contents · N modules | N% read` toggle bar (`.gp-toc-toggle`) sits above the article; closes on section select, backdrop click, Escape; body scroll locks via `body.gp-no-scroll`. Desktop ≥900px unchanged (toggle/backdrop `display:none !important`).
- **Mobile nav**: hamburger (`.menu-btn`) only <768px; classed `.mobile-nav` panel (48px links, active highlight, slide-down) + `.nav-backdrop`; closes on route change (`useLocation` effect) + Escape. Replaced the old inline-styled dropdown.
- **Padding dedupe**: <768px `.app-main` owns the gutter (`20px 14px`), `.gp-page` horizontal 0 (was 48px/side total → ~28px/side; content 365px wide on 390px screens). <480px: tighter gutters, stacked full-width prev/next buttons (44px targets), footer stacks, hero stats compress.
- **Grid blowout fix**: `.gp-chapter-layout` uses `minmax(0, 1fr)` + `.gp-chapter-content { min-width: 0 }` — wide tables/code previously stretched the whole page horizontally on phones.
- **Overflow nets**: `.math-inline-wrap { max-width:100%; overflow-x:auto }` (wide inline KaTeX scrolls, not the page); `overflow-wrap: break-word` on prose; `body { overflow-x: clip }`; `.gp-tabs` scrollable; 44px targets on tabs/subject rows.
- Misc: 404 `.nf-title/.nf-sub` styled, `.nf-screen` min-height uses `calc(100dvh - 190px)` (no fold overshoot), Tests teaser padding reduced on phones, `prefers-reduced-motion` kills animations.
- Verified at 390×844 and 360×740 (both themes) + 1280×800 desktop regression: zero horizontal overflow anywhere, drawer/nav/Escape/scroll-lock all exercised, 4/4 wide tables scroll, desktop sidebar intact.
