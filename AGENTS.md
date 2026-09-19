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
